# DCM beam-position feedback & reliable energy moves — design and commissioning plan

**Status:** Part A (IVU brake fix) and Part B (managed `energy_walk` + per-energy BPM3 range,
installed by default via the energy-move preprocessor) are **implemented and live-validated 2.1 ↔
16.1 keV** (2.1 keV = beamline minimum) — see the §7 phase markers and §8 for what shipped vs the
original proposal. Still open: the Pilatus-threshold finishing touches (§11), moving calibration to
the Redis `_config` seam, and the OAV setpoint-calibration phase (§10). The architecture in §5 is
kept as the original proposal / future-refactor target.

**Scope.** Two related problems:

1. **(Part A — bug fix, low risk)** The undulator (IVU) gap does not always move on the first
   command during an energy change, so an energy move is currently unreliable.
2. **(Part B — larger project)** Automate large energy changes by managing the DCM pitch/roll
   beam-position feedback: progress in small steps, keep the beam centred, and re-centre the
   feedback piezos with the coarse in-vacuum motors before they run out of range — replacing the
   manual procedure used today.

---

## 1. Background: how an energy move works today

The photon energy is a `PseudoPositioner` (`energy`) over three real axes:

* `bragg` — DCM Bragg angle (`XF:12ID:m65`)
* `dcmgap` — DCM gap / height (`XF:12ID:m66`)
* `ivugap` — in-vacuum undulator (IVU) gap (`SR:C12-ID:G1{IVU:1-Ax:Gap}-Mtr`)

Code references:

* Device class: [`src/smi_beamline/devices/energy.py`](../src/smi_beamline/devices/energy.py)
  — `Energy` (`forward`/`inverse`/`set`/`small_move`).
* IVU motor class: [`src/smi_beamline/devices/machine.py`](../src/smi_beamline/devices/machine.py)
  — `InsertionDevice` (brake + gap-speed + `move`).
* Startup wiring: [`startup/smibase/energy.py`](../startup/smibase/energy.py)
  — `energy`, `dcm_pitch`, `feedback()`, `move_energy()`.

### The move choreography (`Energy.set`, energy.py:240)

1. Disable DCM pitch & roll feedback up front (`put("1", wait=True)`).
2. Start the pseudo move (`bragg`, `ivugap`, `dcmgap` concurrently).
3. Re-enable feedback from the move's completion callback (`_reenable_feedback`).
4. Return the move `Status`, which completes ~immediately when the underlying move finishes.

`small_move` (energy.py:288) is the exception: it moves only `bragg`+`ivugap` in lock-step and
**leaves feedback ON** because the step is small enough not to lose the beam.

---

## 2. Part A — the IVU "doesn't move the first time" bug

### Root cause

`InsertionDevice.move` (machine.py:42):

```python
def move(self, position, wait=True, **kwargs):
    self.brake.put(1, wait=True)          # waits only for the CA put ack
    return super().move(position, ...)    # issues the gap setpoint immediately
```

`self.brake.put(1, wait=True)` waits only for the **Channel Access put acknowledgement** (the
setpoint value landed), *not* for the mechanical brake to physically disengage and the readback
`BrakesDisengaged-Sts` to confirm. The gap setpoint is then issued while the IVU is still braked,
the controller drops the first motion command, and the motor record reports `DMOV` done (no
motion attempted). The ophyd `Status` "succeeds" with the gap never having moved — which is why a
second, manual move is needed. This exactly matches the operators' "move it twice" workaround.

### Fix: confirm the brake, then verify motion, retry once

In `InsertionDevice.move`, keep it **non-blocking / `Status`-chained** (the `Energy`
pseudo-positioner drives `ivugap.move(..., wait=False)` concurrently with bragg/dcmgap):

