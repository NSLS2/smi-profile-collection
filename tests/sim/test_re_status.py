"""Tier-2 (sim) tests: the RE-busy signal preprocessor against a RunEngine + a fake Redis client.

No hardware and no real Redis are touched.  These exercise ``smi_beamline.plans.re_status``:
the cross-process "RE is busy" lock-out flag the alignment GUI polls.  We assert the flag is

* held high (key present, ``busy=True``) for the duration of a plan,
* cleared on clean completion, on exception, and on abort,
* heartbeat-refreshed (TTL re-asserted) while a plan runs,
* a no-op (plan still runs, nothing published) when no Redis client is wired,
* installed idempotently on ``RE.preprocessors``.
"""
import json
import threading
import time

import pytest

pytest.importorskip("bluesky")
from bluesky import RunEngine  # noqa: E402
import bluesky.plans as bp  # noqa: E402
import bluesky.plan_stubs as bps  # noqa: E402
from ophyd.sim import det  # noqa: E402

from smi_beamline.plans import re_status as rs  # noqa: E402


# --------------------------------------------------------------------------- a fake Redis client
class FakeRedis:
    """Minimal thread-safe in-memory stand-in for redis.Redis with TTL semantics.

    Supports just what re_status uses: ``setex`` / ``get`` / ``delete``.  TTL is honoured on read
    (an expired key reads as absent), and every ``setex`` is recorded so the heartbeat can be
    observed.  Strings are stored/returned as bytes, like the real client's default.
    """

    def __init__(self):
        self._store = {}                  # key -> (value_bytes, expiry_epoch)
        self._lock = threading.Lock()
        self.setex_calls = []             # (key, ttl) per setex, for heartbeat assertions
        self.delete_calls = []

    def setex(self, key, ttl, value):
        if isinstance(value, str):
            value = value.encode()
        with self._lock:
            self._store[key] = (value, time.monotonic() + ttl)
            self.setex_calls.append((key, ttl))

    def get(self, key):
        with self._lock:
            item = self._store.get(key)
            if item is None:
                return None
            value, expiry = item
            if time.monotonic() >= expiry:
                del self._store[key]
                return None
            return value

    def delete(self, *keys):
        with self._lock:
            for key in keys:
                self.delete_calls.append(key)
                self._store.pop(key, None)


def _busy_doc(client):
    raw = client.get(rs.RE_BUSY_KEY)
    if raw is None:
        return None
    return json.loads(raw.decode())


# --------------------------------------------------------------------------- core held/cleared
def test_flag_is_held_during_plan_and_cleared_after():
    client = FakeRedis()
    RE = RunEngine({})

    seen = {}

    def _probe():
        # mid-plan: the flag must be present and busy
        seen["mid"] = _busy_doc(client)
        yield from bps.null()

    def plan():
        yield from bps.open_run()
        yield from _probe()
        yield from bps.close_run()

    RE(rs.re_busy_signal(plan(), status_store=client, ttl=5, interval=10))

    assert seen["mid"] is not None
    assert seen["mid"]["busy"] is True
    # cleared after the plan completes
    assert _busy_doc(client) is None
    assert rs.RE_BUSY_KEY in client.delete_calls


def test_flag_payload_has_context_fields():
    client = FakeRedis()
    RE = RunEngine({})
    captured = {}

    def _probe():
        captured["doc"] = _busy_doc(client)
        yield from bps.null()

    RE(rs.re_busy_signal(_probe(), status_store=client))
    doc = captured["doc"]
    assert doc["busy"] is True
    for field in ("since", "host", "pid", "source", "expires_in"):
        assert field in doc
    assert doc["source"] == "RE"


# --------------------------------------------------------------------------- anti-latch: on error
def test_flag_cleared_on_exception():
    client = FakeRedis()
    RE = RunEngine({})

    class Boom(Exception):
        pass

    def bad_plan():
        yield from bps.open_run()
        raise Boom("kaboom")

    with pytest.raises(Boom):
        RE(rs.re_busy_signal(bad_plan(), status_store=client))

    # finally cleared the flag despite the exception
    assert _busy_doc(client) is None
    assert rs.RE_BUSY_KEY in client.delete_calls


