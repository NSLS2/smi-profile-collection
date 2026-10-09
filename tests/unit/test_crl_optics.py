import math

import pytest

from smi_beamline.devices.crl_optics import (
    COMBINATIONS, DEFAULT_HOLDERS, MEASURED_SAMPLE_DISTANCE_AT_Z0_MM,
    CRLGeometry, CRLModel, NoFocusSolution, beryllium_delta, diamond_delta,
    material_delta,
)


def test_inventory_and_enumeration():
    assert len(COMBINATIONS) == 255
    assert sum(h.count for h in DEFAULT_HOLDERS) == 41
    assert {n for c in COMBINATIONS for n in c.holders} == {1, 2, 3, 4, 5, 9, 10, 11}
    assert [h.out_mm for h in DEFAULT_HOLDERS] == [10] * 6 + [-10] * 6
    assert {h.number: h.material for h in DEFAULT_HOLDERS if h.count} == {
        1: "Be", 2: "Be", 3: "Be", 4: "Be", 5: "Be", 9: "Be",
        10: "Be", 11: "Be",
    }


def test_physics_scale_and_additive_power():
    model = CRLModel()
    # Independent order-of-magnitude references at 10 keV.
    assert beryllium_delta(10) == pytest.approx(3.4e-6, rel=0.01)
    assert diamond_delta(10) == pytest.approx(7.3e-6, rel=0.01)
    assert model.focal_length_mm(10, [1]) == pytest.approx(7340, rel=0.01)
    assert model.focal_length_mm(10, [9]) == pytest.approx(29370, rel=0.01)
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
            assert s.image_distance_mm + s.z_mm == pytest.approx(
                MEASURED_SAMPLE_DISTANCE_AT_Z0_MM)
            assert -300 <= s.z_mm <= 300


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


def test_selection_prioritizes_fewest_holders_over_z_margin():
    model = CRLModel()
    combo = next(c for c in COMBINATIONS if c.holders == (3,))
    energy = model.combination_energy_range(combo)[1]
    candidates = model.candidates(energy)
    recommended = candidates[0]
    centered = next(s for s in candidates if s.holders == (3, 5, 9, 11))
    assert recommended.holders == (3,)
    assert recommended.z_mm == pytest.approx(-300)
    assert recommended.z_margin_mm == pytest.approx(0, abs=1e-8)
    assert centered.z_margin_mm > 280
    assert len(recommended.holders) < len(centered.holders)
    assert model.recommend(energy) == recommended


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


def test_ssa_holder3_focus():
    solution = CRLModel().recommend(16.1)
    assert solution.holders == (3,)
    assert solution.z_mm == pytest.approx(262.91230292711367)
    p = 10.5 + solution.z_mm / 1000
    q = (1600 - solution.z_mm) / 1000
    assert 1 / p + 1 / q == pytest.approx(1000 / solution.focal_length_mm)


@pytest.mark.parametrize("z, p, q", [(-300, 10.2, 1.9), (0, 10.5, 1.6), (300, 10.8, 1.3)])
def test_ssa_source_and_sample_distances(z, p, q):
    geometry = CRLGeometry()
    assert geometry.required_power_per_m(z) == pytest.approx(1 / p + 1 / q)
    assert geometry.focus_positions_mm(1 / p + 1 / q) == pytest.approx((z,))


def test_collimated_override():
    model = CRLModel(CRLGeometry(incident_curvature_per_m=0))
    assert model.recommend(16.1).holders == (2, 4)
    assert all(s.holders != (3,) for s in model.candidates(16.1))


@pytest.mark.parametrize("energy", [0, 2, 25, float("nan"), float("inf"), 10000])
def test_invalid_energy(energy):
    with pytest.raises(ValueError):
        CRLModel().recommend(energy)


@pytest.mark.parametrize("holders", [[], [6], [12], [1, 1], [0], [1, 13]])
def test_invalid_holder_selection(holders):
    with pytest.raises(ValueError):
        CRLModel().focal_length_mm(10, holders)


@pytest.mark.parametrize("kwargs", [
    {"z_min_mm": 300}, {"sample_distance_mm": 200},
    {"incident_curvature_per_m": -4}, {"z_max_mm": math.nan},
])
def test_invalid_geometry(kwargs):
    with pytest.raises(ValueError):
        CRLGeometry(**kwargs)


def test_material_validation_and_density_scaling():
    with pytest.raises(ValueError):
        beryllium_delta(10, density_g_cm3=-1)
    with pytest.raises(ValueError):
        material_delta(10, "glass")
    assert beryllium_delta(10, density_g_cm3=1.848 / 2) == pytest.approx(
        beryllium_delta(10) / 2)
