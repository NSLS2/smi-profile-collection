

from ophyd import (
    EpicsMotor,
    EpicsSignal,
    Device,
    Component as Cpt,
)


class SMARACT(Device):
   # x = Cpt(EpicsMotor, "XF:12IDC-ES:2{MCS:1-Ax:0}Mtr", labels=["piezo"])
   # y = Cpt(EpicsMotor, "XF:12IDC-ES:2{MCS:1-Ax:3}Mtr", labels=["piezo"])
   # z = Cpt(EpicsMotor, "XF:12IDC-ES:2{MCS:1-Ax:6}Mtr", labels=["piezo"])
    # swapping Th and ch as of Oct 2024 when old th motor seems to fail it's sensor
    #th = Cpt(EpicsMotor, "4}Mtr", labels=["piezo"])
    #ch = Cpt(EpicsMotor, "1}Mtr", labels=["piezo"])
   # ch1 = Cpt(EpicsMotor, "XF:12IDC-ES:2{MCS:1-Ax:4}Mtr", labels=["piezo"])
   # th1 = Cpt(EpicsMotor, "XF:12IDC-ES:2{MCS:1-Ax:1}Mtr", labels=["piezo"])
    # changing the smaract 1 motors to ch1 and th1 to add smaract 2 replacements below
    x = Cpt(EpicsMotor, "XF:12ID2C-ES{MCS:2-Ax:3}Mtr", labels=["piezo"])
    y = Cpt(EpicsMotor, "XF:12ID2C-ES{MCS:2-Ax:5}Mtr", labels=["piezo"])
    z = Cpt(EpicsMotor, "XF:12ID2C-ES{MCS:2-Ax:4}Mtr", labels=["piezo"])
    ch = Cpt(EpicsMotor, "XF:12ID2C-ES{MCS:2-Ax:2}Mtr", labels=["piezo"])
    th = Cpt(EpicsMotor, "XF:12ID2C-ES{MCS:2-Ax:6}Mtr", labels=["piezo"])




class BDMStage(Device):
    x = Cpt(EpicsSignal, "ACT2:POSITION", write_pv="ACT2:CMD:TARGET", kind="hinted")
    y = Cpt(EpicsSignal, "ACT1:POSITION", write_pv="ACT1:CMD:TARGET", kind="hinted")
    th = Cpt(EpicsSignal, "ACT0:POSITION", write_pv="ACT0:CMD:TARGET", kind="hinted")


from ophyd import Component as Cpt
from ophyd import EpicsMotor
from ophyd.pseudopos import (
    PseudoPositioner,
    PseudoSingle,
    pseudo_position_argument,
    real_position_argument,
)

import numpy as np

import numpy as np

from ophyd import Component as Cpt
from ophyd import EpicsMotor, EpicsSignalRO
from ophyd.pseudopos import (
    PseudoPositioner,
    PseudoSingle,
    pseudo_position_argument,
    real_position_argument,
)
class readbackEpicsMotor(EpicsMotor):
    """
    Compatibility motor class for PseudoPositioner.

    Ensures a readback attribute exists.
    """

    readback = Cpt(EpicsSignalRO, ".RBV")

import numpy as np

from ophyd import (
    Component as Cpt,
    Device,
    EpicsMotor,
    EpicsSignalRO,
    Signal,
)

from ophyd.pseudopos import (
    PseudoPositioner,
    PseudoSingle,
    pseudo_position_argument,
    real_position_argument,
)


class ReadbackEpicsMotor(EpicsMotor):
    """
    EPICS motor with explicit readback component for
    compatibility with PseudoPositioner.
    """

    readback = Cpt(EpicsSignalRO, ".RBV")


