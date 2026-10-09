"""Real energy transforms and RunEngine plans, with entirely in-memory motors."""
import numpy as np
import pytest
from bluesky import RunEngine
import bluesky.plan_stubs as bps
import bluesky.plans as bp
from bluesky.utils import RunEngineInterrupted
from ophyd import Component as Cpt, Signal, SoftPositioner
from ophyd.sim import SynSignal

from smi_beamline.devices.energy import Energy
from smi_beamline.plans.harmonic_lock import with_harmonic_lock
from smi_beamline.plans.energy_walk import energy_walk
from smi_beamline.plans.energy_move_preprocessor import install_energy_move_preprocessor
from _fakes import FakeDiag


class SimEnergy(Energy):
    bragg = Cpt(SoftPositioner, init_pos=12.7)
    dcmgap = Cpt(SoftPositioner, init_pos=12.8)
    ivugap = Cpt(SoftPositioner, init_pos=7400)
    pitch_feedback_disabled = Cpt(Signal, value="0")
    roll_feedback_disabled = Cpt(Signal, value="0")


@pytest.fixture
def en():
    return SimEnergy("", name="energy")


def test_range_selection_and_no_side_effects(en):
    before = (en.position, en.target_harmonic.get(), en.harmonic.get(), en.locked_harmonic.get())
    h = en.harmonic_for_range(8000, 9000)
    assert h == en.harmonic_for_range(9000, 8000)
    assert (en.position, en.target_harmonic.get(), en.harmonic.get(), en.locked_harmonic.get()) == before
    gaps = [en.energy_to_gap(e, h) for e in np.linspace(8000, 9000, 1001)]
    assert min(gaps) >= 6200 and max(gaps) < 15100
    for higher in range(h + 2, 22, 2):
        with pytest.raises(RuntimeError, match="No single harmonic"):
            en.harmonic_for_range(8000, 9000, harmonic=higher)
    assert en.harmonic_for_range(8000, 8000) == en._harmonic_and_gap(8000)[0]
    with pytest.raises(RuntimeError, match="No single harmonic"):
        en.harmonic_for_range(2100, 24000)


@pytest.mark.parametrize("kwargs", [
    {"start": np.nan}, {"stop": np.inf}, {"start": 2050}, {"stop": 24001},
    {"max_harmonic": 2}, {"max_harmonic": -1}, {"harmonic": 3.5},
    {"gap_margin_um": -1}, {"gap_margin_um": np.nan}, {"gap_margin_um": 4450},
    {"harmonic": 3, "max_harmonic": 7},
])
def test_bad_range_inputs(en, kwargs):
    args = dict(start=8000, stop=9000)
    args.update(kwargs)
    with pytest.raises(ValueError):
        en.harmonic_for_range(**args)


def test_search_ceiling_margin_and_existing_lock(en):
    en.target_harmonic.put(3)
    en.locked_harmonic.put(1)
    h = en.harmonic_for_range(8000, 9000)
    assert h <= 3
    assert en.harmonic_for_range(8000, 9000, max_harmonic=21) >= h
    h = en.harmonic_for_range(8000, 9000, max_harmonic=21, gap_margin_um=100)
    for e in np.linspace(8000, 9000, 101):
        assert 6300 <= en.energy_to_gap(e, h) < 15000


def test_offset_knot_excursion_rejected(en):
    h = en.harmonic_for_range(8000, 9000)
    en.ivu_gap_offset_energies_eV.put([8000, 8500, 9000])
    en.ivu_gap_offset_values_um.put([0, 20000, 0])
    assert all(6200 <= en.energy_to_gap(e, h) < 15100 for e in (8000, 9000))
    with pytest.raises(RuntimeError):
        en.harmonic_for_range(8000, 9000, harmonic=h)


def test_interior_extremum_between_offset_knots(en):
    # Subtract a chord of the nonlinear fit: both endpoints equal 6201 um,
    # but the convex fit dips below the lower gap limit in the interior.
    a, b, h = 8000, 12000, 3
    en.ivu_gap_offset_energies_eV.put([a, b])
    en.ivu_gap_offset_values_um.put([en._ideal_gap_um(e, h) - 6201 for e in (a, b)])
    assert en.energy_to_gap(a, h) == pytest.approx(6201)
    assert en.energy_to_gap(b, h) == pytest.approx(6201)
    assert en.energy_to_gap((a + b) / 2, h) < 6200
    with pytest.raises(RuntimeError):
        en.harmonic_for_range(a, b, harmonic=h)


