"""Tier-2 (sim) tests: the RE-busy signal preprocessor against a RunEngine + a fake Redis client.

No hardware and no real Redis are touched.  These exercise ``smi_beamline.plans.re_status``:
the cross-process "RE is busy" lock-out flag the alignment GUI polls.  We assert the flag is

* held high (key present, ``busy=True``) for the duration of a plan,
* cleared on clean completion, on exception, and on abort,
* heartbeat-refreshed (TTL re-asserted) while a plan runs,
* a no-op (plan still runs, nothing published) when no Redis client is wired,
* installed idempotently on ``RE.preprocessors``.

Plus the persistent ``beam_down`` operator-mode flag: set (persistent, no TTL) / clear / read,
the env-var fallback, and the Redis-OR-env effective predicate.
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

    Supports just what re_status uses: ``set`` (no expiry) / ``setex`` (TTL) / ``get`` / ``delete``.
    TTL is honoured on read (an expired key reads as absent); a plain ``set`` key never expires.
    Every ``setex`` / ``set`` is recorded so the heartbeat and the persistent writes can be
    observed.  Strings are stored/returned as bytes, like the real client's default.
    """

    def __init__(self):
        self._store = {}                  # key -> (value_bytes, expiry_monotonic_or_None)
        self._lock = threading.Lock()
        self.setex_calls = []             # (key, ttl) per setex, for heartbeat assertions
        self.set_calls = []               # (key,) per set, for persistent-write assertions
        self.delete_calls = []

    def setex(self, key, ttl, value):
        if isinstance(value, str):
            value = value.encode()
        with self._lock:
            self._store[key] = (value, time.monotonic() + ttl)
            self.setex_calls.append((key, ttl))

    def set(self, key, value):
        if isinstance(value, str):
            value = value.encode()
        with self._lock:
            self._store[key] = (value, None)   # None expiry -> persistent
            self.set_calls.append((key,))

    def get(self, key):
        with self._lock:
            item = self._store.get(key)
            if item is None:
                return None
            value, expiry = item
            if expiry is not None and time.monotonic() >= expiry:
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
        # Read AFTER the first RE-executed message: the preprocessor peeks the leading message to
        # check for the opt-out marker, so the flag is asserted just before the first message runs.
        yield from bps.null()
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
        yield from bps.null()                 # first message -> flag asserted by now
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


# ===================================================================== per-plan opt-out (GUI free)
# Plans that hold the RE but never move the alignment motors (e.g. pump_waxs) opt out of the busy
# flag so the GUI stays free.  These cover both opt-out paths and guard the non-opt-out path's
# correctness (send-forwarding) and the "marker must be first" rule.

def test_marker_opt_out_never_publishes_on_a_no_run_plan():
    """A bare message-generator plan (no open_run) that yields no_re_busy_lock() first never sets
    the flag -- this is exactly the pump_waxs shape (no run, no metadata)."""
    client = FakeRedis()
    RE = RunEngine({})

    seen = {}

    def pump_like():
        yield from rs.no_re_busy_lock()       # opt out FIRST
        # ... a long maintenance body that opens no run and moves no alignment motors:
        seen["mid"] = _busy_doc(client)
        yield from bps.sleep(0.05)
        seen["end"] = _busy_doc(client)

    RE(rs.re_busy_signal(pump_like(), status_store=client, ttl=5, interval=0.01))

    # Flag was never published at any point, and nothing was written to Redis.
    assert seen["mid"] is None and seen["end"] is None
    assert _busy_doc(client) is None
    assert client.setex_calls == []          # heartbeat never started
    # (no SETEX at all -> the GUI sees "idle" the whole time and may align)


def test_marker_opt_out_propagates_exceptions():
    """An error inside an opted-out plan must still surface (the marker only suppresses the flag)."""
    client = FakeRedis()
    RE = RunEngine({})

    class Boom(Exception):
        pass

    def pump_like():
        yield from rs.no_re_busy_lock()
        raise Boom("kaboom")

    with pytest.raises(Boom):
        RE(rs.re_busy_signal(pump_like(), status_store=client, ttl=5, interval=10))
    assert client.setex_calls == []          # never locked
    assert _busy_doc(client) is None



    """Through the real installed preprocessor, the marker still suppresses the flag."""
    client = FakeRedis()
    RE = RunEngine({})
    rs.install_re_busy_signal(RE, status_store=client, ttl=5, interval=0.01)

    captured = {}

    def pump_like():
        yield from rs.no_re_busy_lock()
        captured["mid"] = _busy_doc(client)
        yield from bps.null()

    RE(pump_like())
    assert captured["mid"] is None
    assert client.setex_calls == []


