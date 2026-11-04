

from ophyd import (
    EpicsMotor,
    EpicsSignal,
    EpicsSignalRO,
    PVPositionerIsClose,
    Device,
    Component as Cpt,
)


from .status import sample_status


class SMARACT(Device):
    status_description = sample_status("um")
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




class SmarActAxis(PVPositionerIsClose):
    """One axis of a SmarAct open-loop piezo stepper exposed through its raw controller PVs.

    The BDM stage is a SmarAct controller whose channels are published as
    ``XF:12IDC-ES:2:ACT<n>:*`` (no EPICS motor record).  Previously each axis was a bare
    ``EpicsSignal`` (read ``ACT<n>:POSITION``, write ``ACT<n>:CMD:TARGET``), so a ``set``/``mv``
    completed the instant the CA put was acknowledged -- **not** when the stage had physically
    finished moving.  In a plan like ``bp.rel_scan([pil2M], bdm.y, ...)`` that meant the detector
    could read before the BDM had settled.

    Done-detection (why ``PVPositionerIsClose`` and not the controller's flags)
    --------------------------------------------------------------------------
    This controller's status flags are **unreliable**: on the SMI BDM, ``RD_MOVING`` reads ``1``
    permanently (even at rest, and long after the stage has demonstrably reached target) and
    ``RD_INRANGE`` reads ``0`` permanently.  A ``done``-flag-based ``PVPositioner`` would therefore
    hang forever.  The ``POSITION`` readback, however, IS live and reliable (it ramps to the
    target and settles).  So the move is considered complete when the **readback is close to the
    setpoint** (``np.isclose`` with :attr:`atol`), which depends only on the trustworthy readback.

    The controller's in-range / moving / error / EOT / connection flags are still exposed as
    readable signals (``kind="config"``) for monitoring/diagnostics; they do **not** gate the
    move (and given their unreliability here, should not be relied upon).
    """

    # --- the PVPositioner contract; completion is |readback - setpoint| <= atol ---
    setpoint = Cpt(EpicsSignal, "CMD:TARGET")
    readback = Cpt(EpicsSignalRO, "POSITION", kind="hinted")
    #: absolute settle tolerance (controller units).  The BDM settles to within ~1e-5 of target;
    #: 0.01 is comfortably loose enough never to hang yet tight enough to mean "arrived".
    atol = 0.01

    stop_signal = Cpt(EpicsSignal, "CMD:STOP")
    stop_value = 1

    # --- diagnostics (do NOT gate the move; unreliable on this controller -- see class docstring) ---
    moving_flag = Cpt(EpicsSignalRO, "RD_MOVING", kind="config")
    in_range = Cpt(EpicsSignalRO, "RD_INRANGE", kind="config")
    st_in_range = Cpt(EpicsSignalRO, "ST_INRANGE", kind="config")
    st_error = Cpt(EpicsSignalRO, "ST_ERROR", kind="config")
    st_connect = Cpt(EpicsSignalRO, "ST_CONNECT", kind="config")
    st_enabled = Cpt(EpicsSignalRO, "ST_ENABLED", kind="config")
    st_eot_fwd = Cpt(EpicsSignalRO, "ST_EOT_FWD", kind="config")
    st_eot_bwd = Cpt(EpicsSignalRO, "ST_EOT_BWD", kind="config")
    ref_position = Cpt(EpicsSignalRO, "REF_POSITION", kind="config")


class BDMStage(Device):
    """Beam-diagnostic-module stage: three SmarAct axes with real move-completion.

    Each axis (``x``/``y``/``th``) keeps its previous PV mapping and its mover interface --
    ``bps.mv(bdm.x, val)`` and ``bp.rel_scan([pil2M], bdm.x, ...)`` work as before -- but now via
    :class:`SmarActAxis`, so a move waits until the readback reaches the target instead of
    returning on the CA put-ack.  Read the current value with ``bdm.x.position`` (the positioner
    readback); the former bare-signal ``bdm.x.get()`` returned a scalar, whereas a positioner's
    ``.get()`` returns a namedtuple, so the call sites that read the value now use ``.position``.
    """
    x = Cpt(SmarActAxis, "ACT2:", kind="hinted")
    y = Cpt(SmarActAxis, "ACT1:", kind="hinted")
    th = Cpt(SmarActAxis, "ACT0:", kind="hinted")


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
from ophyd.status import MoveStatus

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


class DeadbandEpicsMotor(ReadbackEpicsMotor):
    """
    EPICS motor that skips writes for moves already inside a configured deadband.

    This is used under ``STG_pseudo`` to avoid heating a real axis with tiny
    pseudo-positioner correction moves caused by transform/readback roundoff.
    """

    deadband = 0.0

    def move(self, position, wait=True, **kwargs):
        try:
            current = self.position
            if current is not None and abs(float(position) - float(current)) <= self.deadband:
                moved_cb = kwargs.get("moved_cb")
                status = MoveStatus(self, position)
                status.set_finished()
                if moved_cb is not None:
                    moved_cb(status, obj=self)
                return status
        except (TypeError, ValueError):
            pass

        return super().move(position, wait=wait, **kwargs)


