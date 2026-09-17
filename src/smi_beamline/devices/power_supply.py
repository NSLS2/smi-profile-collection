from ophyd import Component as Cpt
from ophyd import Device, EpicsSignal, EpicsSignalRO


class PowerSupply(Device):
    current = Cpt(EpicsSignalRO, "I")
    current_limit = Cpt(EpicsSignal, "I-Lim")
    out_main_readback = Cpt(EpicsSignalRO, "E:OutMain-RB")
    out_main_setpoint = Cpt(EpicsSignal, "E:OutMain-SP")
    lock_command = Cpt(EpicsSignal, "Enbl:Lock-Cmd")
    lock_status = Cpt(EpicsSignalRO, "Enbl:Lock-Sts")
    out_main_command = Cpt(EpicsSignal, "Enbl:OutMain-Cmd")
    out_main_status = Cpt(EpicsSignalRO, "Enbl:OutMain-Sts")
    operating_status_bc = Cpt(EpicsSignalRO, "Sts:Opr-Sts.BC")
    operating_status_bd = Cpt(EpicsSignalRO, "Sts:Opr-Sts.BD")
