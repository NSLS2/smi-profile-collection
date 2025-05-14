from ophyd import (
    EpicsMotor,
    Device,
    Component as Cpt,
)


class MIR(Device):
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")
    th = Cpt(EpicsMotor, "P}Mtr")
