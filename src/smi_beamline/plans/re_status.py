"""
smi_beamline.plans.re_status
============================

Cross-process RunEngine status / control flags in Redis, so out-of-process clients (the sample
alignment GUI; the queueserver running on a *separate* host) can coordinate with the RunEngine
without env vars or shared files.  Two distinct flags live here:

1. **re_busy** (ephemeral, TTL) -- "the RunEngine is busy" lock-out the alignment GUI polls so it
   does not fight the RE for the motors while a plan runs.  Written by the RE, read by the GUI.
2. **beam_down** (persistent, no TTL) -- "the beam is down" operator-mode flag the suspender setup
   reads **once at startup** to BUILD-but-not-ENABLE the ring-current/shutter suspenders (so a
   restart during a shutdown does not immediately pause everything).  Written by an operator (or
   the ``start-beamdown`` task), read by the profile bootstrap.  Replaces the old ``BEAM_DOWN``
   environment variable, which did not carry across to the separate queueserver host.

Where they live
---------------
Both are keys in the RE-status Redis store on **db=3** (a *raw* ``redis.Redis`` client, injected
through :mod:`smi_beamline.devices._context` as ``get_status_store()``).  This is a different db
from the *persistent* beamline config (db=1, ``mdsave``) and sample store (db=2, ``samplestore``)
**on purpose** -- db=3 holds RunEngine *runtime* status/control, not calibration/config, so it is
never swept up by config dump/restore tooling.

Note the two flags have **opposite lifetimes**, by design:

* ``re_busy`` is written with a short **TTL** and heartbeat-refreshed -- it must auto-clear if the
  worker dies (see "anti-latching" below).
* ``beam_down`` is written with **no expiry** -- it is an operator mode that must *survive* RE /
  worker restarts (set it once, restart freely, it stays down) until explicitly cleared.

::

    key   : "swaxsstatus:re_busy"          (RE_BUSY_KEY)            -- ephemeral, TTL
    value : JSON, e.g.
            {"busy": true, "since": "2026-06-17T10:30:00.123456",
             "host": "xf12id2-ws3", "pid": 12345, "plan": "rel_scan",
             "scan_id": 412, "source": "RE", "expires_in": 30}

    key   : "swaxsstatus:beam_down"         (BEAM_DOWN_KEY)          -- persistent, no TTL
    value : JSON, e.g.
            {"beam_down": true, "since": "2026-06-17T09:00:00.000000",
             "host": "xf12id2-ws3", "by": "operator", "reason": "scheduled shutdown"}

The GUI reads ``re_busy``; if it is **absent** or its JSON ``busy`` is false, the RE is idle and the
GUI may move.  (Absent == idle is the safe default -- see "anti-latching" below.)

Anti-latching (why a TTL **and** a finally)
-------------------------------------------
A lock-out flag has one catastrophic failure mode: getting **stuck on** so the GUI is disabled
forever.  Two independent mechanisms prevent that:

1. **finally** -- the flag is published by wrapping the whole plan in
   :func:`bluesky.preprocessors.finalize_wrapper`, so it is cleared whether the plan finishes,
   raises, or is aborted (Ctrl-C).  This covers every *in-process* exit.
2. **TTL heartbeat** -- the key is written with a short expiry (``ttl`` seconds, default
   :data:`DEFAULT_TTL`) and a background daemon thread re-writes it every :data:`DEFAULT_INTERVAL`
   seconds while the plan runs.  If the worker dies in a way ``finally`` **cannot** catch -- a hard
   ``kill -9``, a segfault, an OOM kill, the box losing power -- the key simply **expires** within
   ``ttl`` seconds and the GUI unlocks itself.  The flag can never latch.

This is why the store is a raw ``redis.Redis`` client and not a ``RedisJSONDict``: only the raw
client exposes the ``SETEX`` / per-key expiry the heartbeat needs.

Queueserver
-----------
Installed on ``RE.preprocessors``, this wraps the **top-level plan** the RunEngine executes.  That
gives **per-plan** busy semantics, which is exactly right in both worlds:

* interactive terminal -- "busy" spans each plan a human launches (motors are moving);
* queueserver -- "busy" spans each queued plan, and clears between them, so the GUI may move the
  sample while the queue is idle / paused between items.

The only beamline-specific wiring is the Redis client (reached through the seam, like every other
device/plan module), so this module is hardware-free and unit-testable off the beamline: pass a
fake client to :func:`install_re_busy_signal` / :func:`re_busy_signal` (``status_store=...``) and it
never touches the seam.
"""
import datetime
import json
import os
import socket
import threading

