import warnings
import time as ttime
import os
import math
import numpy as np
from ophyd import (
    PVPositioner,
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    Device,
    Signal,
    PseudoPositioner,
    PseudoSingle,
    SoftPositioner,
)
from ophyd.utils.epics_pvs import set_and_wait
from ophyd.status import StatusBase, MoveStatus
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from ophyd import Component as Cpt

from .machine import InsertionDevice




class DCMInternals(Device):
    height = Cpt(EpicsMotor, "XF:12ID:m66")
    pitch = Cpt(EpicsMotor, "XF:12ID:m67")
    roll = Cpt(EpicsMotor, "XF:12ID:m68")
    theta = Cpt(EpicsMotor, "XF:12ID:m65")

class Energy(PseudoPositioner):
    # synthetic axis
    energy = Cpt(PseudoSingle, kind="hinted", labels=["mono"])
    # real motors
    dcmgap = Cpt(EpicsMotor, "XF:12ID:m66", read_attrs=["user_readback"])
    bragg = Cpt(EpicsMotor, "XF:12ID:m65", read_attrs=["user_readback"], labels=["mono"])
    #    dcmpitch = Cpt(EpicsMotor, 'XF:12ID:m67', read_attrs=['readback'])
    pitch_feedback_disabled = Cpt(EpicsSignal, "XF:12IDB-BI:2{EM:BPM3}fast_pidY_incalc.CLCN", name="manual_PID_disable_pitch")
    roll_feedback_disabled = Cpt(EpicsSignal, "XF:12IDB-BI:2{EM:BPM3}fast_pidX_incalc.CLCN", name="manual_PID_disable_roll")
    ANG_OVER_EV = 12398.42
    D_Si111 = 3.1293


    ivugap = Cpt(
        InsertionDevice,
        "SR:C12-ID:G1{IVU:1-Ax:Gap}-Mtr",
        read_attrs=["user_readback"],
        configuration_attrs=[],
        labels=["mono"],
        add_prefix=(),
    )
    

    # ivugap = Cpt(SoftPositioner, init_pos=7000)

    enableivu = Cpt(Signal, value=True)
    enabledcmgap = Cpt(Signal, value=True)

    # this is also the maximum harmonic that will be tried
    target_harmonic = Cpt(Signal, value=21)
    harmonic = Cpt(Signal, kind="hinted",value=21)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hints = None

    def energy_to_bragg(self, target_energy, delta_bragg=0):
        bragg_angle = (np.arcsin((self.ANG_OVER_EV / target_energy) / (2 * self.D_Si111)) / np.pi * 180- delta_bragg)
        return bragg_angle

    def energy_to_gap(self,target_energy, undulator_harmonic=1, man_offset=0):
        fundamental_energy = target_energy / float(undulator_harmonic)
        f = fundamental_energy

        gap_mm = -533.56314 + (1926.52257) * (
            0.28544 / (1 + 10 ** ((-10782.55855 - f) * 1.44995e-4))
            + (1 - 0.28544) / (1 + 10 ** ((7180.06758 - f) * 6.34167e-4))
        )
        e_exp = np.array([ 2450, 2470, 3600, 4050, 6400, 6510, 6550, 7700, 8980, 9700, 12000, 12620, 14000, 14400, 16100, 18000])
        off_exp = np.array([-20,  -35,   29,   30,   25,   25,    25,   35,   19,   50,    35,    45,     45,     45,  35,  25])


        auto_offset = np.interp(target_energy, e_exp, off_exp, left=min(off_exp), right=max(off_exp))
        gap = gap_mm * 1000 - auto_offset - man_offset

        if target_energy <3000:
            gap = (gap_mm * 1000 -20)
        return gap

    @pseudo_position_argument
    def forward(self, p_pos):
        energy = p_pos.energy
        self.harmonic.put(int(self.target_harmonic.get()))

        if not self.harmonic.get() % 2:
            raise RuntimeError("harmonic must be odd")

        if energy <= 2050:
            raise ValueError(
                "The energy you entered is too low ({} eV). "
                "Minimum energy = 2050 eV".format(energy)
            )

        if energy >= 24001:
            raise ValueError(
                "The energy you entered is too high ({} eV). "
                "Maximum energy = 24000 eV".format(energy)
            )

        # compute where we would move everything to in a perfect world

        target_ivu_gap = self.energy_to_gap(energy, self.harmonic.get())
        while not (6200 <= target_ivu_gap < 15100):
            self.harmonic.put(int(self.harmonic.get()) - 2)
            if self.harmonic.get() < 1:
                raise RuntimeError("can not find a valid gap")
            target_ivu_gap = self.energy_to_gap(energy, self.harmonic.get())

        target_bragg_angle = self.energy_to_bragg(energy)

        dcm_offset = 25
        target_dcm_gap = (dcm_offset / 2) / np.cos(target_bragg_angle * np.pi / 180)

        # sometimes move the crystal gap
        if not self.enabledcmgap.get():
            target_dcm_gap = self.dcmgap.position

        # sometimes move the undulator
        if not self.enableivu.get():
            target_ivu_gap = self.ivugap.position

        return self.RealPosition(
            bragg=target_bragg_angle, ivugap=target_ivu_gap, dcmgap=target_dcm_gap
        )

    @real_position_argument
    def inverse(self, r_pos):
        bragg = r_pos.bragg
        try:
            e = self.ANG_OVER_EV / (2 * self.D_Si111 * math.sin(math.radians(bragg)))
        except ZeroDivisionError:
            e = -1.0e23
        return self.PseudoPosition(energy=float(e))

    @pseudo_position_argument
    def set(self, position):
        (energy,) = position
        if np.abs(energy - self.position[0]) < 0.01:
            return MoveStatus(self, energy, success=True, done=True)
        # print(position, self.position)

        # TODO change self.settle_time here based on energy we are moving to
        if False:
            self.settle_time = per_energy(energy)
        def turn_on_feedback(*arg, **kwargs):
            try:
                self.pitch_feedback_disabled.set("0").wait()
                self.roll_feedback_disabled.set("0").wait()
            except Exception as e:
                print(e, type(e))
        
        self.pitch_feedback_disabled.set("1").wait()
        self.roll_feedback_disabled.set("1").wait()
        sts = super().set([float(_) for _ in position])
        self.subscribe(turn_on_feedback, event_type=self._SUB_REQ_DONE, run=False)
        return sts


