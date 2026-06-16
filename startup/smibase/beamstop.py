
print(f"Loading {__file__}")

from smiclasses.beamstop import SAXSBeamStops
from ophyd import EpicsMotor
from time import ctime


saxs_bs = SAXSBeamStops("XF:12IDC-ES:2{BS:SAXS-Ax:", name="saxs_beamstop")
waxs_bs = EpicsMotor("XF:12ID2C-ES{MCS:2-Ax:1}Mtr", name="waxs_beamstop")


from smiclasses import _context

_context.baseline_register([saxs_bs])
