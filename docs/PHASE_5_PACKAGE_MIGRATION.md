# Phase 5 Package Migration Handoff

Date: 2026-07-07
Branch: `phase-5-package-startup-cleanup`

## Goal

Finish moving real beamline source out of `startup/` and into the installable/testable
`src/smi_beamline` package. The intended end state is:

- `src/smi_beamline/` owns device classes, live instance construction, plans, helpers, and tests.
- `startup/` is only the profile execution/bootstrap layer for IPython and QServer.
- `startup/smibase/*.py` files become temporary compatibility shims and are deleted once internal
  imports no longer depend on them.

## Completed Today

Created package directory `src/smi_beamline/instances/` by moving the old factory module from:

- `src/smi_beamline/instances.py`

to:

- `src/smi_beamline/instances/__init__.py`

The public import remains:

```python
from smi_beamline import instances
from smi_beamline.instances import make_devices
```

Migrated these live instance-construction modules from `startup/smibase` into
`src/smi_beamline/instances`:

- `amptek`
- `attenuators`
- `beam`
- `beamstop`
- `bladecoater`
- `crls`
- `electrometers`
- `energy`
- `ioLogik`
- `linkam`
- `machine`
- `manipulators`
- `mirrors`
- `motors`
- `pilatus`
- `prosilica`
- `shutter`
- `slits`
- `suspenders`
- `waxschamber`
- `xbpms`

For each migrated module, the corresponding `startup/smibase/*.py` file is now a compatibility shim:

```python
from smi_beamline.instances.<module> import *
```

The factory import list in `src/smi_beamline/instances/__init__.py` now imports the migrated modules
from `smi_beamline.instances.*`; it no longer imports device groups from `smibase.*`.

Most package-internal plan/helper imports have also been repointed from `smibase.*` shims to
`smi_beamline.instances.*`. The remaining `src/` reference to `smibase.base` is the bootstrap-owned
`mdsave` import used by the beam-snapshot helper.

## Hardware Test Adjustment

Updated `tests/hardware/test_hardware_connect.py` because the hardware smoke test was stricter than
the live beamline requires:

- Shutters now check essential `status`, `open_cmd`, and `close_cmd` PVs instead of requiring the
  optional upstream `enabled_status` PV. This fixed the persistent GV7 failure on
  `XF:12IDC-VA:2{Det:1M-GV:7}Enbl-Sts`.
- `test_waxs_arc_readback_present` now connects only `waxs.motors.arc` instead of the full
  `pil900KW` detector tree. This avoids requiring stale/nonexistent Pilatus readbacks
  `GainMenu_RBV` and `ThresholdApply_RBV` while still testing the WAXS arc PV used by the arc-block
  logic.

The live hardware test was rerun after this and passed. Occasional first-run timeout on a slow PV is
known; a second run passed cleanly.

## Verification Run

Offline verification after migrations:

```bash
pixi run test-unit
# 110 passed

pixi run test-sim
# 181 passed
```

Additional import smoke used during migration:

```bash
PYTHONPATH=src pixi run -e test python -c \
  "from smi_beamline import instances; print([m for _, m in instances.DEVICE_MODULES if m.startswith('smi_beamline.instances')])"
```

Live verification:

```bash
pixi run test-hardware
# passed
```

The `bsui` console has also been confirmed working well on the beamline after the full instance
module migration.

After confirming external user scripts use namespace devices rather than `smibase.*` imports, the
temporary migrated-module compatibility shims were deleted from `startup/smibase/`. Offline tests were
rerun after deleting the shims:

```bash
pixi run test-unit
# 110 passed

pixi run test-sim
# 181 passed
```

## Remaining `smibase` Bootstrap Layer

The migrated `startup/smibase/*.py` compatibility shims have been deleted. The remaining
`startup/smibase` modules are bootstrap/support modules, not factory-owned device groups:

- `base`
- `base_dev`
- `zz_smi_plans`

## Next Step

The full instance-module migration is now live-smoke-confirmed and the temporary compatibility shims
have been removed. Before merging this branch back, rerun the live smoke after pulling the latest
commit:

```bash
pixi run test-hardware
```

Also launch `bsui` once from the updated branch as a final console startup check.
