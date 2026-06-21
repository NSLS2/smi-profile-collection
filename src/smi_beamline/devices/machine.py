
from ophyd import (
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    Device,
)
from ophyd import Component
from ophyd.status import StatusBase
import logging
import threading
import time as _time

logger = logging.getLogger("bluesky")


class Ring(Device):
    current = EpicsSignalRO("SR:C03-BI{DCCT:1}I:Real-I", name="ring_current")
    lifetime = EpicsSignalRO("SR:OPS-BI{DCCT:1}Lifetime-I", name="ring_lifetime")
    energy = EpicsSignalRO("SR{}Energy_SRBend", name="ring_energy")
    mode = EpicsSignal("SR-OPS{}Mode-Sts", name="ring_ops", string=True)
    filltarget = EpicsSignalRO("SR-HLA{}FillPattern:DesireImA", name="ring_filltarget")

class IVUBrakeCpt(Component):
    def maybe_add_prefix(self, instance, kw, suffix):
        if kw not in self.add_prefix:
            return suffix

        prefix = "".join(instance.prefix.partition("IVU:1")[:2]) + "}"
        return prefix + suffix


class InsertionDevice(EpicsMotor):
    # SR:C12-ID:G1{IVU:1}BrakesDisengaged-SP
    # SR:C12-ID:G1{IVU:1}BrakesDisengaged-Sts
    brake = IVUBrakeCpt(
        EpicsSignal,
        write_pv="BrakesDisengaged-SP",
        read_pv="BrakesDisengaged-Sts",
        add_prefix=("read_pv", "write_pv", "suffix"),
    )
    gap_speed = Component(EpicsSignal,
        write_pv = "SR:C12-ID:G1{IVU:1}GapSpeed-SP",
        read_pv = "SR:C12-ID:G1{IVU:1}GapSpeed-RB",
        add_prefix = (),
    )

    # --- Brake-confirm + verify/retry tunables (class attrs: adjust without code edits) -------
    #: dwell (s) after BrakesDisengaged-Sts reads disengaged, before commanding the gap, so the
    #: controller is genuinely ready to accept motion (the Sts can read 1 a touch optimistically).
    brake_settle = 0.2
    #: max wait (s) for BrakesDisengaged-Sts == disengaged after writing the SP.
    brake_timeout = 5.0
    #: value the brake SP/Sts use for "disengaged" (1 on the real IVU).
    brake_disengaged_value = 1
    #: how many times to (re-)issue the gap move if the readback didn't reach target.  2 keeps the
    #: operators' manual "move it twice" as an automatic safety net.
    max_move_attempts = 2
    #: "did it actually move / reach target?" tolerance (gap units, um).  An explicit value rather
    #: than the motor RDBD (which is a *retry* deadband and may be 0/closed-loop-tuned).
    move_deadband = 5.0

    def move(self, position, wait=True, **kwargs):
        """Disengage the IVU brake (and CONFIRM it), move the gap, verify it reached target, and
        re-issue the move once if it didn't.

        Background (the "move it twice" bug)
        ------------------------------------
        The gap cannot move until the brake is mechanically disengaged.  Writing
        ``BrakesDisengaged-SP`` and waiting only for the *CA put ack* does NOT guarantee the brake
        has physically released -- the gap setpoint can be issued while still braked, the
        controller drops the first motion command, and the motor record reports ``DMOV`` done with
        no motion.  The ophyd ``Status`` then "succeeds" with the gap never having moved, so a
        second manual move was needed.

        This method instead:

        1. writes the brake SP to *disengaged* and **waits for the readback**
           (``BrakesDisengaged-Sts``) to confirm it, up to :attr:`brake_timeout`, plus a short
           :attr:`brake_settle` dwell;
        2. issues the gap move;
        3. when that completes, if ``|readback - target| > move_deadband`` it re-confirms the brake
           and **re-issues the move**, up to :attr:`max_move_attempts` (the manual "twice" as an
           automatic net).

        It stays **non-blocking / Status-chained**: the whole sequence runs on a daemon thread and
        a single :class:`~ophyd.status.StatusBase` is returned immediately, completing only when
        the gap truly reaches target (or failing after the attempt budget / a timeout).  This is
        what the ``Energy`` pseudo-positioner needs -- it drives ``ivugap.move(..., wait=False)``
        concurrently with bragg/dcmgap.  ``wait=True`` (console convenience) simply waits on that
        Status, exactly like a plain motor move.
        """
        target = float(position)
        timeout = kwargs.get("timeout", None)
        overall = StatusBase()

        def _run():
            try:
                last_status = None
                for attempt in range(1, self.max_move_attempts + 1):
                    self._disengage_brake_and_confirm()
                    # Issue the gap move (non-blocking) and wait for THIS attempt to settle.
                    last_status = super(InsertionDevice, self).move(
                        target, wait=False, **kwargs)
                    self._wait_status(last_status, timeout)

                    err = abs(self.user_readback.get() - target)
                    if err <= self.move_deadband:
                        overall.set_finished()
                        return
                    logger.warning(
                        "IVU gap move attempt %d/%d did not reach target "
                        "(|%.3f - %.3f| = %.3f > %.3f um); %s",
                        attempt, self.max_move_attempts,
                        self.user_readback.get(), target, err, self.move_deadband,
                        "retrying" if attempt < self.max_move_attempts else "giving up")
                # Out of attempts: report failure (propagate the last move's exception if any).
                exc = RuntimeError(
                    "IVU gap failed to reach target {:.3f} um after {} attempts "
                    "(readback {:.3f} um).".format(
                        target, self.max_move_attempts, self.user_readback.get()))
                self._fail_status(overall, exc)
            except Exception as exc:  # noqa: BLE001 -- surface any move/brake failure on the Status
                self._fail_status(overall, exc)

        threading.Thread(target=_run, name="ivu-move", daemon=True).start()

        if wait:
            overall.wait(timeout=timeout)
        return overall

    # ---------------------------------------------------------------- helpers
    def _disengage_brake_and_confirm(self):
        """Write the brake SP to disengaged and wait for the Sts readback to confirm + settle."""
        want = self.brake_disengaged_value
        self.brake.put(want, wait=True)  # CA put ack (the SP landed)
        # Now wait for the *readback* (BrakesDisengaged-Sts) to actually report disengaged.
        deadline = _time.time() + self.brake_timeout
        while _time.time() < deadline:
            try:
                if int(self.brake.get()) == int(want):
                    break
            except Exception:
                pass
            _time.sleep(0.05)
        else:
            raise TimeoutError(
                "IVU brake did not confirm disengaged (BrakesDisengaged-Sts != {}) within {}s"
                .format(want, self.brake_timeout))
        # Brief dwell so the controller is genuinely ready before commanding motion.
        if self.brake_settle:
            _time.sleep(self.brake_settle)

    @staticmethod
    def _wait_status(status, timeout):
        """Block until ``status`` finishes; swallow a move failure (caller checks the readback)."""
        try:
            status.wait(timeout=timeout)
        except Exception as exc:  # a failed/aborted move -> let the readback-vs-target check decide
            logger.debug("IVU gap move status raised (will verify by readback): %r", exc)

    @staticmethod
    def _fail_status(status, exc):
        """Mark ``status`` failed, compatible across ophyd versions (set_exception vs _finished)."""
        try:
            status.set_exception(exc)
        except Exception:
            try:
                status._finished(success=False)
            except Exception:
                pass

