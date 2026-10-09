# Writing energy scans with a single undulator harmonic

Changing undulator harmonic can introduce a large intensity step during an energy
scan. Use `with_harmonic_lock` to choose one harmonic for the entire scan and keep
ordinary energy moves on it. All energies below are **eV**, and IVU gaps/margins are
**µm**. These helpers are available in the live profile namespace after startup.

## Recommended: wrap the acquisition plan

```python
import bluesky.plans as bp

RE(with_harmonic_lock(
    bp.scan([pil2M], energy, 8000, 9000, 101),
    start=8000,
    stop=9000,
))
```

The wrapper:

1. Selects and validates a harmonic for the whole interval before motion.
2. Moves to `start` using the existing setting (normally automatic selection).
   This allows an approach from an energy outside the selected harmonic's range.
3. Sets the lock and moves at `start` again to establish the selected IVU gap,
   even if the monochromator is already at that energy.
4. Runs the supplied plan with the lock active.
5. Restores the previous lock on normal completion, error, or RunEngine abort.

If a lock was already active, it is respected on the approach; an incompatible
approach raises rather than silently releasing it. Clear it explicitly before the
wrapper if automatic approach selection is wanted. Nested wrappers restore their
enclosing lock.

The wrapper returns the wrapped plan's return value. It requires `enableivu=True`.
It does not move back to the original energy or harmonic after acquisition:
restoring the lock is a configuration change only. The next normal energy move
uses the restored setting, including when commanded to the current energy.

### Inside your own plan

```python
def edge_scan(detectors, start, stop, num=101):
    # Configure detector exposure, sample position, etc. here.
    return (yield from with_harmonic_lock(
        bp.scan(detectors, energy, start, stop, num),
        start=start, stop=stop,
        gap_margin_um=100,
    ))

RE(edge_scan([pil2M], 8000, 9000))
```

Wrap the complete acquisition plan **outside** its `open_run`/`run_wrapper` so
positioning and harmonic establishment happen before the run opens. Use
`yield from` inside a plan, and `RE(...)` only at the console.

For library plans with an injected device, import the hardware-independent helper:

```python
from smi_beamline.plans.harmonic_lock import with_harmonic_lock

def edge_scan(detectors, energy, start, stop, num=101):
    return (yield from with_harmonic_lock(
        bp.scan(detectors, energy, start, stop, num),
        start, stop, energy=energy,
    ))
```

The imported helper requires `energy=...`; the live profile convenience function
supplies the beamline device automatically.

### Descending, list, and multi-segment scans

Descending ranges work directly; `start` is always the approach destination:

```python
RE(with_harmonic_lock(
    bp.scan([pil2M], energy, 9000, 8000, 101), 9000, 8000,
))
```

For a monotonic energy list, use its first and last points. For a nonmonotonic
list or multi-segment plan, supply an interval covering **all** requested energies
(including any overshoot or repositioning within the wrapped plan). Positioning
will first go to the supplied `start`, then follow the wrapped plan's moves.
The interval selects the harmonic; it is not an extra energy travel limit.
Moves outside it still obey the lock and raise if that harmonic cannot reach them.

## Preview or specify the harmonic

```python
h = energy.harmonic_for_range(8000, 9000)  # calculation only; no signal writes
h = energy.harmonic_for_range(8000, 9000, gap_margin_um=100)
h = energy.harmonic_for_range(8000, 9000, max_harmonic=7)
energy.harmonic_for_range(8000, 9000, harmonic=3)  # validate this exact choice

RE(with_harmonic_lock(
    bp.scan([pil2M], energy, 8000, 9000, 101),
    8000, 9000, harmonic=3,
))
```

The default preference is the **highest valid odd harmonic**, starting at
`energy.target_harmonic` (normally 21). This preserves the automatic move policy;
it is not a measured-flux optimization. `max_harmonic` overrides the search ceiling
without changing the device. `harmonic` requests an exact choice, and cannot be
combined with `max_harmonic`. The preview helper ignores any existing lock.

A suitable harmonic must satisfy `6200 <= gap < 15100` throughout the interval.
`gap_margin_um` shrinks both sides of that window for selection/validation. Moves
continue to enforce the normal gap limits, not the optional selection margin.
Selection uses the current offset table and the special correction below 3000 eV.
It checks offset breakpoints and both sides of discontinuities, and uses adaptive
interval bounds to detect excursions between them. Numerically unresolved
intervals narrower than 1e-6 eV are conservatively rejected. Avoid changing the
offset calibration during a scan; every move uses its current values.

If no harmonic covers the range, the helper/wrapper raises `RuntimeError` before
starting acquisition. Shorten the interval or split it into separately locked
scans. Invalid energies, harmonics, margins, or calibration tables raise
`ValueError`. Device energy guardrails remain `2050 < energy < 24001` eV; these
are not a statement of the beamline's validated operating range.

## Manual lock and individual moves

`energy.locked_harmonic` is a configuration signal:

| Value | Behavior |
|---|---|
| `0` (default) | Automatic downward search from `target_harmonic` at each move |
| Positive odd integer | Use exactly that harmonic; never fall back to another |

```python
import bluesky.plan_stubs as bps

# Approach first, then establish the chosen harmonic before acquisition.
h = energy.harmonic_for_range(8000, 9000)
RE(move_energy(8000))
RE(bps.mv(energy.locked_harmonic, h))
RE(move_energy(8000))
RE(move_energy(8500))
RE(bps.mv(energy.locked_harmonic, 0))  # resume automatic selection on next move
```

Set the lock and move the energy in **separate, waited operations**; do not put
both in a single `bps.mv` group. The scan wrapper handles this sequencing and
cleanup for you. Inside plans, use `bps.mv`/`move_energy`, not blocking
`energy.move(...)` calls or direct `.put()` writes.

The lock applies to `energy.move`, `energy.set`, `bps.mv(energy, ...)`, ordinary
Bluesky scans, and `energy_walk` (including managed intermediate steps). An
invalid locked target is rejected before device motion. `energy_walk` validates
the entire locked path before its first sub-step. `energy.small_move` requires
the locked harmonic to have already been established with a normal move; it
rejects a mismatch rather than changing harmonics during a synchronized nudge.
Direct moves of real axes such as `energy.ivugap` bypass this policy.

## Run records and interruption

Every run opened by the wrapped plan receives start-document metadata:

```python
{"harmonic_lock": {
    "harmonic": 5,  # illustrative; use the actual selected value
    "start_eV": 8000.0,
    "stop_eV": 9000.0,
    "gap_margin_um": 0.0,
}}
```

`locked_harmonic` is also included in the live energy device's configuration;
`harmonic` records the selected motion harmonic. Include `energy` in your read
devices if you need an explicit per-point harmonic record outside the live
profile's automatic energy recording. The wrapper owns the `harmonic_lock`
metadata key, overwriting any supplied value for that key.

A paused plan retains its lock so it can resume consistently. Completing the
plan or calling `RE.abort()` runs restoration. As with other Bluesky finalizers,
`RE.halt()` or terminating the process cannot guarantee cleanup. Inspect
`energy.locked_harmonic.get()` afterward and reset it with a waited plan operation
if needed. The lock is session configuration, not a persistent Redis setting.
