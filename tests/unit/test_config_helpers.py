"""Unit tests for the Redis-backed-config helpers (smiclasses._config).

These never touch a real Redis: the _context seam returns {} when unconfigured (so reads fall
back to the registered defaults), and a test can inject a plain dict to stand in for ``mdsave``.
"""
import numpy as np
import pytest

from smiclasses import _config, _context


def test_load_returns_registered_default_when_unconfigured():
    # _context is unconfigured (autouse fixture) -> get_config() is {} -> defaults.
    assert _context.get_config() == {}
    assert _config.load("bimorph_hfm_lowdiv_offset_v") == -80
    energies = _config.load("energy_ivu_gap_offset_energies_eV")
    assert energies[0] == 2450 and len(energies) == 16


def test_load_array_returns_numpy():
    arr = _config.load_array("bimorph_hfm_default_v")
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (16,)
    assert arr[0] == -151


def test_load_reads_persisted_value_over_default():
    cfg = {}
    _context.configure(config_dict=cfg)
    cfg["bimorph_hfm_lowdiv_offset_v"] = -50          # a re-calibrated value in "Redis"
    assert _config.load("bimorph_hfm_lowdiv_offset_v") == -50


def test_unknown_key_raises():
    with pytest.raises(KeyError):
        _config.load("not_a_registered_key")


def test_persist_writes_to_config_dict_and_converts_numpy():
    cfg = {}
    _context.configure(config_dict=cfg)
    # numpy array must be stored as a JSON-friendly list (orjson would accept it, but it always
    # reads back as a list, so we normalize on write).
    _config.persist({"bimorph_vfm_default_v": np.asarray([1, 2, 3])})
    assert cfg["bimorph_vfm_default_v"] == [1, 2, 3]
    assert isinstance(cfg["bimorph_vfm_default_v"], list)


def test_persist_rejects_unregistered_key():
    cfg = {}
    _context.configure(config_dict=cfg)
    with pytest.raises(KeyError):
        _config.persist({"bogus_key": 1})


def test_persist_from_signals_roundtrips_through_load():
    """The seed/persist round-trip: persist a Signal's value, then load it back."""
    from ophyd import Signal

    cfg = {}
    _context.configure(config_dict=cfg)

    class _Holder:
        pass

    h = _Holder()
    h.offset = Signal(value=-66, name="offset")
    _config.persist_from_signals(h, {"bimorph_hfm_lowdiv_offset_v": "offset"})
    assert cfg["bimorph_hfm_lowdiv_offset_v"] == -66
    assert _config.load("bimorph_hfm_lowdiv_offset_v") == -66


def test_every_registry_default_is_json_safe():
    """Defaults must be plain JSON types (no numpy) so they round-trip through Redis."""
    import json

    for key, (default, desc) in _config.CONFIG_KEYS.items():
        assert isinstance(desc, str) and desc
        # json.dumps raises on numpy; this guarantees the registered defaults are list/scalar.
        json.dumps(default)
