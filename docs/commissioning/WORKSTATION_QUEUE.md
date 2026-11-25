# SMI workstation QueueServer controls

The worker exports two single-target plans and top-level aliases. These are
references to objects created by the profile factory, not new PV connections.
Aliases allow the camera setting to be listed without expanding all detector
components. The terminal namespace is unchanged.

| Plan | Allowed device argument | Existing object | Value |
| --- | --- | --- | --- |
| `mv` | `oav_acquire_time` | `OAV.cam.acquire_time` (on-axis SAM camera) | Absolute exposure, 0.0001–2 s |
| `mvr` | `sample_piezo_x`, `_y`, `_z` (same prefix) | `piezo.x`, `.y`, `.z` | Relative displacement of one translational axis, um |
| `mvr` | `sample_piezo_th`, `sample_piezo_chi` | `piezo.th`, `.ch` | Relative displacement of one angular axis, degrees |

Run `python -m pytest tests/sim/test_workstation_queue.py` in the profile test environment
for offline QueueServer introspection, permission filtering, device-name resolution
and execution on in-memory signals. This does not load the operational startup file.

After review and deployment to the **worker**, refresh the manager's effective
permissions and its plan/device inventory using the site's normal idle-worker
procedure. In the ws1 monitor verify `mv`, `mvr` and both aliases under
**Queue & Console → Capabilities** (look for each configured piezo alias). A missing device factory group means its
alias and plan will be absent; inspect the worker startup report. Changing only
the workstation checkout or its CLI flags cannot register a worker plan.

For the first trial enable only `--exposure-device oav_acquire_time` with the
verified SAM camera config. Note the current direct readback; after a small
change check both completed history (by item UID) and the fresh readback, then
restore the original exposure and check again. The app's relative-jog step
and units must be selected separately after checking the installed axis, its
direction, limits and available travel. No step size is prescribed here.

### Reviewed piezo XY move

For a reviewed on-axis camera move the worker exposes `move_piezo_xy(x0, y0,
dx, dy)` when both `piezo.x` and `.y` are loaded. All values are native µm.
One queue item checks both starting coordinates, the 100 µm per-axis hard
limit on requested displacement, and both motor targets before yielding one
grouped `bps.mv`. It does not address Z, rotations, or the Huber stack.

### Bookmark positioning

Bookmark editing stays in the existing shared `swaxssamples` db=2 namespace.
`load_holder()` reads holder membership; it is not a holder transfer plan. The
worker's `load_sample(holder_id, sample_id, updated, max_step_um)` resolves a
`Sample` by stable ID using `SampleStore(samplestore)`. It delegates motion to
`smi_plans._core.goto_sample` and its existing refined-before-nominal rule,
skipping theta and Huber axes for this piezo XYZ commissioning scope. Named
arguments or JSON positional args are sufficient; no Python objects on the wire.
The worker refuses a stale version, mismatched measurement holder, non-lab frame,
incomplete XYZ or excessive per-axis displacement before issuing motion. The
caller must verify the actual mount; a stored ID is not physical confirmation.
The plan does not exchange holders, change the active pointer or configure run
metadata. Existing `smi_plans` measurement plans that already hold a `Sample`
continue to use `goto_sample` directly; there is no second positioning algorithm.