try:
    import bluesky.preprocessors as bpp
except Exception:  # pragma: no cover - outside the beamline env
    bpp = None

from smi_beamline.devices import _context as _seam


__all__ = [
    "RE_BUSY_KEY",
    "BEAM_DOWN_KEY",
    "DEFAULT_TTL",
    "DEFAULT_INTERVAL",
    "re_busy_signal",
    "install_re_busy_signal",
    "read_re_busy",
    "clear_re_busy",
    "show_re_status",
    "set_beam_down",
    "clear_beam_down",
    "read_beam_down",
    "beam_down_active",
]


#: The single Redis key the GUI polls.  ``swaxsstatus:`` prefix mirrors the ``swaxs<store>:``
#: convention of the sample store keys (``swaxssamples:...``).
RE_BUSY_KEY = "swaxsstatus:re_busy"

#: Persistent "beam is down" operator-mode key (no TTL).  Read once at startup by the suspender
#: setup; replaces the old ``BEAM_DOWN`` environment variable.
BEAM_DOWN_KEY = "swaxsstatus:beam_down"

#: Seconds the busy key lives for before Redis auto-expires it.  Must be comfortably larger than
#: :data:`DEFAULT_INTERVAL` so a healthy heartbeat always refreshes it well before it lapses; small
#: enough that a *dead* worker's flag clears quickly (the GUI's max stuck-locked time).
DEFAULT_TTL = 30

#: Seconds between heartbeat refreshes while a plan runs.  ~1/3 of the TTL gives two chances to
#: refresh before expiry, tolerating a missed beat (GC pause, slow Redis) without a false "idle".
DEFAULT_INTERVAL = 10


def _now_iso():
    return datetime.datetime.now().isoformat()


def _payload(*, busy, ttl, extra=None):
    """Build the JSON value written to :data:`RE_BUSY_KEY` (see module docstring for the shape)."""
    doc = {
        "busy": bool(busy),
        "since": _now_iso(),
        "host": socket.gethostname(),
        "pid": os.getpid(),
        "source": "RE",
        "expires_in": ttl,
    }
    if extra:
        doc.update({k: v for k, v in extra.items() if v is not None})
    return json.dumps(doc)


class _Heartbeat:
    """A daemon thread that re-``SETEX``-es the busy key every ``interval`` s until stopped.

    Keeping the key alive from a background thread (rather than from the plan's own messages) means
    the TTL is refreshed even during a single long-running ``mv`` / count where no new messages
    flow for many seconds.  ``daemon=True`` so it can never block interpreter shutdown; ``stop()``
    is idempotent and best-effort clears the key on a clean stop.
    """

    def __init__(self, client, *, key, ttl, interval, payload_extra=None):
        self._client = client
        self._key = key
        self._ttl = ttl
        self._interval = interval
        self._extra = payload_extra or {}
        self._stop = threading.Event()
        self._thread = None

    def _publish(self):
        try:
            self._client.setex(self._key, self._ttl,
                               _payload(busy=True, ttl=self._ttl, extra=self._extra))
        except Exception:
            # Never let a Redis hiccup break the scan -- the flag is advisory.  A missed beat just
            # risks the key lapsing early (GUI sees "idle"); the next beat re-asserts it.
            pass

    def _run(self):
        # Refresh immediately, then every ``interval`` s until asked to stop.  ``wait`` returns
        # True the moment ``stop()`` fires, so shutdown is prompt (no full-interval lag).
        self._publish()
        while not self._stop.wait(self._interval):
            self._publish()

    def start(self):
        self._publish()  # assert the flag synchronously before any motion begins
        self._thread = threading.Thread(
            target=self._run, name="re-busy-heartbeat", daemon=True)
        self._thread.start()

    def stop(self, *, clear=True):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=self._interval + 1)
            self._thread = None
        if clear:
            try:
                self._client.delete(self._key)
            except Exception:
                pass


def _resolve_client(status_store):
    """Return the raw Redis client to publish to: explicit arg wins, else the seam (else None)."""
    if status_store is not None:
        return status_store
    return _seam.get_status_store()


