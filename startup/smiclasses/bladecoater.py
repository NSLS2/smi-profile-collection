from ophyd import (EpicsMotor, EpicsSignal, Device, Component as Cpt)

class bladecoater_smaract(Device):
    x1 = Cpt(EpicsMotor, "X1}Mtr", labels=["piezo"])
    x2 = Cpt(EpicsMotor, "X2}Mtr", labels=["piezo"])



# class syringe_pump(Device):
#     x1 = Cpt(EpicsSignal, "Val:Vol-SP", labels=["piezo1"]) 
#     x2 = Cpt(EpicsSignal, "Val:Rate-SP", labels=["piezo2"])
#     x3 = Cpt(EpicsSignal, "Cmd:Run-Cmd", labels=["piezo3"])
#     x4 = Cpt(EpicsSignal, "Cmd:Stop-Cmd", labels=["piezo4"])
#     x5 = Cpt(EpicsSignal, "Val:Dia-RB", labels=['piezo5'] )


class syringe_pump(Device):
    vol = Cpt(EpicsSignal, "Val:Vol-SP",) 
    rate = Cpt(EpicsSignal, "Val:Rate-SP", )
    go = Cpt(EpicsSignal, "Cmd:Run-Cmd",)
    stop_flow = Cpt(EpicsSignal, "Cmd:Stop-Cmd",)
    dia = Cpt(EpicsSignal, "Val:Dia-RB")
    dir = Cpt(EpicsSignal, "Val:Dir-Sel",) 

# XF:12ID2-ES{Pmp:1}Val:Vol-SP

