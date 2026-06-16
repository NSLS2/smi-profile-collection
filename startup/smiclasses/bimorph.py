import re
import numpy as np
from ophyd import (
    EpicsSignal,
    EpicsSignalRO,
    Signal,
    Device,
    Component as Cpt,
)
import bluesky.plan_stubs as bps

from . import _config


#: number of bimorph channels
N_BIMORPH_CH = 16


class _BimorphChannels:
    """Mixin with the generic per-channel mechanics shared by HFM_voltage / VFM_voltage.

    Controller PV map (CAENels bimorph PSU; per channel ``n`` in 0..15) and VERIFIED apply
    mechanism:
      * ``GET-VOUT<n>``    : live OUTPUT voltage read-back            (``ch<n>``)
      * ``SET-VTRGT<n>``   : stage a per-channel TARGET               (``ch<n>_trg``)
      * ``GET-VTRGT<n>``   : read-back of the staged target           (``ch<n>_trg_rb``)
      * ``GET-STATUS<n>``  : per-channel state: "On" / "Busy"         (``ch<n>_status``)
      * ``SET-ALLTRGT``    : the APPLY trigger                        (``apply``)
      * ``SET-VOUT<n>``    : set the OUTPUT directly (unused here; slow, one channel at a time)
      * ``SET-ALLON`` / ``SET-ALLOFF`` : HV on/off ; ``GET-STATUS`` / ``GET-LASTERR`` : diagnostics

    The two-step "stage then apply" sequence (verified on hardware):
      1. write ``SET-VTRGT<n>`` -> after ~1 s ``GET-VTRGT<n>`` reflects it; **no motion**;
      2. write ``SET-ALLTRGT = 1`` (``apply``) -> over a few seconds each ``GET-VTRGT<n>`` is
         ramped onto ``GET-VOUT<n>``, with ``GET-STATUS<n>`` going "On" -> "Busy" -> "On".

    So staging is safe (never moves), and a move is only triggered by ``apply``.  Completion is
    detected by every channel's ``GET-STATUS`` returning to "On" (not "Busy").

    Helpers are plain reads + generator (plan) writers so they compose into RunEngine plans.
    """

    #: per-channel status string that means "settled / not moving"
    STATUS_IDLE = "On"
    STATUS_BUSY = "Busy"

    def read_outputs(self):
        """Return the 16 live OUTPUT voltages (GET-VOUT) as a list of floats. (Not a plan.)"""
        return [float(getattr(self, "ch{}".format(i)).get()) for i in range(N_BIMORPH_CH)]

    def read_targets(self):
        """Return the 16 staged TARGET read-backs (GET-VTRGT) as a list of floats. (Not a plan.)"""
        return [float(getattr(self, "ch{}_trg_rb".format(i)).get()) for i in range(N_BIMORPH_CH)]

    def channel_states(self):
        """Return the 16 per-channel GET-STATUS strings (e.g. 'On'/'Busy'). (Not a plan.)"""
        return [str(getattr(self, "ch{}_status".format(i)).get()) for i in range(N_BIMORPH_CH)]

    def is_busy(self):
        """True if ANY channel reports busy (mid-ramp). (Not a plan.)"""
        return any(s == self.STATUS_BUSY for s in self.channel_states())

    def set_targets(self, voltages):
        """PLAN: stage the 16 per-channel targets (SET-VTRGT).  Does NOT move the mirror.

        ``voltages`` must have length ``N_BIMORPH_CH``.  Staging is safe -- it never actuates;
        the move only happens on :meth:`apply`.
        """
        voltages = list(voltages)
        if len(voltages) != N_BIMORPH_CH:
            raise ValueError("expected {} voltages, got {}".format(N_BIMORPH_CH, len(voltages)))
        args = []
        for i, v in enumerate(voltages):
            args += [getattr(self, "ch{}_trg".format(i)), float(v)]
        yield from bps.mv(*args)

    def sync_targets_to_outputs(self):
        """PLAN: copy each live OUTPUT into its TARGET (targets only -- never moves the mirror).

        Makes the staged target state match what the mirror is actually outputting (useful because
        the targets can be left at 0, which would drive the mirror to 0 if applied).
        """
        yield from self.set_targets(self.read_outputs())

    def apply(self):
        """PLAN: trigger the ramp of the staged targets onto the outputs (write SET-ALLTRGT=1).

        Does NOT wait -- use :meth:`apply_and_wait` to block until the channels settle.  Written
        without put-completion (this controller's put-callback always fails though the put lands).
        """
        self.apply_sig.put(1)
        yield from bps.null()

    def apply_and_wait(self, settle=1.0, timeout=120.0, poll=0.5):
        """PLAN: apply the staged targets, then wait until every channel's status leaves 'Busy'.

        Triggers ``SET-ALLTRGT`` then polls ``GET-STATUS<n>`` until none are busy (and stays
        non-busy for ``settle`` s, to ride out the On->Busy transition latency).  Raises
        TimeoutError if not settled within ``timeout`` s.
        """
        import time as _time

        yield from self.apply()
        deadline = _time.monotonic() + timeout
        stable_since = None
        while True:
            busy = self.is_busy()
            now = _time.monotonic()
            if busy:
                stable_since = None
            else:
                # require a brief stable window: the controller takes ~1 s to even go Busy, so
                # "not busy" immediately after apply could just be pre-transition.
                if stable_since is None:
                    stable_since = now
                elif now - stable_since >= settle:
                    return
            if now > deadline:
                raise TimeoutError(
                    "{}: bimorph did not settle within {:.0f}s (states={})".format(
                        self.name, timeout, self.channel_states()))
            yield from bps.sleep(poll)


