# SMI workstation QueueServer controls

The worker exports two single-target plans and top-level aliases. These are
references to objects created by the profile factory, not new PV connections.
Aliases allow the camera setting to be listed without expanding all detector
components. The terminal namespace is unchanged.

| Plan | Allowed device argument | Existing object | Value |
| --- | --- | --- | --- |
| `mv` | `oav_acquire_time` | `OAV.cam.acquire_time` (on-axis SAM camera) | Absolute exposure, 0.0001–2 s |
| `mvr` | `sample_piezo_x` | `piezo.x` | Relative displacement, native units |

Run `python -m pytest tests/sim/test_workstation_queue.py` in the profile test environment
for offline QueueServer introspection, permission filtering, device-name resolution
and execution on in-memory signals. This does not load the operational startup file.

After review and deployment to the **worker**, refresh the manager's effective
permissions and its plan/device inventory using the site's normal idle-worker
procedure. In the ws1 monitor verify `mv`, `mvr` and both aliases under
**Queue & Console → Capabilities**. A missing device factory group means its
alias and plan will be absent; inspect the worker startup report. Changing only
the workstation checkout or its CLI flags cannot register a worker plan.

For the first trial enable only `--exposure-device oav_acquire_time` with the
verified SAM camera config. Note the current direct readback; after a small
change check both completed history (by item UID) and the fresh readback, then
restore the original exposure and check again. The app's relative-jog step
and units must be selected separately after checking the installed axis, its
direction, limits and available travel. No step size is prescribed here.
