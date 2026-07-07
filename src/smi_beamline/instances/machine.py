from ophyd import EpicsSignalRO

from smi_beamline.devices import _context
from smi_beamline.devices.machine import Ring


ring = Ring(name="ring")

# ring_ops = EpicsSignal('SR-OPS{}Mode-Sts', name='ring_ops', string=True)
mstr_shutter_enable = EpicsSignalRO(
    "SR-EPS{PLC:1}Sts:MstrSh-Sts", name="mstr_shutter_enable"
)
ivu_permit = EpicsSignalRO("XF:12ID-CT{}Prmt:Remote-Sel", name="ivu_permit")
smi_shutter_enable = EpicsSignalRO(
    "SR:C12-EPS{PLC:1}Sts:ID_BE_Enbl-Sts", name="smi_shutter_enable"
)

_context.baseline_register([ring.current])
