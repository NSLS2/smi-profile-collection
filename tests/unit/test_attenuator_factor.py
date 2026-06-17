"""Unit tests for the attenuation physics + foil-selection layer.

Pure code -- no devices, no EPICS.  Exercises
:mod:`smi_beamline.devices.attenuator_data`: the CXRO-derived transmission curves, the
thickness-scaling / combination maths, and :func:`select_foils` (the "fewest foils within
tolerance" auto-selector).
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
    od1 = ad.foil_optical_depth("2_9", E)    # Al 9um x1
    od8 = ad.foil_optical_depth("2_12", E)   # Al 9um x8
    assert od1 >= 0
    assert od8 == pytest.approx(8 * od1, rel=1e-9)   # exact linear scaling


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
# selection: fewest foils within tolerance
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


def test_select_prefers_fewer_foils():
    # at 10 keV a 2-foil combo lands within 10% of 10x; the selector must NOT use 3 foils.
    labels, factor, ok = ad.select_foils(10, 10000.0, tolerance=0.10)
    assert ok
    assert len(labels) <= 2


def test_tighter_tolerance_may_use_more_foils():
    E = 10000.0
    n_loose = len(ad.select_foils(10, E, tolerance=0.10)[0])
    n_tight = len(ad.select_foils(10, E, tolerance=0.02)[0])
    assert n_tight >= n_loose


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
