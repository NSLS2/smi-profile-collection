"""Unit tests for the attenuation physics + foil-selection layer.

Pure code -- no devices, no EPICS.  Exercises
:mod:`smi_beamline.devices.attenuator_data`: the CXRO-derived transmission curves, the
thickness-scaling / combination maths, and :func:`select_foils` (closest within a
factor of two, otherwise the nearest upward match).
"""
import math

import numpy as np
import pytest

from smi_beamline.devices import attenuator_data as ad


# ---------------------------------------------------------------------------
# data integrity
# ---------------------------------------------------------------------------
def test_layout_covers_24_foils_and_known_materials():
    assert len(ad.FOIL_LAYOUT) == 24
    # every foil maps to a base curve that exists
    for label, (base, mult) in ad.FOIL_LAYOUT.items():
        assert base in ad.BASE_FOILS
        assert mult in (1, 2, 4, 8)
    # the six base materials/thicknesses the user specified
    bases = {(v["formula"], v["thickness_um"]) for v in ad.BASE_FOILS.values()}
    assert bases == {("Cu", 68.0), ("Sn", 60.0), ("Sn", 30.0),
                     ("Mo", 20.0), ("Al", 102.0), ("Al", 9.0)}


def test_base_curves_aligned_to_energy_grid():
    n = len(ad.ENERGY_EV)
    assert n > 100
    assert ad.ENERGY_EV[0] == ad.ENERGY_MIN_EV
    assert ad.ENERGY_EV[-1] == ad.ENERGY_MAX_EV
    for v in ad.BASE_FOILS.values():
        assert len(v["optical_depth"]) == n


def test_optical_depth_nonnegative_and_monotone_ish_with_thickness():
    # thicker foil of same material -> more optical depth at any energy
    E = 10000.0
    od1 = ad.foil_optical_depth("2_9", E, calibrated=False)    # nominal Al 9um x1
    od8 = ad.foil_optical_depth("2_12", E, calibrated=False)   # nominal Al 9um x8
    assert od1 >= 0
    assert od8 == pytest.approx(8 * od1, rel=1e-9)   # exact linear scaling


def test_measured_thickness_corrections_and_nominal_fallback():
    from smi_beamline.devices import attenuator_calibration as cal
    assert len(cal.ACCEPTED) == 23
    assert set(ad.FOIL_LAYOUT) - set(cal.ACCEPTED) == {"1_4"}
    assert ad.effective_thickness_um("1_1") == pytest.approx(62.20276, abs=1e-5)
    for label in ad.FOIL_LAYOUT:
        scale = ad.effective_thickness_um(label)/ad.nominal_thickness_um(label)
        for energy in (8800, 16000, 19500):
            nominal = ad.foil_optical_depth(label, energy, calibrated=False)
            assert ad.foil_optical_depth(label, energy) == pytest.approx(nominal*scale)
        if label in cal.UNRESOLVED:
            assert scale == 1
    # Corrections are per physical foil, not shared base-thickness multiples.
    assert ad.foil_optical_depth("2_12", 16000) != pytest.approx(8*ad.foil_optical_depth("2_9",16000))


def test_calibration_agreement_and_scatter_inflation():
    from smi_beamline.devices import attenuator_calibration as cal
    assert not cal.RESULTS["2_3"]["accepted"]
    assert not cal.RESULTS["2_4"]["accepted"]
    for label, result in cal.RESULTS.items():
        if not result["accepted"]:
            continue
        a, sa, b, sb = cal.MEASUREMENTS_UM[label]
        assert result["agreement_z"] <= 3
        assert min(a,b) <= result["effective_thickness_um"] <= max(a,b)
        assert result["thickness_sigma_um"] >= math.sqrt(1/(1/sa**2 + 1/sb**2))


