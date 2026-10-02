# Pilot Bluesky console magics

Loaded automatically by `startup/startup.py` in interactive IPython sessions.
To enable them in an already-running session with this repository's `src` on
the import path:

```ipython
%load_ext smi_beamline.motor_magics
```

After an update, use `%reload_ext smi_beamline.motor_magics` if already loaded.

These are **standalone console commands**. Moves, scans, exposure changes, and
snapshots call the session's `RE` and wait for completion. Position and exposure
readouts do not invoke `RE`.

## Moves and positions

| Commands | Device axes | Units |
| --- | --- | --- |
| `x`, `y`, `z` | `piezo.x`, `.y`, `.z` | um |
| `th`, `ph`, `ch` | `piezo.th`, `.ph`, `.ch` | degrees |
| `sx`, `sy`, `sz` | `stage.x`, `.y`, `.z` | mm |
| `sth`, `sph`, `sch` | `stage.th`, `.ph`, `.ch` | degrees |

**Currently `piezo.ph` is not defined**, so `ph` reports that the axis is
unavailable without invoking `RE`. It will work if that axis is added later.

Examples (these move hardware in a live session):

```ipython
x 1000        # RE(bps.mvr(piezo.x, 1000)): positive 1000 um jog
x -1000       # negative 1000 um jog
x a 1000      # RE(bps.mv(piezo.x, 1000)): absolute position 1000 um
sx 1          # relative stage.x move of 1 mm
sx a 0        # absolute stage.x position 0 mm
sth 0.1       # relative stage.th rotation of 0.1 degree
```

The comments above are explanatory: enter just the command and arguments.
Input accepts one finite number, optionally preceded by `a`, including signs,
decimals, and scientific notation (`sx -1e-3`). Expressions, variable expansion,
units in the input, trailing comments, and multiple commands on a line are
rejected. `x` (or any other bare motor command) displays its current position
in a bordered table, with four decimal places and units. `x ?`, `%x --help`,
or `%x?` displays help without moving anything.
Each move prints the resolved device, relative/absolute mode, value, and units.
The values are passed through directly: motor engineering units must agree
with the table; these wrappers do not perform unit conversion.

`wh` displays all positions in a **2-row × 6-axis box** (piezo and stage rows;
x, y, z, th, ph, ch columns), with units in every cell. Missing/disconnected axes
are shown as `N/A`, with an explanation below; other axes are still displayed.
Readouts use cyan labels and blue/green/magenta value columns. Help examples and
command echoes use syntax-style colors: **cyan commands**, **blue first numeric
argument**, **green second**, and **magenta third**; the absolute-move `a` marker
is yellow. Argument colors restart for each example. Detailed help uses the same
colors for placeholders such as START, STOP, and POINTS. Table borders stay
aligned because padding is calculated before color escapes are added.
Colors respect IPython's `%colors nocolor` and the `NO_COLOR` environment variable.
These colors apply to the guide, readouts, and printed command echoes; the live
input editor retains IPython's own syntax highlighting.

## Beamline overview and startup

Device-state APIs, field descriptions, and location metadata are documented in
[Device state and beamline layout](DEVICE_STATUS.md).

`status` (or `%status`) displays a read-only overview in **36 lines**, with a
132-column box. `status ?` explains the command without reading hardware.
The first row is **Accelerator / FE**: ring current in mA, IVU gap, and FE permit
(`smi_shutter_enable`), independently of the shutter-position readbacks below.
Interactive startup displays the same overview after devices and plans load,
followed by **“Type help for quick commands.”** QueueServer workers skip it.
The module-loading report uses cyan names, green successes, red failures, and
blue timings; the normal no-color settings apply throughout.

The display follows the requested upstream-to-downstream group order:

