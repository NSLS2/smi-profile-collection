# GUI integration: RunEngine status flags in Redis

The SMI profile publishes a couple of small **cross-process flags** to Redis so an
out-of-process GUI (the sample-alignment / visual-positioning UI) and the
queueserver can coordinate with the RunEngine **without** sharing a Python process,
env vars, or files.

There are two flags, both in the same Redis store, with **deliberately opposite
lifetimes**:

| Flag | Key | Lifetime | Written by | Read by | Purpose |
|------|-----|----------|-----------|---------|---------|
| **RE busy** | `swaxsstatus:re_busy` | ephemeral (TTL, auto-expires) | the RunEngine, while a plan runs | the **GUI** | lock the GUI out of motor moves while a plan is running |
| **beam down** | `swaxsstatus:beam_down` | persistent (no TTL) | an operator / the `start-beamdown` task | the profile at startup | start the suspenders BUILT-but-DISABLED (beam is down) |

The GUI's main interest is **`re_busy`** (poll it to gate motion). `beam_down` is
documented here too because it lives in the same store and the GUI may want to
display it (and possibly offer a set/clear control).

The bluesky side is implemented in
[`src/smi_beamline/plans/re_status.py`](../src/smi_beamline/plans/re_status.py).


## Connecting to Redis

All SMI Redis stores share one server; the flags here are on **db 3**.

| Setting | Value |
|---------|-------|
| host | `xf12id2-smi-redis1.nsls2.bnl.gov` |
| port | `6380` |
| **db** | **3** |
| TLS/SSL | **yes** (`ssl=True`) |
| password | contents of `/etc/bluesky/redis.secret` (strip trailing newline) |

> db 3 is the **RunEngine status/control** store. db 1 (`swaxsmetadata`) is
> persistent beamline config and db 2 (`swaxssamples`) is the sample store — do
> **not** put status flags there.

```python
import redis

with open("/etc/bluesky/redis.secret") as f:
    secret = f.read().strip()

r = redis.Redis(
    "xf12id2-smi-redis1.nsls2.bnl.gov",
    port=6380, db=3, ssl=True, password=secret,
)
```


## `re_busy` — gate the GUI's motor moves

### Semantics

* The RunEngine sets this key (`SETEX`, with a TTL) at the start of every plan and
  **deletes** it when the plan finishes, errors, or is aborted.
* While set, a background heartbeat re-writes it every `DEFAULT_INTERVAL` (10 s) so
  the TTL (`DEFAULT_TTL`, 30 s) never lapses during a running plan.
* **Absent key == RunEngine idle == the GUI may move.** This is the safe default.

### Why a TTL (important for the GUI)

The flag can never get **stuck on**. If the RunEngine process dies in a way it
cannot clean up after (a hard `kill -9`, a crash, the box losing power), the key
simply **expires within ~30 s** and the GUI unlocks itself. So:

* **Treat "key absent" as idle** — never cache a stale "busy".
* **Poll** the key (do not subscribe-and-cache); ~1–2 Hz is plenty.
* The 30 s TTL is the GUI's worst-case "stuck locked" window if a worker dies
  mid-plan. (If that ever needs to be shorter, it is a one-line change on the
  bluesky side — ask.)

### Value schema (JSON)

When present, the value is a JSON object:

```json
{
  "busy": true,
  "since": "2026-06-17T10:30:00.123456",
  "host": "xf12id2-ws3",
  "pid": 12345,
  "source": "RE",
  "expires_in": 30,
  "plan": "rel_scan",
  "scan_id": 412,
  "data_session": "pass-123456",
  "sample_name": "mysample_..."
}
```

| field | meaning |
|-------|---------|
| `busy` | always `true` when the key exists |
| `since` | ISO-8601 timestamp the plan started (local time) |
| `host`, `pid` | which worker holds it (for display / debugging) |
| `source` | `"RE"` |
| `expires_in` | the TTL in seconds (informational) |
| `plan`, `scan_id`, `data_session`, `sample_name` | best-effort context ("what is it busy with?"); any may be missing/`null` |

