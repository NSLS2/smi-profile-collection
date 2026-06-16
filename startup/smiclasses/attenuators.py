from ophyd import (
    PVPositioner,
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    Device,
    Signal,
    PseudoPositioner,
    PseudoSingle,
)
from ophyd.utils.epics_pvs import set_and_wait
from ophyd.status import DeviceStatus
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from ophyd import Component as Cpt
import logging
import threading

logger = logging.getLogger("bluesky")


class Attenuator(Device):
    """
    A single attenuator foil that is **unreliable at the hardware level** -- the actuation
    command often has to be re-issued, and the position read-back confirms the new state only
    after a delay.

    The previous ``set`` handled this with a blocking ``while`` loop that re-issued the command
    and **swallowed all errors / always reported success**.  That blocked the RunEngine and --
    worse -- could leave the foil in the wrong position while telling the plan it succeeded.

    This version is **non-blocking and subscription-driven**, and keeps the essential retry
    behavior, but with safe failure semantics:

    * The returned ``Status`` finishes (success) only when ``status`` actually reads the target
      value -- so ``yield from bps.mv(att, 'Insert')`` does not proceed until the foil confirms.
      The confirmation may arrive any time after the command (a real device delay); the
      subscription handles that without blocking -- no ``sleep().wait()`` needed.
    * The command is re-actuated up to ``max_retries`` times if the hardware does not confirm.
      Each attempt uses a short ``cmd_timeout``; **a single attempt timing out is expected** (the
      first few often do) and is swallowed -- only the *repeated* failure is reported.
    * **If it still has not confirmed after the retries / ``timeout`` seconds, the Status is
      marked FAILED (raises).**  A hard stop is the safe outcome: better to halt a run than to
      keep going with an attenuator in the wrong (potentially unsafe) position.

    Attributes:
        open_cmd (EpicsSignal): Command to open (insert) the attenuator.
        close_cmd (EpicsSignal): Command to close (retract) the attenuator.
        status (EpicsSignalRO): The attenuator's position read-back.
        fail_to_close / fail_to_open (EpicsSignalRO): hardware fault flags.
    """
    open_cmd = Cpt(EpicsSignal, "Cmd:Opn-Cmd", string=True)
    open_val = "Open"

    close_cmd = Cpt(EpicsSignal, "Cmd:Cls-Cmd", string=True)
    close_val = "Not Open"

    status = Cpt(EpicsSignalRO, "Pos-Sts", string=True)
    fail_to_close = Cpt(EpicsSignalRO, "Sts:FailCls-Sts", string=True)
    fail_to_open = Cpt(EpicsSignalRO, "Sts:FailOpn-Sts", string=True)

    # User-facing commands
    open_str = "Insert"
    close_str = "Retract"

    #: how many times to re-issue the actuation command before failing
    max_retries = 8
    #: hard wall-clock cap (s) after which the set FAILS if not confirmed
    timeout = 30.0
    #: delay (s) between re-actuation attempts (waited for via a timer, NOT a blocking sleep)
    retry_delay = 0.5
    #: per-attempt command-put timeout (s); a single attempt timing out is EXPECTED (the first
    #: few often do) and is swallowed -- only repeated failure (max_retries / `timeout`) raises.
    cmd_timeout = 1.0

    _OPEN_ALIASES = ("Open", "Insert", "open", "insert", "in", 1, "1")
    _CLOSE_ALIASES = ("Close", "Retract", "close", "retract", "out", 0, "0", "Not Open")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_st = None
        self.read_attrs = ["status"]

    def set(self, val):
        """Drive the foil to ``val`` ('Insert'/'Retract' etc.), retrying until confirmed.

        Returns a ``DeviceStatus`` that finishes when ``status`` reads the target value, or
        **fails** (after ``max_retries`` re-actuations / ``timeout`` seconds) if the foil never
        confirms -- a flaky foil that cannot reach position raises rather than silently
        proceeding in the wrong state.  Non-blocking.
        """
        if self._set_st is not None:
            raise RuntimeError(
                "{}: trying to set while a set is in progress".format(self.name))

        if val in self._OPEN_ALIASES:
            cmd_sig, target = self.open_cmd, self.open_val
        elif val in self._CLOSE_ALIASES:
            cmd_sig, target = self.close_cmd, self.close_val
        else:
            raise ValueError(
                "{}: unknown attenuator state {!r} (use 'Insert'/'Retract')".format(
                    self.name, val))

        st = self._set_st = DeviceStatus(self)
        state = {"attempts": 0, "done": False, "timer": None, "watchdog": None}

        def _cleanup():
            state["done"] = True
            for key in ("timer", "watchdog"):
                t = state.get(key)
                if t is not None:
                    try:
                        t.cancel()
                    except Exception:
                        pass
            try:
                self.status.clear_sub(_status_cb)
            except Exception:
                pass
            self._set_st = None

        def _succeed():
            if state["done"]:
                return
            _cleanup()
            st.set_finished()

        def _fail():
            if state["done"]:
                return
            cur = self._safe_status()
            _cleanup()
            logger.error(
                "%s: failed to reach '%s' after %d attempts / %.0fs (status=%r); "
                "FAILING the set so the run halts rather than continue with the foil in the "
                "wrong position.", self.name, val, state["attempts"], self.timeout, cur)
            st.set_exception(
                TimeoutError("{}: attenuator did not reach {!r} (last status={!r})".format(
                    self.name, target, cur)))

        def _status_cb(value, **kwargs):
            # status reads the target (whenever the device finally reports it) -> success.
            if str(value) == target:
                _succeed()

        def _retry():
            # Runs on a timer thread; re-actuate, then schedule the next check until confirmed,
            # retries exhausted, or the watchdog fails us.  No blocking of the RunEngine loop.
            if state["done"]:
                return
            if str(self._safe_status()) == target:
                _succeed()
                return
            if state["attempts"] >= self.max_retries:
                _fail()
                return
            state["attempts"] += 1
            # Issue one actuation with a SHORT, bounded timeout.  A single attempt timing out is
            # EXPECTED for this flaky hardware (the first few often do) -- swallow it here; only
            # the repeated failure (max_retries / watchdog `timeout`) is reported upward via the
            # returned Status.  The bounded .wait() runs on this timer thread, never the RE loop.
            try:
                cmd_sig.set(1, timeout=self.cmd_timeout).wait()
            except Exception as exc:
                logger.debug("%s: actuation attempt %d to '%s' did not confirm in %.1fs (%r); "
                             "will retry", self.name, state["attempts"], val,
                             self.cmd_timeout, exc)
            if state["attempts"] > 1:
                logger.info("** %s: re-actuating to '%s' (attempt %d)",
                            self.name, val, state["attempts"])
            if not state["done"]:
                t = threading.Timer(self.retry_delay, _retry)
                t.daemon = True
                state["timer"] = t
                t.start()

        # Hard wall-clock cap: fail if not confirmed in time (covers a foil that accepts the
        # command but whose read-back is stuck).
        watchdog = threading.Timer(self.timeout, _fail)
        watchdog.daemon = True
        state["watchdog"] = watchdog
        watchdog.start()

        # If already at target, finish immediately; else subscribe + start the retry loop.
        self.status.subscribe(_status_cb, run=True)
        if not state["done"]:
            _retry()
        return st

    def _safe_status(self):
        try:
            return self.status.get()
        except Exception:
            return None


# Uncomment and complete the following class if needed
# class Attenuation(PseudoPositioner):
#     """
#     PseudoPositioner for controlling multiple attenuators.
#     """
#     # Synthetic axis
#     attenuation = Cpt(PseudoSingle, kind="hinted")

#     # Real axes
#     att1_1 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:1-1}")
#     att1_2 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:1-2}")
#     ...
#     att2_12 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:2-12}")

#     @real_position_argument
#     def inverse(self, r_pos):
#         """
#         Convert real positions to pseudo positions.
#         """
#         return self.PseudoPosition(attenuation=...)

#     @pseudo_position_argument
#     def forward(self, p_pos):
#         """
#         Convert pseudo positions to real positions.
#         """
#         return self.RealPosition(
#             att1_1=att1_1_calc,
#             att1_2=att1_2_calc,
#             ...
#             att2_12=att2_12_calc,
#         )