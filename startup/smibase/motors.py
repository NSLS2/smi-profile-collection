
print(f"Loading {__file__}")

from smiclasses.motors import MDriveMotor, SAXSBeamStop, DetMotor, ThorlabsMotor

## for MDrive, YZhang
MDrive =  MDriveMotor("XF:12ID2-ES{Mdrive-Ax:", name = "MDrive")

## SAXS det position
SAXS = DetMotor("XF:12IDC-ES:2{Det:1M-Ax:", name="SAXS")
## stages for SAXS beamstops
SBS = SAXSBeamStop("XF:12IDC-ES:2{BS:SAXS-Ax:", name="SBS")


thorlabs_su = ThorlabsMotor('XF:12ID2-ES{DDSM100-Ax:X1}Mtr',name='thorlabs_su')



from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([SAXS, SBS, MDrive, thorlabs_su])