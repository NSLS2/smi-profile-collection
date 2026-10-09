# Device state and beamline layout

The console overview separates three responsibilities:

1. **Device classes own state meaning and useful fields.** Shutters implement
   `read_state()`, the sample chamber implements `pressure_state(axis)`, CRLs
   implement `read_lens_state()`, and bimorphs implement `read_output_state()`.
   Pilatus devices expose `energy_difference()` and SAXS exposes
   `selected_beamstop_motors()`. These are read-only methods, not plans.
2. **Instance configuration owns physical location.**
   `src/smi_beamline/instances/layout.py` holds the installation's hutch, beam
   order, labels, and shutter boundaries. The factory attaches this immutable
   `BeamlineLocation` metadata to each device as `beamline_location`. Existing
   explicit overrides are preserved.
3. **The renderer owns presentation.** `beamline_status.py` reads the device's
   `status_description`, evaluates its fields with bounded/cached reads, and
   supplies colors, alignment, clipping, and hutch walls. Devices do not print
   ANSI escapes or depend on IPython/Qt.

## Device methods at the console

```python
fs.read_state()                         # live OPEN / NOT OPEN / UNKNOWN(...)
fe_shutter.read_state()
chamber_pressure.pressure_state("maxs") # value, units, diagnostic state
crl.read_lens_state()                   # {holder_number: IN / OUT / UNKNOWN}
hfm_voltage.read_output_state()         # state, first (ch0), min, max, units
pil2M.energy_difference(16150)          # difference_eV, matches
```

These methods accept `read_signal=callable` so an overview or future GUI can
supply cached/subscribed reads instead of using the default 150 ms signal reads.
The console reader shares a 3 s budget across all fields. Bimorph summaries show
`ON first, low–high V`; the first output is channel 0, independently of min/max.

Classification constants are on the relevant classes/instances:

- `SMIFastShutter.status_values`: 0 open, 7 not open.
- `FrontEndShutterReadback.status_values`: 0 open, 1 not open.
- `TwoButtonShutter.open_val` / `close_val`: existing per-valve polarity.
- `Sample_Chamber.pumped_below` / `vented_above`: diagnostic thresholds.
- `CRL.inserted_tolerance_mm`: strict absolute-position insertion tolerance.
- `Pilatus.energy_match_tolerance_eV`: detector/beamline comparison tolerance.

Diagnostic pressure labels describe the **chamber pressure**, not pump running
state. They do not change pump-plan completion setpoints or interlocks.
State reads never call `put`, `set`, or update `RE.md`. The legacy fast-shutter
`check_status()` explicitly updates its software cache but delegates decoding to
the same `read_state()` method used by the overview.

## Field descriptions

Device classes expose immutable `status_description` rows/fields defined in
`devices/status.py`. These describe labels, readback paths, units, precision,
and semantic readers, independent of terminal formatting. Paths are relative to
the device; `@` introduces a cross-device namespace reference. Cross-device
comparisons/groupings (e.g. detector energy versus beamline energy) belong in
these descriptions, rather than changing the underlying devices' ownership.

Expected missing devices use the same pure-data field descriptions so they stay
visible as `N/A`; loading the layout never imports live instance modules or
constructs devices. The renderer does not guess missing device methods or state
polarity. Device classes and the missing-device catalog share the same immutable
descriptions rather than duplicate lists.

## Change order or add a device

For a temporary session override:

```python
from dataclasses import replace
ssa.beamline_location = replace(ssa.beamline_location, order=95)
```

For a persistent installation change, edit `DEFAULT_LAYOUT` in
`instances/layout.py`. Order numbers are relative beam-path order, not metres.
Hutch wall entries carry the shutter name in `boundary`; colors stay in the UI.

A new device can participate without editing the renderer:

```python
from smi_beamline.instances.layout import BeamlineLocation
from smi_beamline.devices.status import StatusRow, number

monitor.beamline_location = BeamlineLocation("B", 95, "New monitor", "")
monitor.status_description = (
    StatusRow("{label}", (number("current", "current", "nA"),)),
)
```

The device must be in the session namespace. Aliases are deduplicated by object
identity. Class-level descriptions can be overridden per instance. Setting a
different hutch alone is descriptive; change order as well to move the device
across the corresponding boundary.

The factory configures this metadata at startup; reloading the magic extension
also attaches it to existing session objects. Reloading the extension does not
reconstruct devices: newly added class methods require the updated classes
(normally a fresh session, or the profile's autoreload mechanism).
