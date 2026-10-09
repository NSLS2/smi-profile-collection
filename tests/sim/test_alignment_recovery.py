"""Exercise scan/fit/recenter under a real RunEngine with in-memory motors."""

import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import numpy as np
import pandas as pd
import pytest
from bluesky import RunEngine
from ophyd.sim import SynAxis, SynSignal
from ophyd.utils import LimitError
from scipy.special import erf

from smi_beamline.plans._alignment import scan_and_center


@pytest.fixture
def harness(monkeypatch):
    # Load the actual ps implementation without importing live device instances.
    for module, names in {
        "energy": ["energy"], "pilatus": ["pil2m_pos", "waxs"],
        "electrometers": ["xbpm2"],
    }.items():
        stub = ModuleType(f"smi_beamline.instances.{module}")
        for name in names:
            setattr(stub, name, None)
        monkeypatch.setitem(sys.modules, stub.__name__, stub)
    path = Path(__file__).parents[2] / "src/smi_beamline/plans/utils.py"
    spec = importlib.util.spec_from_file_location("_alignment_test_utils", path)
    utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utils)
    runs = {}
    descriptors = {}
    starts = []

    def collect(name, doc):
        if name == "start":
            starts.append(doc)
            rows = []
            runs[doc["uid"]] = SimpleNamespace(
                start=doc, rows=rows, table=lambda: pd.DataFrame(rows))
        elif name == "descriptor":
            descriptors[doc["uid"]] = doc["run_start"]
        elif name == "event":
            row = dict(doc["data"])
            row["det_stats1_total"] = row.pop("det")
            runs[descriptors[doc["descriptor"]]].rows.append(row)

    utils.db = runs
    RE = RunEngine({})
    RE.subscribe(collect)
    return SimpleNamespace(RE=RE, ps=utils.ps, runs=runs, starts=starts)


class Motor(SynAxis):
    def __init__(self, *, value=0, limits=(-40, 10)):
        super().__init__(name="stage_y", value=value)
        self.bounds = limits
        self.moves = []

    def check_value(self, value):
        if not self.bounds[0] <= value <= self.bounds[1]:
            raise LimitError(f"real motor target {value} outside {self.bounds}")

    def set(self, value, **kwargs):
        self.check_value(value)
        self.moves.append(value)
        return super().set(value, **kwargs)


def detector(motor, profile):
    return SynSignal(name="det", func=lambda: float(profile(motor.position)))


@pytest.mark.parametrize("der", [False, True])
@pytest.mark.parametrize("scale", [1, 1000])
@pytest.mark.parametrize("polarity", [-1, 1])
def test_good_height_fit_needs_one_scan(harness, der, scale, polarity):
    motor = Motor(limits=(-1000, 1000))
    det = detector(motor, lambda x: 1000 * (1 + polarity * erf(10 * (x / scale - 0.1))))
    harness.RE(scan_and_center([det], motor, 0.5 * scale, 21, harness.ps, der=der))
    assert len(harness.starts) == 1
    assert motor.position / scale == pytest.approx(0.1, abs=0.04)


@pytest.mark.parametrize("bad_center", [32401249.437869146, -1e8, np.nan, np.inf])
def test_reported_profile_recovers_toward_low_edge(harness, bad_center):
    motor = Motor(value=2)
    measured_y = np.array([
        533707, 239073, 128889, 62809, 33207, 20634, 12459,
        6134, 1712, 421, 123, 23, 7, 7, 9, 4, 7, 8, 0, 6, 6,
    ])
    det = detector(motor, lambda x: np.interp(x, np.linspace(1.5, 2.5, 21), measured_y))
    calls = []

    def stats(**kwargs):
        calls.append(kwargs["uid"])
        if len(calls) == 1:
            # Deliberately contradict the direction indicated by the data.
            stats.x_data = np.linspace(1.5, 2.5, 21)[1:]
            stats.y_data = np.diff(measured_y)
            stats.cen = bad_center
            stats.peak = 2.2
        else:
            stats.x_data = np.linspace(1, 2, 21)[1:]
            stats.y_data = -np.exp(-((stats.x_data - 1.45) / 0.1)**2)
            stats.cen = 1.45
            stats.peak = 1.45
        stats.fit_kind = "step"
        stats.fit_success = True

    harness.RE(scan_and_center([det], motor, 0.5, 21, stats, der=True))
    assert len(calls) == 2
    assert calls == [doc["uid"] for doc in harness.starts]
    assert motor.position == 1.45
    assert min(motor.moves) == 1
    assert max(motor.moves) == 2.5


