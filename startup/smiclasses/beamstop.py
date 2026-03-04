from ophyd import (EpicsMotor, Signal, Device, Component as Cpt)
import bluesky.plan_stubs as bps

class SAXSBeamStops(Device):
    x_rod = Cpt(EpicsMotor, "IBB}Mtr")
    y_rod = Cpt(EpicsMotor, "IBM}Mtr")
    x_pin = Cpt(EpicsMotor, "OBB}Mtr")
    y_pin = Cpt(EpicsMotor, "OBM}Mtr")

