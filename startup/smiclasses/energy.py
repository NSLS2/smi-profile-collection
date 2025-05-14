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
    """
    Device representing the internal motors of the Double Crystal Monochromator (DCM).

    Attributes:
        height (EpicsMotor): Motor controlling the height of the DCM.
        pitch (EpicsMotor): Motor controlling the pitch of the DCM.
        roll (EpicsMotor): Motor controlling the roll of the DCM.
        theta (EpicsMotor): Motor controlling the theta angle of the DCM.
    """
    height = Cpt(EpicsMotor, "XF:12ID:m66")
    pitch = Cpt(EpicsMotor, "XF:12ID:m67")
    roll = Cpt(EpicsMotor, "XF:12ID:m68")
    theta = Cpt(EpicsMotor, "XF:12ID:m65")


class Energy(PseudoPositioner):
    """
    PseudoPositioner for controlling the monochromator energy.

    Attributes:
        energy (PseudoSingle): Synthetic axis representing the energy.
        dcmgap (EpicsMotor): Real motor controlling the DCM gap.
        bragg (EpicsMotor): Real motor controlling the Bragg angle.
        pitch_feedback_disabled (EpicsSignal): Signal to disable pitch feedback.
        roll_feedback_disabled (EpicsSignal): Signal to disable roll feedback.
        ivugap (InsertionDevice): Real motor controlling the IVU gap.
        enableivu (Signal): Signal to enable or disable IVU movement.
        enabledcmgap (Signal): Signal to enable or disable DCM gap movement.
        target_harmonic (Signal): Target harmonic for the undulator.
        harmonic (Signal): Current harmonic being used.
    """
    # Synthetic axis
    energy = Cpt(PseudoSingle, kind="hinted", labels=["mono"])

    # Real motors
    dcmgap = Cpt(EpicsMotor, "XF:12ID:m66", read_attrs=["user_readback"], labels=["mono"])
    bragg = Cpt(EpicsMotor, "XF:12ID:m65", read_attrs=["user_readback"], labels=["mono"])

    # Feedback signals
    pitch_feedback_disabled = Cpt(
        EpicsSignal,
        "XF:12IDB-BI:2{EM:BPM3}fast_pidY_incalc.CLCN",
        name="manual_PID_disable_pitch",
    )
    roll_feedback_disabled = Cpt(
        EpicsSignal,
        "XF:12IDB-BI:2{EM:BPM3}fast_pidX_incalc.CLCN",
        name="manual_PID_disable_roll",
    )

    # Constants for energy calculations
    ANG_OVER_EV = 12398.42  # Conversion factor for energy to wavelength
    D_Si111 = 3.1293  # Lattice spacing for Si(111)

    # IVU gap
    ivugap = Cpt(
        InsertionDevice,
        "SR:C12-ID:G1{IVU:1-Ax:Gap}-Mtr",
        read_attrs=["user_readback"],
        configuration_attrs=[],
        labels=["mono"],
        add_prefix=(),
    )

    # Enable/disable signals
    enableivu = Cpt(Signal, value=True)
    enabledcmgap = Cpt(Signal, value=True)

    # Harmonic signals
    target_harmonic = Cpt(Signal, value=21)
    harmonic = Cpt(Signal, kind="hinted", value=21)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hints = None

    def energy_to_bragg(self, target_energy, delta_bragg=0):
        """
        Convert energy to Bragg angle.

        Parameters:
            target_energy (float): Target energy in eV.
            delta_bragg (float): Offset for the Bragg angle.

        Returns:
            float: Bragg angle in degrees.
        """
        bragg_angle = (
            np.arcsin((self.ANG_OVER_EV / target_energy) / (2 * self.D_Si111))
            / np.pi
            * 180
            - delta_bragg
        )
        return bragg_angle

    def energy_to_gap(self, target_energy, undulator_harmonic=1, man_offset=0):
        """
        Convert energy to IVU gap.

        Parameters:
            target_energy (float): Target energy in eV.
            undulator_harmonic (int): Harmonic number.
            man_offset (float): Manual offset for the gap.

        Returns:
            float: IVU gap in mm.
        """
        fundamental_energy = target_energy / float(undulator_harmonic)
        f = fundamental_energy

        # Calculate the gap using a piecewise function
        gap_mm = -533.56314 + (1926.52257) * (
            0.28544 / (1 + 10 ** ((-10782.55855 - f) * 1.44995e-4))
            + (1 - 0.28544) / (1 + 10 ** ((7180.06758 - f) * 6.34167e-4))
        )

        # Experimental offsets for specific energies
        e_exp = np.array([2450, 2470, 3600, 4050, 6400, 6510, 6550, 7700, 8980, 9700, 12000, 12620, 14000, 14400, 16100, 18000])
        off_exp = np.array([-20, -35, 29, 30, 25, 25, 25, 35, 19, 50, 35, 45, 45, 45, 35, 25])

        # Interpolate the offset for the target energy
        auto_offset = np.interp(target_energy, e_exp, off_exp, left=min(off_exp), right=max(off_exp))
        gap = gap_mm * 1000 - auto_offset - man_offset

        # Apply a minimum gap correction for low energies
        if target_energy < 3000:
            gap = gap_mm * 1000 - 20
        return gap

    @pseudo_position_argument
    def forward(self, p_pos):
        """
        Convert pseudo position (energy) to real positions (bragg, dcmgap, ivugap).

        Parameters:
            p_pos (PseudoPosition): Desired pseudo position.

        Returns:
            RealPosition: Calculated real positions.
        """
        energy = p_pos.energy
        self.harmonic.put(int(self.target_harmonic.get()))

        if not self.harmonic.get() % 2:
            raise RuntimeError("Harmonic must be odd.")

        if energy <= 2050:
            raise ValueError("Minimum energy is 2050 eV.")

        if energy >= 24001:
            raise ValueError("Maximum energy is 24000 eV.")

        # Calculate target positions
        target_ivu_gap = self.energy_to_gap(energy, self.harmonic.get())
        while not (6200 <= target_ivu_gap < 15100):
            self.harmonic.put(int(self.harmonic.get()) - 2)
            if self.harmonic.get() < 1:
                raise RuntimeError("Cannot find a valid gap.")
            target_ivu_gap = self.energy_to_gap(energy, self.harmonic.get())

        target_bragg_angle = self.energy_to_bragg(energy)

        # Calculate DCM gap
        dcm_offset = 25
        target_dcm_gap = (dcm_offset / 2) / np.cos(target_bragg_angle * np.pi / 180)

        # Disable DCM gap movement if necessary
        if not self.enabledcmgap.get():
            target_dcm_gap = self.dcmgap.position

        # Disable IVU movement if necessary
        if not self.enableivu.get():
            target_ivu_gap = self.ivugap.position

        return self.RealPosition(
            bragg=target_bragg_angle, ivugap=target_ivu_gap, dcmgap=target_dcm_gap
        )

    @real_position_argument
    def inverse(self, r_pos):
        """
        Convert real positions (bragg) to pseudo position (energy).

        Parameters:
            r_pos (RealPosition): Real positions.

        Returns:
            PseudoPosition: Calculated pseudo position.
        """
        bragg = r_pos.bragg
        try:
            energy = self.ANG_OVER_EV / (2 * self.D_Si111 * math.sin(math.radians(bragg)))
        except ZeroDivisionError:
            energy = -1.0e23
        return self.PseudoPosition(energy=float(energy))

    @pseudo_position_argument
    def set(self, position):
        """
        Set the energy position.

        Parameters:
            position (PseudoPosition): Desired energy position.

        Returns:
            MoveStatus: Status of the move.
        """
        (energy,) = position
        if np.abs(energy - self.position[0]) < 0.01:
            return MoveStatus(self, energy, success=True, done=True)

# TODO change self.settle_time here based on energy we are moving to 
        # if False:
        #     self.settle_time = per_energy(energy)
        def turn_on_feedback(*arg, **kwargs):
            try:
                self.pitch_feedback_disabled.set("0").wait()
                self.roll_feedback_disabled.set("0").wait()
            except Exception as e:
                print(e, type(e))

        # Disable feedback during the move
        self.pitch_feedback_disabled.set("1").wait()
        self.roll_feedback_disabled.set("1").wait()

        # Perform the move
        sts = super().set([float(_) for _ in position])
        self.subscribe(turn_on_feedback, event_type=self._SUB_REQ_DONE, run=False)
        return sts


