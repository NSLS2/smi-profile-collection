print(f"Loading {__file__}")

import os
import bluesky.plans as bp
from bluesky.suspenders import (
    SuspendFloor,
    SuspendBoolLow,
    SuspendBoolHigh,
    SuspendCeil,
)
from ophyd import EpicsMotor, EpicsSignal, Device, Component as Cpt
from smiclasses import _context
RE = _context.get_re()
from .machine import ring, smi_shutter_enable
from .electrometers import ls, xbpm2

# When the beam is down (e.g. testing / restarting Bluesky during a shutdown) the suspenders
# would immediately pause everything (ring current / shutter floors).  Set the environment
# variable BEAM_DOWN=1 before launching Bluesky to BUILD the suspenders but NOT enable them, so
# you can test without running turn_off_suspenders() every restart.  Re-enable with
# turn_on_suspenders() once the beam is back.
BEAM_DOWN = os.environ.get("BEAM_DOWN", os.environ.get("SMI_BEAM_DOWN", "")).strip().lower() \
    in ("1", "true", "yes", "on")


def _install(suspender):
    """Install a suspender unless BEAM_DOWN (then just build it for later turn_on_suspenders())."""
    if not BEAM_DOWN:
        RE.install_suspender(suspender)


# Temperature of the WAXS motor suspender
susp_waxs_motor = SuspendCeil(ls.input_C, 150 + 273, resume_thresh=120 + 273)
_install(susp_waxs_motor)
susp_phi_motor = SuspendCeil(ls.input_D, 150 + 273, resume_thresh=120 + 273)
_install(susp_phi_motor)

# # Count on XBPM2 suspender
# susp_xbpm2_sum = SuspendFloor(xbpm2.sumY, 0.3, resume_thresh=0.8)
# RE.install_suspender(susp_xbpm2_sum)


def stop_turbo():
    turbo_onoff = EpicsSignal("XF:12IDC-VA:2{Det:300KW-TMP:1}OnOff", name="turbo_onoff")
    turbo_onoff.put(0)

    iv1 = EpicsSignal("XF:12IDC-VA:2{Det:300KW-IV:1}Cmd:Cls-Cmd", name="iv1")
    iv1.put(1)


# waxs_pr = SuspendCeil(chamber_pressure.maxs, 9.1E-03, pre_plan = stop_turbo())
# RE.install_suspender(waxs_pr)

"""
#Count on XBPM3 suspender
susp_xbpm3_sum = SuspendFloor( xbpm3.sumY, 0.3, resume_thresh= 0.8 )
RE.install_suspender( susp_xbpm3_sum )
"""

# Ring current suspender
susp_beam = SuspendFloor(ring.current, 100, resume_thresh=350, sleep=600)
_install(susp_beam)

# Front end shutter suspender
susp_smi_shutter = SuspendFloor(smi_shutter_enable, 0.1, resume_thresh=0.9)
_install(susp_smi_shutter)


def turn_on_suspenders():
    RE.install_suspender(susp_waxs_motor)
    RE.install_suspender(susp_phi_motor)
    RE.install_suspender(susp_smi_shutter)
    RE.install_suspender(susp_beam)
    # RE.install_suspender(susp_xbpm2_sum)
    print('Suspenders turned on')


def turn_off_suspenders():
    RE.clear_suspenders()
    print('Suspenders turned off')


if BEAM_DOWN:
    print("\n" + "!" * 72)
    print("!!  BEAM_DOWN is set: suspenders are BUILT but NOT enabled.")
    print("!!  The RunEngine will NOT pause on low ring current / shutter / temperature.")
    print("!!  Run  turn_on_suspenders()  once the beam is back to re-enable them.")
    print("!" * 72 + "\n")
    