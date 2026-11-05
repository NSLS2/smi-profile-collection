"""Offline Huber kinematics checks; these cannot establish installed signs."""

import numpy as np
import pytest

from smi_beamline.devices.manipulators import STG_pseudo


@pytest.fixture
def stage(make_fake):
    return make_fake(STG_pseudo, name="stage")


def test_real_nested_rotations_have_expected_noncommuting_result(stage):
    """An upper phi moves first; bottom theta carries the rotated point."""
    stage.set_theta_center(0, 0, 0)
    stage.set_chi_center(0, 0, 0)
    stage.set_phi_center(0, 0, 0)
    lab = stage.inverse(stage.RealPosition(0, 0, 1, 4, 0, 90))
    np.testing.assert_allclose([lab.x, lab.y, lab.z], [1, 0, 0], atol=1e-12)
    # Rx(4) Ry(90) = Ry(90) Rz(4), not Ry(90) Rx(4).
    np.testing.assert_allclose([lab.theta, lab.chi, lab.phi], [0, 4, 90], atol=1e-12)


def test_distinct_centers_are_carried_by_lower_axes(stage):
    stage.set_theta_center(0, 0, 0)
    stage.set_chi_center(0, 0, 0)
    stage.set_phi_center(0, 0, 1)
    lab = stage.inverse(stage.RealPosition(0, 0, 2, 30, 0, 90))
    # Rotate about phi's (0,0,1) center first: (1,0,1). Then bottom theta
    # carries BOTH the phi center and the point: (1, -1/2, sqrt(3)/2).
    np.testing.assert_allclose([lab.x, lab.y, lab.z], [1, -0.5, 3**0.5/2], atol=1e-12)


@pytest.mark.parametrize("real_phi", [-250, -225, -180, -90, 0, 90, 120])
@pytest.mark.parametrize("theta,chi", [(0, 0), (3.4, -2.6), (-3.5, 3.2)])
def test_mixed_joint_poses_roundtrip_with_phi_winding(stage, real_phi, theta, chi):
    stage.set_theta_center(1.2, -3.4, 2.5)
    stage.set_chi_center(-0.2, 0.3, 1.4)
    stage.set_phi_center(2.1, -0.5, -1.6)
    real = stage.RealPosition(3, -4, 5, theta, chi, real_phi)
    pseudo = stage.inverse(real)
    result = stage.forward(pseudo)
    np.testing.assert_allclose(result, real, atol=1e-11)
    # Lab phi tracks the same winding as the physical motor coordinate.
    assert abs(pseudo.phi - real_phi) < 1


def test_lab_phi_is_continuous_across_minus_180(stage):
    before = stage.inverse(stage.RealPosition(0, 0, 0, 3, -2, -179.99))
    after = stage.inverse(stage.RealPosition(0, 0, 0, 3, -2, -180.01))
    assert 0 < before.phi - after.phi < 0.1


def test_lab_phi_is_a_lab_y_rotation_not_the_physical_phi_joint(stage):
    pseudo = stage.PseudoPosition(0, 0, 0, 4, 0, 90)
    real = stage.forward(pseudo)
    # Ry(90) Rx(4) = Rx(0) Rz(-4) Ry(90).
    np.testing.assert_allclose([real.theta_real, real.chi_real, real.phi_real],
                               [0, -4, 90], atol=1e-12)


@pytest.mark.parametrize("theta,chi,phi", [(4, -2, 45), (-3, 1, -200), (0, 0, 120)])
def test_joint_and_lab_angles_describe_the_same_orientation(stage, theta, chi, phi):
    real = stage.RealPosition(0, 0, 0, theta, chi, phi)
    pseudo = stage.inverse(real)
    t, c, p = np.deg2rad([theta, chi, phi])
    lt, lc, lp = np.deg2rad([pseudo.theta, pseudo.chi, pseudo.phi])
    physical = stage.Rx(t) @ stage.Rz(c) @ stage.Ry(p)
    lab = stage.Ry(lp) @ stage.Rz(lc) @ stage.Rx(lt)
    np.testing.assert_allclose(lab, physical, atol=1e-12)


@pytest.mark.parametrize("theta,chi,phi", [(10, 0, 0), (0, 10, 0), (0, 0, 90),
                                            (4, -2, 45), (-3, 1, -200)])
