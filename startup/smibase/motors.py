

from smi_beamline.devices.motors import MDriveMotor, SAXSBeamStop, DetMotor, ThorlabsMotor
from ophyd import EpicsMotor

## for MDrive, YZhang
MDrive =  MDriveMotor("XF:12ID2-ES{Mdrive-Ax:", name = "MDrive")

## SAXS det position
#SAXS = DetMotor("XF:12IDC-ES:2{Det:1M-Ax:", name="saxs_detector")

## stages for SAXS beamstops
#SBS = SAXSBeamStop("XF:12IDC-ES:2{BS:SAXS-Ax:", name="saxs_beamstop")
 

thorlabs_su = ThorlabsMotor('XF:12ID2-ES{DDSM100-Ax:X1}Mtr',name='thorlabs_su')


# (no devices registered to the baseline here)
# _context.baseline_register([MDrive, thorlabs_su])