print(f"Loading {__file__}")
from ..smiclasses.machine import Ring
from ophyd import EpicsSignalRO

ring = Ring(name="ring")

# ring_ops = EpicsSignal('SR-OPS{}Mode-Sts', name='ring_ops', string=True)
mstr_shutter_enable = EpicsSignalRO(
    "SR-EPS{PLC:1}Sts:MstrSh-Sts", name="mstr_shutter_enable"
)
ivu_permit = EpicsSignalRO("XF:12ID-CT{}Prmt:Remote-Sel", name="ivu_permit")
smi_shutter_enable = EpicsSignalRO(
    "SR:C12-EPS{PLC:1}Sts:ID_BE_Enbl-Sts", name="smi_shutter_enable"
)



from .base import sd

sd.baseline.extend([ring.current])