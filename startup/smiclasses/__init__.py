"""Backwards-compatibility shim: ``smiclasses`` -> ``smi_beamline.devices``.

The device classes moved to ``smi_beamline/devices/`` (Phase 4).  During the transition, the
``smibase`` instance modules and the test suite still import them as ``smiclasses.<module>`` and
``from smiclasses import _context`` etc.  This package transparently re-exports the new location:
importing ``smiclasses.X`` returns the **same module object** as ``smi_beamline.devices.X`` (so
identity and state are shared -- e.g. the ``_context`` seam is the very same module the devices
use).

This file is temporary and will be removed once all importers are repointed to
``smi_beamline.devices`` directly.
"""
import importlib
import pkgutil
import sys

import smi_beamline.devices as _devices

# Register every devices submodule under the ``smiclasses.<name>`` alias, pointing at the SAME
# module object, so ``import smiclasses.X`` / ``from smiclasses.X import Y`` resolve without
# re-executing the module.  (The submodules are hardware-free, so importing them here is safe.)
for _info in pkgutil.iter_modules(_devices.__path__):
    _full_target = _devices.__name__ + "." + _info.name
    _module = importlib.import_module(_full_target)
    sys.modules[__name__ + "." + _info.name] = _module
    globals()[_info.name] = _module

# Also re-export the package's already-bound public names (e.g. anything devices/__init__ exposes).
for _name in dir(_devices):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_devices, _name)