def re_busy_signal(plan, *, status_store=None, ttl=DEFAULT_TTL, interval=DEFAULT_INTERVAL):
    """Wrap ``plan`` so the Redis busy flag is held high for its whole duration, then cleared.

    A plain plan-preprocessor (``plan -> plan``): meant for ``RE.preprocessors`` but also usable ad
    hoc.  Starts a TTL heartbeat (see :class:`_Heartbeat`) before the first message and stops +
    clears it in a ``finally``, so the flag is released on success, exception, or abort, and
    auto-expires if the process is killed outright.

    If **no** Redis client is available (off the beamline / tests / GUI offline -- the seam returns
    ``None``), the plan is yielded through **unchanged**: the busy signal is advisory and its
    absence must never block running a plan.

    Parameters
    ----------
    plan : generator
        The bluesky plan (message generator) to wrap.
    status_store : redis.Redis, optional
        Raw Redis client to publish to.  Defaults to the injected
        :func:`smi_beamline.devices._context.get_status_store`.  Pass a fake here in tests.
    ttl : int
        Seconds the key lives before Redis expires it (the GUI's worst-case stuck-locked time).
    interval : int
        Seconds between heartbeat refreshes.  Should be < ``ttl``.
    """
    client = _resolve_client(status_store)
    if client is None:
        # Nothing to publish to -- run the plan verbatim.
        return (yield from plan)

    # Best-effort context for the GUI ("what is it busy with?").  Never let metadata gathering
    # raise -- it is decoration, not function.
    extra = {}
    try:
        RE = _seam.get_re()
        if RE is not None:
            md = RE.md
            extra = {
                "plan": md.get("plan_name"),
                "scan_id": md.get("scan_id"),
                "data_session": md.get("data_session"),
                "sample_name": md.get("sample_name"),
            }
    except Exception:
        extra = {}

    hb = _Heartbeat(client, key=RE_BUSY_KEY, ttl=ttl, interval=interval, payload_extra=extra)

    def _wrapped():
        hb.start()
        return (yield from plan)

    def _release():
        hb.stop(clear=True)
        # ``finalize_wrapper`` wants a *plan* (generator) -- yield nothing, just run the cleanup.
        return
        yield  # pragma: no cover - makes _release a generator without emitting a message

    return (yield from bpp.finalize_wrapper(_wrapped(), _release()))


def install_re_busy_signal(RE, *, status_store=None, ttl=DEFAULT_TTL,
                           interval=DEFAULT_INTERVAL, replace=True, verbose=False):
    """Append the RE-busy preprocessor to ``RE.preprocessors`` (the beamline default).

    After this, every top-level plan run through ``RE`` holds the Redis busy flag high for its
    duration (heartbeat-refreshed, ``finally``-cleared, TTL-auto-expiring).  Mirrors
    :func:`smi_beamline.plans.scan_naming.install_default_scan_naming`: the installed preprocessor
    is tagged ``_smi_re_busy = True`` so re-running this de-dups instead of stacking copies.

    Parameters
    ----------
    RE : RunEngine
        The live RunEngine.
    status_store : redis.Redis, optional
        Raw Redis client; defaults to the seam's :func:`get_status_store`.
    ttl, interval : int
        Heartbeat TTL and refresh interval (seconds); see :func:`re_busy_signal`.
    replace : bool
        If True (default), first remove any previously-installed RE-busy preprocessor so
        re-running in a live session does not stack duplicates.
    verbose : bool
        Print whether a Redis client was found (and the key being published).

    Returns
    -------
    callable
        The installed preprocessor (also appended to ``RE.preprocessors``).
    """
    if replace:
        RE.preprocessors[:] = [
            pp for pp in RE.preprocessors if not getattr(pp, "_smi_re_busy", False)
        ]

    def _pp(plan):
        return (yield from re_busy_signal(
            plan, status_store=status_store, ttl=ttl, interval=interval))

    try:
        _pp._smi_re_busy = True
        _pp._smi_ttl = ttl
        _pp._smi_interval = interval
    except (AttributeError, TypeError):
        pass

    RE.preprocessors.append(_pp)

    if verbose:
        client = _resolve_client(status_store)
        if client is None:
            print("RE-busy signal: no Redis status store wired -- flag will NOT be published "
                  "(plans still run normally).")
        else:
            print(f"RE-busy signal: publishing '{RE_BUSY_KEY}' "
                  f"(ttl={ttl}s, heartbeat={interval}s) while plans run.")
    return _pp


