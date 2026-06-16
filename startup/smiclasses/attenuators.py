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
    #: the read-back must stay at the target for this long (s) before the foil is considered "in
    #: position".  This DEBOUNCES the hardware's bounce-back: a foil can momentarily read the
    #: target and then fall back, so a single transient reading must NOT latch success.
    settle_time = 0.6

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
        state = {"attempts": 0, "done": False, "timer": None, "watchdog": None,
                 "settle": None}

        def _cancel_settle():
            t = state.get("settle")
            if t is not None:
                try:
                    t.cancel()
                except Exception:
                    pass
            state["settle"] = None

        def _cleanup():
            state["done"] = True
            _cancel_settle()
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

        def _settle_confirm():
            # Fired settle_time after the status reached target; succeed only if it is STILL at
            # target (it did not bounce back).
            if state["done"]:
                return
            if str(self._safe_status()) == target:
                _succeed()
            else:
                _cancel_settle()   # bounced away; the retry loop will re-actuate

        def _status_cb(value, **kwargs):
            # status changed.  If it is at target, ARM the settle timer (don't succeed yet -- it
            # may bounce back).  If it moved away from target, cancel any pending settle.
            if state["done"]:
                return
            if str(value) == target:
                if state["settle"] is None:
                    t = threading.Timer(self.settle_time, _settle_confirm)
                    t.daemon = True
                    state["settle"] = t
                    t.start()
            else:
                _cancel_settle()

        def _retry():
            # Runs on a timer thread; re-actuate, then schedule the next check until confirmed
            # (settled), retries exhausted, or the watchdog fails us.  No blocking of the RE loop.
            if state["done"]:
                return
            # If we're currently at target, let the settle timer confirm it -- do NOT re-actuate
            # (and do not succeed here, since a momentary reading may bounce back).
            if str(self._safe_status()) == target:
                if state["settle"] is None:
                    t = threading.Timer(self.settle_time, _settle_confirm)
                    t.daemon = True
                    state["settle"] = t
                    t.start()
                # keep a (slow) heartbeat so we re-check if the settle timer was cancelled
                if not state["done"]:
                    hb = threading.Timer(self.settle_time + self.retry_delay, _retry)
                    hb.daemon = True
                    state["timer"] = hb
                    hb.start()
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


class Attenuators(Device):
    """An aggregate over a bank of :class:`Attenuator` foils that moves them **as one unit**.

    Why this exists
    ---------------
    Moving several foils with one ``bps.mv(att2_5, 'Insert', att2_6, 'Insert', ...)`` was
    observed to misbehave on the real hardware: the foils all actuate, but one or more *bounce
    back* out of position while the overall move still reports success.  Driving them through a
    single device fixes this because:

    * the per-foil :class:`Attenuator` now requires the read-back to be **stable** (settled) for
      ``Attenuator.settle_time`` before it counts as in-position, so a transient correct reading
      that bounces back no longer latches success; and
    * this aggregate's ``set`` does not finish until **every** foil's settled-confirmation has
      completed (and re-actuates any that fall back), so the combined move is only "done" when
      the whole requested combination is genuinely in place.

    Usage
    -----
    ``set`` takes the foils that should be **inserted**; every other foil in the bank is
    **retracted**.  Accepts foil child-attribute names or the foil objects themselves::

        yield from bps.mv(attenuators, ['f5', 'f6'])         # insert f5,f6; retract the rest
        yield from bps.mv(attenuators, [attenuators.f5])     # by object
        yield from bps.mv(attenuators, [])                   # retract all (no attenuation)

    The returned Status finishes only when all 12 foils confirm; if any foil cannot reach
    position it FAILS (the foil's own safe-fail), halting the run rather than running with the
    wrong attenuation.
    """

    def set(self, inserted):
        """Insert the foils in ``inserted`` and retract all others; finish when all confirm.

        Parameters
        ----------
        inserted : iterable
            Foil child-attribute names (e.g. ``'f5'``) and/or foil objects that should end up
            INSERTED.  Everything else in the bank is RETRACTED.
        """
        want_in = self._resolve_foils(inserted)

        statuses = []
        for name in self.component_names:
            foil = getattr(self, name)
            if not isinstance(foil, Attenuator):
                continue
            target = "Insert" if foil in want_in else "Retract"
            statuses.append(foil.set(target))

        if not statuses:
            # nothing to do -> an already-finished status
            st = DeviceStatus(self)
            st.set_finished()
            return st

        # Combine: the aggregate is done only when EVERY foil's (settled) status is done; it
        # fails if any foil fails.
        combined = statuses[0]
        for s in statuses[1:]:
            combined = combined & s
        return combined

    def _resolve_foils(self, inserted):
        """Return the set of foil objects requested to be inserted (from names or objects)."""
        foils_by_name = {name: getattr(self, name) for name in self.component_names
                         if isinstance(getattr(self, name), Attenuator)}
        by_obj = set(foils_by_name.values())
        want = set()
        for item in (inserted or []):
            if isinstance(item, Attenuator):
                if item not in by_obj:
                    raise ValueError(
                        "{}: {!r} is not a foil of this bank".format(self.name, item))
                want.add(item)
            elif item in foils_by_name:
                want.add(foils_by_name[item])
            else:
                raise ValueError(
                    "{}: unknown foil {!r}; expected one of {}".format(
                        self.name, item, sorted(foils_by_name)))
        return want

    def inserted_foils(self):
        """Return the child-attribute names of the foils currently reading 'Open'."""
        out = []
        for name in self.component_names:
            foil = getattr(self, name)
            if isinstance(foil, Attenuator) and foil._safe_status() == foil.open_val:
                out.append(name)
        return out


def make_attenuator_bank(class_name, prefix_fmt, foil_indices):
    """Build an :class:`Attenuators` subclass with foils ``f<i>`` for ``i`` in ``foil_indices``.

    ``prefix_fmt`` is a format string taking the foil index, e.g.
    ``"XF:12IDC-OP:2{{Fltr:2-{}}}"``.  Returns the new class (instantiate with ``name=...``).
    """
    body = {"f{}".format(i): Cpt(Attenuator, prefix_fmt.format(i), add_prefix=("suffix",))
            for i in foil_indices}
    return type(class_name, (Attenuators,), body)


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