class HFM_voltage(_BimorphChannels, Device):
    # Per-channel components generated flat (ch<n>, ch<n>_trg, ch<n>_trg_rb, ch<n>_status) so the
    # historical access pattern (hfm_voltage.ch0 / .ch0_trg) and the set_target dir()-walk keep
    # working.  Defined via a class-body loop to avoid 64 hand-typed lines.
    for _i in range(N_BIMORPH_CH):
        locals()["ch{}".format(_i)] = Cpt(EpicsSignal, "GET-VOUT{}".format(_i))
        locals()["ch{}_trg".format(_i)] = Cpt(EpicsSignal, "SET-VTRGT{}".format(_i),
                                               put_complete=False)
        locals()["ch{}_trg_rb".format(_i)] = Cpt(EpicsSignalRO, "GET-VTRGT{}".format(_i))
        locals()["ch{}_status".format(_i)] = Cpt(EpicsSignalRO, "GET-STATUS{}".format(_i),
                                                  string=True)
    del _i

    shift_rel = Cpt(EpicsSignal, "SET-ALLSHIFT")
    # SET-ALLTRGT is the APPLY trigger: writing 1 ramps the staged SET-VTRGT targets onto the
    # outputs (GET-STATUS goes On->Busy->On).  put_complete False: the controller's put-callback
    # always fails though the put lands.
    apply_sig = Cpt(EpicsSignal, "SET-ALLTRGT", put_complete=False)
    set_tar = apply_sig  # backwards-compat alias (old move_target wrote set_tar)

    # Default HFM bimorph voltages for the SMI SWAXS hutch, plus the additive low-divergence
    # offset.  Seeded from the persistent Redis config (mdsave); the registered defaults equal the
    # values that were previously hardcoded here, so behavior is unchanged until re-calibrated +
    # persisted.  kind="config" so they are recorded in every run.  Tables read back as lists.
    default_hfm_v = Cpt(Signal, value=_config.load("bimorph_hfm_default_v"), kind="config")
    lowdiv_offset_v = Cpt(Signal, value=_config.load("bimorph_hfm_lowdiv_offset_v"), kind="config")

    def set_target(self, mode="SWAXS"):
        """PLAN: stage the default HFM voltages (SET-VTRGT only; does NOT apply/move)."""
        defaults = np.asarray(self.default_hfm_v.get())
        offset = self.lowdiv_offset_v.get()
        # offset (default -80) shifts to the low-divergence configuration
        yield from self.set_targets([offset + defaults[i] for i in range(N_BIMORPH_CH)])

    def move_target(self):
        """PLAN: apply the staged targets (trigger the ramp).  See _BimorphChannels.apply()."""
        yield from self.apply()

    def shift_relative(self, relative_value=0):
        yield from bps.mv(self.shift_rel, relative_value)

    def move_abs(self, mode="SWAXS"):
        yield from self.set_target(mode=mode)
        yield from bps.sleep(5)
        yield from self.move_target()




class VFM_voltage(_BimorphChannels, Device):
    for _i in range(N_BIMORPH_CH):
        locals()["ch{}".format(_i)] = Cpt(EpicsSignal, "GET-VOUT{}".format(_i))
        locals()["ch{}_trg".format(_i)] = Cpt(EpicsSignal, "SET-VTRGT{}".format(_i),
                                               put_complete=False)
        locals()["ch{}_trg_rb".format(_i)] = Cpt(EpicsSignalRO, "GET-VTRGT{}".format(_i))
        locals()["ch{}_status".format(_i)] = Cpt(EpicsSignalRO, "GET-STATUS{}".format(_i),
                                                  string=True)
    del _i

    shift_rel = Cpt(EpicsSignal, "SET-ALLSHIFT")
    apply_sig = Cpt(EpicsSignal, "SET-ALLTRGT", put_complete=False)  # APPLY trigger (write 1)
    set_tar = apply_sig  # backwards-compat alias

    # Default VFM bimorph voltages (SWAXS hutch and OPLS hutch), seeded from the persistent Redis
    # config (mdsave).  Registered defaults equal the values previously hardcoded here, so behavior
    # is unchanged until re-calibrated + persisted.  kind="config"; tables read back as lists.
    # Alternate edge tables kept for reference:
    #   Ca edge: -430 + [ 39,  85, 311, 310,  -15, 485,  68, 447, 291, 130, 606, 170, 272, 437, 192, -308]
    #   S  edge: [-281, -235, -9, -10, -335, 165, -252, 127, -29, -190, 286, -150, -48, 117, -128, -628]
    default_vfm_v = Cpt(Signal, value=_config.load("bimorph_vfm_default_v"), kind="config")
    default_vfm_opls_v = Cpt(Signal, value=_config.load("bimorph_vfm_opls_default_v"), kind="config")

    def set_target(self, mode="SWAXS"):
        """PLAN: stage the default VFM voltages for ``mode`` (SET-VTRGT only; does NOT apply)."""
        if mode == "SWAXS":
            table = np.asarray(self.default_vfm_v.get())
        elif mode == "OPLS":
            table = np.asarray(self.default_vfm_opls_v.get())
        else:
            print("Unknown mode, you should choose between SWAXS or OPLS")
            return
        yield from self.set_targets([table[i] for i in range(N_BIMORPH_CH)])

    def move_target(self):
        """PLAN: apply the staged targets (trigger the ramp).  See _BimorphChannels.apply()."""
        yield from self.apply()

    def shift_relative(self, relative_value=0):
        yield from bps.mv(self.shift_rel, relative_value)

    def move_abs(self, mode="SWAXS"):
        yield from self.set_target(mode=mode)
        yield from bps.sleep(5)
        yield from self.move_target()

