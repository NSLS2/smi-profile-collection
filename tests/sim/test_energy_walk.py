"""Tier-2 (sim) tests for the feedback-managed energy_walk plan.

These run the *real* ``energy_walk`` / ``recenter_axis_plan`` / ``settle_oval_plan`` logic under a
RunEngine against FAKE signals (plain ``ophyd.Signal``/``SynAxis``), with a lightweight stand-in
for ``DCMDiag`` that holds the same attribute surface (``oval`` / ``fb_disable`` / ``motor`` /
``sumY`` / ``assumed_sign`` / ``flux_table`` / ``OVAL_RANGE`` / ``_energy_source``).  No hardware.

We model the feedback coupling just enough to drive the choreography: when feedback is ON, a
coarse-motor step changes the corresponding OVAL by ``gain * motor_delta`` (with the verified
signs).  This lets us check: the flux gate reverts + raises on low flux; recenter only fires when
``|OVAL| > window`` and drives it under target; a wrong-way sign aborts; and feedback is restored
ON on any exit.
"""
import pytest

pytest.importorskip("bluesky")
from bluesky import RunEngine  # noqa: E402
from ophyd import Signal  # noqa: E402
from ophyd.sim import SynAxis  # noqa: E402

from smi_beamline.plans.energy_walk import energy_walk, recenter_axis_plan, settle_oval_plan  # noqa: E402


# --------------------------------------------------------------------------- fake DCMDiag
class FakeOval(Signal):
    """An OVAL signal coupled to a coarse motor: when feedback is ON, moving the motor changes
    this OVAL by ``gain * motor_delta`` (sign per the real system), **clamped at +/-rail** to model
    the piezo DAC saturation."""
    def __init__(self, name, motor, fb_disable, gain, rail=4095.0):
        super().__init__(name=name, value=0.0)
        self._motor = motor
        self._fb = fb_disable           # "0" = feedback ON
        self._gain = gain
        self._rail = rail
        self._last_motor = float(motor.position)

    def get(self):
        # advance OVAL by the motor change since last read, only while feedback is ON
        cur_m = float(self._motor.position)
        dm = cur_m - self._last_motor
        self._last_motor = cur_m
        if dm and str(self._fb.get()) == "0":
            v = float(super().get()) + self._gain * dm
            v = max(-self._rail, min(self._rail, v))   # clamp at the hardware rail
            super().put(v)
        return super().get()


class FakeDiag:
    OVAL_RANGE = 8192.0
    OVAL_RAIL = {"roll": 4095.0, "pitch": 8191.0}
    OVAL_RAIL_MARGIN = 200.0
    OVAL_RECENTER_WINDOW = {"roll": 2000.0, "pitch": 4000.0}
    OVAL_TARGET = 400.0

    def rail(self, axis):
        return self.OVAL_RAIL.get(axis, self.OVAL_RANGE)

    def recenter_window(self, axis):
        return self.OVAL_RECENTER_WINDOW.get(axis, 0.5 * self.rail(axis))

    def __init__(self, energy, sumY=10.0, gains=None, flux_table=None,
                 oval0=None):
        gains = gains or {"roll": 600000.0, "pitch": -600000.0}     # verified signs
        self._energy_source = energy
        self.assumed_sign = {"roll": +1.0, "pitch": -1.0}
        self.flux_table = flux_table
        self.motor = {"roll": SynAxis(name="m68"), "pitch": SynAxis(name="m67")}
        self.fb_disable = {"roll": Signal(name="fb_roll", value="0"),
                           "pitch": Signal(name="fb_pitch", value="0")}
        self.oval = {
            a: FakeOval(f"oval_{a}", self.motor[a], self.fb_disable[a], gains[a],
                        rail=self.OVAL_RAIL[a])
            for a in ("roll", "pitch")
        }
        if oval0:
            for a, v in oval0.items():
                self.oval[a].put(v)
        self.sumY = Signal(name="sumY", value=sumY)


@pytest.fixture
def energy():
    en = SynAxis(name="energy")
    en.set(9000.0)
    return en


# --------------------------------------------------------------------------- recenter logic
def test_recenter_drives_oval_under_target(energy):
    diag = FakeDiag(energy, oval0={"roll": 3000.0, "pitch": 0.0})
    RE = RunEngine({})
    RE(recenter_axis_plan(diag, "roll", target=400.0, settle=0.05, sample_interval=0.02,
                          verbose=False))
    assert abs(diag.oval["roll"].get()) < 400.0


def test_recenter_from_the_rail(energy):
    """Starting AT the rail (4095) must NOT abort -- it should step toward 0 and converge."""
    diag = FakeDiag(energy, oval0={"roll": 4095.0, "pitch": 0.0})   # railed
    RE = RunEngine({})
    RE(recenter_axis_plan(diag, "roll", target=400.0, settle=0.05, sample_interval=0.02,
                          verbose=False))
    assert abs(diag.oval["roll"].get()) < 400.0