def test_position_displacements_match_reported_lab_orientation(stage, theta, chi, phi):
    """Position and angular transforms must describe the same rigid rotation."""
    stage.set_theta_center(1.2, -3.4, 2.5)
    stage.set_chi_center(-0.2, 0.3, 1.4)
    stage.set_phi_center(2.1, -0.5, -1.6)
    real = stage.RealPosition(3, -4, 5, theta, chi, phi)
    origin = stage.inverse(real)
    base = np.array([origin.x, origin.y, origin.z])
    columns = []
    for axis in range(3):
        displaced = list(real)
        displaced[axis] += 1
        point = stage.inverse(stage.RealPosition(*displaced))
        columns.append(np.array([point.x, point.y, point.z]) - base)

    # Construct the lab Euler rotation independently of the stage's Rx/Ry/Rz
    # helpers; paired forward/inverse transforms could otherwise hide a sign error.
    t, c, p = np.deg2rad([origin.theta, origin.chi, origin.phi])
    ct, st, cc, sc, cp, sp = np.cos(t), np.sin(t), np.cos(c), np.sin(c), np.cos(p), np.sin(p)
    rx = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
    rz = np.array([[cc, -sc, 0], [sc, cc, 0], [0, 0, 1]])
    ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
    np.testing.assert_allclose(np.column_stack(columns), ry @ rz @ rx, atol=1e-12)


def test_positive_lab_rotations_have_reference_frame_senses(stage):
    for axis in ("theta", "chi", "phi"):
        getattr(stage, f"set_{axis}_center")(0, 0, 0)
    # +theta tips +Y toward +Z; +chi tips +X toward +Y; +phi tips +Z toward +X.
    cases = [((0, 1, 0, 90, 0, 0), (0, 0, 1)),
             ((1, 0, 0, 0, 45, 0), (2**-0.5, 2**-0.5, 0)),
             ((0, 0, 1, 0, 0, 90), (1, 0, 0))]
    for pose, expected in cases:
        point = stage.inverse(stage.RealPosition(*pose))
        np.testing.assert_allclose([point.x, point.y, point.z], expected, atol=1e-12)


def test_historical_center_defaults_are_negative_z(stage):
    for axis in ("theta", "chi", "phi"):
        assert getattr(stage, f"cz_{axis}").get() == -1.38


def test_zero_cradle_real_phi_within_pseudo_limits_is_accepted(stage):
    for motor in stage.real_positioners:
        motor.user_setpoint._limits = (-1000, 1000)
    pseudo = stage.inverse(stage.RealPosition(0, 0, 0, 0, 0, -200))
    assert pseudo.phi == pytest.approx(-200)
    stage.check_value(pseudo)


def test_z_uses_epics_user_coordinate_without_extra_reversal(stage):
    real = stage.RealPosition(1, 2, 3, 0, 0, 0)
    pseudo = stage.inverse(real)
    np.testing.assert_allclose([pseudo.x, pseudo.y, pseudo.z], [1, 2, 3], atol=1e-12)
    np.testing.assert_allclose(stage.forward(pseudo), real, atol=1e-12)


def test_physical_phi_only_changes_lab_angles_but_not_real_cradle(stage):
    real_a = stage.RealPosition(0, 0, 0, 2, -1, -200)
    real_b = real_a._replace(phi_real=-110)
    pseudo_a = stage.inverse(real_a)
    pseudo_b = stage.inverse(real_b)
    assert abs(pseudo_a.theta - pseudo_b.theta) > 0.01
    assert abs(pseudo_a.chi - pseudo_b.chi) > 0.1
    np.testing.assert_allclose(stage.forward(pseudo_b), real_b, atol=1e-11)
    # A sample normal aligned with the physical phi axis remains fixed.
    def normal(pseudo):
        t, c, p = np.deg2rad([pseudo.theta, pseudo.chi, pseudo.phi])
        return stage.Ry(p) @ stage.Rz(c) @ stage.Rx(t) @ np.array([0, 1, 0])
    np.testing.assert_allclose(normal(pseudo_a), normal(pseudo_b), atol=1e-12)


def test_euler_singularities_and_nonfinite_values_are_rejected(stage):
    with pytest.raises(ValueError, match="Lab Euler chi"):
        stage.forward(stage.PseudoPosition(0, 0, 0, 0, 90, 0))
    with pytest.raises(ValueError, match="Real chi"):
        stage.inverse(stage.RealPosition(0, 0, 0, 0, 90, 0))
    with pytest.raises(ValueError, match="finite"):
        stage.check_value(stage.PseudoPosition(float("nan"), 0, 0, 0, 0, 0))


def test_pseudo_limits_and_deadbands(stage):
    assert stage.phi.limits == (-250, 120)
    assert stage.x_real.deadband == 0.001
    assert stage.z_real.deadband == 0.001
    assert stage.theta_real.deadband == 0.0001
    assert stage.chi_real.deadband == 0.0001
    assert stage.phi_real.deadband == 0.0001
    with pytest.raises(ValueError, match="pseudo single limits"):
        stage.check_value(stage.PseudoPosition(0, 0, 0, 0, 0, -251))


def test_real_limit_is_checked_after_angle_conversion(stage):
    from ophyd.utils.errors import LimitError

    for motor in stage.real_positioners:
        motor.user_setpoint._limits = (-1000, 1000)
    stage.chi_real.user_setpoint._limits = (-2, 2)
    with pytest.raises(LimitError):
        # Valid pseudo limits, but equivalent real chi is -4 degrees.
        stage.check_value(stage.PseudoPosition(0, 0, 0, 4, 0, 90))
