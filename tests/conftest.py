"""pytest configuration for the SMI profile-collection test suite.

Three test tiers (see ``docs/TESTING.md``):

* ``tests/unit``     -- ``@pytest.mark.unit``: pure code, constructs **no** devices.
* ``tests/sim``      -- ``@pytest.mark.sim``: builds **fake**, non-broadcasting
  ``ophyd.sim`` devices via :mod:`smiclasses.device_factory`; no hardware.
* ``tests/hardware`` -- ``@pytest.mark.hardware``: connects to **real** EPICS PVs.
  **Deselected by default**; opt in with ``pytest --run-hardware``.

Tests are auto-tagged with their tier marker from the directory they live in, so
``pytest -m sim`` / ``-m "not hardware"`` work without per-file boilerplate.

Hardware safety: unless ``--run-hardware`` is passed, this file forces the EPICS
Channel Access environment into a no-broadcast state so the unit/sim tiers can
never reach the live beamline.
"""
import os
import sys

import pytest

# Make ``import smiclasses.<module>`` work without installing the profile as a package.
_STARTUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "startup"))
if _STARTUP_DIR not in sys.path:
    sys.path.insert(0, _STARTUP_DIR)

_TIERS = ("unit", "sim", "hardware")


def _lock_down_epics():
    """Force EPICS CA to not auto-discover / not broadcast off-box.

    ``setdefault`` so an operator who deliberately exported these for a hardware
    run is respected, but the default test invocation is always sandboxed.
    """
    os.environ.setdefault("EPICS_CA_AUTO_ADDR_LIST", "NO")
    os.environ.setdefault("EPICS_CA_ADDR_LIST", "127.0.0.1")


def pytest_addoption(parser):
    parser.addoption(
        "--run-hardware",
        action="store_true",
        default=False,
        help="run the hardware tier (tests marked @pytest.mark.hardware) which "
        "connect to REAL EPICS PVs. Off by default.",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: pure-code test; constructs no devices")
    config.addinivalue_line("markers", "sim: builds fake (non-broadcasting) devices; no hardware")
    config.addinivalue_line(
        "markers", "hardware: connects to REAL hardware; opt-in via --run-hardware"
    )
    if not config.getoption("--run-hardware"):
        _lock_down_epics()


def pytest_collection_modifyitems(config, items):
    # 1. auto-tag each test with the tier marker for the directory it lives in
    for item in items:
        path = str(item.fspath)
        for tier in _TIERS:
            if (os.sep + tier + os.sep) in path:
                item.add_marker(getattr(pytest.mark, tier))
                break
    # 2. unless explicitly enabled, skip the hardware tier entirely
    if config.getoption("--run-hardware"):
        return
    skip_hw = pytest.mark.skip(reason="hardware tier: pass --run-hardware to enable")
    for item in items:
        if "hardware" in item.keywords:
            item.add_marker(skip_hw)


@pytest.fixture(autouse=True)
def _unconfigured_context():
    """Keep the ``smiclasses._context`` seam in its unconfigured (test) state.

    The seam degrades gracefully when not configured (``get_md() -> {}``,
    ``get_config() -> {}``, ``current_energy_eV() -> None``).  Reset it between
    tests in case one configures it.
    """
    from smiclasses import _context

    saved = (_context._run_engine, _context._config_dict, _context._energy_source)
    _context._run_engine = None
    _context._config_dict = None
    _context._energy_source = None
    yield
    (_context._run_engine, _context._config_dict, _context._energy_source) = saved


@pytest.fixture(autouse=True)
def _clean_device_factory():
    """Reset device_factory in-process overrides + registry between tests."""
    from smiclasses import device_factory

    device_factory.clear_overrides()
    saved = dict(device_factory._REGISTRY)
    device_factory._REGISTRY.clear()
    yield
    device_factory.clear_overrides()
    device_factory._REGISTRY.clear()
    device_factory._REGISTRY.update(saved)
