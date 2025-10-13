print(f"Loading {__file__}")

from smiclasses.shutter import TwoButtonShutter, SMIFastShutter
from ophyd import EpicsMotor
from .energy import energy
import bluesky.plan_stubs as bps


ph_shutter = TwoButtonShutter("XF:12IDA-PPS:2{PSh}", name="ph_shutter")


def shopen(feedback=True):
    yield from bps.mv(ph_shutter.open_cmd, 1)
    yield from bps.sleep(1)

    if feedback:
        yield from bps.mv(energy.pitch_feedback_disabled, "0")
        yield from bps.mv(energy.roll_feedback_disabled, "0")

    # #Check if te set-up is in-air or not. If so, open the GV automatically when opening the shutter
    # if get_chamber_pressure(chamber_pressure.waxs) > 1E-02 and get_chamber_pressure(chamber_pressure.maxs) < 1E-02:
    #    yield from bps.mv(GV7.open_cmd, 1 )
    #    yield from bps.sleep(1)
    #    yield from bps.mv(GV7.open_cmd, 1 )
    #    yield from bps.sleep(1)


def shclose(feedback=True):
    if not feedback:
        print('feedback is always turned off when closing the shutter for safety')
    yield from bps.mv(energy.pitch_feedback_disabled, "1")
    yield from bps.mv(energy.roll_feedback_disabled, "1")
    yield from bps.sleep(3)
    yield from bps.mv(ph_shutter.close_cmd, 1)

    # #Check if te set-up is in-air or not. If so, close the GV automatically when opening the shutter
    # if get_chamber_pressure(chamber_pressure.waxs) > 1E-02 and get_chamber_pressure(chamber_pressure.maxs) < 1E-02:
    #   yield from bps.mv(GV7.close_cmd, 1 )
    #   yield from bps.sleep(1)
    #   yield from bps.mv(GV7.close_cmd, 1 )
    #   yield from bps.sleep(1)


fs = SMIFastShutter("", name="fs")

fs_motor = EpicsMotor("XF:12IDC:2{Sh:E-Ax:Y}Mtr", name="fshutter_motor")


GV7 = TwoButtonShutter("XF:12IDC-VA:2{Det:1M-GV:7}", name="GV7")



from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([ GV7, ph_shutter])