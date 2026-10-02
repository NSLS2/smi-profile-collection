# Bimorph voltage moves

`load_bimorph(name)` now uses the device's `move_voltages()` plan for each mirror:

```python
RE(load_bimorph("tender"))
RE(hfm_voltage.move_voltages(target_voltages))  # 16 absolute target voltages
```

## Uniform-shift fast path (default)

1. Read all 16 actual `GET-VOUT<n>` values and `GET-STATUS<n>` states.
2. Require finite outputs and all channels `On` before moving.
3. Compute requested-minus-current voltage for every channel. If one common
   shift predicts **every target within 0.5 V**, write that shift once to
   `HFM:SET-ALLSHIFT` or `VFM:SET-ALLSHIFT`. The common shift is the midpoint of
   the smallest and largest differences, minimizing the worst-channel error.
4. Confirm all 16 actual outputs within 0.5 V of their requested absolute
   targets and all states `On`, continuously across a 1 s sampled settling window.

Already-matching outputs are verified without a write. If the requested shape
is not a uniform offset, the existing sequential `SET-VTRGT<n>` staging and
`SET-ALLTRGT` apply path is used, followed by the same output verification.

This avoids the per-channel staging delay for the usual common-offset change.
It does not rely on catching a brief `Busy` transition or on an action PV's
stored value. Repeated identical shifts on separate calls are each issued.

```python
RE(load_bimorph("tender", use_shift=False))
RE(vfm_voltage.move_voltages(targets, use_shift=False, debug=True))
```

`use_shift=False` forces stage/apply when motion is needed. Direct device calls
also accept `tolerance`, `settle`, `timeout`, and `poll` (defaults: 0.5 V, 1 s,
120 s, and 0.5 s). Timeout covers verification; sequential staging retains its
existing separate per-channel timeouts/retries.

## Failure and staging behavior

- A relative action is never automatically retried, including after an ambiguous
  write error, and never falls back to a second move after it has been dispatched.
  Verification failure reports the output differences and channel states.
- The RE checkpoint is cleared before the relative write so interruption cannot
  replay it. An immediate pause at that point cannot be resumed from an earlier
  checkpoint. Inspect the outputs and deliberately reissue the desired absolute
  targets after resolving the interruption.
- `stage_bimorph`, `set_target`, `set_targets`, and `sync_targets_to_outputs`
  remain staging-only. They never issue `SET-ALLSHIFT`.
- The fast path does not separately write the staged target registers or send
  `SET-ALLTRGT`. Its completion criterion is the actual outputs. Use an explicit
  staging operation before a later manual apply if staged targets need replacing.
- `move_abs()` for each mirror and beam-snapshot restores also use
  `move_voltages()`. Partial-channel snapshot restores still build a complete
  target vector preserving unselected channels.

These paths are tested with simulated outputs and delayed/no-response cases.
Beamline staff tested the automatic selection and confirmed it working on 2026-10-02.
