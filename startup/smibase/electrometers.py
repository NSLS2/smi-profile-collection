print(f"Loading {__file__}")

from smiclasses.electrometers import XBPM, new_LakeShore, Keithly2450
from ophyd import EpicsSignal
from nslsii.ad33 import QuadEMV33


ls = new_LakeShore("XF:12ID-ES", name="ls")


xbpm1 = XBPM("XF:12IDA-BI:2{EM:BPM1}", name="xbpm1") # fast shutter
xbpm2 = XBPM("XF:12IDA-BI:2{EM:BPM2}", name="xbpm2") # xbpm2
xbpm3 = XBPM("XF:12IDB-BI:2{EM:BPM3}", name="xbpm3") # xbpm3
xbpm3.sumY.kind = "hinted"
xbpm3.sumX.kind = "hinted"
xbpm2.sumY.kind = "hinted"
xbpm2.sumX.kind = "hinted"


ssacurrent = EpicsSignal(
    "XF:12IDB-BI{EM:SSASlit}SumAll:MeanValue_RBV", name="ssacurrent"
)

pdcurrent = EpicsSignal(
    "XF:12ID:2{EM:Tetr1}Current2:MeanValue_RBV", name="pdcurrent", auto_monitor=True
)
pdcurrent1 = EpicsSignal(
    "XF:12ID:2{EM:Tetr1}Current2Ave", name="pdcurrent1", auto_monitor=True
)
pdcurrent2 = EpicsSignal(
    "XF:12ID:2{EM:Tetr1}SumAllAve", name="pdcurrent2", auto_monitor=True
)



keithly2450 = Keithly2450("XF:12IDA{dmm:2}:K2450:1:", name="keithly2450")
hfmcurrent = EpicsSignal("XF:12IDA{dmm:2}:K2450:1:reading", name="hfmcurrent")

pin_diode = QuadEMV33("XF:12ID:2{EM:Tetr1}", name="pin_diode")
pin_diode.stage_sigs["conf.port_name"] = "TetrAMM"
pin_diode.stage_sigs["acquire_mode"] = 2

for i in (1, 2, 3, 4):
    getattr(pin_diode, f"current{i}").mean_value.kind = "normal"
pin_diode.current2.mean_value.kind = "hinted"




from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([xbpm2, xbpm3,ls])