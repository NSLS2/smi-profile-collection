"""
pytest configuration for the SMI profile-collection device-class tests.

These tests exercise the ophyd **device classes** in ``startup/smiclasses`` **without any
hardware** -- they must import and (via ``ophyd.sim.make_fake_device``) instantiate against
mock PVs.  This is the off-beamline safety net the profile historically lacked.

The device classes were decoupled from the live-beamline bootstrap (``smibase.base``) via the
``smiclasses._context`` seam, so importing ``smiclasses.*`` no longer triggers EPICS / Redis /
Tiled / IPython.  We add ``startup/`` to ``sys.path`` so ``import smiclasses.<mod>`` resolves.
"""
import os
import sys

import pytest

# Make ``import smiclasses.<module>`` work without installing the profile as a package.
_STARTUP_DIR = os.path.join(os.path.dirname(__file__), "..", "startup")
sys.path.insert(0, os.path.abspath(_STARTUP_DIR))


@pytest.fixture(autouse=True)
def _unconfigured_context():
    """Ensure the device-class context seam is in its unconfigured (test) state.

    The seam degrades gracefully when not configured (``get_md() -> {}``,
    ``get_config() -> {}``, ``current_energy_eV() -> None``), which is exactly what we want for
    hardware-free tests.  This fixture resets it between tests in case one configures it.
    """
    from smiclasses import _context
    saved = (_context._run_engine, _context._config_dict, _context._energy_source)
    _context._run_engine = None
    _context._config_dict = None
    _context._energy_source = None
    yield
    (_context._run_engine, _context._config_dict, _context._energy_source) = saved
