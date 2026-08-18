"""Tier-2 (sim) tests for the large-energy-move preprocessor.

The preprocessor intercepts ``Msg('set', energy, target)`` in any plan and, when the jump exceeds
``threshold_eV``, replaces it with the ``energy_walk`` sub-plan (``step_eV`` sub-steps); smaller
moves pass straight through as a plain ``set``.  These run the real preprocessor + energy_walk
against the FakeDiag from ``test_energy_walk`` (fast feedback model), under a RunEngine.
"""
import warnings

import pytest

from bluesky import RunEngine
import bluesky.plan_stubs as bps
from ophyd.sim import SynAxis, det

from smi_beamline.plans.energy_move_preprocessor import (
    energy_move_preprocessor, install_energy_move_preprocessor)

# reuse the shared fake DCM-feedback model
from _fakes import FakeDiag  # noqa: E402


@pytest.fixture
def energy():
    en = SynAxis(name="energy")
    en.set(9000.0)
    return en


def _install(RE, energy, diag, **kw):
    # feed the fake diag + fast settle into energy_walk via walk_kwargs
    walk_kwargs = dict(diag=diag, oval_settle_s=0.02, oval_settle_window=1e9,
                       recenter_settle=0.02, flux_settle=0.02)
    walk_kwargs.update(kw.pop("walk_kwargs", {}))
    return install_energy_move_preprocessor(
        RE, energy, walk_kwargs=walk_kwargs, **kw)


def test_large_move_is_intercepted_and_substepped(energy):
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)

    visited = []
    energy.subscribe(lambda value, **k: visited.append(round(float(value), 1)), run=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        RE(bps.mv(energy, 10000.0))          # 1000 eV -> managed walk, 500 eV steps

    assert abs(float(energy.position) - 10000.0) < 1.0
    assert any(abs(v - 9500.0) < 1.0 for v in visited), visited   # stopped at the 9500 sub-step
    # feedback ended ON (managed move restores it)
    assert str(diag.fb_disable["roll"].get()) == "0"


def test_small_move_passes_through_plain(energy):
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)

    # a 100 eV move (<= threshold) must NOT toggle feedback (no managed walk)
    fb_writes = []
    diag.fb_disable["roll"].subscribe(lambda value, **k: fb_writes.append(str(value)), run=False)
    RE(bps.mv(energy, 9100.0))
    assert abs(float(energy.position) - 9100.0) < 1.0
    assert fb_writes == [], "small move wrongly triggered the managed walk (feedback toggled)"


def test_large_move_emits_one_warning(energy):
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)
    with pytest.warns(UserWarning, match="managed move"):
        RE(bps.mv(energy, 10000.0))


def test_below_validated_floor_warns_but_runs(energy):
    energy.set(2400.0)
    # very low end: flux threshold is 5 below 2.2 keV, so keep flux above it
    diag = FakeDiag(energy, sumY=12.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)
    with pytest.warns(UserWarning, match="below the validated feedback range"):
        RE(bps.mv(energy, 2000.0))           # ends below the 2100 eV validated floor
    assert abs(float(energy.position) - 2000.0) < 1.0


def test_no_infinite_recursion_on_large_move(energy):
    """The walk's own sub-step sets (<= step_eV) must not re-trigger the preprocessor."""
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)
    # a 2000 eV move -> 4 sub-steps; completes without runaway recursion
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        RE(bps.mv(energy, 11000.0))
    assert abs(float(energy.position) - 11000.0) < 1.0


def test_scan_fine_steps_stay_plain_but_first_jump_managed(energy):
    """A scan whose first point is a big jump gets the managed walk for that jump; the fine
    intra-scan steps (<= threshold) stay plain."""
    import bluesky.plans as bp
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)

    fb_writes = []
    diag.fb_disable["roll"].subscribe(lambda value, **k: fb_writes.append(str(value)), run=False)
    # scan from 11000..11020 in 5 eV steps -> the open jump 9000->11000 is managed (feedback
    # toggles), the 5 eV scan steps are plain (no extra toggles).
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        RE(bp.scan([det], energy, 11000.0, 11020.0, 5))
    assert abs(float(energy.position) - 11020.0) < 1.0
    # feedback was toggled (managed walk happened for the big jump) and ended ON
    assert "1" in fb_writes and str(diag.fb_disable["roll"].get()) == "0"


