"""Per-device fake/real construction seam for the SMI profile.

A single chokepoint so every device can be built either as a **real**
(EPICS-connected) ophyd device or as a **fake** (in-memory, *non-broadcasting*
``ophyd.sim`` device), decided **per device**.  The same factory is meant to be
used both by the live-beamline bootstrap (``smibase/*`` instantiation) and by
the off-beamline ``sim`` test suite.

Why this exists
---------------
* When a piece of hardware is broken/absent for a long time, it can be pinned to
  ``fake`` in production (one config entry) while everything else stays real.
* The ``sim`` test tier sets ``SMI_FAKE_DEVICES=all`` to build the entire device
  tree with zero hardware, then runs plans against it.

Fake devices are produced by :func:`ophyd.sim.make_fake_device`, which swaps
every ``EpicsSignal``/``EpicsSignalRO``/``EpicsMotor`` for an in-memory fake.
**No Channel Access connection is ever opened for a fake device**, so they are
safe and do not broadcast on the network.

Mode resolution
---------------
For a device ``name`` the mode is resolved in this priority order:

1. an explicit ``force=`` argument to :func:`make_device`
2. environment ``SMI_REAL_DEVICES`` (comma list of names, or ``all``)
3. environment ``SMI_FAKE_DEVICES`` (comma list of names, or ``all``)
4. an in-process override set via :func:`configure_modes` (used by tests)
5. a config file mapping (path from ``SMI_DEVICE_MODES_FILE``; CSV ``name,mode``)
6. the module default: ``"real"``

So ``SMI_FAKE_DEVICES=all`` with ``SMI_REAL_DEVICES=energy`` builds everything
fake except ``energy``; ``SMI_FAKE_DEVICES=pil300KW,rayonix`` fakes just those
two and leaves the rest real.
"""
from __future__ import annotations

import os
from typing import Dict, Optional, Tuple

from ophyd.sim import make_fake_device

__all__ = [
    "make_device",
    "device_mode",
    "configure_modes",
    "clear_overrides",
    "registry",
    "registered",
    "REAL",
    "FAKE",
]

REAL = "real"
FAKE = "fake"

# name -> (mode, instance) for everything built through make_device()
_REGISTRY: Dict[str, Tuple[str, object]] = {}

# in-process per-name overrides (priority 4); primarily for tests
_OVERRIDES: Dict[str, str] = {}


def _parse_name_list(value: Optional[str]) -> Tuple[set, bool]:
    """Parse a comma list env value into (set_of_names, is_all)."""
    if not value:
        return set(), False
    tokens = {t.strip() for t in value.split(",") if t.strip()}
    lowered = {t.lower() for t in tokens}
    if "all" in lowered:
        return set(), True
    if lowered <= {"none", ""}:
        return set(), False
    return tokens, False


def _file_modes() -> Dict[str, str]:
    """Load a ``name,mode`` CSV from ``SMI_DEVICE_MODES_FILE`` if present."""
    path = os.environ.get("SMI_DEVICE_MODES_FILE")
    if not path or not os.path.exists(path):
        return {}
    modes: Dict[str, str] = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2 and parts[1].lower() in (REAL, FAKE):
                modes[parts[0]] = parts[1].lower()
    return modes


def device_mode(name: str) -> str:
    """Resolve the build mode (``"real"``/``"fake"``) for a device ``name``."""
    fake_set, fake_all = _parse_name_list(os.environ.get("SMI_FAKE_DEVICES"))
    real_set, real_all = _parse_name_list(os.environ.get("SMI_REAL_DEVICES"))

    # 2. explicit real wins over explicit fake / global fake
    if name in real_set:
        return REAL
    # 3. explicit fake
    if name in fake_set:
        return FAKE
    # 2b/3b. global toggles (real-all beats fake-all)
    if real_all:
        return REAL
    if fake_all:
        return FAKE
    # 4. in-process overrides
    if name in _OVERRIDES:
        return _OVERRIDES[name]
    # 5. config file
    file_modes = _file_modes()
    if name in file_modes:
        return file_modes[name]
    # 6. default
    return REAL


def configure_modes(mapping: Optional[Dict[str, str]] = None, **kwargs) -> None:
    """Set in-process per-name mode overrides (priority 4). Mainly for tests.

    ``configure_modes({"pil2M": "fake"})`` or ``configure_modes(pil2M="fake")``.
    """
    if mapping:
        _OVERRIDES.update({k: v.lower() for k, v in mapping.items()})
    if kwargs:
        _OVERRIDES.update({k: v.lower() for k, v in kwargs.items()})


def clear_overrides() -> None:
    """Drop all in-process overrides (test teardown)."""
    _OVERRIDES.clear()


def _apply_seed(dev, seed: Dict[str, object]) -> None:
    """Set fake-signal values after construction.

    ``seed`` maps a dotted attribute path (relative to ``dev``) to a value, e.g.
    ``{"beamstop.x_pin.user_readback": -227}``.  Uses ``sim_put`` when available
    (FakeEpicsSignal) so readbacks update without a CA round-trip.
    """
    for dotted, value in seed.items():
        target = dev
        for part in dotted.split("."):
            target = getattr(target, part)
        if hasattr(target, "sim_put"):
            target.sim_put(value)
        else:
            target.put(value)


def make_device(cls, *args, name, force: Optional[str] = None,
                seed: Optional[Dict[str, object]] = None, register: bool = True,
                **kwargs):
    """Build ``cls`` as a real or fake device, decided per ``name``.

    Parameters
    ----------
    cls : type
        The ophyd device class to instantiate.
    *args, **kwargs :
        Passed through to the constructor (prefix, etc.).
    name : str
        Device name; also the key used for mode resolution and the registry.
    force : {"real", "fake"}, optional
        Override mode resolution entirely.
    seed : dict, optional
        Only applied for fake devices: dotted-path -> initial value.
    register : bool
        Record the result in the module registry (default True).
    """
    mode = (force or device_mode(name)).lower()
    if mode == FAKE:
        build_cls = make_fake_device(cls)
    else:
        build_cls = cls
    dev = build_cls(*args, name=name, **kwargs)
    if mode == FAKE and seed:
        _apply_seed(dev, seed)
    if register:
        _REGISTRY[name] = (mode, dev)
    return dev


def registry() -> Dict[str, Tuple[str, object]]:
    """Return a copy of the {name: (mode, instance)} registry."""
    return dict(_REGISTRY)


def registered(mode: Optional[str] = None):
    """List registered device names, optionally filtered by mode."""
    if mode is None:
        return list(_REGISTRY)
    return [n for n, (m, _) in _REGISTRY.items() if m == mode]