- Accelerator / FE: ring current, IVU gap, FE permit
- **Hutch A wall — FE shutter**: WBS, energy/DCM, HFM/VFM/VDM and bimorphs, then xBPM2
- **Hutch B wall — photon shutter**: SSA, then xBPM3
- **Hutch C wall — fast shutter**: ESlit, then the downstream rows below
- Attenuation factor/transmission at current energy, plus inserted foil labels
- Inserted CRL holder list (`abs(position) < 3 mm`); unknown holders listed separately
- CSlit gaps and centers
- Chamber pressures, isolation valves, turbo/power commands
- Piezo and stage translation/rotation positions
- WAXS then SAXS detector state, exposure, images, energy/threshold settings,
  energy mismatch, detector positioning axes, and selected SAXS beamstop X/Y

This is a curated operational overview of those groups, rather than a recursive
dump of every ophyd signal (which would include command PVs and image arrays).
Each xBPM row shows X/Y stage positions from `xbpm2_pos` / `xbpm3_pos` and the
electrometer's `sumX` readback. Sum units come from signal metadata, or `raw` when
unavailable; the X/Y values are motor positions rather than beam-centroid signals.
`fe_shutter` is a read-only device using `XF:12ID-PPS{Sh:FE}Sts:Cls-Sts`
(closed-status bit: 0 `OPEN`, 1 `NOT OPEN`). `ph_shutter` is the A-hutch photon
shutter. Fast-shutter state comes directly from `fs.status_pv` (0 `OPEN`, 7 `NOT OPEN`),
not its cached software status. Valve enum strings and per-device polarity are
respected. Hutch boundaries are horizontal walls with a green `OPEN` or red
`CLOSED` shutter opening; `CLOSED` is the compact display label for closed/not-open
readbacks. Missing or unrecognized values remain amber (`N/A`, `UNKNOWN`, etc.),
never converted to open/closed. Ordinary valve rows retain `NOT OPEN` verbatim.

Values have aligned columns: **blue numbers in every column**, neutral units,
green open/ON/idle/OK states, and amber closed/OFF/unknown states. Other text is
yellow; errors and detector energy differences greater than 100 eV are red. Motor units come from the motor record
where unspecified. Sample translations use um/mm and rotations deg. Pressure
units come from signal metadata; absent metadata is labeled `raw`, and gauge
strings such as `LO` are preserved. Turbo/power command values are explicitly
labeled `cmd`, not presented as independent running/power confirmations.
For numeric pressure readings, values **greater than 7e3** display red `Vented`,
and values **less than 5e-3** display green `Pumped`. Intermediate values,
including the exact boundaries, remain numeric with units. These thresholds
apply directly to the gauge values; red `Vented` indicates state, not a read error.

Attenuation comes from `attenuation.read_state()`, which evaluates the object's
live foil states without changing its computed signals or `RE.md`. Foil labels
use `bank_number` (e.g. `1_3,2_5`); an unknown foil state is reported rather than
treated as out. This read-only method is separate from the existing `compute()` /
`read()` methods, which refresh stored state. The SAXS beamstop row uses
`pil2M.active_beamstop` (the reported selection) and the corresponding rod/pin
motor readbacks; removed selections retain their `_removed` label. Selection
`none` leaves X/Y unavailable rather than choosing a beamstop arbitrarily.

Reads use **150 ms timeouts and a 3 s total read budget**, with cached duplicate
reads within each invocation. Missing, offline, failed, and deferred fields stay
inline as `N/A`, `OFFLINE`, `ERROR`, `TIMEOUT`, or `BUDGET`. Long fields are clipped
with `…` to preserve alignment. This is a sequential snapshot, not a simultaneous
measurement. No RE, `put`, `set`, `stage`, or `trigger` calls are made. Read-only
status is available even with RE paused; normal standalone-command rules apply.

## Scans

Every motor command has `scan` and `rscan` variants, using **pil2M** and its
current exposure settings:

```ipython
xscan -1000 1000 21
yscan -100 100 11
thscan -0.1 0.1 21
sxscan -1 1 21
syscan -1 1 21
xrscan 1000 21
sxrscan 1 21
```

