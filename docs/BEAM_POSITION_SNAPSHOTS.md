# Beam Position Snapshots

Status: **NEEDS LIVE TESTING**. Offline tests cover snapshot capture, motor batching,
energy/BPM3 gain restore ordering, harmonic recording, shutter/feedback state, XBPM
restoration, and bimorph diagnostics. These expanded restore paths still need live validation.

The beam-position snapshot helpers live in `smi_beamline.plans.beam_snapshot` and are loaded into
the collection namespace by the device factory.

## Tested Scope

Minimal live testing on 2026-07-03 confirmed:

- `save_beam_position_snapshot(...)` saves the current beam-positioning state to `mdsave`.
- `list_beam_position_snapshots()` lists the saved snapshot index.
- `restore_beam_position_snapshot(..., dry_run=True)` reports a selected changed motor as
  `would move` without moving hardware.
- `restore_beam_position_snapshot(..., dry_run=False)` restores a selected motor to the saved
  snapshot value.
- Bimorph restore uses the dedicated bimorph target/apply helpers, not motor-style moves.

Offline coverage lives in `tests/unit/test_beam_snapshot.py` and
`tests/unit/test_bimorph_debug.py`; run it with Pixi as described in [TESTING.md](TESTING.md).

## Current Behavior

Save a snapshot:

```python
snap = save_beam_position_snapshot(
    "beam_test_2026_07_03",
    note="first live beam position snapshot test",
)
```

List saved snapshots:

```python
list_beam_position_snapshots()
```

Dry-run restore a single item:

```python
restore_beam_position_snapshot(
    "beam_test_2026_07_03",
    names=["wbs.h"],
    dry_run=True,
)
```

Apply restore for a selected item:

```python
RE(restore_beam_position_snapshot(
    "beam_test_2026_07_03",
    names=["wbs.h"],
    dry_run=False,
))
```

## Readable comparison and dry-run reports

Comparison and restore previews now lead with counts for the selected values:
unchanged, would change, and other differences needing review. Unchanged rows
are hidden by default. Changes and review items use boxed, aligned columns for
setting name, current value, saved/target value, delta, units, and status.
Long values wrap rather than overflowing columns or being silently truncated.
Narrow terminals use a vertical field/value box for each setting.

```python
# Assign the result so IPython does not echo the entire returned list as well.
rows = restore_beam_position_snapshot("good_focus", dry_run=True)
rows = compare_beam_position_snapshot("good_focus")

# Opt in to the full table, including unchanged values.
rows = restore_beam_position_snapshot("good_focus", show_unchanged=True)
```

These are display changes only: all selected rows are still returned, and
selection, tolerance, restoration eligibility, batching, shutter/feedback
behavior, and default dry-run safety are unchanged. Comparison deltas retain
their existing current-minus-saved sign; restore deltas are target-minus-current.
The report labels a non-dry-run preview as a plan, not completed restoration.

Missing values, failed readbacks, nonfinite values, and read-only differences
remain visible under review items; they are never counted as verified unchanged.
An unknown current value is shown for review even if the existing restoration
policy schedules it as `would move`. This presentation does not add a new
execution guard: resolve such uncertainty before explicitly executing a restore.
Matching read-only settings are counted as unchanged but remain excluded from
restoration by the existing policy. Group metadata remains in the returned rows.
No camera overlay fields are added to snapshots by this display change.

## Restore Rules

- New snapshots (schema version 3) contain 85 items, including all 17 CRL motors,
  photon energy in eV
  (`energy.energy`, group `energy`) and BPM3 gain/range (`xbpm3.range`, group `diagnostics`),
  using `XF:12IDB-BI:2{EM:BPM3}Range`.
- DCM pitch and roll were already captured; they are now restorable, including from older
  snapshots marked `restore=False`.
- Before any selected restore changes, disable both DCM feedback loops, wait the established
  3-second dwell, then close and wait for `ph_shutter` (`XF:12IDA-PPS:2{PSh}`) to confirm closed
  (30-second wait timeout). Dry runs and restores with no changes do not operate these controls.
- Restore photon energy first using the existing `Energy.forward()` calculation and real-axis
  moves. This avoids the normal energy-move callback re-enabling feedback and avoids the
  beam-dependent managed-energy preprocessor. IVU moves retain brake confirmation/retry.
  The calculation uses the current harmonic/configuration and respects `enableivu` and
  `enabledcmgap`; these configuration settings are not restored from the snapshot.
  An active harmonic lock is respected. After successful IVU motion, the harmonic record is
  updated explicitly (the forward calculation itself does not change configuration).
- Restore BPM3 range next, with exact enum matching (not positional tolerance).
- Motors are restored with one concurrent Bluesky `bps.mv` per nonempty batch, waiting for
  completion before starting the next batch:
  1. DCM pitch and roll.
  2. Slit centers (`h`, `v`) across WBS, SSA, ESLIT, and CSLIT.
  3. Slit gaps (`hg`, `vg`) across those slits.
  4. Mirror translations (`x`, `y`) across HFM, VFM, and VDM.
  5. Mirror pitch (`th`) across those mirrors.
  6. XBPM2 and XBPM3 positions (`x`, `y`, in the `diagnostics` group).
  7. CRL body (`x`, `y`, `z`, `ph`, `th`, in the `crl` group).
  8. All twelve CRL holders (`lens1` through `lens12`, also in the `crl` group).
- Slit center and gap coordinates are kept in separate batches because they share blades.
- XBPM positions are restored from both new snapshots and older snapshots that incorrectly
  marked these motors `restore=False`. Comparison and dry-run tables reflect this correction.
- Raw Bragg, DCM gap, and IVU gap snapshot entries remain comparison-only; energy restoration
  calculates their targets rather than restoring those entries independently.