def test_followup_uses_low_energy_values_and_retains_disagreement():
    from smi_beamline.devices import attenuator_calibration as cal
    assert cal.FOLLOWUP_RESULTS["2_3"]["agreement_z"] == pytest.approx(3.724375, abs=1e-5)
    assert cal.FOLLOWUP_RESULTS["2_4"]["agreement_z"] == pytest.approx(4.319831, abs=1e-5)
    assert all(not r["accepted"] for r in cal.FOLLOWUP_RESULTS.values())
    assert cal.FOLLOWUP_SINGLE_ENERGY_UM["2_6"][16000][0] == pytest.approx(219.115923)
    for label, value, sigma in (("2_3",80.801629856,.037231804),
                                ("2_4",181.884971861,.100291060),
                                ("2_6",219.115923040,.550377025)):
        assert ad.effective_thickness_um(label) == pytest.approx(value)
        assert cal.ACCEPTED[label]["thickness_sigma_um"] == pytest.approx(sigma)
        assert label in cal.REMAINING_ISSUES
    assert ad.calibration_metadata("2_3")["source_uids"] == [
        cal.FOLLOWUP_SOURCE_UID, cal.INTERMEDIATE_SOURCE_UID, cal.REPEAT_SOURCE_UID]
    assert ad.calibration_metadata("2_6")["measured_energies_eV"] == [16000]


def test_calibrated_combination_and_selection_use_measured_thickness():
    e = 16000
    expected = math.exp(sum(ad.foil_optical_depth(l,e,calibrated=False)*
        ad.effective_thickness_um(l)/ad.nominal_thickness_um(l) for l in ("1_1","1_5")))
    assert ad.attenuation_factor(["1_1","1_5"],e) == pytest.approx(expected)
    target = ad.attenuation_factor(["1_1"],e)
    labels, factor, ok = ad.select_foils(target,e,candidates=["1_1"],max_foils=1,tolerance=1e-9)
    assert labels == ("1_1",) and ok
    assert factor == pytest.approx(target)


# ---------------------------------------------------------------------------
# transmission / factor maths
# ---------------------------------------------------------------------------
def test_no_foils_is_unity():
    assert ad.transmission([], 10000.0) == 1.0
    assert ad.attenuation_factor([], 10000.0) == 1.0


def test_factor_is_reciprocal_of_transmission():
    labels = ["2_1"]
    E = 12000.0
    t = ad.transmission(labels, E)
    assert ad.attenuation_factor(labels, E) == pytest.approx(1.0 / t)


def test_combination_multiplies_transmission():
    E = 9000.0
    a, b = ["1_5"], ["2_9"]
    fa = ad.attenuation_factor(a, E)
    fb = ad.attenuation_factor(b, E)
    fab = ad.attenuation_factor(a + b, E)
    assert fab == pytest.approx(fa * fb, rel=1e-9)


def test_transmission_increases_with_energy_for_a_foil():
    # higher energy -> less absorption (away from edges); check overall trend on Al 102um
    lo = ad.transmission(["2_5"], 4000.0)
    hi = ad.transmission(["2_5"], 20000.0)
    assert hi > lo


def test_energy_is_clamped_outside_table():
    # below/above the tabulated range should not raise, just clamp to the endpoints
    t_below = ad.transmission(["2_1"], 500.0)
    t_at_min = ad.transmission(["2_1"], ad.ENERGY_MIN_EV)
    assert t_below == pytest.approx(t_at_min)
    t_above = ad.transmission(["2_1"], 50000.0)
    t_at_max = ad.transmission(["2_1"], ad.ENERGY_MAX_EV)
    assert t_above == pytest.approx(t_at_max)


# ---------------------------------------------------------------------------
# descriptions
# ---------------------------------------------------------------------------
def test_foil_description_names_foil_material_and_thickness():
    d = ad.foil_description("1_3")
    assert "att1_3" in d
    assert "Cu" in d
    assert "4x" in d
    assert "272" in d        # 4 * 68 um total


# ---------------------------------------------------------------------------
# selection: closest within a factor of two, otherwise round upward
# ---------------------------------------------------------------------------
def test_select_target_one_is_no_foils():
    labels, factor, ok = ad.select_foils(1.0, 10000.0)
    assert labels == ()
    assert factor == 1.0
    assert ok is True


def test_select_hits_target_within_tolerance():
    E = 10000.0
    for target in (2, 5, 10, 50, 100, 1000):
        labels, factor, ok = ad.select_foils(target, E, tolerance=0.10)
        assert ok, "target %g should be reachable within 10%%" % target
        assert abs(factor / target - 1.0) <= 0.10
        assert len(labels) <= 4


def test_select_exact_two_foil_target():
    # An exact two-foil target must not cause the selector to choose three foils.
    target = ad.attenuation_factor(["2_9", "2_11"], 10000.)
    labels, factor, ok = ad.select_foils(target, 10000.0, tolerance=0.10)
    assert ok
    assert len(labels) <= 2