# --------------------------------------------------------------------------- small-move drift guard
def _track_motor(diag, axis):
    moves = []
    diag.motor[axis].subscribe(lambda value, **k: moves.append(round(float(value), 6)), run=False)
    return moves


def test_small_move_recenters_when_oval_drifted(energy):
    """A small move that finds pitch OVAL past its window recentres the coarse motor (back under
    target) and warns -- without ever toggling feedback."""
    energy.set(9000.0)
    # pitch OVAL parked well past its 4000 window (but not at the 8191 rail); roll fine.
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 50.0, "pitch": 5000.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)

    pitch_moves = _track_motor(diag, "pitch")
    fb_writes = []
    diag.fb_disable["pitch"].subscribe(lambda value, **k: fb_writes.append(str(value)), run=False)
    with pytest.warns(UserWarning, match="pitch OVAL .* drifted past its window"):
        RE(bps.mv(energy, 9100.0))               # 100 eV: plain set, then drift recentre

    assert abs(float(energy.position) - 9100.0) < 1.0
    assert pitch_moves, "pitch coarse motor was not stepped to recentre the drifted OVAL"
    assert abs(float(diag.oval["pitch"].get())) < 400.0   # pulled back under target
    assert fb_writes == [], "drift recentre must keep feedback ON (no fb_disable writes)"


def test_small_move_no_recenter_when_in_window(energy):
    """A small move with OVAL inside the window does nothing extra (no motor motion, no warning)."""
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)

    roll_moves = _track_motor(diag, "roll")
    pitch_moves = _track_motor(diag, "pitch")
    with warnings.catch_warnings():
        warnings.simplefilter("error")           # any warning would fail the test
        RE(bps.mv(energy, 9100.0))
    assert abs(float(energy.position) - 9100.0) < 1.0
    assert roll_moves == [] and pitch_moves == [], "in-window small move should not move the motors"


def test_small_move_drift_check_can_be_disabled(energy):
    """check_drift=False leaves small moves entirely plain even when OVAL has drifted."""
    energy.set(9000.0)
    diag = FakeDiag(energy, sumY=10.0, oval0={"roll": 50.0, "pitch": 5000.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0, check_drift=False)

    pitch_moves = _track_motor(diag, "pitch")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        RE(bps.mv(energy, 9100.0))
    assert abs(float(energy.position) - 9100.0) < 1.0
    assert pitch_moves == [], "check_drift=False must not recentre"


# --------------------------------------------------------------------------- low-energy enforcement
def test_low_energy_small_move_is_managed_and_substepped(energy):
    """Below 2500 eV the 50 eV rule is enforced even for a <=threshold move: a 200 eV move at low
    energy goes through the managed walk (feedback toggles) and stops at 50 eV sub-steps."""
    energy.set(2600.0)
    diag = FakeDiag(energy, sumY=12.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)

    visited = []
    energy.subscribe(lambda value, **k: visited.append(round(float(value), 1)), run=False)
    fb_writes = []
    diag.fb_disable["roll"].subscribe(lambda value, **k: fb_writes.append(str(value)), run=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        RE(bps.mv(energy, 2400.0))           # 200 eV, <= threshold, but below 2500 -> managed @50 eV

    assert abs(float(energy.position) - 2400.0) < 1.0
    assert "1" in fb_writes, "low-energy small move should have been managed (feedback toggled)"
    assert any(abs(v - 2450.0) < 1.0 for v in visited), visited   # hit a 50 eV sub-step below 2500
    assert str(diag.fb_disable["roll"].get()) == "0"


def test_low_energy_single_50ev_move_stays_plain(energy):
    """A move equal to the low-energy sub-step (50 eV) is one step -> stays a plain set."""
    energy.set(2300.0)
    diag = FakeDiag(energy, sumY=12.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)
    fb_writes = []
    diag.fb_disable["roll"].subscribe(lambda value, **k: fb_writes.append(str(value)), run=False)
    RE(bps.mv(energy, 2250.0))               # exactly 50 eV -> plain
    assert abs(float(energy.position) - 2250.0) < 1.0
    assert fb_writes == [], "a single 50 eV low-energy move should stay plain"