def test_name_skip_list_opts_out_without_body_change():
    """A plan whose generator function name is in skip_plans opts out with no body change."""
    client = FakeRedis()
    RE = RunEngine({})

    seen = {}

    def pump_waxs():                          # name matches the skip-list below
        seen["mid"] = _busy_doc(client)       # NOTE: no no_re_busy_lock() in the body
        yield from bps.sleep(0.05)

    RE(rs.re_busy_signal(pump_waxs(), status_store=client, ttl=5, interval=0.01,
                         skip_plans={"pump_waxs"}))
    assert seen["mid"] is None
    assert _busy_doc(client) is None
    assert client.setex_calls == []


def test_default_skip_plans_contains_pump_and_vent():
    assert "pump_waxs" in rs.DEFAULT_SKIP_PLANS
    assert "vent_waxs" in rs.DEFAULT_SKIP_PLANS


def test_non_opted_out_plan_still_publishes():
    """Regression guard: an ordinary plan (no marker, not in skip-list) is still locked."""
    client = FakeRedis()
    RE = RunEngine({})

    seen = {}

    def normal():
        yield from bps.null()                 # first message -> flag asserted by now
        seen["mid"] = _busy_doc(client)
        yield from bps.null()

    RE(rs.re_busy_signal(normal(), status_store=client, ttl=5, interval=10,
                         skip_plans={"pump_waxs"}))
    assert seen["mid"] is not None and seen["mid"]["busy"] is True
    assert _busy_doc(client) is None          # cleared after
    assert client.setex_calls                  # the flag WAS published


def test_non_opt_out_preserves_message_responses():
    """The leading-message peek must not drop the RE's response to the FIRST message: a plan that
    reads back values gets them all (send-forwarding through the wrapper is correct)."""
    client = FakeRedis()
    RE = RunEngine({})

    from bluesky.utils import Msg

    # A command whose handler returns a known value, so the plan can observe its response.
    async def _echo(msg):
        return ("ECHO", msg.args[0])
    RE.register_command("echo", _echo)

    got = []

    def reader():
        r1 = yield Msg("echo", None, 1)       # FIRST message (the one that gets peeked)
        got.append(r1)
        r2 = yield Msg("echo", None, 2)
        got.append(r2)

    RE(rs.re_busy_signal(reader(), status_store=client, ttl=5, interval=10))
    # Both responses delivered, including the first message's -- proves no response was dropped.
    assert got == [("ECHO", 1), ("ECHO", 2)]


def test_marker_only_counts_as_first_message():
    """A no_re_busy_lock() marker that appears LATER (not first) does NOT opt out -- the plan is
    locked as usual (only the leading message is inspected)."""
    client = FakeRedis()
    RE = RunEngine({})

    seen = {}

    def late_marker():
        yield from bps.null()                 # a real first message -> NOT the marker
        seen["mid"] = _busy_doc(client)
        yield from rs.no_re_busy_lock()       # too late to opt out
        yield from bps.null()

    RE(rs.re_busy_signal(late_marker(), status_store=client, ttl=5, interval=10))
    assert seen["mid"] is not None and seen["mid"]["busy"] is True
    assert client.setex_calls                  # still locked


def test_no_re_busy_lock_is_a_harmless_noop_message():
    """no_re_busy_lock() yields a single null message the RE executes without error."""
    RE = RunEngine({})
    cmds = []

    def plan():
        yield from rs.no_re_busy_lock()
        yield from bps.null()

    # Spy on the messages the RE sees by running through a trivial msg collector.
    from bluesky.preprocessors import msg_mutator

    def _collect(msg):
        cmds.append(msg.command)
        return msg

    RE(msg_mutator(plan(), _collect))
    assert cmds[0] == "null"                   # the marker is a null no-op
    # and it carried the sentinel kwarg the preprocessor keys on
    # (re-derive directly from the stub to assert the contract)
    m = next(rs.no_re_busy_lock())
    assert m.command == "null"
    assert m.kwargs.get(rs.NO_RE_BUSY_MARKER) is True


