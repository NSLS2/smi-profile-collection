import math

import pytest

from smi_beamline.devices.crl_optics import (
    COMBINATIONS, DEFAULT_HOLDERS, CRLGeometry, CRLModel, NoFocusSolution, diamond_delta,
)


def test_inventory_and_enumeration():
    assert len(COMBINATIONS) == 255
    assert sum(h.count for h in DEFAULT_HOLDERS) == 41
    assert {n for c in COMBINATIONS for n in c.holders} == {1, 2, 3, 4, 5, 9, 10, 11}
    assert [h.out_mm for h in DEFAULT_HOLDERS] == [10] * 6 + [-10] * 6


def test_physics_scale_and_additive_power():
    model = CRLModel()
    # Independent order-of-magnitude reference: diamond delta ~7.3e-6 at 10 keV.
    assert diamond_delta(10) == pytest.approx(7.3e-6, rel=0.01)
    assert model.focal_length_mm(10, [1]) == pytest.approx(3425, rel=0.01)
    assert model.focal_length_mm(20, [1]) == pytest.approx(4 * model.focal_length_mm(10, [1]))
    assert 1 / model.focal_length_mm(10, [1, 9]) == pytest.approx(
        1 / model.focal_length_mm(10, [1]) + 1 / model.focal_length_mm(10, [9]))


@pytest.mark.parametrize("curvature", [0, -0.1, 0.1, 3])
def test_conjugate_equation_and_ranking(curvature):
    g = CRLGeometry(incident_curvature_per_m=curvature)
    model = CRLModel(g)
    for energy in (2.1, 3, 5, 8, 12, 16, 24):
        candidates = model.candidates(energy)
        ranks = [(len(s.holders), s.element_count, s.holders) for s in candidates]
        assert ranks == sorted(ranks)
        for s in candidates:
            c_at_z = curvature / (1 + curvature * s.z_mm / 1000)
            assert 1000 / s.image_distance_mm == pytest.approx(
                1000 / s.focal_length_mm - c_at_z, abs=1e-10)
            assert s.image_distance_mm + s.z_mm == pytest.approx(615)
            assert -50 <= s.z_mm <= 250


def test_selection_bands_boundaries_and_gaps():
    model = CRLModel()
    bands = model.selection_bands()
    assert bands[0].energy_min_keV == 2.1
    assert bands[-1].energy_max_keV == 24
    for band in bands:
        mid = (band.energy_min_keV + band.energy_max_keV) / 2
        if band.holders is None:
            with pytest.raises(NoFocusSolution):
                model.recommend(mid)
        else:
            assert model.recommend(mid).holders == band.holders
            for e in (band.energy_min_keV, band.energy_max_keV):
                assert band.holders in [s.holders for s in model.candidates(e)]
    for left, right in zip(bands, bands[1:]):
        assert left.energy_max_keV == right.energy_min_keV


def test_exact_travel_limits_and_unreachable():
    model = CRLModel()
    g = model.geometry
    combo = next(c for c in COMBINATIONS if c.holders == (2,))
    low, high = model.combination_energy_range(combo)
    for energy, z in ((low, g.z_max_mm), (high, g.z_min_mm)):
        solution = next(s for s in model.candidates(energy) if s.holders == (2,))
        assert solution.z_mm == pytest.approx(z)
    impossible = CRLModel(CRLGeometry(sample_distance_mm=1, z_min_mm=-0.1, z_max_mm=0.1))
    with pytest.raises(NoFocusSolution):
        impossible.recommend(24)


@pytest.mark.parametrize("energy", [0, 2, 25, float("nan"), float("inf"), 10000])
def test_invalid_energy(energy):
    with pytest.raises(ValueError):
        CRLModel().recommend(energy)


@pytest.mark.parametrize("holders", [[], [6], [12], [1, 1], [0], [1, 13]])
def test_invalid_holder_selection(holders):
    with pytest.raises(ValueError):
        CRLModel().focal_length_mm(10, holders)


@pytest.mark.parametrize("kwargs", [
    {"z_min_mm": 250}, {"sample_distance_mm": 200},
    {"incident_curvature_per_m": -4}, {"z_max_mm": math.nan},
])
def test_invalid_geometry(kwargs):
    with pytest.raises(ValueError):
        CRLGeometry(**kwargs)


def test_density_validation_and_scaling():
    with pytest.raises(ValueError):
        CRLModel(density_g_cm3=-1)
    assert CRLModel(density_g_cm3=3.515 / 2).focal_length_mm(10, [1]) == pytest.approx(
        2 * CRLModel().focal_length_mm(10, [1]))
