
from ophyd import (
    EpicsMotor,
    EpicsSignalRO,
    EpicsSignal,
    Device,
    Component as Cpt,
    PseudoPositioner,
)


# SLIT = 4-axis position/gap type device
class SLIT(Device):
    h = Cpt(EpicsMotor, "Hpos}Mtr")
    hg = Cpt(EpicsMotor, "Hgap}Mtr")
    v = Cpt(EpicsMotor, "Vpos}Mtr")
    vg = Cpt(EpicsMotor, "Vgap}Mtr")


# can't use same class unless we rename the PVs: AB, CD to V, H
# temporary names for now, needs to be checked:
# chs_ABgap = EpicsMotor('XF:12IDC-OP:2{Slt:C-Ax:AB_gap}Mtr', name='chs_ABgap')
# chs_ABpos = EpicsMotor('XF:12IDC-OP:2{Slt:C-Ax:AB_pos}Mtr', name='chs_ABpos')
# chs_CDgap = EpicsMotor('XF:12IDC-OP:2{Slt:C-Ax:CD_gap}Mtr', name='chs_CDgap')
# chs_CDpos = EpicsMotor('XF:12IDC-OP:2{Slt:C-Ax:CD_pos}Mtr', name='chs_CDpos')


# SLTH, SLTV = 2-axis position/gap device
# note that the gap and position may not be indepedent on this device
# therefore we may add code that defines pseudopositions in future

# also note this could be tightened up if we changed some EPICS PV names
# so that either the H,V slits have the same device name OR their
# axis names become generic like Pos,Gap for each one.


class SLTH(Device):
    h = Cpt(EpicsMotor, "Hpos}Mtr")
    hg = Cpt(EpicsMotor, "Hgap}Mtr")


class SLTV(Device):
    v = Cpt(EpicsMotor, "Vpos}Mtr")
    vg = Cpt(EpicsMotor, "Vgap}Mtr")




# apertures: would be good if one class could capture pinhole mask and
# crl aperture, but currently the PVs aren't the same


class APER(Device):
    x = Cpt(EpicsMotor, "Xap}Mtr")
    y = Cpt(EpicsMotor, "Yap}Mtr")



# pinhole mask (phm) ,or A hutch aperture (aap)
# not currently installed, needs PV change to work w/same class as above
# aap = APER('XF:12IDA-OP:0{Msk:PH-Ax:', name='aap')

# temporary names if it is installed w/o PV change
# phm_x = EpicsMotor('XF:12IDA-OP:0{Msk:PH-Ax:X}Mtr', name='phm_x')
# phm_y = EpicsMotor('XF:12IDA-OP:0{Msk:PH-Ax:Y}Mtr', name='phm_y')
