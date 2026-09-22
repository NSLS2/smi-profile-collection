import pytest

from ophyd import EpicsMotor
from smi_beamline.devices.crls import CRL
from smi_beamline.devices.crl_optics import CRLGeometry, NoFocusSolution


def test_crl_preserves_all_motor_components(make_fake):
    expected = {f"lens{i}": f"L{i}}}Mtr" for i in range(1, 13)}
    expected.update({axis: f"{axis.title()}}}Mtr" for axis in ("x", "y", "z", "ph", "th")})
    assert set(CRL.component_names) == set(expected)
    crl = make_fake(CRL, name="crl")
    for name, suffix in expected.items():
        component = getattr(CRL, name)
        assert component.cls is EpicsMotor
        assert component.suffix == suffix
        assert hasattr(getattr(crl, name), "move")
    assert crl.lens_inventory[11].aperture_mm == 2


def test_optics_helpers_do_not_read_or_move_motors(make_fake, monkeypatch):
    crl = make_fake(CRL, name="crl")

    def unexpected(*args, **kwargs):
        pytest.fail("Optics calculations must not interact with motors")

    for name in crl.component_names:
        motor = getattr(crl, name)
        for method in ("get", "read", "move", "set"):
            monkeypatch.setattr(motor, method, unexpected)
        monkeypatch.setattr(motor.user_readback, "get", unexpected)
        monkeypatch.setattr(motor.user_setpoint, "put", unexpected)
    solution = crl.recommend_focus(10)
    assert solution.holders == (2,)
    assert solution.z_mm == pytest.approx(186.34, abs=0.1)
    assert crl.focus_candidates(10)[0] == solution
    assert crl.focal_length(10, [2]) == solution.focal_length_mm
    with pytest.raises(NoFocusSolution):
        crl.recommend_focus(2.8)
    varied = crl.recommend_focus(10, geometry=CRLGeometry(incident_curvature_per_m=0.1))
    assert varied.holders == (2,)
    assert varied.z_mm < solution.z_mm
