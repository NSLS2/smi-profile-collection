# SAXS beamstop wobble tracking — bug analysis and fix plan

**Status:** there is a **temporary workaround live in the code** (uncommitted as of 2026-06-23,
in `SAXS_Detector.calc_offsets`, `src/smi_beamline/devices/pilatus.py`). It disables the wobble
correction applied to the SAXS beamstop park positions so that `restore_beamstop()` /
`modeMeasurement()` land **exactly** on the last `save_beamstop()` position. This document explains
the underlying bug the workaround masks, and the proper fix, so the correction can be re-enabled
later **without** reintroducing the restore-offset error.

This is a beamstop-parking issue only. **The beam-center used for data analysis is not affected** —
that path (`beam_offset_x/y_mm` → `beam_center_*`) keeps the full wobble correction either way.


## 1. Physical setup

The SAXS detector rides on a long z-travel carriage. The carriage **wobbles** laterally (in x and
y) as it moves along z — i.e. the beam lands at a slightly different detector pixel at different
sample-to-detector distances. A dedicated **scan of beam center vs. distance** was taken and stored,
giving the lateral beam offset as a function of z:

```
beam_offset_x_mm(z),  beam_offset_y_mm(z)      # interpolated from distance_calibration
```

The **beamstop is mounted on the same carriage**, so to first order it sees the **same** lateral
wobble. Therefore, in principle, to keep the beamstop centered on the beam as z changes, you apply
the wobble delta to a nominal beamstop position:

```
beamstop_x(z) = nominal_beamstop_x + (wobble shift at z)
```

with the sign chosen so the beamstop follows the beam. (The current code subtracts the delta; the
exact sign is part of what must be re-derived if/when the correction is re-enabled — see §5.)


## 2. The relevant code path

Subscriptions on `motor.x/y/z` call `update_beam_center` whenever the carriage moves
(`pilatus.py` `__init__`). `update_beam_center` calls **`calc_offsets(z)`**, which does two distinct
jobs:

1. **Beam center (analysis).** Interpolate `beam_offset_x/y_mm` from the `distance_calibration`
   table at the current z, then compute `beam_center_x/y_mm`, `beam_center_*_px`,
   `sample_distance_mm`. *(Correct; not in question.)*

2. **Beamstop park positions (parking).** Compute a wobble `delta` and apply it to the saved
   beamstop positions, writing the `*_offset_*_mm` **config signals** that the beamstop-move helpers
   consume:

   ```python
   delta_x = self.beam_offset_x_mm.get() - nominal_beam_offset_x   # wobble shift vs reference z
   delta_y = self.beam_offset_y_mm.get() - nominal_beam_offset_y

   base_rod_x = mdsave.get('saxs_rod_offset_x_mm', 6.8)            # the SAVED beamstop position
   ...
   self.rod_offset_x_mm.set(base_rod_x - delta_x)                 # <-- the disputed line
   self.rod_offset_y_mm.set(base_rod_y - delta_y)
   self.pd_offset_x_mm.set(base_pd_x - delta_x)
   self.pd_offset_y_mm.set(base_pd_y - delta_y)
   ```

The beamstop-move helpers (`insert_beamstop`, `restore_rod`, `restore_pin`, `remove_*`) then move
the physical beamstop to whatever `rod_offset_x_mm` / `pd_offset_x_mm` currently hold.

`save_beamstop()` (→ `save_rod_position` / `save_pd_position`) writes the **current physical motor
position** straight into those same config signals and persists it:

```python
self.rod_offset_x_mm.set(self.beamstop.x_rod.position)            # absolute position at current z
_config.persist_from_signals(self, {'saxs_rod_offset_x_mm': 'rod_offset_x_mm'})
```


## 3. The bug: the wobble delta is double-counted on restore

The saved value and the runtime correction are in **inconsistent reference frames**:

- **What `save_beamstop()` stores** is the *absolute* motor position the operator dialed in — the
  beamstop where it actually belonged at **that** distance. The wobble at that z is **already baked
  into** that number. It is, by construction, the exact final position to return to at that
  distance.

- **What `calc_offsets()` assumes** is that `saxs_rod_offset_x_mm` is a *pre-wobble nominal* (a value
  defined at the reference z), to which it should **add** the wobble delta for the current z.

So after a `save_beamstop()` at distance *z₀* and a later `restore_beamstop()` at the same *z₀*:

```
moved-to  = base_rod_x − delta_x(z₀)
          = (correct position at z₀)  −  (wobble shift at z₀)      # delta applied a SECOND time
          ≠  correct position at z₀
```

The wobble is counted **twice** — once because it was already in the saved absolute position, and
again because `calc_offsets` re-applies it — so the restore lands off by roughly the wobble delta.
That is the "over-correction" the workaround comment describes.

### The governing principle (operator's intent)

> A `save_beamstop()` position is, by definition, **exactly** the position the motor should move
> back to **at that distance**. Nothing further should be applied to it from then on.