> The flag is **read-only** from the GUI's side — the RunEngine is the sole writer.
> Do not write `re_busy` from the GUI.

### Recommended GUI logic

```python
import json

def re_is_busy(r):
    """True if the RunEngine is running a plan (GUI should lock out moves)."""
    raw = r.get("swaxsstatus:re_busy")
    if raw is None:
        return False                      # absent -> idle (safe default)
    try:
        return bool(json.loads(raw).get("busy", True))
    except (ValueError, TypeError):
        return True                       # present but unparseable -> assume busy

def re_busy_details(r):
    """The busy payload dict (for a status line), or None if idle."""
    raw = r.get("swaxsstatus:re_busy")
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return {"busy": True}
```

Gate every "small move" action behind `re_is_busy(r)`; disable the relevant
buttons and (optionally) show `re_busy_details(r)` ("Busy: `rel_scan` (scan 412)
since 10:30") so the user knows why.

Polling pattern (Qt example sketch):

```python
# in the GUI: a ~1 Hz timer
def _tick(self):
    busy = re_is_busy(self.r)
    self.move_buttons.setEnabled(not busy)
    self.status_label.setText("RE busy" if busy else "RE idle")
```


## `beam_down` — operator mode (display / optional control)

### Semantics

* **Persistent** (written with `SET`, **no TTL**). It is an operator mode: set it
  once and it survives RunEngine / worker restarts until explicitly cleared.
* It is read **once, at profile startup**, by the suspender setup: if set, the
  ring-current / shutter / temperature suspenders are **built but not enabled**, so
  restarting bluesky during a beam-down does not immediately pause everything.
* It does **not** live-toggle already-running suspenders — it only affects the
  **next** startup.

> Because it persists, after using `start-beamdown` the suspenders stay disabled on
> every subsequent start until someone clears it (`beam-up` task or
> `clear_beam_down()` in a session).

### Value schema (JSON)

```json
{
  "beam_down": true,
  "since": "2026-06-17T09:00:00.000000",
  "host": "xf12id2-ws3",
  "by": "operator",
  "reason": "scheduled shutdown"
}
```

`reason` and `by` are optional.

### GUI usage

Read-only display is the simplest integration:

```python
def beam_is_down(r):
    raw = r.get("swaxsstatus:beam_down")
    if raw is None:
        return False
    try:
        return bool(json.loads(raw).get("beam_down", False))
    except (ValueError, TypeError):
        return True
```

If the GUI offers a **set/clear control**, write the same schema. Set (persistent —
note `set`, **not** `setex`):

```python
import datetime, socket

def set_beam_down(r, reason=None, by="gui"):
    doc = {"beam_down": True,
           "since": datetime.datetime.now().isoformat(),
           "host": socket.gethostname(), "by": by}
    if reason:
        doc["reason"] = reason
    r.set("swaxsstatus:beam_down", json.dumps(doc))   # NO ttl -> persistent

def clear_beam_down(r):
    r.delete("swaxsstatus:beam_down")
```

> A change to `beam_down` only takes effect on the **next** bluesky startup, so the
> GUI should make clear this is a "for the next restart" setting, not a live toggle.


## Quick reference

| | `re_busy` | `beam_down` |
|---|---|---|
| key | `swaxsstatus:re_busy` | `swaxsstatus:beam_down` |
| Redis db | 3 | 3 |
| set with | `SETEX` (TTL ~30 s) | `SET` (no TTL) |
| absent means | RE idle (GUI may move) | beam not flagged down |
| GUI should | **poll** ~1–2 Hz; gate moves | display; optionally set/clear |
| writer | RunEngine (read-only for GUI) | operator / GUI / `start-beamdown` |
| top-level JSON flag | `"busy"` | `"beam_down"` |

CLI helpers (on a machine with the profile on `PYTHONPATH`/`src`):

```bash
pixi run beam-down     # set the persistent beam_down flag
pixi run beam-up       # clear it
pixi run beam-status   # print beam_down + re_busy
```
