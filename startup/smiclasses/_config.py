"""
smiclasses._config
==================

Lightweight helpers for the **Redis-backed persistent-config dict** (``mdsave``), reached through
:mod:`smiclasses._context` so device classes stay import-clean (no ``smibase`` import).

Design notes / what this is NOT
-------------------------------
* This does **not** touch Redis itself.  It only reads/writes the existing ``mdsave``
  (``RedisJSONDict``) that the profile already stands up in ``smibase.base``, and trusts it to
  persist.  Off the beamline (tests / bare import) ``_context.get_config()`` returns an empty
  ``{}`` and every read falls back to the registered default, so nothing here needs a live Redis.

* **Storage format is JSON** (``redis_json_dict`` uses ``orjson``).  Practical consequence:
  sequences are stored as JSON arrays and **always read back as plain ``list``** (even if a numpy
  array was written).  So calibration tables are kept as lists in Redis and converted with
  ``np.asarray`` at the point of use.  Use :func:`load_array` for those.

The pattern this generalizes is the one the Pilatus already uses by hand
(``Cpt(Signal, value=mdsave.get(key, default), kind="config")`` to seed, and a wall of
``mdsave[key] = sig.get()`` lines to persist).
"""

import numpy as np

from . import _context

__all__ = [
    "CONFIG_KEYS",
    "load",
    "load_array",
    "persist",
    "persist_from_signals",
]


# ---------------------------------------------------------------------------
# Registry: every persistent-config key, its default, and a one-line description / units.
# This is the single place documenting what lives in the Redis ``mdsave`` dict.  Defaults are the
# values that were previously hardcoded in source, so behavior is unchanged until a value is
# explicitly re-calibrated and persisted.
# ---------------------------------------------------------------------------
#: name -> (default, description).  Defaults for table-valued keys are plain lists (NOT numpy).
CONFIG_KEYS = {
    # --- energy / IVU gap (smiclasses/energy.py) ---
    "energy_ivu_gap_offset_energies_eV": (
        [2450, 2470, 3600, 4050, 6400, 6510, 6550, 7700, 8980, 9700, 12000, 12620, 14000, 14400, 16100, 18000],
        "IVU-gap experimental offset table: the energies (eV) at which off_exp is measured.",
    ),
    "energy_ivu_gap_offset_values_um": (
        [-20, -35, 29, 30, 25, 25, 25, 35, 19, 50, 35, 45, 45, 45, 35, 25],
        "IVU-gap experimental offset table: the gap offset (um) at each offset energy.",
    ),
    # --- bimorph mirror default voltages (smiclasses/bimorph.py) ---
    "bimorph_hfm_default_v": (
        [-151, 261, 250, 293, 175, 236, 168, 231, 242, 200, 291, 222, 215, 157, 311, 36],
        "Default HFM bimorph voltages (16 ch) for the SMI SWAXS hutch.",
    ),
    "bimorph_vfm_default_v": (
        [39, -102, 277, 234, 325, 163, 392, 280, 365, 273, 196, 400, 219, 304, 51, -327],
        "Default VFM bimorph voltages (16 ch) for the SMI SWAXS hutch.",
    ),
    "bimorph_vfm_opls_default_v": (
        [-206, -191, 6, 71, -316, 184, -223, 120, 45, -130, 202, -111, 17, 62, -75, -553],
        "Default VFM bimorph voltages (16 ch) for the OPLS hutch.",
    ),
    "bimorph_hfm_lowdiv_offset_v": (
        -80,
        "Additive offset applied to the HFM defaults to reach the low-divergence configuration.",
    ),
}


def _default(key):
    try:
        return CONFIG_KEYS[key][0]
    except KeyError:
        raise KeyError(
            "unknown config key {!r}; register it in smiclasses._config.CONFIG_KEYS".format(key))


def load(key, default=None):
    """Return the persisted value for ``key`` from ``mdsave``, else its registered default.

    Pass ``default`` only to override the registry default (rarely needed).  Scalars come back
    as-is; sequences come back as ``list`` (see module docstring).  Safe off-beamline: an
    unconfigured/empty config simply yields the default.
    """
    cfg = _context.get_config()
    reg_default = default if default is not None else _default(key)
    try:
        return cfg.get(key, reg_default)
    except Exception:
        # never let a config read break device construction
        return reg_default


def load_array(key, default=None, dtype=float):
    """Like :func:`load`, but return a ``numpy`` array (tables are stored as JSON lists).

    Use this for the calibration tables that the code indexes / feeds to ``np.interp`` so the
    consumer always gets array semantics regardless of how the value was stored.
    """
    return np.asarray(load(key, default), dtype=dtype)


def persist(mapping):
    """Write ``{key: value}`` back to ``mdsave`` (the persistent Redis dict).

    Numpy arrays are accepted (``redis_json_dict`` serializes them; they read back as lists).
    No-op off the beamline (empty config) -- writing to the ``{}`` fallback is harmless and the
    values are not needed there.  Returns the number of keys written.
    """
    cfg = _context.get_config()
    n = 0
    for key, value in mapping.items():
        if key not in CONFIG_KEYS:
            raise KeyError(
                "refusing to persist unregistered config key {!r}; add it to "
                "smiclasses._config.CONFIG_KEYS".format(key))
        if isinstance(value, np.ndarray):
            value = value.tolist()
        cfg[key] = value
        n += 1
    return n


def persist_from_signals(device, key_to_attr):
    """Persist several config Signals at once: ``{redis_key: "signal_attr_name"}``.

    Replaces the hand-written ``mdsave[key] = device.sig.get()`` walls.  Reads each named signal
    on ``device`` and writes it under the corresponding key.  Returns the number written.
    """
    return persist({key: getattr(device, attr).get() for key, attr in key_to_attr.items()})