class STG_temps(Device):
    x = Cpt(
            EpicsSignal,
            "3",
            name="X temp",
            kind="normal",
            doc="Temperature of the Huber X motor",
        )
    y = Cpt(
            EpicsSignal,
            "4",
            name="Y temp",
            kind="normal",
            doc="Temperature of the Huber Y motor",
        )
    z = Cpt(
            EpicsSignal,
            "2",
            name="Z temp",
            kind="normal",
            doc="Temperature of the Huber Z motor",
        )
    th = Cpt(
            EpicsSignal,
            "6",
            name="Theta temp",
            kind="normal",
            doc="Temperature of the Huber Theta motor",
        )
    phi = Cpt(
            EpicsSignal,
            "7",
            name="Phi temp",
            kind="normal",
            doc="Temperature of the Huber Phi motor",
        )
    chi = Cpt(
            EpicsSignal,
            "5",
            name="Chi temp",
            kind="normal",
            doc="Temperature of the Huber Chi motor",
        )


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

    Pseudo XYZ coordinates are laboratory-frame coordinates of a point on the
    upper stack. Real translations compensate at the requested endpoint.

        x       : inboard / outboard
        y       : up / down
        z       : upstream / downstream

    The angular coordinates are a fixed-axis Euler convention, in degrees:

        R_lab = Ry(phi) @ Rz(chi) @ Rx(theta)

    The real axes form the nested chain R_real = Rx(theta_real) @
    Rz(chi_real) @ Ry(phi_real). Thus pseudo angles are generally NOT the
    real motor angles, and moving any pseudo angle can move multiple motors.
    At finite rotations Euler coordinates are not three independent rotations
    about fixed lab axes. Real motor EPICS user coordinates supply the angular
    zeros; no extra angular zero is applied here.

    For GI CD-SAXS the physical phi axis must be NORMAL to the sample plane.
    After aligning the axis and sample to the beam, fly phi_real alone: theta
    and chi must not move during that exposure. A pseudo phi move is not a
    substitute. For a fixed illuminated point during a phi_real-only fly, that
    point must also lie on the physical phi axis; no XYZ compensation occurs.
    Verify beam direction, signs, centers, limits, and physical performance
    before using this idealized model. Motor signs (especially Z) are not yet
    experimentally confirmed.

    ================================================================
    ROTATION CENTERS
    ================================================================

    Rotation centers are configuration signals in the shared zero-pose
    coordinate system (the lab frame when all three real angles are zero).
    Each center is fixed in its own joint's parent frame. A change to EPICS
    angular zeros changes this reference and requires revalidation.

    Each rotational axis may have an independent center:
        theta center
        chi center
        phi center

    These are NOT pseudo axes.
    """

    real_move_deadband = 0.001
    angular_move_deadband = 0.0001
    status_description = sample_status("mm")

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
        doc="Lab Euler theta in Ry(phi) Rz(chi) Rx(theta)",
    )

    chi = Cpt(
        PseudoSingle,
        limits=(-89.999, 89.999),
        kind="hinted",
        doc="Lab Euler chi in Ry(phi) Rz(chi) Rx(theta)",
    )

    phi = Cpt(
        PseudoSingle,
        limits=(-250, 120),
        kind="hinted",
        doc="Lab Euler phi in Ry(phi) Rz(chi) Rx(theta)",
    )

    # ------------------------------------------------------------------
    # REAL MOTORS
    # ------------------------------------------------------------------

    x_real = Cpt(
        DeadbandEpicsMotor,
        "X}Mtr",
        labels=["stage"],
        kind="normal",
    )

    y_real = Cpt(
        DeadbandEpicsMotor,
        "Y}Mtr",
        labels=["stage"],
        kind="normal",
    )

    z_real = Cpt(
        DeadbandEpicsMotor,
        "Z}Mtr",
        labels=["stage"],
        kind="normal",
    )

    theta_real = Cpt(
        DeadbandEpicsMotor,
        "theta}Mtr",
        labels=["stage"],
        kind="normal",
    )

    chi_real = Cpt(
        DeadbandEpicsMotor,
        "chi}Mtr",
        labels=["stage"],
        kind="normal",
    )

    phi_real = Cpt(
        DeadbandEpicsMotor,
        "phi}Mtr",
        labels=["stage"],
        kind="normal",
    )

    def __init__(self, *args, real_move_deadband=None, angular_move_deadband=None, **kwargs):
        super().__init__(*args, **kwargs)
        if real_move_deadband is not None:
            self.real_move_deadband = real_move_deadband
        if angular_move_deadband is not None:
            self.angular_move_deadband = angular_move_deadband
        for motor in (self.x_real, self.y_real, self.z_real):
            motor.deadband = self.real_move_deadband
        for motor in (self.theta_real, self.chi_real, self.phi_real):
            motor.deadband = self.angular_move_deadband

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

    @staticmethod
    def _unwrap_near(angle, reference):
        """Choose the 360-degree branch nearest the supplied phi coordinate."""
        return reference + (angle - reference + 180.0) % 360.0 - 180.0

    @staticmethod
    def _check_rotation(rotation, middle_cosine):
        if not np.all(np.isfinite(rotation)):
            raise ValueError("Huber orientation angles must be finite")
        if abs(middle_cosine) < 1e-10:
            raise ValueError("Huber Euler orientation is at a singularity")

    @classmethod
    def _lab_to_joints(cls, theta, chi, phi):
        """Decompose Ry(phi) Rz(chi) Rx(theta) into nested real joints.

        Select the branch with |real chi| < 90 degrees, appropriate to the
        cradle. Preserve phi winding rather than wrapping at +/-180 degrees.
        Real motor limit checks still determine whether the pose is reachable.
        """
        if not np.all(np.isfinite([theta, chi, phi])) or abs(chi) >= 90:
            raise ValueError("Lab Euler chi must be finite and strictly between -90 and 90 degrees")
        t, c, p = np.deg2rad([theta, chi, phi])
        rot = cls.Ry(p) @ cls.Rz(c) @ cls.Rx(t)
        real_chi = np.arcsin(np.clip(-rot[0, 1], -1.0, 1.0))
        cls._check_rotation(rot, np.cos(real_chi))
        real_theta = np.arctan2(rot[2, 1], rot[1, 1])
        real_phi = np.arctan2(rot[0, 2], rot[0, 0])
        theta, chi, phi_principal = np.rad2deg([real_theta, real_chi, real_phi])
        return theta, chi, cls._unwrap_near(phi_principal, phi)

    @classmethod
    def _joints_to_lab(cls, theta, chi, phi):
        """Decompose nested real joints into the lab Euler convention."""
        if not np.all(np.isfinite([theta, chi, phi])) or abs(chi) >= 90:
            raise ValueError("Real chi must be finite and strictly between -90 and 90 degrees")
        t, c, p = np.deg2rad([theta, chi, phi])
        rot = cls.Rx(t) @ cls.Rz(c) @ cls.Ry(p)
        lab_chi = np.arcsin(np.clip(rot[1, 0], -1.0, 1.0))
        cls._check_rotation(rot, np.cos(lab_chi))
        lab_theta = np.arctan2(-rot[1, 2], rot[1, 1])
        lab_phi = np.arctan2(-rot[2, 0], rot[0, 0])
        theta, chi, phi_principal = np.rad2deg([lab_theta, lab_chi, lab_phi])
        return theta, chi, cls._unwrap_near(phi_principal, phi)

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

        theta_real, chi_real, phi_real = self._lab_to_joints(
            pseudo_pos.theta, pseudo_pos.chi, pseudo_pos.phi
        )
        theta, chi, phi = np.deg2rad([theta_real, chi_real, phi_real])

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
        # A point on the top stack is carried by phi, then chi, then theta.
        # To find the real translations for a lab point, invert theta first.
        # --------------------------------------------------------------

        # theta
        p = (
            Rtheta.T @ (p - c_theta)
            + c_theta
        )

        # chi
        p = (
            Rchi.T @ (p - c_chi)
            + c_chi
        )

        # phi
        p = (
            Rphi.T @ (p - c_phi)
            + c_phi
        )

        return self.RealPosition(
            x_real=p[0],
            y_real=p[1],
            z_real=p[2],
            theta_real=theta_real,
            chi_real=chi_real,
            phi_real=phi_real,
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
        # Apply from top to bottom: each lower axis carries the axes above it.
        # --------------------------------------------------------------

        # phi
        p = (
            Rphi @ (p - c_phi)
            + c_phi
        )

        # chi
        p = (
            Rchi @ (p - c_chi)
            + c_chi
        )

        # theta
        p = (
            Rtheta @ (p - c_theta)
            + c_theta
        )

        lab_theta, lab_chi, lab_phi = self._joints_to_lab(
            real_pos.theta_real, real_pos.chi_real, real_pos.phi_real
        )

        return self.PseudoPosition(
            x=p[0],
            y=p[1],
            z=p[2],

            theta=lab_theta,
            chi=lab_chi,
            phi=lab_phi,
        )

    # ------------------------------------------------------------------
    # LIMIT CHECKING
    # ------------------------------------------------------------------

    def check_value(self, pos):
        # The base implementation checks BOTH pseudo limits and all transformed
        # real limits. Endpoint checks are not a collision or trajectory check.
        if not np.all(np.isfinite(pos)):
            raise ValueError("Huber pseudo coordinates must be finite")
        super().check_value(pos)

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