def test_flag_cleared_on_abort():
    from bluesky.utils import RunEngineInterrupted

    client = FakeRedis()
    RE = RunEngine({})

    def pausing_plan():
        yield from bps.open_run()
        yield from bps.checkpoint()
        yield from bps.pause()           # request a pause -> RE returns control (interrupted)
        yield from bps.close_run()

    # pause() makes the RE() call raise RunEngineInterrupted and leaves the plan suspended.
    with pytest.raises(RunEngineInterrupted):
        RE(rs.re_busy_signal(pausing_plan(), status_store=client))

    # now abort -> the finalize cleanup runs and the flag is released
    RE.abort()
    assert _busy_doc(client) is None
    assert rs.RE_BUSY_KEY in client.delete_calls


# --------------------------------------------------------------------------- heartbeat refresh
def test_heartbeat_refreshes_ttl_while_running():
    client = FakeRedis()
    RE = RunEngine({})

    # interval shorter than the plan's dwell so several refreshes happen during the one sleep
    def slow_plan():
        yield from bps.open_run()
        yield from bps.sleep(0.35)
        yield from bps.close_run()

    RE(rs.re_busy_signal(slow_plan(), status_store=client, ttl=5, interval=0.1))

    # start() publishes once synchronously, _run() publishes once more immediately, then ~every
    # 0.1s for 0.35s -> comfortably more than the 2 initial writes.
    assert len(client.setex_calls) >= 3
    assert all(call == (rs.RE_BUSY_KEY, 5) for call in client.setex_calls)
    # and it is cleared at the end
    assert _busy_doc(client) is None


# --------------------------------------------------------------------------- no client -> no-op
def test_no_client_runs_plan_unchanged():
    # status_store=None and the seam unconfigured (autouse fixture) -> publish nothing, run plan.
    RE = RunEngine({})
    names = []

    def cb(name, doc):
        if name == "start":
            names.append(doc)

    RE(rs.re_busy_signal(bp.count([det], num=1), status_store=None), cb)
    assert len(names) == 1                # the plan ran and emitted its run normally


# --------------------------------------------------------------------------- install / idempotency
def test_install_appends_and_is_idempotent():
    client = FakeRedis()
    RE = RunEngine({})

    pp1 = rs.install_re_busy_signal(RE, status_store=client)
    assert pp1 in RE.preprocessors
    n_after_first = len(RE.preprocessors)

    # re-installing replaces (de-dups) rather than stacking
    pp2 = rs.install_re_busy_signal(RE, status_store=client)
    assert len(RE.preprocessors) == n_after_first
    assert pp1 not in RE.preprocessors and pp2 in RE.preprocessors
    assert getattr(pp2, "_smi_re_busy", False) is True


def test_installed_preprocessor_publishes_through_RE():
    client = FakeRedis()
    RE = RunEngine({})
    rs.install_re_busy_signal(RE, status_store=client, ttl=5, interval=10)

    captured = {}

    def _probe():
        captured["doc"] = _busy_doc(client)
        yield from bps.null()

    RE(_probe())
    assert captured["doc"] is not None and captured["doc"]["busy"] is True
    assert _busy_doc(client) is None      # cleared after


# --------------------------------------------------------------------------- read/clear helpers
def test_read_and_clear_helpers():
    client = FakeRedis()
    # nothing set yet -> idle
    assert rs.read_re_busy(status_store=client) is None
    # set it via setex directly (simulating a live worker) and read it back
    client.setex(rs.RE_BUSY_KEY, 30, json.dumps({"busy": True, "plan": "foo"}))
    doc = rs.read_re_busy(status_store=client)
    assert doc["busy"] is True and doc["plan"] == "foo"
    # clear forcibly
    assert rs.clear_re_busy(status_store=client) is True
    assert rs.read_re_busy(status_store=client) is None


def test_read_clear_with_no_client():
    assert rs.read_re_busy(status_store=None) is None
    assert rs.clear_re_busy(status_store=None) is False
