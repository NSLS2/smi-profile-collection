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

# Make ``import smi_beamline`` (the Phase-4 package under src/) importable off-beamline.
_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

_TIERS = ("unit", "sim", "hardware", "integration")


def _lock_down_epics():
    """Force EPICS CA to not auto-discover / not broadcast off-box.

    ``setdefault`` so an operator who deliberately exported these for a hardware
    run is respected, but the default test invocation is always sandboxed.
    (Loopback ``127.0.0.1`` is also exactly what the local fake-IOC integration
    tier needs, so this is compatible with ``--run-iocs``.)
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
    parser.addoption(
        "--run-iocs",
        action="store_true",
        default=False,
        help="run the integration tier (tests marked @pytest.mark.integration) which "
        "spin up LOCAL, loopback-only fake caproto IOCs. Off by default.",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: pure-code test; constructs no devices")
    config.addinivalue_line("markers", "sim: builds fake (non-broadcasting) devices; no hardware")
    config.addinivalue_line(
        "markers", "hardware: connects to REAL hardware; opt-in via --run-hardware"
    )
    config.addinivalue_line(
        "markers", "integration: drives real device logic against a LOCAL fake IOC; "
        "opt-in via --run-iocs"
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
    if not config.getoption("--run-hardware"):
        skip_hw = pytest.mark.skip(reason="hardware tier: pass --run-hardware to enable")
        for item in items:
            if "hardware" in item.keywords:
                item.add_marker(skip_hw)
    # 3. unless explicitly enabled, skip the integration (fake-IOC) tier entirely
    if not config.getoption("--run-iocs"):
        skip_ioc = pytest.mark.skip(reason="integration tier: pass --run-iocs to enable")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_ioc)


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
