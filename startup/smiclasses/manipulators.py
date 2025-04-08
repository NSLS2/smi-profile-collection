

from ophyd import (
    EpicsMotor,
    EpicsSignal,
    Device,
    Component as Cpt,
)

class STG(Device):
    x = Cpt(EpicsMotor, "X}Mtr", labels=["stage"])
    y = Cpt(EpicsMotor, "Y}Mtr", labels=["stage"])
    z = Cpt(EpicsMotor, "Z}Mtr", labels=["stage"])
    th = Cpt(EpicsMotor, "theta}Mtr", labels=["stage"])
    ph = Cpt(EpicsMotor, "phi}Mtr", labels=["stage"])
    ch = Cpt(EpicsMotor, "chi}Mtr", labels=["stage"])


class SMPL(Device):
    x = Cpt(EpicsMotor, "X}Mtr", labels=["sample"])
    y = Cpt(EpicsMotor, "Y}Mtr", labels=["sample"])
    z = Cpt(EpicsMotor, "Z}Mtr", labels=["sample"])
    al = Cpt(EpicsMotor, "alpha}Mtr", labels=["sample"])
    az = Cpt(EpicsMotor, "azimuth}Mtr", labels=["sample"])
    ka = Cpt(EpicsMotor, "kappa}Mtr", labels=["sample"])


class HEXAPOD(Device):
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")
    z = Cpt(EpicsMotor, "Z}Mtr")
    a = Cpt(EpicsMotor, "A}Mtr")
    b = Cpt(EpicsMotor, "B}Mtr")
    c = Cpt(EpicsMotor, "C}Mtr")


class SMARACT(Device):
    x = Cpt(EpicsMotor, "0}Mtr", labels=["piezo"])
    y = Cpt(EpicsMotor, "3}Mtr", labels=["piezo"])
    z = Cpt(EpicsMotor, "6}Mtr", labels=["piezo"])
    # swapping Th and ch as of Oct 2024 when old th motor seems to fail it's sensor
    #th = Cpt(EpicsMotor, "4}Mtr", labels=["piezo"])
    #ch = Cpt(EpicsMotor, "1}Mtr", labels=["piezo"])
    ch = Cpt(EpicsMotor, "4}Mtr", labels=["piezo"])
    th = Cpt(EpicsMotor, "1}Mtr", labels=["piezo"])


class BDMStage(Device):
    x = Cpt(EpicsSignal, "ACT2:POSITION", write_pv="ACT2:CMD:TARGET", kind="hinted")
    y = Cpt(EpicsSignal, "ACT1:POSITION", write_pv="ACT1:CMD:TARGET", kind="hinted")
    th = Cpt(EpicsSignal, "ACT0:POSITION", write_pv="ACT0:CMD:TARGET", kind="hinted")

