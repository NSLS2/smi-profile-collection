"""Smoke test: every ``smiclasses`` device-class module imports with no hardware.

Before Phase 1, ``smiclasses.pilatus`` / ``smiclasses.prosilica`` (and anything importing them)
could not be imported off the beamline: they pulled in ``smibase.base`` at module load (Tiled
login / Duo push / Redis / a secret file) and read EPICS at class-definition time.  After
decoupling via ``smiclasses._context``, all of these must import cleanly.
"""
import importlib

import pytest

# Every module under startup/smiclasses that defines device classes.
SMICLASSES_MODULES = [
    "_context",
    "amptek",
    "attenuators",
    "beamstop",
    "bimorph",
    "bladecoater",
    "crls",
    "electrometers",
    "energy",
    "ioLogik",
    "linkam",
    "machine",
    "manipulators",
    "mirrors",
    "motors",
    "pilatus",
    "prosilica",
    "shutter",
    "slits",
    "waxschamber",
    "xbpms",
]


@pytest.mark.parametrize("modname", SMICLASSES_MODULES)
def test_smiclasses_module_imports_without_hardware(modname):
    """Importing the module must not touch EPICS / Redis / IPython / smibase."""
    mod = importlib.import_module("smiclasses.{}".format(modname))
    assert mod is not None


def test_smiclasses_does_not_import_smibase():
    """Guard: no smiclasses module should import smibase at module load (the old cycle)."""
    import os

    here = os.path.dirname(__file__)
    smiclasses_dir = os.path.abspath(os.path.join(here, "..", "..", "startup", "smiclasses"))
    offenders = []
    for fn in os.listdir(smiclasses_dir):
        if not fn.endswith(".py"):
            continue
        with open(os.path.join(smiclasses_dir, fn)) as fh:
            for i, line in enumerate(fh, 1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "from smibase" in stripped or "import smibase" in stripped:
                    offenders.append("{}:{}  {}".format(fn, i, stripped))
    assert not offenders, "smiclasses must not import smibase (breaks the cycle):\n" + "\n".join(
        offenders)
