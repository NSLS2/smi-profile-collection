print(f"Loading {__file__}")

from ophyd import EpicsSignal
from ..smiclasses.xbpms import XBPM

xbpm1_pos = XBPM("XF:12IDA-BI:2{XBPM:1-Ax:", name="xbpm1_pos")
xbpm2_pos = XBPM("XF:12IDA-BI:2{XBPM:2-Ax:", name="xbpm2_pos")
xbpm3_pos = XBPM("XF:12IDB-BI:2{XBPM:3-Ax:", name="xbpm3_pos")


xbpm3y = EpicsSignal("XF:12IDB-BI:2{EM:BPM3}PosY:MeanValue_RBV", name="xbpm3y")



from .base import sd

sd.baseline.extend([xbpm1_pos, xbpm2_pos, xbpm3_pos])