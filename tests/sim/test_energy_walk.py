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
from _fakes import FakeDiag, FakeOval  # noqa: E402,F401  (shared fake DCM-feedback model)


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
                              max_steps=40, rail_max_steps=10, verbose=False))


def test_recenter_aborts_when_flux_falls_and_stays_down_at_rail(energy):
    """While stuck rail-stepping, if the (settled) flux falls and STAYS down, abort on flux (before
    the rail-stuck step budget)."""
    from ophyd import Signal

    # Keep OVAL pinned at the rail every step (so it KEEPS rail-stepping): use a coupling that
    # drives further into the clamped +rail (like the wrong-sign case), so at_rail stays True.
    diag = FakeDiag(energy, gains={"roll": +600000.0, "pitch": -600000.0}, oval0={"roll": 4095.0})
    diag.assumed_sign["roll"] = -1.0    # 'toward 0' pushes INTO +rail -> OVAL stays at 4095

    # Flux collapses as soon as we start stepping and stays down.
    class CollapsedFlux(Signal):
        def __init__(self, motor, **kw):
            super().__init__(name="sumY", value=10.0, **kw)
            self._m = motor
            self._m0 = float(motor.position)
        def get(self):
            return 10.0 if abs(float(self._m.position) - self._m0) < 1e-6 else 0.5

    diag.sumY = CollapsedFlux(diag.motor["roll"])
    RE = RunEngine({})
    with pytest.raises(Exception, match="intensity fell and stayed down"):
        RE(recenter_axis_plan(diag, "roll", target=400.0, settle=0.03, sample_interval=0.02,
                              max_steps=40, rail_max_steps=10,
                              flux_drop_frac=0.5, flux_drop_consec=2, verbose=False))


def test_recenter_tolerates_a_single_flux_dip_at_rail(energy):
    """A one-step flux dip (then recovery) while rail-stepping must NOT abort (it converges)."""
    from ophyd import Signal

    diag = FakeDiag(energy, oval0={"roll": 4095.0})    # correct sign -> escapes rail quickly

    class DipOnceFlux(Signal):
        def __init__(self, **kw):
            super().__init__(name="sumY", value=10.0, **kw)
            self._reads = 0
        def get(self):
            self._reads += 1
            return 2.0 if self._reads == 2 else 10.0   # a single low read, then fine

    diag.sumY = DipOnceFlux()
    RE = RunEngine({})
    RE(recenter_axis_plan(diag, "roll", target=400.0, settle=0.03, sample_interval=0.02,
                          rail_max_steps=10, flux_drop_frac=0.5, flux_drop_consec=2,
                          verbose=False))
    assert abs(diag.oval["roll"].get()) < 400.0


def test_recenter_aborts_on_wrong_sign(energy):
    # gain sign OPPOSITE to assumed -> a step moves OVAL away from 0 -> must abort
    diag = FakeDiag(energy, gains={"roll": -600000.0, "pitch": -600000.0},
                    oval0={"roll": 3000.0})
    RE = RunEngine({})
    with pytest.raises(Exception):
        RE(recenter_axis_plan(diag, "roll", target=400.0, settle=0.05, sample_interval=0.02,
                              deadband=10.0, verbose=False))


class _JumpyOval(Signal):
    """OVAL coupled to a motor (correct sign) but with a small ONE-SHOT wrong-way blip on the first
    ``n_bad`` motor steps -- models the jumpy/hysteretic pitch loop (small noise the wrong way that a
    bigger corrective step then overcomes)."""
    def __init__(self, name, motor, gain, value, n_bad=1, blip=120.0, rail=8191.0):
        super().__init__(name=name, value=float(value))
        self._motor = motor
        self._gain = gain
        self._blip = blip
        self._bad_left = n_bad
        self._rail = rail
        self._last = float(motor.position)

    def get(self):
        cur_m = float(self._motor.position)
        dm = cur_m - self._last
        if dm:
            self._last = cur_m
            base = float(super().get()) + self._gain * dm
            if self._bad_left > 0:
                self._bad_left -= 1
                # push the WRONG way (away from 0) by a small amount, overriding this step's coupling
                base = float(super().get()) + (self._blip if super().get() >= 0 else -self._blip)
            base = max(-self._rail, min(self._rail, base))
            super().put(base)
        return super().get()


def test_recenter_forgives_a_small_wrongway_blip(energy):
    """A single small wrong-way settled step (noise/hysteresis) is forgiven; the loop then converges
    instead of aborting."""
    diag = FakeDiag(energy, oval0={"roll": 0.0, "pitch": 4500.0})
    # replace pitch OVAL with a jumpy one: 1 small wrong-way blip, then correct coupling.
    diag.oval["pitch"] = _JumpyOval("oval_pitch", diag.motor["pitch"],
                                    gain=-600000.0, value=4500.0, n_bad=1, blip=120.0)
    RE = RunEngine({})
    RE(recenter_axis_plan(diag, "pitch", target=400.0, settle=0.05, sample_interval=0.02,
                          deadband=10.0, wrong_way_oval=500.0, wrong_way_max=2, verbose=False))
    assert abs(diag.oval["pitch"].get()) < 400.0