def read_re_busy(*, status_store=None):
    """Return the current busy payload as a dict, or ``None`` if idle / unavailable.

    Convenience for the console (and a reference for the GUI): reads :data:`RE_BUSY_KEY` and parses
    its JSON.  Returns ``None`` when the key is absent (RE idle / never set / expired) or no Redis
    client is wired.  ``{"busy": ...}`` otherwise.
    """
    client = _resolve_client(status_store)
    if client is None:
        return None
    try:
        raw = client.get(RE_BUSY_KEY)
    except Exception:
        return None
    if raw is None:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "replace")
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        # Present but unparseable -> treat as "busy, details unknown" rather than hide it.
        return {"busy": True, "raw": raw}


def clear_re_busy(*, status_store=None):
    """Force-clear the busy flag (delete :data:`RE_BUSY_KEY`).  Returns True if a client was found.

    An operator escape hatch: if a flag is ever stuck (it should not be -- it has a TTL), this
    removes it immediately so the GUI unlocks.  Safe to call when already idle (delete is a no-op).
    """
    client = _resolve_client(status_store)
    if client is None:
        return False
    try:
        client.delete(RE_BUSY_KEY)
    except Exception:
        return False
    return True


def show_re_status(*, status_store=None):
    """Print the current RE busy/idle status (console helper)."""
    doc = read_re_busy(status_store=status_store)
    if doc is None:
        print(f"RE status: IDLE  (key '{RE_BUSY_KEY}' absent)")
        return
    if not doc.get("busy", True):
        print(f"RE status: IDLE  ({doc})")
        return
    bits = [f"plan={doc.get('plan')}", f"scan_id={doc.get('scan_id')}",
            f"since={doc.get('since')}", f"host={doc.get('host')}", f"pid={doc.get('pid')}"]
    print("RE status: BUSY  " + "  ".join(b for b in bits if not b.endswith("None")))


# =============================================================================================
# beam_down: persistent "the beam is down" operator-mode flag (no TTL).
# =============================================================================================
# Read ONCE at startup by smibase.suspenders to BUILD-but-not-ENABLE the suspenders.  Unlike
# re_busy this is deliberately persistent (survives RE / worker restarts) and is written by an
# operator / the start-beamdown task, not by the RE.

#: Env-var fallback names (the OLD mechanism), still honoured by :func:`beam_down_active` so the
#: existing ``BEAM_DOWN=1`` workflow keeps working and there is a hatch when Redis is unreachable.
_BEAM_DOWN_ENV_VARS = ("BEAM_DOWN", "SMI_BEAM_DOWN")

#: Truthy spellings accepted from the env var.
_TRUTHY = ("1", "true", "yes", "on")


def _beam_down_from_env():
    """True if any of the legacy BEAM_DOWN/SMI_BEAM_DOWN env vars is set truthy."""
    for name in _BEAM_DOWN_ENV_VARS:
        if os.environ.get(name, "").strip().lower() in _TRUTHY:
            return True
    return False


def set_beam_down(*, reason=None, by=None, status_store=None):
    """Set the persistent ``beam_down`` flag (no expiry) so suspenders start DISABLED.

    Written with **no TTL** -- it must survive RE/worker restarts until :func:`clear_beam_down`
    removes it.  Takes effect on the **next** profile startup (the suspender setup reads it once);
    it does not enable/disable already-installed suspenders in a live session -- use
    ``turn_on_suspenders()`` / ``turn_off_suspenders()`` for that.

    Parameters
    ----------
    reason : str, optional
        Free-text note stored in the payload (e.g. ``"scheduled shutdown"``).
    by : str, optional
        Who set it (defaults to ``$USER`` or ``"unknown"``).
    status_store : redis.Redis, optional
        Raw Redis client; defaults to the seam's :func:`get_status_store`.

    Returns
    -------
    bool
        True if a client was found and the flag was written, else False.
    """
    client = _resolve_client(status_store)
    if client is None:
        return False
    doc = {
        "beam_down": True,
        "since": _now_iso(),
        "host": socket.gethostname(),
        "by": by or os.environ.get("USER", "unknown"),
    }
    if reason:
        doc["reason"] = reason
    try:
        client.set(BEAM_DOWN_KEY, json.dumps(doc))   # set, not setex -> persistent, no TTL
    except Exception:
        return False
    return True


def clear_beam_down(*, status_store=None):
    """Clear the persistent ``beam_down`` flag (delete :data:`BEAM_DOWN_KEY`).

    Takes effect on the next startup (suspenders will then install normally).  Returns True if a
    Redis client was found.  Safe to call when already clear (delete is a no-op).
    """
    client = _resolve_client(status_store)
    if client is None:
        return False
    try:
        client.delete(BEAM_DOWN_KEY)
    except Exception:
        return False
    return True