- Older snapshots do not contain photon energy or BPM3 gain. They remain readable, but these
  missing settings cannot be restored; save a new snapshot to capture them.
- Snapshots from before schema version 3 have no CRL positions. Comparing them reports CRLs
  as `missing saved`; restoring them does not move the CRLs.
- `names`, `groups`, `exclude`, and `tolerance` still limit which moves enter each batch.
- Bimorph voltages are restored after the motor batches with `move_voltages()`. Its uniform-offset
  fast path writes `SET-ALLSHIFT`; otherwise, it stages targets sequentially through `SET-VTRGT<n>`
  and triggers `SET-ALLTRGT`. The selected path depends on the requested and current outputs, so a
  restore may write either action PV. Both paths verify the output readbacks.
- For partial bimorph restores, unselected channels are staged from current outputs before apply;
  this avoids applying stale target values to unselected channels.
- Restore leaves the photon shutter closed and feedback disabled. It does not automatically
  reopen the shutter or re-enable feedback, including if a restore fails after closure.

## Recording a Good CRL Focus

A good-focus record is a **full beam-position snapshot**, including mirror positions and
bimorph voltages, energy, SSA and other slit settings, BPM settings, and CRL positions.
It uses the same Redis-backed `mdsave` storage, listing, comparison, and restore helpers.
Readbacks are collected sequentially; save after alignment motion has settled.

```python
snap = save_beam_position_snapshot(
    "good_focus_16p1keV_2026_10_15_1430",
    crl_inserted=[3],
    note="Best focus at sample with holder 3; alignment optimized",
)
```

Each record includes its creation timestamp, operator, and note. Use a unique dated name
for each good alignment: saving an existing name replaces that record. Omitting the name
generates a name with the current date and time (to the second).

All CRL body coordinates (`x`, `y`, `z`, `ph`, `th`) and all twelve holder readbacks are
saved in `items`. The additional `crl_alignment` metadata records each holder's IN/OUT/UNKNOWN
state and the measured `in_mm` for IN holders. `crl_inserted=[3]` explicitly declares holder 3
IN and the other holders OUT; `crl_inserted=[]` declares all OUT. If omitted, the states use
the device's current zero-centered insertion tolerance (normally `abs(readback) < 3 mm`).
The record identifies whether these states were operator-declared or inferred. Unreadable
or nonfinite positions are UNKNOWN, even when declared IN, and have no recorded IN position.

```python
snap["crl_alignment"]
list_beam_position_snapshots()
compare_beam_position_snapshot(snap["snapshot_name"])

# Preview the full beam alignment, including mirrors, SSA, energy, and CRLs.
restore_beam_position_snapshot(snap["snapshot_name"])

# Restore that full alignment.
RE(restore_beam_position_snapshot(snap["snapshot_name"], dry_run=False))
```

Restoration uses the exact saved motor readbacks for every holder, including OUT positions;
it does not substitute nominal IN/OUT positions. The IN annotations retain the measured
alignment context without changing the global nominal holder inventory. Existing selection
filters apply: for example, `groups=["crl"]` limits a preview or restore to CRL motors.

## Diagnosing Bimorph Writes

Enable timestamped diagnostics for a restore:

```python
RE(restore_beam_position_snapshot(
    "beam_test_2026_07_03",
    groups=["mirror_voltages"],
    dry_run=False,
    bimorph_debug=True,
))
```

To isolate staging, copy one mirror's live outputs into its targets without sending apply:

```python
targets = hfm_voltage.read_outputs()
RE(hfm_voltage.set_targets(targets, debug=True))
```

Repeat with `vfm_voltage` to check the other controller. This writes staged targets; it does not
trigger a voltage ramp. It exercises the write path even if the snapshot restore would skip
unchanged channels. A test with targets already matching readbacks does not prove that a changed
target would be accepted.

Diagnostics go to stderr with immediate flushing, alongside CA exceptions. They include:

- Mirror, channel, attempt, write PV, requested voltage, and put-completion configuration.
- Write dispatch and asynchronous status completion (including failures).
- Each target readback, error from requested voltage, stable-read count, and elapsed time.
- Verification retries/timeouts and stage completion.
- Separate apply-write and settling markers when apply is requested.

Debug mode leaves CA messages unsuppressed during writes. An asynchronous status/CA error can
appear after the write-dispatch marker; target acceptance is checked independently through
`GET-VTRGT`. Save output from `STAGE begin` through the error and subsequent verification lines.

The named-state helpers also accept `debug=True`: `stage_bimorph`, `apply_bimorph`, and
`load_bimorph`. Defaults remain quiet. Load the updated code in the profile before testing;
reloading only the snapshot module will not update existing bimorph device methods.

## Pending Testing

- [ ] CRL body/holder capture, insertion annotations, and full-alignment restore under live conditions.
- [ ] New snapshot energy (eV), BPM3 range enum, pitch, and roll values against live readbacks.
- [ ] Feedback disables before shutter closure; closure is confirmed before any restore motion.
- [ ] Closed-shutter energy restore with managed-energy preprocessing installed: feedback stays
      off, no beam-dependent alignment/ranging occurs, and Bragg/DCM/IVU reach expected targets.
- [ ] BPM3 gain and DCM pitch/roll restoration, including old-snapshot pitch/roll compatibility.
- [ ] Motor batches and XBPM positions under live conditions.
- [ ] Bimorph staging diagnostics and the reported CA exceptions; full/partial voltage restore.
- [ ] Selection filters, dry runs, no-op restores, shutter timeout, failed/interrupted restore,
      and final shutter-closed/feedback-off state.
- [x] Run offline snapshot and bimorph coverage, including energy/gain restore ordering.
