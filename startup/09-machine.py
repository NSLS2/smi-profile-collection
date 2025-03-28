print(f"Loading {__file__}")
import time as ttime
import os
from ophyd import (
    PVPositioner,
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    Device,
    Signal,
    PseudoPositioner,
    PseudoSingle,
)
from ophyd.utils.epics_pvs import set_and_wait
from ophyd.status import StatusBase, MoveStatus, DeviceStatus
from ophyd import Component as Cpt
from ophyd import Component
from scipy.interpolate import InterpolatedUnivariateSpline


class Ring(Device):
    current = EpicsSignalRO("SR:C03-BI{DCCT:1}I:Real-I", name="ring_current")
    lifetime = EpicsSignalRO("SR:OPS-BI{DCCT:1}Lifetime-I", name="ring_lifetime")
    energy = EpicsSignalRO("SR{}Energy_SRBend", name="ring_energy")
    mode = EpicsSignal("SR-OPS{}Mode-Sts", name="ring_ops", string=True)
    filltarget = EpicsSignalRO("SR-HLA{}FillPattern:DesireImA", name="ring_filltarget")


ring = Ring(name="ring")

# ring_ops = EpicsSignal('SR-OPS{}Mode-Sts', name='ring_ops', string=True)
mstr_shutter_enable = EpicsSignalRO(
    "SR-EPS{PLC:1}Sts:MstrSh-Sts", name="mstr_shutter_enable"
)
ivu_permit = EpicsSignalRO("XF:12ID-CT{}Prmt:Remote-Sel", name="ivu_permit")
smi_shutter_enable = EpicsSignalRO(
    "SR:C12-EPS{PLC:1}Sts:ID_BE_Enbl-Sts", name="smi_shutter_enable"
)


class IVUBrakeCpt(Component):
    def maybe_add_prefix(self, instance, kw, suffix):
        if kw not in self.add_prefix:
            return suffix

        prefix = "".join(instance.prefix.partition("IVU:1")[:2]) + "}"
        return prefix + suffix


class InsertionDevice(EpicsMotor):
    # SR:C12-ID:G1{IVU:1}BrakesDisengaged-SP
    # SR:C12-ID:G1{IVU:1}BrakesDisengaged-Sts
    brake = IVUBrakeCpt(
        EpicsSignal,
        write_pv="BrakesDisengaged-SP",
        read_pv="BrakesDisengaged-Sts",
        add_prefix=("read_pv", "write_pv", "suffix"),
    )

    def move(self, *args, **kwargs):
        self.brake.set(1).wait() # changed from set_and_wait Oct 2024 - Eliot
        return super().move(*args, **kwargs)


# ivu_gap = InsertionDevice('SR:C12-ID:G1{IVU:1-Ax:Gap}-Mtr', name='ivu_gap')