- `xscan START STOP POINTS` runs
  `RE(bp.scan([pil2M], piezo.x, START, STOP, POINTS))`.
  Endpoints are **absolute**. On normal completion the motor stays at STOP.
- `xrscan SPAN POINTS` runs
  `RE(bp.rel_scan([pil2M], piezo.x, -SPAN, SPAN, POINTS))`.
  SPAN is a **positive half-width**, so `xrscan 1000 21` spans offsets of
  -1000 to +1000 um about the current position. Bluesky's `bp.rel_scan`
  (not `bps.rel_scan`) restores the starting position on normal completion.
- POINTS must be an integer of at least 2 and includes both endpoints.
- Axis names and units follow the motor table above. All six axes are
  registered for each device; piezo phi remains unavailable.
- Stage names normally follow the motor prefix: `sxscan`, `syscan`, `sthscan`,
  and `sxrscan`, `syrscan`, `sthrscan`, etc. The alternate spellings
  `xsscan`, `ysscan`, `thsscan`, and `xsrscan`, `ysrscan`, `thsrscan`, etc.
  are also accepted.

## Exposure

```ipython
exp
exp 0.5
exp 0.5 2
```

- `exp` reads **actual camera settings**: exposure seconds, period seconds,
  and images per trigger, separately for pil2M and pil900KW in a colored table.
  If the session enables Amptek via `amptek_det`, its preset exposure is also
  displayed (burst count and period do not apply).
- `exp N` calls `RE(det_exposure_time(N, N))`: one image of N seconds.
- `exp N M` calls `RE(det_exposure_time(N, M))`: N seconds per image and
  **M seconds total measurement time**, not M images. The existing helper uses
  `int(M / N)` images, including its truncation behavior, and sets acquire
  period to N + 0.001 seconds. Require N > 0 and M >= N.
- Both setters read back detector settings after RE finishes. The existing
  helper's optional Amptek update and two-pass Pilatus configuration are retained.

## Snapshots

| Command | Plan |
| --- | --- |
| `snaps` | `RE(bp.count([pil2M], 1, md={"sample_name": "snapshot"}))` |
| `snapw` | `RE(bp.count([pil900KW], 1, md={"sample_name": "snapshot"}))` |
| `snapsw` | `RE(bp.count([pil2M, pil900KW], 1, md={"sample_name": "snapshot"}))` |

These acquire one **trigger/event**, using current detector settings. A trigger
can contain multiple images if `exp` configured a burst. The sample name is
per-run metadata; `RE.md['sample_name']` is preserved. The existing scan-naming
preprocessor may append its normal recorded-field template to `snapshot`.

## Energy

```ipython
e
e 16150
e ?
```

`e` shows the beamline energy and both detector energy settings in **eV**, with
two decimal places, plus each detector's signed offset from the beamline.
Camera `cam.cam_energy` readbacks are converted from keV to eV; the remembered
`energyset` values are not used. Differences up to and including **100 eV** show
green `OK`; larger differences show red `MISMATCH` with highlighted energy and
offset. Missing, timed-out, or non-finite detector readbacks show `N/A` / `UNKNOWN`
while the other readings remain visible. Status labels also work without color.
`e VALUE` displays the same comparison after updating settings. It performs
an absolute move and then updates detector settings, in this order:

```python
RE(bps.mv(energy, VALUE))
set_energy(VALUE)
```

The energy must be a positive finite number and RE must be idle. The magic checks
that both `energy` and a callable `set_energy` exist before moving. The second call
only runs after the RE call returns successfully; move errors or interruptions
skip it. The RE move retains the session's managed-energy preprocessor.

The existing `set_energy` helper itself calls `energy.move(VALUE)` before setting
the energy/thresholds on pil900KW and pil2M, so the requested sequence repeats the
move to the same target. This second, blocking call is outside RE. If the detector
update fails, the exception is reported and the completed energy move is not
rolled back. `e` follows the same standalone-call restrictions as the other magics.

