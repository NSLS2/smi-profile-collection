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
* ``get_sample_store()`` -> the ``samplestore`` RedisJSONDict on db=2 (or a plain dict fallback).
* ``get_status_store()`` -> the raw Redis client for EPHEMERAL RE liveness/status on db=3 (or
  ``None`` if not configured).
* ``current_energy_eV()`` -> the live beamline energy in eV (or ``None`` if unavailable).

None of these import ``smibase``; they only read what was injected.  This keeps the device
classes import-clean and hardware-free at import time.
"""

__all__ = [
    "configure", "get_md", "get_config", "current_energy_eV", "is_configured",
    "get_re", "get_sd", "get_bec", "get_db", "get_sample_store", "get_status_store",
    "baseline_register",
]


# Injected by the profile bootstrap (see smibase.base).  Left as ``None`` until configured so
# the module imports with no side effects and no smibase/EPICS/Redis dependency.
_run_engine = None
_config_dict = None
_energy_source = None  # a zero-arg callable returning energy in eV, or an object with .energy.readback
_sd = None             # SupplementalData (carries the baseline)
_bec = None            # BestEffortCallback
_db = None             # databroker / Broker
_sample_store = None   # Redis-backed sample/holder store (RedisJSONDict on db=2) or dict fallback
_status_store = None   # raw Redis client for EPHEMERAL RE liveness/status (db=3), or None


def configure(*, run_engine=None, config_dict=None, energy_source=None,
              sd=None, bec=None, db=None, sample_store=None, status_store=None):
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
    sd : SupplementalData, optional
        The ``sd`` object whose ``.baseline`` the modules extend.  Stored so device/instance
        modules can register baselines via :func:`baseline_register` instead of grabbing ``sd``
        from ``get_ipython().user_ns``.
    bec : BestEffortCallback, optional
        The live ``bec`` (best-effort callback).
    db : object, optional
        The live databroker / ``Broker``.
    sample_store : mapping, optional
        The persistent **sample/holder store** (the Redis-backed ``samplestore`` on db=2, a
        ``RedisJSONDict``).  Stored by reference; reached via :func:`get_sample_store` by the
        sample-system plans (load/unload, history append) without importing ``smibase.base``.
    status_store : redis.Redis, optional
        The **raw** Redis client for EPHEMERAL RE liveness/status (db=3).  A raw client (not a
        ``RedisJSONDict``) so the busy flag can be written with a TTL (``SETEX``) and refreshed by
        a heartbeat -- see :mod:`smi_beamline.plans.re_status`.  Reached via
        :func:`get_status_store`.
    """
    global _run_engine, _config_dict, _energy_source, _sd, _bec, _db, _sample_store, _status_store
    if run_engine is not None:
        _run_engine = run_engine
    if config_dict is not None:
        _config_dict = config_dict
    if energy_source is not None:
        _energy_source = energy_source
    if sd is not None:
        _sd = sd
    if bec is not None:
        _bec = bec
    if db is not None:
        _db = db
    if sample_store is not None:
        _sample_store = sample_store
    if status_store is not None:
        _status_store = status_store


def is_configured():
    """True if the live profile has wired the seam (False under bare import / tests)."""
    return _run_engine is not None


def get_sd():
    """Return the injected ``sd`` (SupplementalData), or ``None`` if not configured."""
    return _sd


def get_re():
    """Return the injected RunEngine (``RE``), or ``None`` if not configured."""
    return _run_engine


def get_bec():
    """Return the injected ``bec``, or ``None`` if not configured."""
    return _bec


def get_db():
    """Return the injected databroker, or ``None`` if not configured."""
    return _db


def baseline_register(*devices):
    """Add ``devices`` to ``sd.baseline`` (the per-scan baseline), via the injected ``sd``.

    Replaces the ``sd = get_ipython().user_ns['sd']; sd.baseline.extend([...])`` pattern in the
    instance modules with dependency injection.  No-op (returns ``False``) if the seam is not
    configured with an ``sd`` (e.g. under bare import / tests / a worker that opts out), so the
    modules stay importable headless.  ``devices`` may be passed as individual args or a single
    iterable.
    """
    if _sd is None:
        return False
    # accept baseline_register(a, b, c) or baseline_register([a, b, c])
    if len(devices) == 1 and not hasattr(devices[0], "name"):
        try:
            devices = tuple(devices[0])
        except TypeError:
            pass
    _sd.baseline.extend(list(devices))
    return True


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


def get_sample_store():
    """Return the persistent **sample/holder store** (Redis ``samplestore`` on db=2).

    Returns the injected ``RedisJSONDict`` on the live beamline, or a plain-dict fallback
    (``{}``) when the seam is unconfigured (bare import / tests / GUI offline).  The fallback
    keeps the sample-system plans and ``SampleStore`` facade importable and exercisable headless,
    exactly like :func:`get_config` does for ``mdsave``.
    """
    if _sample_store is not None:
        return _sample_store
    return {}


def get_status_store():
    """Return the raw Redis client for EPHEMERAL RE liveness/status (db=3), or ``None``.

    Unlike :func:`get_config` / :func:`get_sample_store` (which fall back to an empty ``dict``
    so device classes stay importable off the beamline), this returns ``None`` when unconfigured.
    The status store is a *raw* ``redis.Redis`` client -- callers need its TTL-aware ``setex`` /
    ``delete`` for the heartbeat lock-out flag, which a dict cannot emulate -- so consumers
    (see :mod:`smi_beamline.plans.re_status`) must treat ``None`` as "no status store wired"
    (off-beamline / tests / GUI offline) and simply skip publishing, rather than crash.
    """
    return _status_store


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
