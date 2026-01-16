
print(f"Loading {__file__}")

from smiclasses.beamstop import SAXSBeamStops
from ophyd import EpicsMotor
from time import ctime



saxs_bs = SAXSBeamStops("XF:12IDC-ES:2{BS:SAXS-Ax:", name="saxs_beamstop")
waxs_bs = EpicsMotor("XF:12ID2C-ES{MCS:2-Ax:1}Mtr", name="waxs_beamstop")



from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([saxs_bs])