@pytest.mark.parametrize("side", [-1, 1])
def test_off_scan_peak_is_found_by_rescan(harness, side):
    motor = Motor()
    peak = side * 0.65
    det = detector(motor, lambda x: 1000 * np.exp(-((x - peak) / 0.15)**2))
    harness.RE(scan_and_center([det], motor, 0.5, 21, harness.ps, target="peak"))
    assert len(harness.starts) == 2
    assert motor.position == pytest.approx(peak)


@pytest.mark.parametrize("bad_y", [0, np.nan, np.inf])
def test_unusable_data_stops_without_recentering(harness, bad_y):
    motor = Motor()
    harness.ps.cen = 1e9  # stale result must never be reused
    det = detector(motor, lambda x: bad_y)
    with pytest.raises(RuntimeError, match="No usable alignment feature"):
        harness.RE(scan_and_center([det], motor, 0.5, 21, harness.ps))
    assert len(harness.starts) == 1
    assert motor.position == 0  # rel_scan restored the starting center
    assert np.isnan(harness.ps.cen)


def bad_stats(side=1):
    def stats(**kwargs):
        stats.x_data = np.linspace(-0.5, 0.5, 21)
        stats.y_data = np.exp(side * stats.x_data)
        stats.cen = 1e8
        stats.peak = side * 0.5
        stats.fit_kind = "step"
        stats.fit_success = True
    return stats


def test_retry_budget_stops_runaway_search(harness):
    motor = Motor()
    det = detector(motor, np.exp)
    with pytest.raises(RuntimeError, match="failed after 4 scans"):
        harness.RE(scan_and_center([det], motor, 0.5, 21, bad_stats()))
    assert len(harness.starts) == 4
    assert motor.position == 1.5
    assert max(motor.moves) == 2


def test_rescan_limits_checked_before_recentering(harness):
    motor = Motor(limits=(-0.6, 0.6))
    det = detector(motor, np.exp)
    with pytest.raises(RuntimeError, match="would exceed motor limits"):
        harness.RE(scan_and_center([det], motor, 0.5, 21, bad_stats()))
    assert len(harness.starts) == 1
    assert motor.position == 0
    assert motor.moves[-1] == 0


def test_initial_limits_checked_before_scan(harness):
    motor = Motor(limits=(-0.4, 0.4))
    det = detector(motor, np.exp)
    with pytest.raises(RuntimeError, match="would exceed motor limits"):
        harness.RE(scan_and_center([det], motor, 0.5, 21, harness.ps))
    assert not harness.starts
    assert not motor.moves


def test_zero_retries_still_rejects_bad_fit(harness):
    motor = Motor()
    det = detector(motor, np.exp)
    with pytest.raises(RuntimeError, match="failed after 1 scans"):
        harness.RE(scan_and_center([det], motor, 0.5, 21, bad_stats(), max_retries=0))
    assert len(harness.starts) == 1
    assert motor.position == 0


def test_recovery_does_not_oscillate(harness):
    motor = Motor()
    det = detector(motor, np.exp)
    calls = 0

    def stats(**kwargs):
        nonlocal calls
        calls += 1
        source = bad_stats(side=1 if calls == 1 else -1)
        source(**kwargs)
        stats.__dict__.update(source.__dict__)

    with pytest.raises(RuntimeError, match="already scanned center"):
        harness.RE(scan_and_center([det], motor, 0.5, 21, stats))
    assert len(harness.starts) == 2
    assert motor.position == 0.5


def test_fit_exception_recovers_from_current_profile(harness):
    motor = Motor()
    det = detector(motor, np.exp)
    stats = bad_stats()
    calls = 0

    def failing_stats(**kwargs):
        nonlocal calls
        calls += 1
        stats(**kwargs)
        failing_stats.__dict__.update(stats.__dict__)
        if calls == 1:
            failing_stats.cen = np.nan
            failing_stats.fit_success = False
            raise ValueError("Fit produced NaN")
        failing_stats.x_data = np.linspace(0, 1, 21)
        failing_stats.y_data = np.exp(-((failing_stats.x_data - 0.5) / 0.1)**2)
        failing_stats.cen = failing_stats.peak = 0.5
        failing_stats.fit_kind = "peak"

    harness.RE(scan_and_center([det], motor, 0.5, 21, failing_stats))
    assert calls == 2
    assert motor.position == 0.5