## Help

`help` or `%help` displays a friendly boxed, color-coded guide to all command
families, with examples and units. Bare `help` is specially routed to this guide
because Python's built-in help would otherwise shadow the magic. `help(object)`
still uses Python's normal help, and an existing user variable named `help` is
preserved (use `%help` in that case).

Every command accepts `?`, `-h`, or `--help`. A help token anywhere among the
arguments suppresses execution and explains the command, including the equivalent
RE call for actions. For example:

```ipython
x ?
xscan ?
xrscan 1000 ?
exp ?
snapsw ?
wh ?
```

Help does not read hardware. A scan command with no arguments also shows help;
motor commands and `exp` with no arguments read settings, and snapshot commands
with no arguments acquire data.

## Shutter and RunEngine control

| Commands | Equivalent |
| --- | --- |
| `so`, `sopen` | `RE(shopen())` |
| `sc`, `sclose` | `RE(shclose())` |
| `stop` | `RE.stop()` |

The shutter aliases take no arguments and use the existing session plans with
their defaults: opening enables pitch/roll feedback; closing disables feedback
before closing the shutter. These require an idle RE like other plan commands.

`stop` directly calls the RunEngine method, without the idle-state guard, so it
can gracefully terminate a **paused run**. RunEngine state errors propagate
normally. A synchronous running RE occupies the prompt; pause it using the usual
interrupt workflow before entering `stop`. This is not an emergency hardware
stop and does not itself run `shclose()`. Bluesky's graceful stop closes the run
with a successful exit status, rather than the failure status of an abort.

## Bare names and `%`

Registration enables IPython `automagic`, so `x 1000` and `%x 1000` both work
when there is no Python variable named `x`. The extension registers magics
directly and creates no `x`, `sx`, etc. variables, so no deletion is normally
needed. An existing variable takes precedence over a bare magic name. Use
`%x 1000` to be explicit, or deliberately `del x` if you no longer need that
variable. Registration preserves all existing user variables. `%automagic on`
restores bare commands if automagic was subsequently turned off.

## Execution and safety

- Commands that start plans require an **idle RE**, including rejecting a paused RE. Resolve a
  paused run with the usual resume/abort/stop workflow before issuing a jog.
- Calls from functions, generators/plans, and callbacks are rejected even if
  RE is idle. Use these as top-level IPython commands only. In reusable plans
  use `yield from bps.mvr(...)` / `yield from bps.mv(...)`. The call-context
  check is an accidental-misuse guard, not a Python sandbox.
- The same RE, preprocessors, suspenders, and device limit checks are used as
  for the longhand commands. Errors and interrupts propagate normally. No
  automatic retry is performed (retrying a relative jog could move twice).
- The main added risks are **short-name typos**, confusing relative with
  absolute motion, and the **1000-fold difference** between piezo translation
  units and stage translation units. There is no confirmation prompt or extra
  jog-size cap. For initial live commissioning use small, known-clear moves
  and verify direction, units, and readback before larger jogs.
- `stage` is a lab-frame pseudo-positioner. A single stage-axis command can
  drive multiple physical motors, especially for rotation-center compensation.
  Motor limits do not establish collision-free trajectories.
- An idle local RE is not a beamline-wide ownership lock: another process or
  QueueServer can still control hardware. Follow the existing single-operator /
  single-controller practice. The startup does not load these magics in workers.
- Ordinary `mv`/`mvr` does not open a data-taking run, so do not assume a jog
  produces a Tiled run record. IPython command history is not a motion audit log.

## Hardware-free tests

```bash
pixi run -e test python -m pytest tests/sim/test_motor_magics.py
```

The tests use an isolated IPython shell, a real Bluesky RunEngine, and in-memory
motors and detectors. They check recorded scan positions, relative-scan return,
snapshot detector selection and metadata, exposure-helper dispatch and readouts,
help/parsing, and standalone/idle guards. They do not load beamline startup or
connect to EPICS.