def test_recenter_aborts_when_stuck_at_rail_wrong_sign(energy):
    """Wrong sign while railed: OVAL stays pinned at the rail (no response) -> rail-stuck abort."""
    # gain sign opposite to assumed: 'toward 0' steps push further into the (clamped) rail, so OVAL
    # stays at +4095 every step -> the rail-stuck guard must abort.
    diag = FakeDiag(energy, gains={"roll": +600000.0, "pitch": -600000.0},
                    oval0={"roll": 4095.0})
    # assumed_sign roll=+1, but make the *effective* response wrong by flipping the motor coupling:
    diag.assumed_sign["roll"] = -1.0   # now 'toward 0' picks the motor dir that pushes INTO +rail
    RE = RunEngine({})
    with pytest.raises(Exception):
        RE(recenter_axis_plan(diag, "roll", target=400.0, settle=0.03, sample_interval=0.02,
                              max_steps=20, verbose=False))


def test_recenter_aborts_on_wrong_sign(energy):
    # gain sign OPPOSITE to assumed -> a step moves OVAL away from 0 -> must abort
    diag = FakeDiag(energy, gains={"roll": -600000.0, "pitch": -600000.0},
                    oval0={"roll": 3000.0})
    RE = RunEngine({})
    with pytest.raises(Exception):
        RE(recenter_axis_plan(diag, "roll", target=400.0, settle=0.05, sample_interval=0.02,
                              deadband=10.0, verbose=False))


def test_settle_oval_returns_true_when_stable(energy):
    diag = FakeDiag(energy, oval0={"roll": 100.0, "pitch": 100.0})
    RE = RunEngine({})
    # feedback OFF so reads don't drift; OVAL is constant -> settles
    out = {}
    def plan():
        out["settled"] = yield from settle_oval_plan(diag, seconds=0.1, interval=0.02, timeout=2.0)
    RE(plan())
    assert out["settled"] is True


# --------------------------------------------------------------------------- energy_walk
def test_energy_walk_happy_path(energy):
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 100.0, "pitch": 100.0})
    RE = RunEngine({})
    RE(energy_walk(9100.0, diag=diag, energy=energy, oval_settle_s=0.1, oval_settle_window=50.0,
                   recenter_settle=0.05, verbose=False))
    assert abs(float(energy.position) - 9100.0) < 1.0
    # feedback left ON
    assert str(diag.fb_disable["roll"].get()) == "0"
    assert str(diag.fb_disable["pitch"].get()) == "0"


def test_energy_walk_recenters_when_oval_large(energy):
    # roll starts beyond the +/-3000 window -> energy_walk must recenter it under target
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 3500.0, "pitch": 50.0})
    RE = RunEngine({})
    RE(energy_walk(9100.0, diag=diag, energy=energy, oval_settle_s=0.1, oval_settle_window=1e9,
                   oval_window=3000.0, oval_target=400.0, recenter_settle=0.05, verbose=False))
    assert abs(diag.oval["roll"].get()) < 400.0


def test_energy_walk_uses_per_axis_window(energy):
    """With no oval_window override: roll triggers at >2000, pitch at >4000 (per-axis defaults).

    roll OVAL=2500 (>2000 -> recenter), pitch OVAL=3500 (<4000 -> NO recenter).
    """
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 2500.0, "pitch": 3500.0})
    RE = RunEngine({})
    RE(energy_walk(9100.0, diag=diag, energy=energy, oval_settle_s=0.1, oval_settle_window=1e9,
                   recenter_settle=0.05, verbose=False))
    assert abs(diag.oval["roll"].get()) < 400.0          # roll WAS recentered (2500 > 2000)
    assert abs(diag.oval["pitch"].get()) == pytest.approx(3500.0, abs=50)  # pitch left alone (<4000)


def test_energy_walk_reverts_and_raises_on_low_flux(energy):
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=0.2, oval0={"roll": 50.0, "pitch": 50.0})  # below any threshold
    RE = RunEngine({})
    with pytest.raises(Exception):
        RE(energy_walk(9100.0, diag=diag, energy=energy, flux_settle=0.02, verbose=False))
    # reverted to the starting energy
    assert abs(float(energy.position) - 9000.0) < 1.0
    # feedback restored ON by finalize
    assert str(diag.fb_disable["roll"].get()) == "0"


def test_energy_walk_restores_feedback_on_error(energy):
    # force an error AFTER feedback is turned off (low flux) and confirm feedback ends ON
    diag = FakeDiag(energy, sumY=0.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    try:
        RE(energy_walk(9100.0, diag=diag, energy=energy, flux_settle=0.02, verbose=False))
    except Exception:
        pass
    assert str(diag.fb_disable["roll"].get()) == "0"
    assert str(diag.fb_disable["pitch"].get()) == "0"
