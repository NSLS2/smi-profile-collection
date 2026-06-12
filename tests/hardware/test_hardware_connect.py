"""Tier-3 HARDWARE smoke tests -- connect to REAL EPICS PVs.

These are **deselected by default**.  Run them only on the beamline with::

    pixi run -e test test-hardware        # or:  pytest --run-hardware

Each test builds a device through the factory in REAL mode (``force="real"``)
and asserts it can connect within a short timeout.  They never move anything --
connection + read only.  Add real-prefix devices here as needed; keep them
read-only and side-effect free.
"""
import pytest

from smiclasses import device_factory as df

# Real PV prefixes (mirror the smibase instantiation layer).
_PIL2M_PREFIX = "XF:12ID2-ES{Pilatus:Det-2M}"
_PIL900KW_PREFIX = "XF:12IDC-ES:2{Det:900KW}"
_CONNECT_TIMEOUT = 5.0


def _connect(cls, prefix, name, **kwargs):
    dev = df.make_device(cls, prefix, name=name, force=df.REAL, register=False, **kwargs)
    dev.wait_for_connection(timeout=_CONNECT_TIMEOUT)
    return dev


def test_pil2M_connects():
    from smiclasses.pilatus import SAXS_Detector

    det = _connect(SAXS_Detector, _PIL2M_PREFIX, "pil2M", asset_path="pilatus2m-1")
    assert det.connected


def test_pil900KW_connects():
    from smiclasses.pilatus import WAXS_Detector

    det = _connect(WAXS_Detector, _PIL900KW_PREFIX, "pil900KW", asset_path="pilatus900kw-1")
    assert det.connected