class STG_pseudo(PseudoPositioner):
    """
    Sample manipulator pseudo-positioner.

    ================================================================
    REAL STACK ORDER (bottom -> top)
    ================================================================

        theta   : rotation about laboratory X axis
        chi     : rotation about laboratory Z axis
        phi     : rotation about laboratory Y axis

        y       : vertical translation (up/down)
        x       : horizontal translation (inboard/outboard)
        z       : beam direction translation (upstream/downstream)

    ================================================================
    PSEUDO COORDINATES
    ================================================================

    Pseudo XYZ coordinates remain fixed in laboratory space
    while the real motors compensate during rotations.

        x       : inboard / outboard
        y       : up / down
        z       : upstream / downstream

        theta   : rotation about lab X
        chi     : rotation about lab Z
        phi     : rotation about lab Y

    ================================================================
    ROTATION CENTERS
    ================================================================

    Rotation centers are configuration signals stored in
    laboratory coordinates.

    Each rotational axis may have an independent center:
        theta center
        chi center
        phi center

    These are NOT pseudo axes.
    """

    # ------------------------------------------------------------------
    # PSEUDO AXES
    # ------------------------------------------------------------------

    x = Cpt(
        PseudoSingle,
        limits=(-50, 50),
        kind="hinted",
        doc="Inboard / Outboard laboratory coordinate",
    )

    y = Cpt(
        PseudoSingle,
        limits=(-50, 50),
        kind="hinted",
        doc="Vertical Up / Down laboratory coordinate",
    )

    z = Cpt(
        PseudoSingle,
        limits=(-25, 25),
        kind="hinted",
        doc="Upstream / Downstream laboratory coordinate",
    )

    theta = Cpt(
        PseudoSingle,
        limits=(-90, 90),
        kind="hinted",
        doc="Rotation about laboratory X axis",
    )

    chi = Cpt(
        PseudoSingle,
        limits=(-180, 180),
        kind="hinted",
        doc="Rotation about laboratory Z axis",
    )

    phi = Cpt(
        PseudoSingle,
        limits=(-90, 90),
        kind="hinted",
        doc="Rotation about laboratory Y axis",
    )

    # ------------------------------------------------------------------
    # REAL MOTORS
    # ------------------------------------------------------------------

    x_real = Cpt(
        ReadbackEpicsMotor,
        "X}Mtr",
        labels=["stage"],
        kind="normal",
    )

    y_real = Cpt(
        ReadbackEpicsMotor,
        "Y}Mtr",
        labels=["stage"],
        kind="normal",
    )

    z_real = Cpt(
        ReadbackEpicsMotor,
        "Z}Mtr",
        labels=["stage"],
        kind="normal",
    )

    theta_real = Cpt(
        ReadbackEpicsMotor,
        "theta}Mtr",
        labels=["stage"],
        kind="normal",
    )

    chi_real = Cpt(
        ReadbackEpicsMotor,
        "chi}Mtr",
        labels=["stage"],
        kind="normal",
    )

    phi_real = Cpt(
        ReadbackEpicsMotor,
        "phi}Mtr",
        labels=["stage"],
        kind="normal",
    )

    # ------------------------------------------------------------------
    # ROTATION CENTER CONFIGURATION SIGNALS
    # ------------------------------------------------------------------

    # theta center
    cx_theta = Cpt(Signal, value=2.7, kind="config")
    cy_theta = Cpt(Signal, value=-1.5, kind="config")
    cz_theta = Cpt(Signal, value=-1.38, kind="config")

    # chi center
    cx_chi = Cpt(Signal, value=2.7, kind="config")
    cy_chi = Cpt(Signal, value=-1.5, kind="config")
    cz_chi = Cpt(Signal, value=-1.38, kind="config")

    # phi center
    cx_phi = Cpt(Signal, value=2.7, kind="config")
    #cx_phi = Cpt(Signal, value=2.19, kind="config")
    cy_phi = Cpt(Signal, value=-1.5, kind="config")
    cz_phi = Cpt(Signal, value=-1.38, kind="config")

    # ------------------------------------------------------------------
    # BACKWARDS-COMPATIBLE AXIS ALIASES
    # ------------------------------------------------------------------
    # The legacy STG (hexapod) Device exposed the rotation axes as
    # .th / .ph / .ch.  STG_pseudo names the corresponding pseudo axes
    # .theta / .phi / .chi.  Expose the old names as properties returning
    # the same PseudoSingle components so existing user/plan code
    # (e.g. bps.mv(stage.th, ...), stage.th.position) keeps working
    # unchanged.  (.x/.y/.z already match the legacy names.)
    @property
    def th(self):
        return self.theta

    @property
    def ph(self):
        return self.phi

    @property
    def ch(self):
        return self.chi

    # ------------------------------------------------------------------
    # ROTATION MATRICES
    # ------------------------------------------------------------------

    @staticmethod
    def Rx(theta):
        c = np.cos(theta)
        s = np.sin(theta)

        return np.array([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c],
        ])

    @staticmethod
    def Ry(phi):
        c = np.cos(phi)
        s = np.sin(phi)

        return np.array([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c],
        ])

    @staticmethod
    def Rz(chi):
        c = np.cos(chi)
        s = np.sin(chi)

        return np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1],
        ])

    # ------------------------------------------------------------------
    # FORWARD TRANSFORM
    #
    # pseudo -> real
    # ------------------------------------------------------------------

    @pseudo_position_argument
    def forward(self, pseudo_pos):

        # --------------------------------------------------------------
        # desired LAB-FRAME coordinate
        # --------------------------------------------------------------

        p = np.array([
            pseudo_pos.x,
            pseudo_pos.y,
            pseudo_pos.z,
        ])

        # --------------------------------------------------------------
        # angles
        # --------------------------------------------------------------

        theta = np.deg2rad(pseudo_pos.theta)
        chi = np.deg2rad(pseudo_pos.chi)
        phi = np.deg2rad(pseudo_pos.phi)

        # --------------------------------------------------------------
        # centers
        # --------------------------------------------------------------

        c_theta = np.array([
            self.cx_theta.get(),
            self.cy_theta.get(),
            self.cz_theta.get(),
        ])

        c_chi = np.array([
            self.cx_chi.get(),
            self.cy_chi.get(),
            self.cz_chi.get(),
        ])

        c_phi = np.array([
            self.cx_phi.get(),
            self.cy_phi.get(),
            self.cz_phi.get(),
        ])

        # --------------------------------------------------------------
        # rotation matrices
        # --------------------------------------------------------------

        Rtheta = self.Rx(theta)
        Rchi = self.Rz(chi)
        Rphi = self.Ry(phi)

        # --------------------------------------------------------------
        # STACK ORDER:
        #
        # theta -> chi -> phi -> xyz
        #
        # For pseudo->real compensation we apply inverse transforms
        # in reverse order.
        # --------------------------------------------------------------

        # phi
        p = (
            Rphi.T @ (p - c_phi)
            + c_phi
        )

        # chi
        p = (
            Rchi.T @ (p - c_chi)
            + c_chi
        )

        # theta
        p = (
            Rtheta.T @ (p - c_theta)
            + c_theta
        )

        return self.RealPosition(
            x_real=p[0],
            y_real=p[1],
            z_real=p[2],
            theta_real=pseudo_pos.theta,
            chi_real=pseudo_pos.chi,
            phi_real=pseudo_pos.phi,
        )

    # ------------------------------------------------------------------
    # INVERSE TRANSFORM
    #
    # real -> pseudo
    # ------------------------------------------------------------------

    @real_position_argument
    def inverse(self, real_pos):

        p = np.array([
            real_pos.x_real,
            real_pos.y_real,
            real_pos.z_real,
        ])

        theta = np.deg2rad(real_pos.theta_real)
        chi = np.deg2rad(real_pos.chi_real)
        phi = np.deg2rad(real_pos.phi_real)

        # --------------------------------------------------------------
        # centers
        # --------------------------------------------------------------

        c_theta = np.array([
            self.cx_theta.get(),
            self.cy_theta.get(),
            self.cz_theta.get(),
        ])

        c_chi = np.array([
            self.cx_chi.get(),
            self.cy_chi.get(),
            self.cz_chi.get(),
        ])

        c_phi = np.array([
            self.cx_phi.get(),
            self.cy_phi.get(),
            self.cz_phi.get(),
        ])

        # --------------------------------------------------------------
        # rotation matrices
        # --------------------------------------------------------------

        Rtheta = self.Rx(theta)
        Rchi = self.Rz(chi)
        Rphi = self.Ry(phi)

        # --------------------------------------------------------------
        # Apply forward transforms in stack order
        # --------------------------------------------------------------

        # theta
        p = (
            Rtheta @ (p - c_theta)
            + c_theta
        )

        # chi
        p = (
            Rchi @ (p - c_chi)
            + c_chi
        )

        # phi
        p = (
            Rphi @ (p - c_phi)
            + c_phi
        )

        return self.PseudoPosition(
            x=p[0],
            y=p[1],
            z=p[2],

            theta=real_pos.theta_real,
            chi=real_pos.chi_real,
            phi=real_pos.phi_real,
        )

    # ------------------------------------------------------------------
    # LIMIT CHECKING
    # ------------------------------------------------------------------

    def check_value(self, pos):

        real = self.forward(pos)

        self.x_real.check_value(real.x_real)
        self.y_real.check_value(real.y_real)
        self.z_real.check_value(real.z_real)

        self.theta_real.check_value(real.theta_real)
        self.chi_real.check_value(real.chi_real)
        self.phi_real.check_value(real.phi_real)

    # ------------------------------------------------------------------
    # CONVENIENCE METHODS
    # ------------------------------------------------------------------

    def set_theta_center(self, x, y, z):
        self.cx_theta.put(x)
        self.cy_theta.put(y)
        self.cz_theta.put(z)

    def set_chi_center(self, x, y, z):
        self.cx_chi.put(x)
        self.cy_chi.put(y)
        self.cz_chi.put(z)

    def set_phi_center(self, x, y, z):
        self.cx_phi.put(x)
        self.cy_phi.put(y)
        self.cz_phi.put(z)