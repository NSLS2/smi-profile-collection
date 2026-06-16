# Testing the SMI profile-collection

The test suite has **three tiers**. They are selected by pytest markers and by
the directory a test lives in (tests are auto-tagged from their directory):

| Tier | Directory | Marker | Touches | Default |
|------|-----------|--------|---------|---------|
| Pure code | `tests/unit/` | `unit` | nothing (no devices built) | always run |
| Simulated | `tests/sim/` | `sim` | **fake**, non-broadcasting `ophyd.sim` devices | always run |
| Hardware | `tests/hardware/` | `hardware` | **real** EPICS PVs | **off** unless `--run-hardware` |

## Running

```bash
pixi run -e test test            # unit + sim (the safe default; no hardware)
pixi run -e test test-unit       # pure-code tier only
pixi run -e test test-sim        # fake-device tier only
pixi run -e test test-hardware   # HARDWARE tier -- ONLY on the beamline
```

Equivalent raw pytest:

```bash
pytest -m "not hardware"         # safe default
pytest -m unit
pytest -m sim
pytest --run-hardware -m hardware
```

### Hardware safety

Unless `--run-hardware` is passed, `tests/conftest.py`:

- forces `EPICS_CA_AUTO_ADDR_LIST=NO` / `EPICS_CA_ADDR_LIST=127.0.0.1` (no CA
  broadcast can leave the process), and
- skips every `hardware`-marked test.

Fake devices (the `sim` tier) are built with `ophyd.sim.make_fake_device`, which
replaces every `EpicsSignal`/`EpicsMotor` with an in-memory fake — **no Channel
Access connection is ever opened**, so the `unit` and `sim` tiers cannot reach
the live beamline even if CA were enabled.

### What the hardware tier covers

`tests/hardware/test_hardware_connect.py` builds each device from the `DEVICES`
list (which mirrors the `smibase` prefixes/classes) in **REAL** mode and asserts
`wait_for_connection`. It is **connection + read only — nothing is moved, opened,
closed, or triggered** — so it is safe to run **with no beam**. Covered today:
detectors (`pil2M`, `pil900KW`), the sample stack (`stage`, `piezo`, `bdm`),
`energy`, flux (`xbpm2`, `xbpm3`, `pin_diode`), `ls`, shutters (`ph_shutter`,
`GV7`), a representative attenuator (`att2_9`), plus the WAXS arc readback and the
Huber `stage` `.th/.ph/.ch` back-compat aliases. Extend by adding rows to
`DEVICES` (keep them read-only).

## Live connectivity check from the IPython terminal — `hardware_check()`

For an interactive smoke-test inside the running Bluesky session (the companion to
the pytest `hardware` tier), call `hardware_check()`. Unlike the pytest tier — which
rebuilds classes from prefixes — this checks the **already-instantiated** beamline
objects in the namespace (so anything pinned `fake` via the device factory shows up
as connected-fake). It is **read-only**: nothing moves/opens/triggers; safe with no
beam.

```python
hardware_check()                      # default key-device set -> prints a table
hardware_check(["pil2M", "pil900KW"]) # just the detectors
res = hardware_check(read=False)      # connection only, no value reads; returns a dict
```

It prints `device / status / t(s) / value` and a `N/M connected` summary, and returns
`{name: {"ok", "connected", "value", "error"}}`. Statuses: `OK`, `NO CONN`,
`MISSING` (name not in namespace), `ERROR`. The default device list is
`smibase.utils.HARDWARE_CHECK_DEVICES`.

## The device factory — fake vs. real, per device

`startup/smiclasses/device_factory.py` is a single chokepoint for building a
device as real or fake. It is used both by the live profile bootstrap and by the
`sim` tests.

```python
from smiclasses.device_factory import make_device
from smiclasses.pilatus import SAXS_Detector

pil2M = make_device(SAXS_Detector, "XF:12ID2-ES{Pilatus:Det-2M}",
                    name="pil2M", asset_path="pilatus2m-1")
```

With no configuration, every device is **real** — identical to the current
behaviour. The mode for a device `name` is resolved in priority order:

1. an explicit `force="real"|"fake"` argument to `make_device()`
2. env `SMI_REAL_DEVICES` (comma list of names, or `all`)
3. env `SMI_FAKE_DEVICES` (comma list of names, or `all`)
4. in-process overrides set via `device_factory.configure_modes(...)` (tests)
5. a CSV file `name,mode` pointed to by `SMI_DEVICE_MODES_FILE`
6. default: `real`

### Faking one broken device in production

If a detector is broken/absent for a long stretch, pin **just that device** to a
fake so the rest of the profile still boots and runs:

```bash
export SMI_FAKE_DEVICES=pil300KW       # one device fake, everything else real
```

or check a row into the modes file and point `SMI_DEVICE_MODES_FILE` at it:

```
# name,mode
pil300KW,fake
```

### Faking the whole instrument

```bash
export SMI_FAKE_DEVICES=all            # the sim test suite does exactly this
export SMI_REAL_DEVICES=energy         # ...optionally exempting some devices
```

### Seeding fake state

For the `sim` tier you can put a fake device into a known state **after**
construction:

```python
make_device(SAXSBeamStops, "FAKE:", name="bs", force="fake",
            seed={"x_rod.user_readback": 6.8})
```

Note `seed` runs *after* `__init__`, so it cannot influence values that a
device reads during construction (e.g. `SAXS_Detector.active_beamstop`, which is
inferred from positions at init time); use component defaults / `force` for that.

## Caveats / current limits

- The `sim` tier builds the **`smiclasses`** device classes as fakes. Importing
  the **`smibase`** instantiation modules off-beamline is not yet possible (they
  call `get_ipython()` and touch Redis at import). Wiring the live `smibase`
  instantiations through `make_device` (so the production per-device toggle is
  live) is a follow-up; it is behaviour-preserving because the default mode is
  `real`.
- A fake `EpicsMotor`'s move status does not auto-complete, so `bps.mv` on a
  fake motor will hang under the RunEngine. Drive `Signal`/`EpicsSignal`
  components in `sim` plan tests (as `det_exposure_time` does), or seed motor
  readbacks directly.
