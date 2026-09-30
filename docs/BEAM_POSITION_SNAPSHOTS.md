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

## Restore Rules

- New snapshots (schema version 2) contain 68 items, including photon energy in eV
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
- Slit center and gap coordinates are kept in separate batches because they share blades.
- XBPM positions are restored from both new snapshots and older snapshots that incorrectly
  marked these motors `restore=False`. Comparison and dry-run tables reflect this correction.
- Raw Bragg, DCM gap, and IVU gap snapshot entries remain comparison-only; energy restoration
  calculates their targets rather than restoring those entries independently.
- Older snapshots do not contain photon energy or BPM3 gain. They remain readable, but these
  missing settings cannot be restored; save a new snapshot to capture them.
- `names`, `groups`, `exclude`, and `tolerance` still limit which moves enter each batch.
- Bimorph voltages are restored through `read_outputs()`, `set_targets(...)`, and
  `apply_and_wait()` after the motor batches. These are the same device helpers used by
  `load_bimorph(...)`: stage and verify targets sequentially within each mirror, then trigger
  apply and wait for settling. The controller requires sequential target staging; live testing
  found that batched channel writes could leave targets stale.
- For partial bimorph restores, unselected channels are staged from current outputs before apply;
  this avoids applying stale target values to unselected channels.
- Restore leaves the photon shutter closed and feedback disabled. It does not automatically
  reopen the shutter or re-enable feedback, including if a restore fails after closure.

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
