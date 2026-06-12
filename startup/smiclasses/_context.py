"""
smiclasses._context
====================

A tiny **dependency seam** that lets the ophyd *device classes* in ``smiclasses`` reach the
few runtime objects they legitimately need -- the RunEngine metadata dict (``RE.md``), the
Redis-backed persistent-config dict (``mdsave``), and the current beamline energy -- **without
importing** ``smibase.base`` / ``smibase.energy`` at module load.

Why this exists
---------------
Importing ``smibase.base`` from a device class pulls in, at import time, a whole live-beamline
bootstrap (``nslsii.configure_base``, a Tiled login / Duo push, a Redis connection, reading a
secret file).  That:

* makes the device classes **impossible to import / unit-test off the beamline**, and
* creates a **circular import** (``smibase.pilatus`` -> ``smiclasses.pilatus`` ->
  ``smibase.base``).

This module is the seam that breaks both.  The live profile *injects* the real objects once,
early in startup (see ``configure(...)``); tests inject fakes.  ``RE.md`` and ``mdsave`` remain
fully available to the devices (proposal metadata, raw-data directory, data-security tags, and
persistent calibration are unchanged) -- they are simply reached through this accessor rather
than a hard ``smibase`` import.

Contract
--------
* ``configure(*, run_engine=None, config_dict=None, energy_source=None)`` -- called once by the
  profile bootstrap to wire the real objects.
* ``get_md()`` -> the ``RE.md`` mapping (or an empty dict if not configured, e.g. under test).
* ``get_config()`` -> the ``mdsave`` RedisJSONDict (or a plain dict fallback under test).
* ``current_energy_eV()`` -> the live beamline energy in eV (or ``None`` if unavailable).

None of these import ``smibase``; they only read what was injected.  This keeps the device
classes import-clean and hardware-free at import time.
"""

__all__ = ["configure", "get_md", "get_config", "current_energy_eV", "is_configured"]


# Injected by the profile bootstrap (see smibase.base).  Left as ``None`` until configured so
# the module imports with no side effects and no smibase/EPICS/Redis dependency.
_run_engine = None
_config_dict = None
_energy_source = None  # a zero-arg callable returning energy in eV, or an object with .energy.readback


def configure(*, run_engine=None, config_dict=None, energy_source=None):
    """Wire the real runtime objects into the seam (called once, early, by the profile).

    Parameters
    ----------
    run_engine : bluesky RunEngine, optional
        The live ``RE`` whose ``.md`` carries proposal/data-session/data-security metadata and
        the raw-data directory.  Stored by reference, so later ``RE.md`` mutations are seen.
    config_dict : mapping, optional
        The persistent-config dict (the Redis-backed ``mdsave``).  Stored by reference.
    energy_source : callable() -> float | object, optional
        Either a zero-arg callable returning the current energy in eV, or an object exposing
        ``.energy.readback`` (e.g. the ``energy`` pseudo-positioner); used by
        :func:`current_energy_eV`.
    """
    global _run_engine, _config_dict, _energy_source
    if run_engine is not None:
        _run_engine = run_engine
    if config_dict is not None:
        _config_dict = config_dict
    if energy_source is not None:
        _energy_source = energy_source


def is_configured():
    """True if the live profile has wired the seam (False under bare import / tests)."""
    return _run_engine is not None


def get_md():
    """Return the ``RE.md`` mapping, or an empty dict if not configured (e.g. under test)."""
    if _run_engine is not None:
        return _run_engine.md
    return {}


def get_config():
    """Return the persistent-config dict (Redis ``mdsave``), or a plain-dict fallback.

    The fallback lets device classes that seed ``Cpt(Signal, value=cfg.get(key, default))`` be
    imported/instantiated off the beamline; on the live beamline the real RedisJSONDict is used.
    """
    if _config_dict is not None:
        return _config_dict
    return {}


def current_energy_eV():
    """Return the current beamline energy in eV, or ``None`` if no source is wired/available.

    Accepts either a callable energy source or an object with ``.energy.readback`` (the
    ``energy`` pseudo-positioner).  Never raises -- callers should treat ``None`` as "unknown".
    """
    src = _energy_source
    if src is None:
        return None
    try:
        if callable(src):
            return float(src())
        # object with .energy.readback (e.g. the energy pseudo-positioner)
        return float(src.energy.readback.get())
    except Exception:
        return None
