
from ophyd import (
    EpicsMotor,
    Device,
    Component as Cpt,
)


class XBPM(Device):
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")

