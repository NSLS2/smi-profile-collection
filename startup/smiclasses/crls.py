

from ophyd import (
    EpicsMotor,
    EpicsSignalRO,
    EpicsSignal,
    Device,
    Component as Cpt,
    PseudoPositioner,
)


class CRL(Device):
    lens1 = Cpt(EpicsMotor, "L1}Mtr")
    lens2 = Cpt(EpicsMotor, "L2}Mtr")
    lens3 = Cpt(EpicsMotor, "L3}Mtr")
    lens4 = Cpt(EpicsMotor, "L4}Mtr")
    lens5 = Cpt(EpicsMotor, "L5}Mtr")
    lens6 = Cpt(EpicsMotor, "L6}Mtr")
    lens7 = Cpt(EpicsMotor, "L7}Mtr")
    lens8 = Cpt(EpicsMotor, "L8}Mtr")
    lens9 = Cpt(EpicsMotor, "L9}Mtr")
    lens10 = Cpt(EpicsMotor, "L10}Mtr")
    lens11 = Cpt(EpicsMotor, "L11}Mtr")
    lens12 = Cpt(EpicsMotor, "L12}Mtr")
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")
    z = Cpt(EpicsMotor, "Z}Mtr")
    ph = Cpt(EpicsMotor, "Ph}Mtr")
    th = Cpt(EpicsMotor, "Th}Mtr")



# aperture motors, see 10-slits.py