def test_low_energy_branch_and_table_edge_discontinuity(en):
    en.ivu_gap_offset_energies_eV.put([3000, 4000])
    en.ivu_gap_offset_values_um.put([20000, 0])
    with pytest.raises(RuntimeError):
        en.harmonic_for_range(2900, 3100, harmonic=1)
    # At the table's final knot offset is -10000, immediately above it right=max is 0.
    # Build endpoints in range while the left-hand limit at the knot is not.
    en.ivu_gap_offset_energies_eV.put([8000, 8500])
    en.ivu_gap_offset_values_um.put([0, -10000])
    h = 3
    with pytest.raises(RuntimeError):
        en.harmonic_for_range(8000, 9000, harmonic=h)


@pytest.mark.parametrize("offsets, energies", [([0], [9000, 8000]), ([0, 1], [9000, 8000]),
                                             ([0, np.nan], [8000, 9000])])
def test_bad_offset_table(en, offsets, energies):
    en.ivu_gap_offset_energies_eV.put(energies)
    en.ivu_gap_offset_values_um.put(offsets)
    with pytest.raises(ValueError, match="offset table"):
        en.harmonic_for_range(8000, 9000)


def test_locked_moves_and_same_energy_harmonic_change(en):
    en.move(9000)
    auto_h = en.harmonic.get()
    lower = en.harmonic_for_range(9000, 9000, max_harmonic=auto_h - 2)
    old_gap = en.ivugap.position
    en.locked_harmonic.put(lower)
    # forward/check_value calls must not advertise an unexecuted harmonic change.
    en.forward(9000)
    assert en.harmonic.get() == auto_h
    en.move(9000)
    assert en.harmonic.get() == lower
    assert en.ivugap.position == pytest.approx(en.energy_to_gap(9000, lower))
    assert en.ivugap.position != old_gap
    en.move(9100)
    assert en.harmonic.get() == lower
    en.locked_harmonic.put(0)
    en.move(9100)
    assert en.harmonic.get() == en._harmonic_and_gap(9100)[0]


@pytest.mark.parametrize("lock", [21, 2, -1, 3.5, np.nan])
def test_invalid_lock_rejected_before_feedback_or_motion(en, lock):
    en.move(9000)
    before = en.real_position
    h = en.harmonic.get()
    changes = []
    en.pitch_feedback_disabled.subscribe(lambda **kw: changes.append(kw), run=False)
    en.locked_harmonic.put(lock)
    with pytest.raises((ValueError, RuntimeError)):
        en.move(9000)
    assert not changes
    assert en.real_position == before
    assert en.harmonic.get() == h


def test_lock_requires_ivu_and_small_move_requires_established_harmonic(en):
    en.move(9000)
    en.locked_harmonic.put(3)
    with pytest.raises(RuntimeError, match="Establish"):
        list(en.small_move(9010))
    en.enableivu.put(False)
    with pytest.raises(RuntimeError, match="enableivu"):
        en.move(9010)


def test_scan_wrapper_approach_metadata_and_restore(en):
    en.move(2100)  # chosen scan harmonic cannot cover the approach from here
    engine = RunEngine({})
    det = SynSignal(func=lambda: 1, name="det")
    docs, moves, harmonics = [], [], []
    engine.subscribe(lambda name, doc: docs.append((name, doc)))
    en.ivugap.subscribe(lambda value, **kw: moves.append(value), run=False)
    en.harmonic.subscribe(lambda value, **kw: harmonics.append(value), run=False)
    selected = en.harmonic_for_range(8000, 9000)
    engine(with_harmonic_lock(bp.scan([det, en], en, 8000, 9000, 5),
                              8000, 9000, energy=en))
    assert en.locked_harmonic.get() == 0
    assert en.position.energy == pytest.approx(9000)
    start = next(doc for name, doc in docs if name == "start")
    assert start["harmonic_lock"] == dict(harmonic=selected, start_eV=8000,
                                         stop_eV=9000, gap_margin_um=0)
    events = [doc for name, doc in docs if name == "event"]
    assert len(events) == 5
    assert {doc["data"]["energy_harmonic"] for doc in events} == {selected}
    assert moves and harmonics