def read_beam_down(*, status_store=None):
    """Return the ``beam_down`` payload dict, or ``None`` if not set / unavailable.

    Reads only the Redis key (does NOT consult the env var -- use :func:`beam_down_active` for the
    effective state).  ``None`` when the key is absent or no client is wired.
    """
    client = _resolve_client(status_store)
    if client is None:
        return None
    try:
        raw = client.get(BEAM_DOWN_KEY)
    except Exception:
        return None
    if raw is None:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "replace")
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        # Present but unparseable -> treat as "beam down, details unknown" (fail safe = suspenders
        # off, which is the cautious choice during a suspected shutdown).
        return {"beam_down": True, "raw": raw}


def beam_down_active(*, status_store=None):
    """Return True if the beam should be treated as DOWN at startup (Redis flag OR env var).

    This is the single predicate the suspender setup calls.  It is True when **either** the
    persistent Redis ``beam_down`` flag is set **or** a legacy ``BEAM_DOWN``/``SMI_BEAM_DOWN`` env
    var is set truthy (so the old workflow and a Redis-unreachable fallback both still work).
    Never raises.
    """
    if _beam_down_from_env():
        return True
    doc = read_beam_down(status_store=status_store)
    if doc is None:
        return False
    return bool(doc.get("beam_down", False))


# ---------------------------------------------------------------------- standalone CLI (pixi task)
def _standalone_status_client():
    """Build a raw Redis client to db=3 directly (for use OUTSIDE the profile, e.g. the pixi task).

    The seam is not configured in a bare ``python -m`` invocation, so mirror the connection
    ``smibase.base`` makes (same host/port/SSL, secret from ``/etc/bluesky/redis.secret``).  Returns
    ``None`` (with a printed note) if redis or the secret is unavailable, so the caller degrades
    instead of crashing the launch.
    """
    try:
        import redis
    except Exception as exc:  # pragma: no cover - redis always present on the beamline
        print(f"beam_down CLI: redis unavailable ({exc!r})")
        return None
    try:
        with open("/etc/bluesky/redis.secret", "r") as f:
            secret = f.read().strip()
    except Exception as exc:
        print(f"beam_down CLI: cannot read redis secret ({exc!r})")
        return None
    return redis.Redis("xf12id2-smi-redis1.nsls2.bnl.gov", db=3, ssl=True, port=6380,
                       password=secret)


def _main(argv=None):
    """Tiny CLI so the ``start-beamdown`` pixi task can set the flag before launching IPython.

    Usage::

        python -m smi_beamline.plans.re_status set-beam-down [--reason TEXT]
        python -m smi_beamline.plans.re_status clear-beam-down
        python -m smi_beamline.plans.re_status status
    """
    import argparse

    parser = argparse.ArgumentParser(prog="re_status", description="RE-status Redis flags (db=3).")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_set = sub.add_parser("set-beam-down", help="set the persistent beam_down flag")
    p_set.add_argument("--reason", default=None, help="free-text reason stored in the flag")
    sub.add_parser("clear-beam-down", help="clear the persistent beam_down flag")
    sub.add_parser("status", help="print the current beam_down / re_busy flags")
    args = parser.parse_args(argv)

    client = _standalone_status_client()
    if client is None:
        print("beam_down CLI: no Redis client -- nothing done.")
        return 1

    if args.cmd == "set-beam-down":
        ok = set_beam_down(reason=args.reason, status_store=client)
        print(f"beam_down: SET ({BEAM_DOWN_KEY})" if ok else "beam_down: FAILED to set")
        return 0 if ok else 1
    if args.cmd == "clear-beam-down":
        ok = clear_beam_down(status_store=client)
        print(f"beam_down: CLEARED ({BEAM_DOWN_KEY})" if ok else "beam_down: FAILED to clear")
        return 0 if ok else 1
    if args.cmd == "status":
        bd = read_beam_down(status_store=client)
        print(f"beam_down : {'DOWN' if (bd and bd.get('beam_down')) else 'up'}  ({bd})")
        show_re_status(status_store=client)
        return 0
    return 1


if __name__ == "__main__":   # pragma: no cover - exercised via the pixi task, not the test suite
    import sys
    sys.exit(_main())
