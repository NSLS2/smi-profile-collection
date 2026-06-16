"""Smoke test: every ``smi_beamline.devices`` device-class module imports with no hardware.

Before Phase 1, the device classes (then ``smiclasses.pilatus`` / ``smiclasses.prosilica`` ...)
could not be imported off the beamline: they pulled in ``smibase.base`` at module load (Tiled
login / Duo push / Redis / a secret file) and read EPICS at class-definition time.  After
decoupling via ``smi_beamline.devices._context`` (and the Phase-4 move out of ``startup/``), all of
these must import cleanly with no IPython/EPICS/Redis/``smibase``.
"""
import importlib
import os
import pkgutil

import pytest

import smi_beamline.devices as _devices

# Every module under smi_beamline/devices that defines device classes (discovered, so the list
# can't drift out of date).
DEVICE_MODULES = sorted(info.name for info in pkgutil.iter_modules(_devices.__path__))


@pytest.mark.parametrize("modname", DEVICE_MODULES)
def test_device_module_imports_without_hardware(modname):
    """Importing the module must not touch EPICS / Redis / IPython / smibase."""
    mod = importlib.import_module("smi_beamline.devices.{}".format(modname))
    assert mod is not None


def test_devices_do_not_import_smibase():
    """Guard: no device module should import smibase at module load (the old cycle)."""
    devices_dir = os.path.dirname(_devices.__file__)
    offenders = []
    for fn in os.listdir(devices_dir):
        if not fn.endswith(".py"):
            continue
        with open(os.path.join(devices_dir, fn)) as fh:
            for i, line in enumerate(fh, 1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "from smibase" in stripped or "import smibase" in stripped:
                    offenders.append("{}:{}  {}".format(fn, i, stripped))
    assert not offenders, "device modules must not import smibase (breaks the cycle):\n" + "\n".join(
        offenders)
