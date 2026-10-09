from ophyd import (
    EpicsMotor,
    Device,
    Component as Cpt,
)


from .status import MIRROR_STATUS


class MIR(Device):
    status_description = MIRROR_STATUS
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")
    th = Cpt(EpicsMotor, "P}Mtr")
