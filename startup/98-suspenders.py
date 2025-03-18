print(f"Loading {__file__}")

import bluesky.plans as bp
from bluesky.suspenders import (
    SuspendFloor,
    SuspendBoolLow,
    SuspendBoolHigh,
    SuspendCeil,
)
from ophyd import EpicsMotor, EpicsSignal, Device, Component as Cpt

# Temperature of the WAXS motor suspender
susp_waxs_motor = SuspendCeil(ls.input_C, 150 + 273, resume_thresh=120 + 273)
RE.install_suspender(susp_waxs_motor)

# Count on XBPM2 suspender
susp_xbpm2_sum = SuspendFloor(xbpm2.sumY, 0.3, resume_thresh=0.8)
RE.install_suspender(susp_xbpm2_sum)


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
RE.install_suspender(susp_beam)

# Front end shutter suspender
susp_smi_shutter = SuspendFloor(smi_shutter_enable, 0.1, resume_thresh=0.9)
RE.install_suspender(susp_smi_shutter)


def turn_on_suspenders():
    RE.install_suspender(susp_waxs_motor)
    RE.install_suspender(susp_smi_shutter)
    RE.install_suspender(susp_beam)
    RE.install_suspender(susp_xbpm2_sum)
    print('Suspenders turned on')
    

def turn_off_suspenders():
    RE.clear_suspenders()
    print('Suspenders turned off')
    