print(f"Loading {__file__}")

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
)
from ophyd.utils.epics_pvs import set_and_wait
from ophyd.status import StatusBase, MoveStatus
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from ophyd import Component as Cpt
from scipy.interpolate import InterpolatedUnivariateSpline

ANG_OVER_EV = 12398.42  # A*eV
# TODO move inside energy class
D_Si111 = 3.1293
# D_Si111 = 3.135555


def energy_to_gap(target_energy, undulator_harmonic=1, man_offset=0):
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

    # Work this out for tender
    if target_energy < 6000:
        #K edge -10
        #Cl edge -20
        gap = (gap_mm * 1000 -20)
        #gap = (gap_mm * 1000 -48)

    # if target_energy > 17500:
    #     #K edge -10
    #     #Cl edge -20
    #     gap = (gap_mm * 1000 -25)
    #     #gap = (gap_mm * 1000 -48)



    # -30 for 12.62; -33 for 14 keV; -21 for 16.1 keV, 18.25keV; -50 for 9540eV; -20 for 2450eV; -30 for 4050eV
    # -29 for 9700 keV -- 11.150 keV, -55 for 6.55 keV, -35 for 7.7 kev;  -29 for 3.6 keV

    return gap


def energy_to_bragg(target_energy, delta_bragg=0):
    bragg_angle = (
        np.arcsin((ANG_OVER_EV / target_energy) / (2 * D_Si111)) / np.pi * 180
        - delta_bragg
    )
    return bragg_angle


def wait_all(motors_list, sleep=0.0, debug=False):
    """Wait until the last motor finished movement.
    :param motors_list: the list of all motors to wait.
    :return: None
    """
    while True:
        motor_statuses = []
        for m in motors_list:
            motor_statuses.append(m.moving)
        if debug:
            print("Motor statuses: {}".format(motor_statuses))
        if True in motor_statuses:
            yield from bps.sleep(sleep)
        else:
            break


def move_dcm(target_energy, delta_bragg=0):
    bragg_angle = energy_to_bragg(target_energy, delta_bragg)
    dcm_gap_value = (12.5) / np.cos(bragg_angle * np.pi / 180)
    dcm.bragg.move(bragg_angle, wait=False)
    dcm.dcmgap.move(dcm_gap_value, wait=True)

    wait_all([dcm.bragg, dcm.dcmgap], sleep=0, debug=False)

    print("DCM gap calculated      : {:.5f}".format(dcm_gap_value))
    print("DCM gap from PV         : {:.5f}".format(dcm.dcmgap.get().user_readback))

    print("Bragg angle calculated  : {:.5f}".format(bragg_angle))
    print("Bragg angle from PV     : {:.5f}".format(dcm.bragg.get().user_readback))


class DCMInternals(Device):
    height = Cpt(EpicsMotor, "XF:12ID:m66")
    pitch = Cpt(EpicsMotor, "XF:12ID:m67")
    roll = Cpt(EpicsMotor, "XF:12ID:m68")
    theta = Cpt(EpicsMotor, "XF:12ID:m65")

from ophyd.sim import SoftPositioner
class Energy(PseudoPositioner):
    # synthetic axis
    energy = Cpt(PseudoSingle, kind="hinted", labels=["mono"])
    # real motors
    dcmgap = Cpt(EpicsMotor, "XF:12ID:m66", read_attrs=["user_readback"])
    bragg = Cpt(EpicsMotor, "XF:12ID:m65", read_attrs=["user_readback"], labels=["mono"])
    #    dcmpitch = Cpt(EpicsMotor, 'XF:12ID:m67', read_attrs=['readback'])
    pitch_feedback_disabled = Cpt(EpicsSignal, "XF:12IDB-BI:2{EM:BPM3}fast_pidY_incalc.CLCN", name="manual_PID_disable_pitch")
    roll_feedback_disabled = Cpt(EpicsSignal, "XF:12IDB-BI:2{EM:BPM3}fast_pidX_incalc.CLCN", name="manual_PID_disable_roll")

    
    ivugap = Cpt(
        InsertionDevice,
        "SR:C12-ID:G1{IVU:1-Ax:Gap}-Mtr",
        read_attrs=["user_readback"],
        configuration_attrs=[],
        labels=["mono"],
    )

    enableivu = Cpt(Signal, value=True)
    enabledcmgap = Cpt(Signal, value=True)

    # this is also the maximum harmonic that will be tried
    target_harmonic = Cpt(Signal, value=21)
    harmonic = Cpt(Signal, kind="hinted")

    # TODO make this a derived component

    # TODO: if the energy.move is commanded to go to the current energy, then it will wait forever because nothing moves.

    # wlambda = Cpt(Signal, value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hints = None

    @pseudo_position_argument
    def forward(self, p_pos):
        energy = p_pos.energy
        self.harmonic.put(self.target_harmonic.get())

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

        target_ivu_gap = energy_to_gap(energy, self.harmonic.get())
        while not (6200 <= target_ivu_gap < 15100):
            self.harmonic.put(self.harmonic.get() - 2)
            if self.harmonic.get() < 1:
                raise RuntimeError("can not find a valid gap")
            target_ivu_gap = energy_to_gap(energy, self.harmonic.get())

        target_bragg_angle = energy_to_bragg(energy)

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
            e = ANG_OVER_EV / (2 * D_Si111 * math.sin(math.radians(bragg)))
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


energy = Energy(
    prefix="",
    name="energy",
    read_attrs=["energy", "ivugap", "bragg", "harmonic"],
    configuration_attrs=["enableivu", "enabledcmgap", "target_harmonic"],
)
energy.settle_time = 1
dcm = energy
ivugap = energy.ivugap
# DCM motor shortcuts. Early scans used the names at right (p2h, etc).
dcm_gap = dcm.dcmgap  # Height in CSS # EpicsMotor('XF:12ID:m66', name='p2h')
dcm_pitch = EpicsMotor("XF:12ID:m67", name="dcm_pitch")
# dcm_roll = dcm.roll  # Roll in CSS # EpicsMotor('XF:12ID:m68', name='p2r')
bragg = dcm.bragg  # Theta in CSS  # EpicsMotor('XF:12ID:m65', name='bragg')
# dcm_x = dcm.x  # E Mono X in CSS

dcm_config = DCMInternals("", name="dcm_config")

bragg.read_attrs = ["user_readback"]

#new_ivu_gap = EpicsMotor("SR:C12-ID:G1{IVU:1-Ax:Gap}-Mtr", name="new_ivu_gap")


# def move_E(E, gap_off=0):
#     energy.move(E)
#     if gap_off != 0:
#         cur_gap = ivugap.user_readback.value
#         ivugap.move(cur_gap + gap_off)

dcm_theta = EpicsMotor("XF:12ID:m65", name="dcm_theta")