def test_wrapper_failure_restores_previous_lock(en):
    en.locked_harmonic.put(3)
    en.move(8000)
    def failing():
        yield from bps.mv(en, 8500)
        raise RuntimeError("acquisition failed")
    with pytest.raises(RuntimeError, match="acquisition failed"):
        RunEngine({})(with_harmonic_lock(failing(), 8000, 9000, energy=en))
    assert en.locked_harmonic.get() == 3


def test_wrapper_abort_restores_lock(en):
    engine = RunEngine({})
    def pausing():
        yield from bps.pause()
    with pytest.raises(RunEngineInterrupted):
        engine(with_harmonic_lock(pausing(), 8000, 9000, energy=en))
    assert en.locked_harmonic.get() != 0
    engine.abort()
    assert en.locked_harmonic.get() == 0


def test_invalid_range_wrapper_does_not_move(en):
    before = en.real_position
    def unused():
        yield from bps.null()
    with pytest.raises(RuntimeError, match="No single harmonic"):
        RunEngine({})(with_harmonic_lock(unused(), 2100, 24000, energy=en))
    assert en.real_position == before


def test_wrapper_returns_result_and_nested_lock(en):
    engine = RunEngine({}, call_returns_result=True)
    def inner():
        assert en.locked_harmonic.get() == 3
        yield from bps.null()
        return "result"
    def outer():
        previous = en.locked_harmonic.get()
        result = yield from with_harmonic_lock(inner(), 8200, 8500, energy=en, harmonic=3)
        assert en.locked_harmonic.get() == previous
        return result
    result = engine(with_harmonic_lock(outer(), 8000, 9000, energy=en))
    assert result.plan_result == "result"
    assert en.locked_harmonic.get() == 0


def test_exact_gap_boundaries(en, monkeypatch):
    en.ivu_gap_offset_energies_eV.put([8000, 9000])
    en.ivu_gap_offset_values_um.put([0, 0])
    monkeypatch.setattr(en, "_ideal_gap_um", lambda e, h: 6200.0)
    assert en.harmonic_for_range(8000, 9000, harmonic=3) == 3
    with pytest.raises(RuntimeError):
        en.harmonic_for_range(8000, 9000, harmonic=3, gap_margin_um=1)
    monkeypatch.setattr(en, "_ideal_gap_um", lambda e, h: 15100.0)
    with pytest.raises(RuntimeError):
        en.harmonic_for_range(8000, 9000, harmonic=3)


def test_managed_scan_preserves_lock_at_intermediate_steps(en):
    en.move(8000)
    engine = RunEngine({})
    diag = FakeDiag(en)
    install_energy_move_preprocessor(
        engine, en, diag=diag, verbose=False, check_drift=False,
        walk_kwargs=dict(diag=diag, oval_settle_s=0, set_bpm3_range=False))
    observed = []
    selected = en.harmonic_for_range(8000, 10000)
    def scan():
        yield from bps.mv(en, 10000)
        observed.append(en.harmonic.get())
    en.harmonic.subscribe(lambda value, **kw: observed.append(value), run=False)
    with pytest.warns(UserWarning, match="managed move"):
        engine(with_harmonic_lock(scan(), 8000, 10000, energy=en, harmonic=selected))
    assert set(observed) == {selected}
    assert en.position.energy == pytest.approx(10000)
    assert en.locked_harmonic.get() == 0


def test_managed_invalid_locked_path_does_not_partially_move(en):
    en.move(8000)
    en.locked_harmonic.put(en.harmonic.get())
    before = en.real_position
    diag = FakeDiag(en)
    with pytest.raises(RuntimeError, match="No single harmonic"):
        RunEngine({})(energy_walk(2100, energy=en, diag=diag, verbose=False))
    assert en.real_position == before


def test_managed_same_energy_establishes_harmonic(en):
    en.move(9000)
    en.locked_harmonic.put(3)
    RunEngine({})(energy_walk(9000, energy=en, diag=FakeDiag(en), verbose=False,
                              oval_settle_s=0, set_bpm3_range=False))
    assert en.harmonic.get() == 3
    assert en.ivugap.position == pytest.approx(en.energy_to_gap(9000, 3))


def test_wrapper_approach_respects_existing_lock(en):
    en.move(2100)
    en.locked_harmonic.put(1)
    before = en.real_position
    def unused():
        yield from bps.null()
    with pytest.raises(RuntimeError, match="Locked harmonic"):
        RunEngine({})(with_harmonic_lock(unused(), 24000, 24000, energy=en))
    assert en.real_position == before
    assert en.locked_harmonic.get() == 1
