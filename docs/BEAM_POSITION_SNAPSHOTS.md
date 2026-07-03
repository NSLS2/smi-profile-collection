# Beam Position Snapshots

Status: done for the initial commissioning scope; waiting for more extensive in situ testing.

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

Unit coverage exists in `tests/unit/test_beam_snapshot.py` for save, compare, motor restore, and
selected bimorph-channel restore behavior.

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

- Slit and mirror motors marked `restore=True` are restored with Bluesky `bps.mv`.
- DCM, energy, undulator, and XBPM diagnostic axes are saved for comparison but are not restored.
- Bimorph voltages are restored through `read_outputs()`, `set_targets(...)`, and
  `apply_and_wait()`.
- For partial bimorph restores, unselected channels are staged from current outputs before apply;
  this avoids applying stale target values to unselected channels.

## Remaining Work

The snapshot project is considered complete for initial deployment.  Remaining work is broader
in situ validation across realistic beamline recovery cases, especially full-mirror bimorph
restores and mixed motor/bimorph restore sequences.