def test_recenter_still_aborts_on_a_large_wrongway_step(energy):
    """A LARGE wrong-way step (real sign error, |dOVAL| >= wrong_way_oval) aborts immediately even
    with the small-blip tolerance enabled."""
    diag = FakeDiag(energy, gains={"roll": -600000.0, "pitch": -600000.0},
                    oval0={"roll": 3000.0})
    RE = RunEngine({})
    with pytest.raises(RuntimeError, match="WRONG way"):
        RE(recenter_axis_plan(diag, "roll", target=400.0, settle=0.05, sample_interval=0.02,
                              deadband=10.0, wrong_way_oval=500.0, wrong_way_max=2, verbose=False))


def test_recenter_aborts_after_too_many_small_wrongway_steps(energy):
    """If the small wrong-way moves persist past wrong_way_max (not noise), abort."""
    diag = FakeDiag(energy, oval0={"roll": 0.0, "pitch": 4500.0})
    # many wrong-way blips in a row -> exceeds the tolerance -> abort
    diag.oval["pitch"] = _JumpyOval("oval_pitch", diag.motor["pitch"],
                                    gain=-600000.0, value=4500.0, n_bad=99, blip=120.0)
    RE = RunEngine({})
    with pytest.raises(RuntimeError, match="WRONG way"):
        RE(recenter_axis_plan(diag, "pitch", target=400.0, settle=0.05, sample_interval=0.02,
                              deadband=10.0, wrong_way_oval=500.0, wrong_way_max=2, verbose=False))


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


def test_energy_walk_substeps_a_large_move(energy):
    """A move larger than step_eV is progressed in <= step_eV increments (each landing exactly),
    and ends at the final target."""
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 100.0, "pitch": 100.0})
    visited = []
    energy.subscribe(lambda value, **k: visited.append(round(float(value), 1)), run=False)
    RE = RunEngine({})
    RE(energy_walk(10000.0, diag=diag, energy=energy, step_eV=500.0, oval_settle_s=0.05,
                   oval_settle_window=50.0, recenter_settle=0.05, verbose=False))
    assert abs(float(energy.position) - 10000.0) < 1.0
    # it stopped at the 9500 sub-step on the way (not a single 9000->10000 jump)
    assert any(abs(v - 9500.0) < 1.0 for v in visited), visited


def test_energy_walk_reverts_to_previous_substep_on_low_flux(energy):
    """If flux fails at a later sub-step, revert to the PREVIOUS (last good) sub-step, not start."""
    energy.set(9000.0)

    # flux is fine at <=9500 but drops below threshold beyond that.
    class FluxByEnergy(Signal):
        def __init__(self, en, **kw):
            super().__init__(name="sumY", value=10.0, **kw)
            self._en = en
        def get(self):
            return 10.0 if float(self._en.position) <= 9500.5 else 0.2

    diag = FakeDiag(energy, oval0={"roll": 50.0, "pitch": 50.0})
    diag.sumY = FluxByEnergy(energy)
    RE = RunEngine({})
    with pytest.raises(Exception):
        RE(energy_walk(10000.0, diag=diag, energy=energy, step_eV=500.0, flux_settle=0.02,
                       oval_settle_s=0.05, oval_settle_window=50.0, recenter_settle=0.05,
                       verbose=False))
    # reverted to 9500 (the last good sub-step), NOT 9000 (the start)
    assert abs(float(energy.position) - 9500.0) < 1.0, float(energy.position)
    assert str(diag.fb_disable["roll"].get()) == "0"   # feedback restored ON


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


# --------------------------------------------------------------------------- BPM3 range (gain)
def test_energy_walk_sets_bpm3_range_per_energy_band(energy):
    """Walking across the range-table boundaries switches the BPM3 range (gain) and ends on the
    final-energy band, confirmed via the readback."""
    energy.set(9000.0)                                   # starts in the <10 keV band (idx 3)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 100.0, "pitch": 100.0})
    diag.range_rb.put(3)
    seen = []
    diag.range_rb.subscribe(lambda value, **k: seen.append(int(value)), run=False)
    RE = RunEngine({})
    RE(energy_walk(13000.0, diag=diag, energy=energy, step_eV=500.0, oval_settle_s=0.05,
                   oval_settle_window=50.0, recenter_settle=0.05, verbose=False))
    # final energy 13 keV -> 10 uA (index 1)
    assert int(diag.range_rb.get()) == 1
    # passed through the 100 uA band (index 2) on the way (10 <= E < 12 keV)
    assert 2 in seen, seen


def test_energy_walk_can_skip_bpm3_range(energy):
    """set_bpm3_range=False leaves the range untouched."""
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 100.0, "pitch": 100.0})
    diag.range_rb.put(3)
    RE = RunEngine({})
    RE(energy_walk(13000.0, diag=diag, energy=energy, step_eV=500.0, oval_settle_s=0.05,
                   oval_settle_window=50.0, recenter_settle=0.05, set_bpm3_range=False,
                   verbose=False))
    assert int(diag.range_rb.get()) == 3      # never changed
