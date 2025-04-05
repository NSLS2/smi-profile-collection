print(f"Loading {__file__}")

from ophyd import EpicsSignal, Device, Component as Cpt
from ophyd import EpicsSignal, EpicsSignalRO
from ophyd import Component as Cpt
from nslsii.ad33 import QuadEMV33


class output_lakeshore(Device):

    status = Cpt(EpicsSignal, "Val:Range-Sel")
    P = Cpt(EpicsSignal, "Gain:P-SP")
    I = Cpt(EpicsSignal, "Gain:I-SP")
    D = Cpt(EpicsSignal, "Gain:I-SP")
    temp_set_point = Cpt(EpicsSignal, "T-SP")

    def turn_on(self):
        yield from bps.mv(self.status, 1)

    def turn_off(self):
        yield from bps.mv(self.status, 0)

    def mv_temp(self, temp):
        yield from bps.mv(self.temp_set_point, temp)


class new_LakeShore(Device):
    """
    Lakeshore is the device reading the temperature from the heating stage for SAXS and GISAXS.
    This class define the PVs to read and write to control lakeshore
    :param Device: ophyd device
    """

    input_A = Cpt(EpicsSignal, "{Env:01-Chan:A}T-I")
    input_A_celsius = Cpt(EpicsSignal, "{Env:01-Chan:A}T:C-I")

    input_B = Cpt(EpicsSignal, "{Env:01-Chan:B}T-I")
    input_C = Cpt(EpicsSignal, "{Env:01-Chan:C}T-I")
    input_D = Cpt(EpicsSignal, "{Env:01-Chan:D}T-I")

    output1 = Cpt(output_lakeshore, "{Env:01-Out:1}", name="ls_outpu1")
    output2 = Cpt(output_lakeshore, "{Env:01-Out:2}", name="ls_outpu2")
    output3 = Cpt(output_lakeshore, "{Env:01-Out:3}", name="ls_outpu3")
    output4 = Cpt(output_lakeshore, "{Env:01-Out:4}", name="ls_outpu4")
    # xrange =


ls = new_LakeShore("XF:12ID-ES", name="ls")
# ls.ch1_read.kind = 'hinted'
# # ls.ch1_sp.kind = 'hinted'
# ls.ch2_read.kind = 'hinted'
# # ls.ch2_sp.kind = 'hinted'
# ls.ch3_read.kind = 'hinted'


class XBPM(Device):
    """
    XBPM are diamond windows that generate current when the beam come through. It is used to know the position
    of the beam at the bpm postion as well as the amount of incoming photons. 3 bpms are available at SMI: bpm1
    is position upstream, bpm2 after the focusing mirrons and bpm3 downstream
    :param Device: ophyd device
    """

    ch1 = Cpt(EpicsSignal, "Current1:MeanValue_RBV")
    ch2 = Cpt(EpicsSignal, "Current2:MeanValue_RBV")
    ch3 = Cpt(EpicsSignal, "Current3:MeanValue_RBV")
    ch4 = Cpt(EpicsSignal, "Current4:MeanValue_RBV")
    sumX = Cpt(EpicsSignal, "SumX:MeanValue_RBV")
    sumY = Cpt(EpicsSignal, "SumY:MeanValue_RBV")
    posX = Cpt(EpicsSignal, "PosX:MeanValue_RBV")
    posY = Cpt(EpicsSignal, "PosY:MeanValue_RBV")


xbpm1 = XBPM("XF:12IDA-BI:2{EM:BPM1}", name="xbpm1")
xbpm2 = XBPM("XF:12IDA-BI:2{EM:BPM2}", name="xbpm2")
xbpm3 = XBPM("XF:12IDB-BI:2{EM:BPM3}", name="xbpm3")
xbpm3.sumY.kind = "hinted"
xbpm3.sumX.kind = "hinted"
xbpm2.sumY.kind = "hinted"
xbpm2.sumX.kind = "hinted"


ssacurrent = EpicsSignal(
    "XF:12IDB-BI{EM:SSASlit}SumAll:MeanValue_RBV", name="ssacurrent"
)

pdcurrent = EpicsSignal(
    "XF:12ID:2{EM:Tetr1}Current2:MeanValue_RBV", name="pdcurrent", auto_monitor=True
)
pdcurrent1 = EpicsSignal(
    "XF:12ID:2{EM:Tetr1}Current2Ave", name="pdcurrent1", auto_monitor=True
)
pdcurrent2 = EpicsSignal(
    "XF:12ID:2{EM:Tetr1}SumAllAve", name="pdcurrent2", auto_monitor=True
)


# this doesn't work, because the PV names do not end in .VAL ??
# full PV names are given in the above.


class Keithly2450(Device):
    run = Cpt(EpicsSignal, "run")
    busy = Cpt(EpicsSignalRO, "busy")
    reading = Cpt(EpicsSignalRO, "reading")

    send_done = Cpt(EpicsSignal, "send_done")

    send_pgm = Cpt(EpicsSignal, "send_pgm.AOUT")
    send_prt = Cpt(EpicsSignal, "send_prt.AOUT")
    send_stb = Cpt(EpicsSignal, "send_stb.SCAN", string=True)
    # calc_done = Cpt(EpicsSignalRO, 'calc_done')
    # fast_thold = Cpt(EpicsSignalRO, 'fast_thold')
    # parse_cmd = Cpt(EpicsSignalRO, 'parse_cmd')
    # fast_done = Cpt(EpicsSignalRO, 'fast_done')

    _default_read_attrs = ("reading",)
    _default_configuration_attrs = ("send_pgm", "send_prt", "send_stb")

    def trigger(self):
        st = DeviceStatus(self)

        def keithy_done_monitor(old_value, value, **kwargs):
            if old_value == 1 and value == 0:
                st._finished()
                self.busy.clear_sub(keithy_done_monitor)

        self.busy.subscribe(keithy_done_monitor, run=False)
        self.run.put(1)
        return st


keithly2450 = Keithly2450("XF:12IDA{dmm:2}:K2450:1:", name="keithly2450")
hfmcurrent = EpicsSignal("XF:12IDA{dmm:2}:K2450:1:reading", name="hfmcurrent")

pin_diode = QuadEMV33("XF:12ID:2{EM:Tetr1}", name="pin_diode")
pin_diode.stage_sigs["conf.port_name"] = "TetrAMM"
pin_diode.stage_sigs["acquire_mode"] = 2

for i in (1, 2, 3, 4):
    getattr(pin_diode, f"current{i}").mean_value.kind = "normal"
pin_diode.current2.mean_value.kind = "hinted"
