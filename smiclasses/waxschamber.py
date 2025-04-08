
from ophyd import Device, EpicsSignal, Component as Cpt

# Read the pressure from the waxs chamber
class sample_chamber_pressure(Device):
    waxs = Cpt(EpicsSignal, "{Det:300KW-TCG:7}P:Raw-I")  # Change PVs
    maxs = Cpt(EpicsSignal, "{B1:WAXS-TCG:9}P:Raw-I")  # Change PVs