def test_install_forwards_skip_plans_and_tags_pp():
    client = FakeRedis()
    RE = RunEngine({})
    pp = rs.install_re_busy_signal(RE, status_store=client, skip_plans={"pump_waxs", "vent_waxs"})
    assert getattr(pp, "_smi_skip_plans") == {"pump_waxs", "vent_waxs"}


# ============================================================================= beam_down flag
def _beam_down_raw(client):
    raw = client.get(rs.BEAM_DOWN_KEY)
    return None if raw is None else json.loads(raw.decode())


def test_beam_down_default_inactive(monkeypatch):
    monkeypatch.delenv("BEAM_DOWN", raising=False)
    monkeypatch.delenv("SMI_BEAM_DOWN", raising=False)
    client = FakeRedis()
    assert rs.beam_down_active(status_store=client) is False
    assert rs.read_beam_down(status_store=client) is None


def test_beam_down_set_is_persistent_no_ttl(monkeypatch):
    monkeypatch.delenv("BEAM_DOWN", raising=False)
    monkeypatch.delenv("SMI_BEAM_DOWN", raising=False)
    client = FakeRedis()

    assert rs.set_beam_down(reason="shutdown", by="alice", status_store=client) is True
    # written with .set (persistent), NOT .setex (TTL) -- this is the whole point
    assert client.set_calls == [(rs.BEAM_DOWN_KEY,)]
    assert client.setex_calls == []

    doc = _beam_down_raw(client)
    assert doc["beam_down"] is True
    assert doc["reason"] == "shutdown" and doc["by"] == "alice"
    assert "since" in doc and "host" in doc

    assert rs.beam_down_active(status_store=client) is True
    assert rs.read_beam_down(status_store=client)["beam_down"] is True


def test_beam_down_clear(monkeypatch):
    monkeypatch.delenv("BEAM_DOWN", raising=False)
    monkeypatch.delenv("SMI_BEAM_DOWN", raising=False)
    client = FakeRedis()
    rs.set_beam_down(status_store=client)
    assert rs.beam_down_active(status_store=client) is True

    assert rs.clear_beam_down(status_store=client) is True
    assert rs.beam_down_active(status_store=client) is False
    assert rs.read_beam_down(status_store=client) is None
    assert rs.BEAM_DOWN_KEY in client.delete_calls


@pytest.mark.parametrize("val,expected", [
    ("1", True), ("true", True), ("YES", True), ("on", True),
    ("0", False), ("", False), ("no", False),
])
def test_beam_down_env_fallback(monkeypatch, val, expected):
    monkeypatch.delenv("SMI_BEAM_DOWN", raising=False)
    monkeypatch.setenv("BEAM_DOWN", val)
    client = FakeRedis()                         # empty store -> only the env var can make it active
    assert rs.beam_down_active(status_store=client) is expected


def test_beam_down_env_or_redis(monkeypatch):
    # env OFF but Redis flag ON -> active (Redis path)
    monkeypatch.delenv("BEAM_DOWN", raising=False)
    monkeypatch.delenv("SMI_BEAM_DOWN", raising=False)
    client = FakeRedis()
    rs.set_beam_down(status_store=client)
    assert rs.beam_down_active(status_store=client) is True
    # env ON but Redis flag OFF -> still active (env path), even with an empty store
    rs.clear_beam_down(status_store=client)
    monkeypatch.setenv("SMI_BEAM_DOWN", "1")
    assert rs.beam_down_active(status_store=client) is True


def test_beam_down_no_client_safe(monkeypatch):
    monkeypatch.delenv("BEAM_DOWN", raising=False)
    monkeypatch.delenv("SMI_BEAM_DOWN", raising=False)
    assert rs.set_beam_down(status_store=None) is False
    assert rs.clear_beam_down(status_store=None) is False
    assert rs.read_beam_down(status_store=None) is None
    assert rs.beam_down_active(status_store=None) is False


def test_beam_down_in_all():
    for name in ("BEAM_DOWN_KEY", "set_beam_down", "clear_beam_down",
                 "read_beam_down", "beam_down_active"):
        assert name in rs.__all__
