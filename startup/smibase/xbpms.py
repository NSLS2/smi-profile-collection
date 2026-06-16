
from ophyd import EpicsSignal
from smi_beamline.devices.xbpms import XBPM

xbpm1_pos = XBPM("XF:12IDA-BI:2{XBPM:1-Ax:", name="xbpm1_pos")
xbpm2_pos = XBPM("XF:12IDA-BI:2{XBPM:2-Ax:", name="xbpm2_pos")
xbpm3_pos = XBPM("XF:12IDB-BI:2{XBPM:3-Ax:", name="xbpm3_pos")


xbpm3y = EpicsSignal("XF:12IDB-BI:2{EM:BPM3}PosY:MeanValue_RBV", name="xbpm3y")


from smi_beamline.devices import _context

_context.baseline_register([xbpm1_pos, xbpm2_pos, xbpm3_pos])