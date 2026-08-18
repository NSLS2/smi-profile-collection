import warnings
import time as ttime
import os
import math
import logging
import threading
import numpy as np
from ophyd import (
    PVPositioner,
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    Device,
    Signal,
    PseudoPositioner,
    PseudoSingle,
    SoftPositioner,
)
from ophyd.utils.epics_pvs import set_and_wait
from ophyd.status import StatusBase, MoveStatus
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from ophyd import Component as Cpt
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
import epics.ca as ca
from .machine import InsertionDevice
from . import _config
from . import _context

logger = logging.getLogger("bluesky")

#: A direct console ``energy.move(E)`` / ``energy.set(E)`` of at least this size (eV) that is NOT
#: running through the RunEngine bypasses the managed-move preprocessor (feedback-managed
#: ``energy_walk``).  A one-line ``warnings.warn`` is emitted in that case (see ``Energy.move``).
#: Kept in sync with the preprocessor's ``threshold_eV`` default (``energy_move_preprocessor``) so
#: the note fires exactly when the managed path *would* have engaged.  Small moves stay silent --
#: they are not managed anyway -- so setup nudges are never nagged.
UNMANAGED_MOVE_WARN_eV = 500.0


def _running_under_run_engine():
    """Best-effort: are we executing on the RunEngine's plan thread?

    The RunEngine runs its plan on a dedicated background thread (``RE._th``, created by
    ``bluesky.run_engine._ensure_event_loop_running`` and named ``"bluesky-run-engine"``) and
    processes ``Msg('set', energy, target)`` by calling ``energy.set(...)`` *from that thread*.
    A bare console ``energy.move(E)`` / ``energy.set(E)`` instead runs on the caller's thread
    (normally the IPython main thread).  So comparing the current thread to the RE's thread tells
    us whether this ``set`` is going through the RunEngine (and therefore the managed-move
    preprocessor) or is a direct, unmanaged move.

    Returns ``True`` (assume managed / stay quiet) whenever the answer is unknown -- no live RE is
    wired into the seam (tests / off-beamline / a plain import), or the private ``_th`` attribute
    is unavailable.  When an RE is wired but exposes no ``_th``, falls back to matching the RE
    loop-thread *name* (``"bluesky-run-engine"``).  Never raises -- this only gates a courtesy
    warning, so any surprise means "stay quiet".
    """
    try:
        re = _context.get_re()
        if re is None:
            # Off-beamline / tests / bare import: no managed path exists, so don't warn.
            return True
        current = threading.current_thread()
        re_thread = getattr(re, "_th", None)
        if re_thread is not None:
            return current is re_thread
        # RE wired but no ``_th`` (unexpected): fall back to the well-known RE loop-thread name.
        return current.name == "bluesky-run-engine"
    except Exception:
        return True


class DCMInternals(Device):
    """
    Device representing the internal motors of the Double Crystal Monochromator (DCM).

    Attributes:
        height (EpicsMotor): Motor controlling the height of the DCM.
        pitch (EpicsMotor): Motor controlling the pitch of the DCM.
        roll (EpicsMotor): Motor controlling the roll of the DCM.
        theta (EpicsMotor): Motor controlling the theta angle of the DCM.
    """
    height = Cpt(EpicsMotor, "XF:12ID:m66")
    pitch = Cpt(EpicsMotor, "XF:12ID:m67")
    roll = Cpt(EpicsMotor, "XF:12ID:m68")
    theta = Cpt(EpicsMotor, "XF:12ID:m65")