The current code violates this: it treats the saved final position as a nominal and re-corrects it.


## 4. The temporary workaround (current code)

`calc_offsets` currently writes the saved positions **verbatim**, with no delta:

```python
self.rod_offset_x_mm.set(base_rod_x)      # was: base_rod_x - delta_x
self.rod_offset_y_mm.set(base_rod_y)
self.pd_offset_x_mm.set(base_pd_x)
self.pd_offset_y_mm.set(base_pd_y)
```

**Effect:** restore is now exact at the saved distance (the principle in §3 holds). **Limitation:**
the beamstop no longer tracks the wobble across z **at all** — it always parks at the one saved
absolute position. That is fine when operating near the z where the position was saved, but at a
**different** distance the beamstop will sit off-beam by the wobble difference between the two
distances. So the workaround trades "wrong at the saved distance" for "right at the saved distance,
drifts at other distances" — acceptable as a stop-gap, not a real fix.


## 5. Proper fix (two options)

The fix must reconcile the reference frames so that **(a)** a saved position restores exactly at its
own distance, **and (b)** the beamstop still follows the wobble when you change distance. Pick one
consistent convention:

### Option A — keep a single nominal + correction, but save the *nominal*

Keep `calc_offsets` applying `delta`, but make `save_beamstop()` store the **wobble-removed nominal**
instead of the raw absolute position, so the later `+delta`/`−delta` reproduces the saved final
position:

```python
# in save_rod_position(), at save time (distance z0):
delta_x0 = self.beam_offset_x_mm.get() - nominal_beam_offset_x
self.rod_offset_x_mm.set(self.beamstop.x_rod.position + delta_x0)   # store NOMINAL (undo wobble)
```

Then at restore (distance z), `calc_offsets` does `nominal − delta_x(z)`, which at `z == z0` returns
the original absolute position (exact restore), and at other z follows the wobble. **Pros:** minimal
change, single source of truth. **Cons:** the persisted `saxs_*_offset_*_mm` value is no longer "the
position you see on the motor," which can confuse anyone reading the config; the sign convention
must be derived carefully and verified on hardware.

### Option B — store the beamstop park position per distance (like the beam center)

Treat the beamstop exactly like the beam center: store `rod_offset_x/y`, `pd_offset_x/y` **per
distance** in `distance_calibration` (the table already carries them — see the "dual storage" note
below — they are simply not read back today), and have `calc_offsets` **interpolate** the beamstop
position from that table instead of `base ± delta`. **Pros:** conceptually uniform with the
beam-center handling; no separate wobble math or sign convention for the beamstop; naturally exact at
every saved distance and interpolated in between. **Cons:** requires a few saved points across z to
be useful (a single point degrades to "constant," i.e. the §4 behavior); needs the interpolation
wired in and the flat `saxs_*_offset_*_mm` config seam reconciled with the per-distance table.

**Recommendation:** Option B is the cleaner long-term design (it mirrors the beam-center path that is
already trusted), provided the per-distance beamstop points are actually collected. Option A is the
smaller change if only a single reference position is ever saved.


## 6. Gotcha to resolve either way: dual storage

`save_rod_position` / `save_pd_position` currently write the saved value to **two** places:

1. the **flat config signal** `saxs_rod_offset_x_mm` (via `mdsave` / `_config.persist_from_signals`)
   — this is the one `calc_offsets` reads back as `base_rod_x`; and
2. a **per-distance entry** in `distance_calibration[z]` (via
   `add_calibration_point(z, get_current_offset_dict())`), which includes `rod_offset_x`,
   `pd_offset_x`, etc.

Today `calc_offsets` reads the **flat** value for the beamstop and interpolates **only**
`beam_offset_x/y` and `sample_offset_z` from the per-distance table — so the per-distance beamstop
entries are **written but never used**. Option B above is essentially "start using them" (and stop
reading the flat value for parking). Whichever option is chosen, make these two stores **consistent**
so there is a single, unambiguous definition of the beamstop park position.


## 7. Checklist to re-enable the correction

1. Decide Option A or B (§5) and make the save and restore paths use the **same** reference frame.
2. Re-derive and **verify the wobble sign** on hardware (does `+delta` move the beamstop toward or
   away from the beam as z increases?). The current `− delta_x` sign is unverified for the beamstop.
3. Confirm the beamstop-vs-detector **lever-arm ratio** assumption (`calc_offsets` currently assumes
   the beamstop is close enough to the detector face that the ratio ≈ 1; if not, scale the delta).
4. Resolve the dual-storage inconsistency (§6).
5. Validate end-to-end: `save_beamstop()` at distance A, move to distance B and back, confirm
   `restore_beamstop()` lands exactly at A **and** that the beamstop stays centered at B.
6. Remove the temporary block in `calc_offsets` and restore the wobble-corrected lines (kept
   commented in place).
