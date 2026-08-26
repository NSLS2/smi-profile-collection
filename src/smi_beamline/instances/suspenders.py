
import os
import bluesky.plans as bp
from bluesky.suspenders import (
    SuspendFloor,
    SuspendBoolLow,
    SuspendBoolHigh,
    SuspendCeil,
)
from ophyd import EpicsMotor, EpicsSignal, Device, Component as Cpt
from smi_beamline.devices import _context
RE = _context.get_re()
from smi_beamline.instances.machine import ring, smi_shutter_enable
from smi_beamline.instances.electrometers import ls, xbpm3
from smi_beamline.instances.manipulators import stage_temps

# When the beam is down (e.g. testing / restarting Bluesky during a shutdown) the suspenders
# would immediately pause everything (ring current / shutter floors).  The "beam is down" state is
# read ONCE here, at startup, from the persistent Redis flag 'swaxsstatus:beam_down' (db=3) -- set
# it with  set_beam_down()  (or the start-beamdown pixi task) BEFORE launching Bluesky to BUILD the
# suspenders but NOT enable them, so you can test/restart without running turn_off_suspenders()
# every time.  Re-enable in a live session with  turn_on_suspenders()  once the beam is back.
#
# Redis (not an env var) so the SAME flag reaches both the interactive terminal and the
# queueserver worker (which runs on a separate host).  The legacy BEAM_DOWN/SMI_BEAM_DOWN env vars
# are still honoured as a fallback (see beam_down_active).
from smi_beamline.plans.re_status import beam_down_active, set_beam_down, clear_beam_down, read_beam_down
BEAM_DOWN = beam_down_active()


def _install(suspender,needs_beam=True):
    """Install a suspender unless BEAM_DOWN (then just build it for later turn_on_suspenders())."""
    if not BEAM_DOWN or not needs_beam:
        RE.install_suspender(suspender)


# Temperature of the WAXS motor suspender
susp_waxs_motor = SuspendCeil(ls.input_C, 150 + 273, resume_thresh=120 + 273)
_install(susp_waxs_motor,needs_beam=False)
susp_x_motor = SuspendCeil(stage_temps.x, 100, resume_thresh=90)
_install(susp_x_motor,needs_beam=False)
susp_y_motor = SuspendCeil(stage_temps.y, 100, resume_thresh=90)
_install(susp_y_motor,needs_beam=False)
susp_z_motor = SuspendCeil(stage_temps.z, 100, resume_thresh=90)
_install(susp_z_motor,needs_beam=False)
susp_th_motor = SuspendCeil(stage_temps.th, 100, resume_thresh=90)
_install(susp_th_motor,needs_beam=False)
susp_chi_motor = SuspendCeil(stage_temps.chi, 100, resume_thresh=90)
_install(susp_chi_motor,needs_beam=False)
susp_phi_motor = SuspendCeil(stage_temps.phi, 100, resume_thresh=90)
_install(susp_phi_motor,needs_beam=False)

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


#Count on XBPM3 suspender
susp_xbpm3_sum = SuspendFloor( xbpm3.sumY, 5, resume_thresh= 20 )
#_install( susp_xbpm3_sum )


# Ring current suspender
susp_beam = SuspendFloor(ring.current, 100, resume_thresh=350, sleep=600)
_install(susp_beam)

# Front end shutter suspender
susp_smi_shutter = SuspendFloor(smi_shutter_enable, 0.1, resume_thresh=0.9)
_install(susp_smi_shutter)


def turn_on_suspenders():
    RE.install_suspender(susp_waxs_motor)
    RE.install_suspender(susp_x_motor)
    RE.install_suspender(susp_y_motor)
    RE.install_suspender(susp_z_motor)
    RE.install_suspender(susp_th_motor)
    RE.install_suspender(susp_chi_motor)
    RE.install_suspender(susp_phi_motor)
    RE.install_suspender(susp_smi_shutter)
    RE.install_suspender(susp_beam)
    #RE.install_suspender(susp_xbpm3_sum)
    print('Suspenders turned on')


def turn_off_suspenders():
    RE.clear_suspenders()
    print('Suspenders turned off')


if BEAM_DOWN:
    print("\n" + "!" * 72)
    print("!!  BEAM_DOWN is set: suspenders requiring beam are NOT enabled.")
    print("!!  The RunEngine will NOT pause on low ring current / shutter.")
    print("!!  Run  turn_on_suspenders()  once the beam is back to re-enable them,")
    print("!!  and  clear_beam_down()  to clear the persistent flag for future restarts.")
    print("!" * 72 + "\n")
    