import re
import numpy as np
from ophyd import (
    EpicsSignal,
    Device,
    Component as Cpt,
)
import bluesky.plan_stubs as bps


class HFM_voltage(Device):
    ch0 = Cpt(EpicsSignal, "GET-VOUT0")
    ch0_trg = Cpt(EpicsSignal, "SET-VTRGT0")
    ch1 = Cpt(EpicsSignal, "GET-VOUT1")
    ch1_trg = Cpt(EpicsSignal, "SET-VTRGT1")
    ch2 = Cpt(EpicsSignal, "GET-VOUT2")
    ch2_trg = Cpt(EpicsSignal, "SET-VTRGT2")
    ch3 = Cpt(EpicsSignal, "GET-VOUT3")
    ch3_trg = Cpt(EpicsSignal, "SET-VTRGT3")
    ch4 = Cpt(EpicsSignal, "GET-VOUT4")
    ch4_trg = Cpt(EpicsSignal, "SET-VTRGT4")
    ch5 = Cpt(EpicsSignal, "GET-VOUT5")
    ch5_trg = Cpt(EpicsSignal, "SET-VTRGT5")
    ch6 = Cpt(EpicsSignal, "GET-VOUT6")
    ch6_trg = Cpt(EpicsSignal, "SET-VTRGT6")
    ch7 = Cpt(EpicsSignal, "GET-VOUT7")
    ch7_trg = Cpt(EpicsSignal, "SET-VTRGT7")
    ch8 = Cpt(EpicsSignal, "GET-VOUT8")
    ch8_trg = Cpt(EpicsSignal, "SET-VTRGT8")
    ch9 = Cpt(EpicsSignal, "GET-VOUT9")
    ch9_trg = Cpt(EpicsSignal, "SET-VTRGT9")
    ch10 = Cpt(EpicsSignal, "GET-VOUT10")
    ch10_trg = Cpt(EpicsSignal, "SET-VTRGT10")
    ch11 = Cpt(EpicsSignal, "GET-VOUT11")
    ch11_trg = Cpt(EpicsSignal, "SET-VTRGT11")
    ch12 = Cpt(EpicsSignal, "GET-VOUT12")
    ch12_trg = Cpt(EpicsSignal, "SET-VTRGT12")
    ch13 = Cpt(EpicsSignal, "GET-VOUT13")
    ch13_trg = Cpt(EpicsSignal, "SET-VTRGT13")
    ch14 = Cpt(EpicsSignal, "GET-VOUT14")
    ch14_trg = Cpt(EpicsSignal, "SET-VTRGT14")
    ch15 = Cpt(EpicsSignal, "GET-VOUT15")
    ch15_trg = Cpt(EpicsSignal, "SET-VTRGT15")
    shift_rel = Cpt(EpicsSignal, "SET-ALLSHIFT")
    set_tar = Cpt(EpicsSignal, "SET-ALLTRGT")

    # This is the default hfm mirror voltage for smi swaxs hutch
    default_hfm_v2 = np.asarray(
        [-151, 261, 250, 293, 175, 236, 168, 231, 242, 200, 291, 222, 215, 157, 311, 36]
    )

    def set_target(self, mode="SWAXS"):
        ch_pattern = re.compile(r"ch(?P<number>\d{1,2})")
        for att_an in dir(self):
            ch_pattern_match = ch_pattern.match(att_an)
            if ch_pattern_match and "trg" in att_an:
                # -80 to move directly to teh good voltag for lowdiv configuration
                yield from bps.mv(
                    getattr(self, att_an),
                    -80 + self.default_hfm_v2[int(ch_pattern_match[1])],
                )
                yield from bps.sleep(5)

    def move_target(self):
        yield from bps.mv(self.set_tar, 0)

    def shift_relative(self, relative_value=0):
        yield from bps.mv(self.shift_rel, relative_value)

    def move_abs(self, mode="SWAXS"):
        yield from self.set_target(mode=mode)
        yield from bps.sleep(5)
        yield from self.move_target()




