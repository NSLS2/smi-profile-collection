from ophyd import EpicsMotor

from smi_beamline.devices import _context
from smi_beamline.devices.beamstop import SAXSBeamStops


saxs_bs = SAXSBeamStops("XF:12IDC-ES:2{BS:SAXS-Ax:", name="saxs_beamstop")
waxs_bs = EpicsMotor("XF:12ID2C-ES{MCS:2-Ax:1}Mtr", name="waxs_beamstop")

_context.baseline_register([saxs_bs])