1. Write `BrakesDisengaged-SP = 1`.
2. Wait for `BrakesDisengaged-Sts == 1` (the `brake` Cpt's read PV), up to a timeout, **plus** a
   short configurable dwell (`brake_settle`, ~0.2 s) so the controller is genuinely ready.
3. Issue the gap move.
4. On completion, if `|readback − target|` exceeds the motor retry deadband, **re-issue once**
   (bounded by `max_move_attempts`, default 2). This keeps the manual "move twice" as an
   automatic safety net even if `BrakesDisengaged-Sts` reports disengaged optimistically.

Suggested new tunables (class attributes, so they are easy to adjust without code edits):

| Attribute | Default | Meaning |
|---|---|---|
| `brake_settle` | 0.2 s | dwell after `BrakesDisengaged-Sts == 1` before commanding motion |
| `brake_timeout` | 5 s | max wait for the brake-disengaged readback |
| `max_move_attempts` | 2 | re-issue the gap move if the readback didn't reach target |
| `move_deadband` | motor `RDBD` or a small um value | "did it actually move?" tolerance |

### Tests

Extend the existing sim IOC + integration tests (they already exercise the brake path):

* [`tests/iocs/sim_energy_ioc.py`](../tests/iocs/sim_energy_ioc.py) — model the failure: a brake
  that reports `disengaged` only after a delay, and an IVU motor that **ignores a setpoint issued
  while still braked** (drops the first move).
* [`tests/integration/test_energy_iocs.py`](../tests/integration/test_energy_iocs.py) — upgrade
  `test_ivu_brake_disengaged_before_move` to assert the gap actually *reaches target*, and add a
  test that a dropped first move is recovered by the retry.

### Risk

Low and self-contained — touches only `InsertionDevice.move`. Ship independently of Part B.

---

## 3. The DCM feedback system (as discovered)

### 3.1 Where the loops live

The fast beam-position feedback runs **entirely in the EPICS IOC** as two standard `epid`
records on BPM3. Bluesky today only toggles the two `..._incalc.CLCN` enable bits. The CS-Studio
panels under `~/git/cs-studio-xf/12id/feedback/` expose the full record.

**Axis convention (confirmed):** `fast_pidX` → **roll**, `fast_pidY` → **pitch**.

### 3.2 PID record fields (per loop)

For `<pid>` ∈ {`fast_pidX` (roll), `fast_pidY` (pitch)}, prefix `XF:12IDB-BI:2{EM:BPM3}`:

| Field | PV | Meaning | Use |
|---|---|---|---|
| `.VAL`  | `…<pid>.VAL`  | setpoint (writable) | target beam position |
| `.CVAL` | `…<pid>.CVAL` | readback / process variable | **is the beam centred?** error = `CVAL − VAL` |
| `.OVAL` | `…<pid>.OVAL` | PID **output → piezo command**, practical window **±4000** | **piezo headroom / "maxed out" detector** |
| `.FBON` | `…<pid>.FBON` | master feedback on/off | alternate enable |
| `.INP`  | `…<pid>.INP`  | input link (BPM3 position source) | config (read for provenance) |
| `.OUTL` | `…<pid>.OUTL` | output link (piezo target) | config (read for provenance) |
| `.SCAN` | `…<pid>.SCAN` | loop update rate | config |
| `_incalc.CLCN` | `…<pid>_incalc.CLCN` | the disable bit **bluesky uses today** ("0"=on, "1"=off) | enable/disable |

> **±4000 is a *practical working window*, not a hard rail.** The operators report the loop
> "stops working" — and may become nonlinear — once `OVAL` leaves roughly this range. The true
> drive limits (`.DRVH`/`.DRVL` or piezo voltage limits) are unknown and should be read on the
> live IOC during Phase 0. Until then, treat `|OVAL| ≳ 4000` as "out of range" and keep a healthy
> margin (e.g. act when `|OVAL| > 3000`).

**There is no separate piezo position readback** — `OVAL` is the only piezo-state signal, and it
*is* the "distance-to-rail" measurement the automation needs. So Part B is **not** blocked on PV
discovery.

### 3.3 Coarse (in-vacuum) DCM motors

From `~/git/cs-studio-xf/12id/op/WBS_DCM_SSA.bob` and `DCM_Cage.opi`:

| Motor | PV | Role | In bluesky |
|---|---|---|---|
| theta | `XF:12ID:m65` | Bragg | `energy.bragg`, `DCMInternals.theta` |
| height | `XF:12ID:m66` | DCM gap/height | `energy.dcmgap`, `DCMInternals.height` |
| **pitch** | `XF:12ID:m67` | coarse pitch (zeros the **Y/pitch** piezo) | `dcm_pitch`, `DCMInternals.pitch` |
| **roll** | `XF:12ID:m68` | coarse roll (zeros the **X/roll** piezo) | `DCMInternals.roll` (no standalone object yet) |

Each has soft limits `.HLM`/`.LLM`. Crystal temperatures:
`XF:12IDA-OP:2{Mono:DCM-Ax:P|R|Ygap}T:I-I`.

> **Terminology flag.** The CS-Studio feedback buttons are titled `VDM_BPM3_Fast_Feedback_X/Y`
> ("VDM" = vertical deflecting mirror), while the bluesky code names the loops DCM `pitch`/`roll`.
> The operators confirm **X↔roll, Y↔pitch** behaviourally, and that the coarse correction is the
> in-vacuum DCM motors m67/m68. The "VDM" label is noted only so a future reader is not confused;
> Phase 0 should confirm the physical actuator chain on the live system.

### 3.4 Beam intensity (feedback denominator)

`xbpm3` = `XBPM("XF:12IDB-BI:2{EM:BPM3}")`
([`startup/smibase/electrometers.py`](../startup/smibase/electrometers.py)):
`sumX`, `sumY` (intensity), `posX`, `posY` (position). Intensity is the PID's effective
denominator, so when it drops (during a large bragg/undulator move) the position error becomes
noisy/huge and the loop slams the piezo — the reason feedback is kept **off** during large moves.

### 3.5 The physics, in one paragraph

A large energy change moves the optics enough that the piezo correction needed to re-centre the
beam exceeds the piezo's working range (`|OVAL|` hits ~±4000). Manually, the operator nudges the
**coarse** in-vacuum pitch/roll motors (m67/m68) so the piezo can return to mid-range, then the
fast loop dials the beam in. If feedback is left ON while bragg+undulator move, intensity drops
too fast, the loop goes unstable, and the beam is lost. Hence today's rule: feedback ON only for
*small* moves; large moves are done manually.

---

## 4. Part B — automated "slow progression" energy move

### 4.1 Target plan

A message-pure bluesky plan, e.g. `energy_walk(target_eV)`:

```
while |E − target| > tol:
    step = choose_step(E, target, last_intensity, last_headroom)   # adaptive
    feedback OFF
    move bragg + IVU by `step`, in lock-step (à la small_move; keeps flux up)
    feedback ON
    wait until centred:   |CVAL − VAL| < pos_window  AND  sum > intensity_thresh
    if near rail (|OVAL| > oval_margin):
        with feedback ON, drive coarse m67/m68 to push OVAL back toward 0
        wait until |OVAL| < oval_ok  AND  beam still centred
verify centred at target; leave feedback ON
```

* `choose_step` shrinks when intensity would drop too far or piezo headroom is low.
* The coarse-recentre step runs **with feedback ON** so the loop holds the beam while the piezo
  hands off range to the coarse motor.
* Direction & magnitude of the coarse move come from the **m67/m68 → OVAL calibration** measured
  in Phase 0 (see §6). Getting the sign wrong drives the piezo *into* the rail and loses the
  beam — this is the single most safety-critical number.
* **Wrong-way abort, with a noise tolerance.** The recentre judges the *settled* OVAL direction; a
  step that moves OVAL *away* from 0 aborts **immediately only if it is large**
  (`|dOVAL| >= wrong_way_oval`, default 500) — a genuine sign/coupling error. A *small* wrong-way
  move is treated as OVAL noise / motor hysteresis (the pitch loop in particular is jumpy) and
  **forgiven up to `wrong_way_max` (default 2) times in a row** — a correct step resets the count,
  and a bigger corrective step usually wins on the retry. This stopped spurious aborts like
  `pitch: settled OVAL +4528 → +4648 (dOVAL +120)` seen on small steps, while still bailing out
  fast on a real sign error.
* **Per-energy BPM3 range (gain).** As each sub-step lands — *before* the flux gate and recentre —
  `energy_walk` sets the BPM3 electrometer range to match the new energy band and confirms it via
  `Range_RBV`, so the sum/position are on the right scale (low energy = more flux = coarser range;
  high energy = less flux = finer range):

  | photon energy | BPM3 range | enum index (0-based) |
  |---|---|---|
  | `< 10 keV`   | 1000 µA | 3 |
  | `10–12 keV`  | 100 µA  | 2 |
  | `>= 12 keV`  | 10 µA   | 1 |

  Index map confirmed on the live IOC ("100 µA" reads back as `2`). PVs: `…{EM:BPM3}Range` (mbbo,
  write) / `…Range_RBV` (mbbi, read). Table lives in `DEFAULT_RANGE_TABLE`
  (`dcm_diag.range_index`); disable with `energy_walk(..., set_bpm3_range=False)`.
* **Low-energy specialisation (validated to the 2100 eV beamline minimum).** Two things change at the
  very low end:
  * **Sub-step size:** `step_eV` is the nominal 500 eV down to `LOW_ENERGY_STEP_BELOW_eV` (2500 eV),
    then **50 eV** (`LOW_ENERGY_STEP_eV`) below it; a boundary-crossing move **lands exactly on
    2500 eV** before switching.  E.g. `5000 → 2100`: 500 eV steps to 2500, then 50 eV steps to 2100.
    The preprocessor also routes a move through `energy_walk` (not a plain set) whenever it sits
    in/enters the `< 2500 eV` region with a span larger than 50 eV, so the fine stepping is enforced
    even for otherwise-"small" low-energy moves.
  * **Flux gate floor:** the BPM3-sum threshold drops to **5** below **2.2 keV** (there is simply
    less flux on BPM3 there); the bands are now `<2.2 keV → 5`, `2.2–8 → 10`, `8–10 → 5`,
    `10–12 → 1`, `≥12 → 0.1` (`DEFAULT_FLUX_TABLE`).

### 4.2 Replacing the Part-A2 "blind settle"

Originally we considered a fixed ~3 s wait after re-enabling feedback. The better, now-feasible
approach is a **wait-until-centred-or-timeout**: poll `|CVAL − VAL|` and `sum` until the beam is
centred and bright, with a max timeout and a minimum dwell. This is the per-step settle used by
`energy_walk` and can also replace the settle inside `Energy.set`.

---

## 5. Proposed code architecture (for Part B)

> **As built (status).** Part B shipped along a lighter path than the `DCMFeedback` device proposed
> below, and is now the **default**:
> * `smi_beamline.plans.dcm_diag.DCMDiag` holds the feedback/OVAL/BPM3/coarse-motor signals + the
>   measured signs, rails, recenter windows, and the flux / BPM3-range tables (rather than a new
>   `DCMFeedback` ophyd device).
> * `smi_beamline.plans.energy_walk.energy_walk` is the managed move (the §4.1 choreography,
>   including per-energy BPM3 range).
> * `smi_beamline.plans.energy_move_preprocessor` routes >500 eV plan moves through it; **installed
>   by default at startup** (`startup.py` → `smibase.energy.enable_managed_energy_moves()`), with a
>   console `disable_managed_energy_moves()` escape hatch.  It also runs a **small-move drift guard**:
>   after a small (≤ threshold) move it checks each axis' OVAL against its recentre window and, if a
>   run of small moves has crept it toward the rail, recentres that axis (feedback ON) — so
>   fine-step scans can't silently walk pitch/roll into the piezo rail.
> * Calibration still lives in code constants for now (the Redis `_config` seam in §5.3 remains the
>   intended next home — see Open items).
>
> The original proposal is kept below as the fuller design / future-refactor target.

### 5.1 New device: `DCMFeedback`

New file `src/smi_beamline/devices/dcm_feedback.py` — `DCMFeedback(Device)` centralising the
feedback signals (today they are two bare PVs inside `Energy`). Per axis (roll=X, pitch=Y):

* `enable` (the `_incalc.CLCN` bit; preserve current "0"/"1" semantics) and optionally `fbon`
  (`.FBON`).
* `setpoint` (`.VAL`), `readback` (`.CVAL`), `output` (`.OVAL`).
* coarse motor (`pitch`=m67, `roll`=m68; reuse `DCMInternals`).
* references to `xbpm3` intensity.
* derived helpers: `error()`, `headroom()` ( `1 − |OVAL|/OVAL_RANGE` ), `near_rail(margin)`,
  `is_centered(pos_window, intensity_thresh)`.
* thresholds/calibration loaded from Redis via the existing `_config` seam (see §5.3).

### 5.2 New plan: `energy_walk`

New file `src/smi_beamline/plans/energy_walk.py` — the progression loop plus a manual,
operator-invoked `recenter_piezo()` single-step plan (used heavily in Phase 3). Compose from
`bps` stubs so it runs under the RunEngine and queueserver. Reuse `bpp.finalize_wrapper` (as
`small_move` already does) so any abort restores feedback state and axis speeds.

### 5.3 Persistence of thresholds / calibration

Use the existing Redis-backed config seam already used for the IVU gap-offset table
(`_config.load(...)` in energy.py:106). Store: `OVAL` range/margins, `pos_window`,
`intensity_thresh`, and the **m67/m68 → OVAL gain & sign** per axis. This keeps them editable
without code changes and recorded in every run as device config.

### 5.4 Wiring & exposure

* `Energy.set` / `small_move` consume `DCMFeedback`; the blind settle becomes wait-until-centred.
* `startup/smibase/energy.py` exposes `energy_walk`, `recenter_piezo`, and the thresholds.
* `startup/user_group_permissions.yaml` exposes the new plans to the queueserver
  (alongside the existing `feedback` / `shopen` entries).

### 5.5 Test scaffolding

Extend [`tests/iocs/sim_energy_ioc.py`](../tests/iocs/sim_energy_ioc.py) to model the loop:

* a BPM3 intensity (`sumX/sumY`) that **falls as bragg/IVU detune** from the flux peak,
* a `CVAL` position error driven by pitch/roll detuning,
* a `fast_pidX/Y` loop that, **when enabled**, drives `OVAL` to null the error and **saturates at
  the working-range limit**,
* the **coarse-motor ↔ OVAL coupling** (moving m67/m68 offsets the needed `OVAL`).

This lets `energy_walk` (step sizing, recentre logic, abort/finalize) be tested off-beam before
any commissioning shift.

---

## 6. Complexities / risks to resolve

| # | Complexity | Mitigation |
|---|---|---|
| 1 | **m67/m68 → OVAL sign & gain** unknown; wrong sign drives the piezo into the rail and loses beam | Measure in Phase 0 (read-only logging); verify on sim IOC; first live use is operator-supervised single steps |
| 2 | **True piezo limits unknown** (±4000 is practical, possibly nonlinear beyond) | Read `.DRVH/.DRVL`/voltage limits on the live IOC in Phase 0; until then act with margin (`|OVAL| > 3000`) |
| 3 | **Intensity as denominator** → loop unstable at low flux | Define an intensity floor; bound max step so intensity never drops below it; keep feedback OFF during the actual axis motion |
| 4 | **Defining "centred" & "healthy"** | Calibrate `pos_window`, `intensity_thresh`, `oval_margin` in Phase 0; persist via `_config` |
| 5 | **Suspender interaction** — BPM3-sum and ring-current suspenders may pause the run on legitimate dips during a walk | Run the walk with the BPM3 suspender relaxed/managed; coordinate thresholds; document |
| 6 | **Abort / finalize safety** — an interrupt must leave feedback + speeds in a known state | Reuse `finalize_wrapper` (proven in `small_move`); explicit known-good teardown |
| 7 | **Termination guards** | Max step count, per-step timeout, coarse-motor limit handling (m67/m68 `.HLM/.LLM`), loss-of-beam abort |
| 8 | **Sim fidelity** | The more faithful the loop model, the more is de-risked before beam time; treat the sim IOC as a first-class deliverable |
| 9 | **Actuator-chain confirmation** ("VDM" vs DCM labelling) | Confirm physically in Phase 0 |

---

## 7. Phased commissioning plan

**Phase 0 — Instrument & characterise (read-only, no beam risk).**
Add a logger that records `fast_pidX/Y.{VAL,CVAL,OVAL}`, `xbpm3.sum{X,Y}`/`pos{X,Y}`, and
`m67`/`m68` during *normal manual* energy changes. Read the true `OVAL` drive limits and the
`.INP/.OUTL` links on the live IOC. Confirm the actuator chain. **Deliverables:** intensity-vs-
detuning curve, `OVAL`-per-eV, and the **m67/m68 → OVAL sign + gain** calibration; safe threshold
values. Persist them via `_config`.

**Phase 1 — Ship Part A. ✅ DONE.** Implement the IVU brake-confirm + verify/retry fix and its tests.
Independent, low risk, immediately improves energy-move reliability.

**Phase 2 — `DCMFeedback` device + passive centring check.** Add the device; after each move,
*log* whether the beam is centred and the piezo headroom — **take no action**. Validates the
thresholds against reality. Optionally replace the `Energy.set` settle with wait-until-centred.
*(Shipped as the read-only `DCMDiag` snapshot/`measure_gain`/supervised `recenter` rather than a
new device.)*

**Phase 3 — `recenter_piezo()` single step (supervised). ✅ DONE** (`DCMDiag.recenter`). Operator-
invoked plan that, with feedback ON, drives m67/m68 to push `OVAL` toward 0. Validated the most
safety-critical calibration (#1) at the console.

**Phase 4 — `energy_walk` (automated progression). ✅ DONE.** Chained steps + recentre on the
extended sim IOC first; then with beam over progressively larger spans. **Live-validated 2.1 keV ↔
16.1 keV, up and down** (2.1 keV = beamline minimum; with the small-wrong-way recentre tolerance and
the low-energy 50 eV stepping / flux floor below).

**Phase 5 — Integrate & expose. ✅ DONE (default).** Folded in via the managed-move preprocessor —
installed by default at startup so every plan's >500 eV energy move uses `energy_walk`; console
`disable_managed_energy_moves()` opts out.  *Remaining:* the Pilatus-threshold finishing touches
(§11), move calibration to the Redis `_config` seam, and the §10 OAV setpoint-calibration phase.

---

## 8. Decisions captured

* **X = roll, Y = pitch** (confirmed by operators; behavioural and matches code naming).
* **±4000 `OVAL` is a practical working window**, not a verified hard limit; may be nonlinear
  beyond. True limits TBD in Phase 0; act with margin until then.
* Coarse re-centring uses the **in-vacuum DCM motors m67 (pitch) / m68 (roll)**.
* Part A (IVU brake fix) is **independent** and shipped first.
* **Per-energy BPM3 range (gain)** is set inside `energy_walk` per sub-step (table in §4.1).
* **Recentre wrong-way abort tolerates small noise:** abort immediately only on a *large* wrong-way
  step (`|dOVAL| >= wrong_way_oval`, default 500); forgive up to `wrong_way_max` (default 2) small
  ones in a row (pitch loop is jumpy / hysteretic). See §4.1.
* **Small-move drift guard:** the preprocessor recentres pitch/roll after a small move if OVAL has
  drifted past its window, so successions of small moves can't creep into the rail. See §5.
* **Low-energy specialisation:** 50 eV sub-steps below 2500 eV (lands on the boundary first) and a
  BPM3 flux floor of 5 below 2.2 keV; the preprocessor enforces the fine stepping for low-energy
  moves even when ≤500 eV. See §4.1.
* The managed-move preprocessor is **installed by default** at startup (`>500 eV` plan moves use
  `energy_walk`; smaller moves stay plain, with the low-energy enforcement above);
  `disable_managed_energy_moves()` is the escape hatch.
* **Live-validated** end-to-end **2.1 keV ↔ 16.1 keV, up and down** (2.1 keV = beamline minimum;
  managed move + 500/50 eV stepping + per-energy range; small wrong-way noise no longer trips the
  recentre).
* Calibration (signs/rails/windows/flux table/range table/step bands) currently lives in code
  constants; the Redis `_config` seam (§5.3) is the intended next home.

## 9. Open items for Phase 0

1. True piezo/`OVAL` drive limits (`.DRVH`/`.DRVL` or voltage) on the live IOC.
2. Confirm the physical actuator chain (DCM crystal piezo vs mirror; "VDM" label).
3. Measured m67/m68 → `OVAL` sign + gain, per axis.
4. Intensity floor below which feedback must stay off; resulting max step size.
5. `pos_window` / `intensity_thresh` / `oval_margin` starting values.

---

## 10. Future phase — OAV-referenced per-energy BPM3 setpoint calibration

**Problem.** Centring on the BPM3 feedback (`CVAL → VAL`, OVAL → 0) gets the beam *close*, but not
*dead on*. The true "beam centred" reference is the **on-axis camera (OAV)** image. The BPM3
setpoint that corresponds to a truly-centred beam appears to be **energy-dependent** (suspected:
beam intensity on the BPM and/or an energy dependence of the BPM response). So the feedback
**setpoint** (`fast_pidX/Y.VAL`, i.e. the BPM3 `PosX/PosY` target) needs a small per-energy offset
to put the beam dead-centre on the OAV.

**Why it can't run live / always.** Calibrating against the OAV requires a **reference sample with
a YAG** loaded into the beam and the **shutter open** — which cannot be done during user data
collection. So this is a **periodic calibration routine**, run on a maintenance/commissioning shift,
that produces a stored offset-vs-energy curve applied to all subsequent energy moves.

**Proposed calibration plan (`calibrate_bpm3_offsets`).**
1. Pre-req (operator/guarded): YAG reference sample in, shutter open, feedback ON.
2. Step the energy across the range in ~100 eV increments (reusing `energy_walk` for the moves).
3. At each energy: take an **OAV image**, find the beam centroid, and **tweak the BPM3 setpoint**
   (`fast_pidX.VAL` / `fast_pidY.VAL` — the `PosX/PosY` targets) in a small feedback loop until the
   OAV centroid is at the defined "dead-centre" pixel (with the loop holding the beam there).
4. Record the resulting BPM3 `PosX/PosY` setpoint offsets (relative to nominal) **vs energy**.
5. Optionally also record/choose the **BPM3 electrometer range/gain** per energy band for best
   responsiveness: `XF:12IDB-BI:2{EM:BPM3}Range_RBV` (read) / its setpoint (write) — a coarser gain
   at low flux, finer at high, so the loop is responsive across the range.
   *(Implemented as a standard step of `energy_walk` — see §4.1; this calibration would only refine
   the bands, not add the mechanism.)*

**Storage & application.**
* Persist the offset-vs-energy table (and the range-vs-energy bands) via the existing Redis
  `_config` seam (like the IVU gap-offset table), so they survive restarts and are recorded as
  device config in every run.
* Fit a smooth curve (e.g. **spline**) so the offset can be interpolated at any energy.
* **Apply in the energy move**: after `energy_walk` settles/recentres at the new energy, set the
  BPM3 `PosX/PosY` setpoint to `nominal + offset(E)` (and select the range band for `E`) so the
  feedback holds the beam *dead on* per the OAV calibration — not just OVAL≈0.

**Notes / risks.**
* Centroiding must be robust to YAG artefacts/saturation; define the "dead-centre" pixel once
  (beam-defining aperture reference).
* The offset is a **setpoint** tweak, distinct from the OVAL re-centring (which keeps the *piezo*
  in range); both are needed — recentre keeps headroom, the offset puts the beam on the OAV target.
* This is a **periodic** routine; the energy move consumes the *stored* curve and never needs the
  YAG/shutter at run time.
* Add a dedicated sim model (OAV centroid that depends on the BPM3 setpoint error + an injected
  per-energy bias) so the calibration loop is testable off-beam.

**Phase placement:** after Part B (`energy_walk`) is in routine use — this refines "close" to
"dead on" and is gated on a YAG/shutter maintenance window.

---

## 11. Finishing touches (Pilatus thresholds tied to managed moves)

Two small, closely-related follow-ups to the managed energy move. Both are about keeping the
**Pilatus camera thresholds/gain in step with the photon energy** — today only the manual
`set_energy()` does this, so a managed move (or a camserver restart) can leave the detectors on a
stale threshold. Treat these as finishing touches on this work, not a new phase.

### 11.1 Set the camera thresholds after a managed (large) move

* **What.** When `energy_walk` finishes a managed move, set the Pilatus threshold/gain for the new
  energy — the same thing `set_energy()` does today via `set_energy_cam(cam, en_ev, ...)`
  (`src/smi_beamline/devices/pilatus.py:752`: writes `cam_energy` / `threshold_energy` / `gain_menu`,
  pulses `threshold_apply`, and stores `energyset`). Today `set_energy()`
  (`startup/smibase/pilatus.py:277`) moves energy **and** sets both cameras (`pil900KW`, `pil2M`);
  the managed-move path (preprocessor → `energy_walk`) currently moves energy **only**.
* **When.** **Only for big moves**, and **after the move is complete** (after the final
  settle/recentre), so threshold writes don't churn on every fine scan step. Natural home: a finalize
  step in `energy_walk` (or a hook the preprocessor calls once the walk returns), gated like the move
  itself (`|Δe| > threshold_eV`). Threshold setting is a plain `put`, so it composes fine with the
  message-pure plan or can run in the finalize.
* **Notes.** Reuse `set_energy_cam`'s existing energy→threshold/gain logic (don't duplicate the
  bands); apply to **all** detectors `set_energy()` covers. The cam already remembers the energy via
  `energyset` (`pilatus.py:61`/`:74`), which feeds 11.2.

### 11.2 On camserver restart, verify thresholds vs current energy and warn

* **What.** When the camserver is (re)started, **check** that the loaded threshold/energy/gain match
  what the **current beamline energy** requires, and **warn loudly if not**. For now just warn (and
  log the expected-vs-actual); optionally **fix** later (re-apply via `set_energy_cam`).
* **Where.** This is exactly the standing `ToDo` in the restart path: `restartWAXS()` /`startWAXS()`
  currently run the **camserver defaults** and never reconcile them with the beamline energy
  (`startup/smibase/pilatus.py:209`, `:273`–`:275` — the commented
  `set_energy_cam(pil900KW.cam, energy.get())`). After a restart, read back the camera's
  threshold/energy (`cam.threshold_read` / `cam.energy_read`, e.g. via `read_threshold()`
  `pilatus.py:231`) and compare to the values `set_energy_cam` would pick for the current energy.
* **Behaviour.** Compare within a small tolerance (threshold is in keV); on mismatch, print a clear
  warning naming the detector, the current energy, and expected-vs-actual threshold/gain. Default
  to **warn-only** (don't silently re-drive the detector during a restart); leave an opt-in to
  auto-correct (`set_energy_cam(cam, energy.get())`) for later. The remembered `energyset` value is a
  convenient cross-check that the restart landed on the right energy.

**Why grouped here.** Both items make the detector thresholds track energy the way the feedback now
tracks the beam — small, safe, and best done right after the managed move lands. No new calibration
or beam-time gating required (unlike §10).

