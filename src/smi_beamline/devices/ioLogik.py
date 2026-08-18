from ophyd import Device, Component as Cpt, EpicsSignal
import bluesky.plan_stubs as bps


class ioLogik1241(Device):
    ch1_read = Cpt(EpicsSignal, "1-RB")
    ch1_sp = Cpt(EpicsSignal, "1-SP")
    ch2_read = Cpt(EpicsSignal, "2-RB")
    ch2_sp = Cpt(EpicsSignal, "2-SP")
    ch3_read = Cpt(EpicsSignal, "3-RB")
    ch3_sp = Cpt(EpicsSignal, "3-SP")
    ch4_read = Cpt(EpicsSignal, "4-RB")
    ch4_sp = Cpt(EpicsSignal, "4-SP")


class ioLogik1240(Device):
    ch1_read = Cpt(EpicsSignal, "1-I")
    ch2_read = Cpt(EpicsSignal, "2-I")
    ch3_read = Cpt(EpicsSignal, "3-I")
    ch4_read = Cpt(EpicsSignal, "4-I")
    ch5_read = Cpt(EpicsSignal, "5-I")
    ch6_read = Cpt(EpicsSignal, "6-I")
    ch7_read = Cpt(EpicsSignal, "7-I")
    ch8_read = Cpt(EpicsSignal, "8-I")

#XF:12ID2A-DM{DM1-IOL1:E1213}:

class Diag_Module(Device):
    # real positions and readbacks
    out_sts = Cpt(EpicsSignal,'DI1-Sts') # when negative - in position
    fs_sts = Cpt(EpicsSignal,'DI3-Sts') # when negative - in position
    pd_sts = Cpt(EpicsSignal,'DI2-Sts') # when negative - in position
    pd_vlv = Cpt(EpicsSignal,'DO2-Cmd')
    fs_vlv = Cpt(EpicsSignal,'DO4-Cmd')
    out_vlv = Cpt(EpicsSignal,'DO6-Cmd')
    # virtual positions and readbacks
    def fs_in(self):
        yield from bps.mv(self.out_vlv,0)
        yield from bps.sleep(.5)
        yield from bps.mv(self.fs_vlv,1)
        yield from bps.mv(self.pd_vlv,1)
        yield from bps.sleep(1)
        yield from bps.mv(self.fs_vlv,0)
        yield from bps.mv(self.out_vlv,0)
        yield from bps.mv(self.pd_vlv,0)
    def out(self):
        yield from bps.mv(self.fs_vlv,0)
        yield from bps.mv(self.pd_vlv,0)
        yield from bps.sleep(.5)
        yield from bps.mv(self.out_vlv,1)
        yield from bps.mv(self.fs_vlv,1)
        yield from bps.sleep(1)
        yield from bps.mv(self.fs_vlv,0)
        # yield from bps.mv(self.out_vlv,0)
        # yield from bps.mv(self.pd_vlv,0)
    def pd_in(self):
        yield from self.out()
        yield from bps.sleep(.5)
        yield from bps.mv(self.out_vlv,0)
        yield from bps.mv(self.fs_vlv,0)
        yield from bps.mv(self.pd_vlv,0)
        yield from bps.sleep(.5)
        yield from bps.mv(self.pd_vlv,1)
        yield from bps.sleep(1)
        yield from bps.mv(self.fs_vlv,0)
        yield from bps.mv(self.out_vlv,0)
        yield from bps.mv(self.pd_vlv,0)