class Energy(PseudoPositioner):
    """
    PseudoPositioner for controlling the monochromator energy.

    Attributes:
        energy (PseudoSingle): Synthetic axis representing the energy.
        dcmgap (EpicsMotor): Real motor controlling the DCM gap.
        bragg (EpicsMotor): Real motor controlling the Bragg angle.
        pitch_feedback_disabled (EpicsSignal): Signal to disable pitch feedback.
        roll_feedback_disabled (EpicsSignal): Signal to disable roll feedback.
        ivugap (InsertionDevice): Real motor controlling the IVU gap.
        enableivu (Signal): Signal to enable or disable IVU movement.
        enabledcmgap (Signal): Signal to enable or disable DCM gap movement.
        target_harmonic (Signal): Target harmonic for the undulator.
        harmonic (Signal): Current harmonic being used.
    """
    # Synthetic axis
    energy = Cpt(PseudoSingle, kind="normal", labels=["mono"])

    # Real motors
    dcmgap = Cpt(EpicsMotor, "XF:12ID:m66", read_attrs=["user_readback"], kind="normal", labels=["mono"])
    bragg = Cpt(EpicsMotor, "XF:12ID:m65", read_attrs=["user_readback"], kind="normal", labels=["mono"])

    # Feedback signals
    pitch_feedback_disabled = Cpt(
        EpicsSignal,
        "XF:12IDB-BI:2{EM:BPM3}fast_pidY_incalc.CLCN",
        name="manual_PID_disable_pitch",
    )
    roll_feedback_disabled = Cpt(
        EpicsSignal,
        "XF:12IDB-BI:2{EM:BPM3}fast_pidX_incalc.CLCN",
        name="manual_PID_disable_roll",
    )

    # Constants for energy calculations
    ANG_OVER_EV = 12398.42  # Conversion factor for energy to wavelength
    D_Si111 = 3.1293  # Lattice spacing for Si(111)

    # IVU gap
    ivugap = Cpt(
        InsertionDevice,
        "SR:C12-ID:G1{IVU:1-Ax:Gap}-Mtr",
        read_attrs=["user_readback"],
        configuration_attrs=[],
        labels=["mono"],
        add_prefix=(),
        kind="normal",
    )

    # Enable/disable signals
    enableivu = Cpt(Signal, value=True)
    enabledcmgap = Cpt(Signal, value=True)

    # IVU-gap experimental offset table (energy -> gap offset), seeded from the persistent Redis
    # config (mdsave) so it survives restarts and is recorded in every run as device config.  The
    # registered defaults equal the values that were previously hardcoded here, so behavior is
    # unchanged until re-calibrated + persisted.  Stored/read as plain lists (see _config).
    ivu_gap_offset_energies_eV = Cpt(
        Signal, value=_config.load("energy_ivu_gap_offset_energies_eV"), kind="config")
    ivu_gap_offset_values_um = Cpt(
        Signal, value=_config.load("energy_ivu_gap_offset_values_um"), kind="config")

    # Harmonic signals
    target_harmonic = Cpt(Signal, value=21)
    harmonic = Cpt(Signal, kind="normal", value=21)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hints = None

    def energy_to_bragg(self, target_energy, delta_bragg=0):
        """
        Convert energy to Bragg angle.

        Parameters:
            target_energy (float): Target energy in eV.
            delta_bragg (float): Offset for the Bragg angle.

        Returns:
            float: Bragg angle in degrees.
        """
        bragg_angle = (
            np.arcsin((self.ANG_OVER_EV / target_energy) / (2 * self.D_Si111))
            / np.pi
            * 180
            - delta_bragg
        )
        return bragg_angle

    def energy_to_gap(self, target_energy, undulator_harmonic=1, man_offset=0):
        """
        Convert energy to IVU gap.

        Parameters:
            target_energy (float): Target energy in eV.
            undulator_harmonic (int): Harmonic number.
            man_offset (float): Manual offset for the gap.

        Returns:
            float: IVU gap in mm.
        """
        fundamental_energy = target_energy / float(undulator_harmonic)
        f = fundamental_energy

        # Calculate the gap using a piecewise function
        gap_mm = -533.56314 + (1926.52257) * (
            0.28544 / (1 + 10 ** ((-10782.55855 - f) * 1.44995e-4))
            + (1 - 0.28544) / (1 + 10 ** ((7180.06758 - f) * 6.34167e-4))
        )

        # Experimental offsets for specific energies (seeded from persistent config; defaults
        # match the values previously hardcoded here).  Read back as lists -> np.asarray.
        e_exp = np.asarray(self.ivu_gap_offset_energies_eV.get(), dtype=float)
        off_exp = np.asarray(self.ivu_gap_offset_values_um.get(), dtype=float)

        # Interpolate the offset for the target energy
        auto_offset = np.interp(target_energy, e_exp, off_exp, left=min(off_exp), right=max(off_exp))
        gap = gap_mm * 1000 - auto_offset - man_offset

        # Apply a minimum gap correction for low energies
        if target_energy < 3000:
            gap = gap_mm * 1000 - 20
        return gap

    @pseudo_position_argument
    def forward(self, p_pos):
        """
        Convert pseudo position (energy) to real positions (bragg, dcmgap, ivugap).

        Parameters:
            p_pos (PseudoPosition): Desired pseudo position.

        Returns:
            RealPosition: Calculated real positions.
        """
        energy = p_pos.energy
        self.harmonic.put(int(self.target_harmonic.get()))

        if not self.harmonic.get() % 2:
            raise RuntimeError("Harmonic must be odd.")

        # Hard guardrails (a few eV outside the operational/validated 2.1 -> 16.1 keV range): the
        # validated floor / low-energy warn threshold is 2100 eV (the beamline minimum), and this
        # 2050 eV ValueError is the absolute backstop just below it.
        if energy <= 2050:
            raise ValueError("Minimum energy is 2050 eV.")

        if energy >= 24001:
            raise ValueError("Maximum energy is 24000 eV.")

        # Calculate target positions
        target_ivu_gap = self.energy_to_gap(energy, self.harmonic.get())
        while not (6200 <= target_ivu_gap < 15100):
            self.harmonic.put(int(self.harmonic.get()) - 2)
            if self.harmonic.get() < 1:
                raise RuntimeError("Cannot find a valid gap.")
            target_ivu_gap = self.energy_to_gap(energy, self.harmonic.get())

        target_bragg_angle = self.energy_to_bragg(energy)

        # Calculate DCM gap
        dcm_offset = 25
        target_dcm_gap = (dcm_offset / 2) / np.cos(target_bragg_angle * np.pi / 180)

        # Disable DCM gap movement if necessary
        if not self.enabledcmgap.get():
            target_dcm_gap = self.dcmgap.position

        # Disable IVU movement if necessary
        if not self.enableivu.get():
            target_ivu_gap = self.ivugap.position

        return self.RealPosition(
            bragg=target_bragg_angle, ivugap=target_ivu_gap, dcmgap=target_dcm_gap
        )

    @real_position_argument
    def inverse(self, r_pos):
        """
        Convert real positions (bragg) to pseudo position (energy).

        Parameters:
            r_pos (RealPosition): Real positions.

        Returns:
            PseudoPosition: Calculated pseudo position.
        """
        bragg = r_pos.bragg
        try:
            energy = self.ANG_OVER_EV / (2 * self.D_Si111 * math.sin(math.radians(bragg)))
        except ZeroDivisionError:
            energy = -1.0e23
        return self.PseudoPosition(energy=float(energy))

    @pseudo_position_argument
    def move(self, position, wait=True, timeout=None, moved_cb=None):
        """Move the energy, disabling DCM pitch/roll feedback for the duration of the move.

        Feedback is disabled up front (a couple of quick CA puts), the move is started, and the
        feedback is re-enabled from the move's completion callback.  The returned ``Status``
        completes when the move finishes; the re-enable is wired to that same completion so it is
        **guaranteed** to run on success or failure.

        This is overridden on ``move`` (not ``set``) on purpose: ophyd's ``PositionerBase.set``
        calls ``self.move`` (and ``PseudoPositioner.set`` -> ``super().set`` -> ``self.move``), so
        **every** entry point funnels through ``move`` -- a bare console ``energy.move(E)``, a direct
        ``energy.set(E)``, and ``bps.mv(energy, E)`` / the RunEngine (whose ``_set`` calls
        ``energy.set`` -> ``move``).  Overriding only ``set`` (as before) missed the bare
        ``energy.move(E)`` path entirely, so that console move skipped the feedback choreography.
        The feedback writes use ``put`` (not ``set``) so they are robust when the completion
        callback runs on a pyepics worker thread.

        Unmanaged-move courtesy warning
        -------------------------------
        A **large** move (``>= UNMANAGED_MOVE_WARN_eV``) made *directly* (``energy.move(E)`` /
        ``energy.set(E)`` at the console, not through the RunEngine) bypasses the managed-move
        preprocessor -- i.e. it does NOT get the feedback-managed ``energy_walk`` (stepped move,
        BPM3 ranging, flux gate, OVAL settle/recentre).  In that case a single ``warnings.warn``
        line is emitted as a gentle reminder to use ``RE(move_energy(E))`` / ``RE(energy_walk(E))``
        for the managed path.  (``warnings.warn`` -- not the "bluesky" logger, which is file-only in
        this deployment -- so the reminder is visible on the console, like the managed-move warning
        in ``energy_move_preprocessor``.)  This is intentionally quiet and only fires for large,
        direct moves: during setup (feedback not yet working) managed movement is meaningless, and
        small nudges aren't managed anyway, so neither is nagged.  The move still proceeds normally.
        """
        (energy,) = position
        if np.abs(energy - self.position[0]) < 0.01:
            return MoveStatus(self, energy, success=True, done=True)

        # Courtesy reminder: a LARGE move made directly (not via the RunEngine) skips the managed
        # ``energy_walk``.  Only warn for large, direct moves (see UNMANAGED_MOVE_WARN_eV) so setup
        # nudges and normal RE-driven moves stay silent.  Use ``warnings.warn`` (not the "bluesky"
        # logger, which is file-only here) so the reminder is actually visible on the console --
        # matching the managed-move warning in energy_move_preprocessor.  Force it through the
        # warnings de-dup filter (``simplefilter("always")`` in a scoped ``catch_warnings`` so the
        # global filter state is untouched) so an operator who repeats the same move still gets the
        # reminder every time.  Never let this gate the actual move.
        try:
            if (abs(energy - self.position[0]) >= UNMANAGED_MOVE_WARN_eV
                    and not _running_under_run_engine()):
                with warnings.catch_warnings():
                    warnings.simplefilter("always")
                    warnings.warn(
                        "energy: direct move {:.1f} -> {:.1f} eV (>= {:.0f} eV) is NOT going "
                        "through the RunEngine, so it skips the feedback-managed energy_walk "
                        "(stepping, BPM3 ranging, flux gate, OVAL recentre).  Use "
                        "RE(move_energy(E)) or RE(energy_walk(E)) for the managed move.  (Fine "
                        "during setup when feedback isn't running -- managed movement is a no-op "
                        "then.)".format(self.position[0], energy, UNMANAGED_MOVE_WARN_eV),
                        stacklevel=2,
                    )
        except Exception:
            pass

        # Disable feedback up front and WAIT for the puts to complete (on the calling thread,
        # where a CA context exists) so feedback is provably off before the move begins -- a
        # fire-and-forget put could otherwise land after a fast move already re-enabled it.
        self.pitch_feedback_disabled.put("1", wait=True)
        self.roll_feedback_disabled.put("1", wait=True)

        # Re-enable feedback when the move finishes (success OR failure).  Wire the callback BEFORE
        # calling ``super().move`` so it is attached even if ``wait=True`` blocks here until done
        # (ophyd fires an add_callback immediately if the status is already finished).  ``position``
        # is already a validated PseudoPosition (``@pseudo_position_argument``), so pass it straight
        # through to the ophyd machinery.
        try:
            move_status = super().move(position, wait=False, timeout=timeout, moved_cb=moved_cb)
        except Exception:
            # Move failed to even start -> re-enable feedback and re-raise.
            self._reenable_feedback()
            raise

        move_status.add_callback(self._reenable_feedback)

        if wait:
            # Preserve the blocking-convenience contract of ``energy.move(E)`` / ``super().move``
            # with wait=True: block here until the motion (and thus the feedback re-enable) is done.
            move_status.wait()
        return move_status

    def _reenable_feedback(self, *args, **kwargs):
        """Re-enable DCM pitch/roll feedback (``put`` so it is safe on a worker thread)."""
        try:
            ca.use_initial_context()
        except Exception:
            pass
        try:
            self.pitch_feedback_disabled.put("0")
            self.roll_feedback_disabled.put("0")
        except Exception as exc:
            logger.warning("energy: failed to re-enable DCM feedback: %r", exc)


    def small_move(self, target_energy, *, min_move_time=1.0, min_velocity=1e-4,
                   min_gap_speed=1e-3):
        """Plan: smoothly move to ``target_energy`` for a SMALL energy step.

        Moves the Bragg angle and the IVU gap **together**, temporarily matching the speed of
        the faster axis to the slower one so both arrive simultaneously.  Keeping the two in
        lock-step means the photon energy stays near the undulator flux peak throughout the
        move, so the beam is not lost (the motivation for this method vs. a normal
        ``bps.mv(energy, E)``, which moves the axes independently).

        Notes
        -----
        * This is a **small-move** helper: it moves only ``bragg`` and ``ivugap`` (not the DCM
          gap).  The DCM-gap change over a small energy step is negligible, so the beam offset
          drift is ignored here; use the normal ``set``/``move`` path for large moves where the
          gap (and harmonic) must change.
        * The DCM pitch/roll BPM feedback is left **ON** during this move so it keeps the beam
          centred while the optics move slowly together (unlike the large-move ``set`` path,
          which disables feedback).
        * The harmonic is taken as-is from ``self.harmonic``; the target IVU gap must fall in
          the valid range for that harmonic or a ``RuntimeError`` is raised (small moves should
          not cross a harmonic boundary -- use the normal move path if they do).
        * The temporary speed changes are restored on success **and on error/abort** (via a
          ``finalize``), so an interrupted small move never leaves the axes at a wrong speed.

        Parameters
        ----------
        target_energy : float
            Target photon energy in eV.
        min_move_time : float
            Floor on the synchronised move duration (s), to avoid commanding very fast moves.
        min_velocity, min_gap_speed : float
            Floors for the Bragg velocity (deg/s) and IVU gap speed (mm/s); a computed speed
            below the floor is clamped to it (the move then takes a little less than
            ``move_time`` for that axis, which is the safe direction).
        """
        current_bragg = self.bragg.position
        current_ivu = self.ivugap.position

        target_bragg = self.energy_to_bragg(target_energy)
        target_ivu = self.energy_to_gap(target_energy, self.harmonic.get())
        logger.debug("small_move -> E=%.3f eV: bragg %.5f->%.5f deg, IVU %.3f->%.3f um",
                     target_energy, current_bragg, target_bragg, current_ivu, target_ivu)

        if not (6200 <= target_ivu < 15100):
            raise RuntimeError(
                "Target IVU gap {:.1f} um out of range for a small move (harmonic={}); "
                "use the normal energy move.".format(target_ivu, int(self.harmonic.get())))

        delta_bragg = target_bragg - current_bragg
        delta_ivu = target_ivu - current_ivu

        # Current (to-be-restored) axis speeds.
        orig_bragg_velocity = self.bragg.velocity.get()
        orig_ivu_gap_speed = self.ivugap.gap_speed.get()

        # Time each axis would take at its current speed; the slower one sets the pace.
        bragg_time = abs(delta_bragg) / orig_bragg_velocity if orig_bragg_velocity else 0.0
        ivu_time = abs(delta_ivu) / orig_ivu_gap_speed if orig_ivu_gap_speed else 0.0
        move_time = max(bragg_time, ivu_time, min_move_time)
        logger.debug("small_move: bragg_time=%.3fs ivu_time=%.3fs -> move_time=%.3fs",
                     bragg_time, ivu_time, move_time)

        # Slow the FASTER axis (and the floored case: both) so each finishes in ~move_time.
        # Clamp to a minimum speed so we never command a sub-minimum (stalling) speed.
        new_bragg_velocity = max(abs(delta_bragg) / move_time, min_velocity)
        new_ivu_gap_speed = max(abs(delta_ivu) / move_time, min_gap_speed)

        def _restore():
            # wait=True so the speeds are actually back to their originals before the plan ends.
            yield from bps.abs_set(self.bragg.velocity, orig_bragg_velocity, wait=True)
            yield from bps.abs_set(self.ivugap.gap_speed, orig_ivu_gap_speed, wait=True)
            logger.debug("small_move: restored bragg velocity=%.4f, IVU gap speed=%.4f",
                         orig_bragg_velocity, orig_ivu_gap_speed)

        def _do_move():
            # Set the matched speeds (wait so they take effect before the move), then move both
            # axes together.
            yield from bps.abs_set(self.bragg.velocity, new_bragg_velocity, wait=True)
            yield from bps.abs_set(self.ivugap.gap_speed, new_ivu_gap_speed, wait=True)
            yield from bps.mv(self.bragg, target_bragg, self.ivugap, target_ivu)

        # Restore speeds whether the move succeeds, errors, or is aborted.
        yield from bpp.finalize_wrapper(_do_move(), _restore())