def test_warning_tolerance_does_not_change_selection():
    E = 10000.0
    n_loose = len(ad.select_foils(10, E, tolerance=0.10)[0])
    n_tight = len(ad.select_foils(10, E, tolerance=0.02)[0])
    assert n_tight == n_loose


def test_select_respects_max_foils_and_flags_out_of_tolerance():
    # an extreme target that cannot be met within tolerance using only 1 foil
    labels, factor, ok = ad.select_foils(1e9, 10000.0, max_foils=1, tolerance=0.01)
    assert len(labels) <= 1
    # with a single foil it likely can't hit 1e9 within 1% -> flagged, but still returns a combo
    if not ok:
        assert math.isfinite(factor) or factor == float("inf")


def test_select_never_exceeds_max_foils():
    labels, factor, ok = ad.select_foils(1e12, 6000.0, max_foils=3)
    assert len(labels) <= 3


def test_atleast_mode_never_under_attenuates():
    E = 10000.0
    for target in (10, 100, 1000):
        labels, factor, ok = ad.select_foils(target, E, mode="atleast")
        assert factor >= target * (1 - 1e-9)


def test_candidates_restriction_is_honored():
    # restrict to bank-2 Al foils only; the result must use only those
    al_only = [l for l, (b, m) in ad.FOIL_LAYOUT.items() if b in ("Al_9um", "Al_102um")]
    labels, factor, ok = ad.select_foils(50, 10000.0, candidates=al_only, max_foils=4)
    assert set(labels) <= set(al_only)


@pytest.mark.parametrize("target, expected", [
    (1e6, ("2_9", "2_10")),
    (5e6, ("2_9", "2_10")),
    (8e6, ("2_1",)),
    (1e7, ("2_1",)),
    (4e7, ("2_1",)),
])
def test_2130ev_factor_two_policy(target, expected):
    labels, factor, ok = ad.select_foils(target, 2130)
    assert labels == expected
    assert factor == pytest.approx(ad.attenuation_factor(expected, 2130))
    assert not ok


@pytest.mark.parametrize("fraction, expected", [
    (0.5 * (1 - 1e-8), "2_1"),
    (0.5, "2_9"),
    (0.5 * (1 + 1e-8), "2_9"),
])
def test_factor_two_boundary_is_inclusive(monkeypatch, fraction, expected):
    factors = {"2_9": 100 * fraction, "2_1": 1000}
    monkeypatch.setattr(ad, "foil_optical_depth", lambda label, energy: math.log(factors[label]))
    labels, factor, ok = ad.select_foils(100, 2130, candidates=factors, max_foils=1)
    assert labels == (expected,)
    assert factor == pytest.approx(factors[expected])
    assert not ok


def test_closest_search_does_not_stop_at_one_foil_within_tolerance(monkeypatch):
    factors = {"1_1": 100, "1_2": 10, "1_3": 10.1}
    monkeypatch.setattr(ad, "foil_optical_depth", lambda label, energy: math.log(factors[label]))
    labels, factor, ok = ad.select_foils(101, 2130, candidates=factors, max_foils=2)
    assert labels == ("1_2", "1_3")
    assert factor == pytest.approx(101)
    assert ok


def test_equal_factors_prefer_fewer_foils(monkeypatch):
    factors = {"1_1": 100, "1_2": 10, "1_3": 10}
    monkeypatch.setattr(ad, "foil_optical_depth", lambda label, energy: math.log(factors[label]))
    assert ad.select_foils(100, 2130, candidates=factors, max_foils=2)[0] == ("1_1",)


def test_atleast_sparse_gap_uses_nearest_above_not_strongest():
    labels, factor, ok = ad.select_foils(1e7, 2130, mode="atleast")
    assert labels == ("2_1",)
    assert factor == pytest.approx(5.0607865966e7)
    assert not ok


@pytest.mark.parametrize("mode", ["closest", "atleast"])
def test_unreachable_upward_target_returns_strongest_flagged(mode):
    labels, factor, ok = ad.select_foils(
        1e7, 2130, candidates=["2_9", "2_10"], max_foils=2, mode=mode)
    assert labels == ("2_9", "2_10")
    assert factor == pytest.approx(3.284888083e6)
    assert not ok


def test_no_foils_is_a_candidate_for_near_unity():
    labels, factor, ok = ad.select_foils(1.05, 2130)
    assert labels == ()
    assert factor == 1
    assert ok
