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
    with pytest.warns(UserWarning, match="managed large move"):
        RE(bps.mv(energy, 10000.0))


def test_below_8keV_warns_but_runs(energy):
    energy.set(7000.0)
    # below 8 keV the flux threshold is >10, so use a flux clearly above it
    diag = FakeDiag(energy, sumY=15.0, oval0={"roll": 50.0, "pitch": 50.0})
    RE = RunEngine({})
    _install(RE, energy, diag, threshold_eV=500.0, step_eV=500.0)
    with pytest.warns(UserWarning, match="validated only >= 8 keV"):
        RE(bps.mv(energy, 7800.0))           # 800 eV move, below 8 keV
    assert abs(float(energy.position) - 7800.0) < 1.0


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
