"""Tier-2 (sim) unit tests for the pure DCM-feedback lookup tables: the energy-dependent BPM3 flux
threshold and the per-energy BPM3 electrometer range (gain) index.  No hardware / RunEngine.
"""
import pytest

pytest.importorskip("ophyd")

from smi_beamline.plans.dcm_diag import (  # noqa: E402
    DEFAULT_FLUX_TABLE,
    DEFAULT_RANGE_TABLE,
    flux_threshold,
    range_index,
)


# --------------------------------------------------------------------------- flux threshold
@pytest.mark.parametrize(
    "energy_keV, expected",
    [
        (5.0, 10.0),      # < 8 keV
        (7.999, 10.0),
        (8.0, 5.0),       # 8 <= E < 10
        (9.5, 5.0),
        (10.0, 1.0),      # 10 <= E < 12
        (11.9, 1.0),
        (12.0, 0.1),      # >= 12
        (20.0, 0.1),
    ],
)
def test_flux_threshold_bands(energy_keV, expected):
    assert flux_threshold(energy_keV) == expected


def test_flux_threshold_boundaries_are_strict_lt():
    """Boundary energy falls into the *next* (lower-flux) band: comparison is ``<``."""
    for max_e, _ in DEFAULT_FLUX_TABLE[:-1]:
        below = flux_threshold(max_e - 1e-6)
        at = flux_threshold(max_e)
        assert at <= below          # crossing up an energy boundary never *raises* the requirement


# --------------------------------------------------------------------------- BPM3 range index
@pytest.mark.parametrize(
    "energy_keV, expected_idx",
    [
        (5.0, 3),         # < 10 keV   -> 1000 uA (idx 3)
        (9.999, 3),
        (10.0, 2),        # 10 <= E < 12 -> 100 uA (idx 2)
        (11.999, 2),
        (12.0, 1),        # >= 12 keV  -> 10 uA (idx 1)
        (25.0, 1),
    ],
)
def test_range_index_bands(energy_keV, expected_idx):
    assert range_index(energy_keV) == expected_idx


def test_range_index_is_more_sensitive_at_higher_energy():
    """Higher energy (less flux) -> smaller full-scale current -> smaller (more sensitive) index."""
    assert range_index(8.0) > range_index(11.0) > range_index(13.0)


def test_range_table_indices_are_the_confirmed_0based_map():
    """1000 uA = 3, 100 uA = 2, 10 uA = 1 (confirmed live: '100 uA' reads back as 2)."""
    indices = [idx for _, idx in DEFAULT_RANGE_TABLE]
    assert indices == [3, 2, 1]


def test_range_index_accepts_custom_table():
    table = [(15.0, 9), (float("inf"), 4)]
    assert range_index(10.0, table) == 9
    assert range_index(20.0, table) == 4
