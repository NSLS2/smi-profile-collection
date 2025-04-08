print(f"Loading {__file__}")

from ..smiclasses.slits import SLIT, SLTH, SLTV, APER

# white beam slits
wbs = SLIT("XF:12IDA-OP:2{Slt:WB-Ax:", name="wbs")

# ssa
ssa = SLIT("XF:12IDB1-OP:2{Slt:SSA-Ax:", name="ssa")


# C hutch slits
cslit = SLIT("XF:12IDC-OP:2{Slt:C-Ax:", name="cslit")
eslit = SLIT("XF:12IDC-OP:2{Slt:E-Ax:", name="eslit")


# FOE mono beam slits
hfmslit = SLTH("XF:12IDA-OP:2{Slt:H-Ax:", name="hfmslit")
vfmslit = SLTV("XF:12IDA-OP:2{Slt:V-Ax:", name="vfmslit")


# C hutch aperture (after crls)
dsa = APER("XF:12IDC-OP:2{Lens:CRL-Ax:", name="dsa")



from .base import sd

sd.baseline.extend([wbs, ssa, eslit, cslit, dsa])