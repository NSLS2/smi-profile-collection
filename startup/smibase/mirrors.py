print(f"Loading {__file__}")

from ..smiclasses.mirrors import MIR
from ..smiclasses.bimorph import VFM_voltage, HFM_voltage


hfm = MIR("XF:12IDA-OP:2{Mir:HF-Ax:", name="hfm")
vfm = MIR("XF:12IDA-OP:2{Mir:VF-Ax:", name="vfm")
vdm = MIR("XF:12IDA-OP:2{Mir:VD-Ax:", name="vdm")


vfm_voltage = VFM_voltage("VFM:", name="vfm_voltage")

hfm_voltage = HFM_voltage("HFM:", name="hfm_voltage")



from .base import sd

sd.baseline.extend([ vfm_voltage, hfm_voltage, hfm, vdm, vfm,])