class VFM_voltage(Device):
    ch0 = Cpt(EpicsSignal, "GET-VOUT0")
    ch0_trg = Cpt(EpicsSignal, "SET-VTRGT0")
    ch1 = Cpt(EpicsSignal, "GET-VOUT1")
    ch1_trg = Cpt(EpicsSignal, "SET-VTRGT1")
    ch2 = Cpt(EpicsSignal, "GET-VOUT2")
    ch2_trg = Cpt(EpicsSignal, "SET-VTRGT2")
    ch3 = Cpt(EpicsSignal, "GET-VOUT3")
    ch3_trg = Cpt(EpicsSignal, "SET-VTRGT3")
    ch4 = Cpt(EpicsSignal, "GET-VOUT4")
    ch4_trg = Cpt(EpicsSignal, "SET-VTRGT4")
    ch5 = Cpt(EpicsSignal, "GET-VOUT5")
    ch5_trg = Cpt(EpicsSignal, "SET-VTRGT5")
    ch6 = Cpt(EpicsSignal, "GET-VOUT6")
    ch6_trg = Cpt(EpicsSignal, "SET-VTRGT6")
    ch7 = Cpt(EpicsSignal, "GET-VOUT7")
    ch7_trg = Cpt(EpicsSignal, "SET-VTRGT7")
    ch8 = Cpt(EpicsSignal, "GET-VOUT8")
    ch8_trg = Cpt(EpicsSignal, "SET-VTRGT8")
    ch9 = Cpt(EpicsSignal, "GET-VOUT9")
    ch9_trg = Cpt(EpicsSignal, "SET-VTRGT9")
    ch10 = Cpt(EpicsSignal, "GET-VOUT10")
    ch10_trg = Cpt(EpicsSignal, "SET-VTRGT10")
    ch11 = Cpt(EpicsSignal, "GET-VOUT11")
    ch11_trg = Cpt(EpicsSignal, "SET-VTRGT11")
    ch12 = Cpt(EpicsSignal, "GET-VOUT12")
    ch12_trg = Cpt(EpicsSignal, "SET-VTRGT12")
    ch13 = Cpt(EpicsSignal, "GET-VOUT13")
    ch13_trg = Cpt(EpicsSignal, "SET-VTRGT13")
    ch14 = Cpt(EpicsSignal, "GET-VOUT14")
    ch14_trg = Cpt(EpicsSignal, "SET-VTRGT14")
    ch15 = Cpt(EpicsSignal, "GET-VOUT15")
    ch15_trg = Cpt(EpicsSignal, "SET-VTRGT15")
    shift_rel = Cpt(EpicsSignal, "SET-ALLSHIFT")
    set_tar = Cpt(EpicsSignal, "SET-ALLTRGT")

    # This is the default vfm mirror voltage for smi swaxs hutch
    default_vfm_v2 = [
        39,
        -102,
        277,
        234,
        325,
        163,
        392,
        280,
        365,
        273,
        196,
        400,
        219,
        304,
        51,
        -327,
    ]
    # default_vfm_v2 = -430 + np.asarray([  39,   85, 311, 310,  -15, 485,   68, 447, 291,  130, 606,  170, 272, 437,  192, -308]) #Ca edge

    # default_vfm_v2 =  [-281, -235,  -9, -10, -335, 165, -252, 127, -29, -190, 286, -150, -48, 117, -128, -628] #S edge

    # This is the default vfm mirror voltage for opls hutch
    default_vfm_opls = [
        -206,
        -191,
        6,
        71,
        -316,
        184,
        -223,
        120,
        45,
        -130,
        202,
        -111,
        17,
        62,
        -75,
        -553,
    ]

    def set_target(self, mode="SWAXS"):
        ch_pattern = re.compile(r"ch(?P<number>\d{1,2})")
        for att_an in dir(self):
            ch_pattern_match = ch_pattern.match(att_an)
            if ch_pattern_match and "trg" in att_an:
                if mode == "SWAXS":
                    yield from bps.mv(
                        getattr(self, att_an),
                        self.default_vfm_v2[int(ch_pattern_match[1])],
                    )
                    yield from bps.sleep(5)
                elif mode == "OPLS":
                    yield from bps.mv(
                        getattr(self, att_an),
                        self.default_vfm_opls[int(ch_pattern_match[1])],
                    )
                    yield from bps.sleep(5)
                else:
                    print("Unknown mode, your should choose between SWAXS or OPLS")

    def move_target(self):
        yield from bps.mv(self.set_tar, 0)

    def shift_relative(self, relative_value=0):
        yield from bps.mv(self.shift_rel, relative_value)

    def move_abs(self, mode="SWAXS"):
        yield from self.set_target(mode=mode)
        yield from bps.sleep(5)
        yield from self.move_target()

