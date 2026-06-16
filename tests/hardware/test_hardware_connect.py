"""Tier-3 HARDWARE smoke tests -- connect to REAL EPICS PVs (read-only).

These are **deselected by default**.  Run them only on the beamline with::

    pixi run -e test test-hardware        # or:  pytest --run-hardware

Each test builds a device through the factory in REAL mode (``force="real"``)
and asserts it can connect within a short timeout.  They are **connection + read
only -- nothing is ever moved, opened, closed, or triggered.**

The device list below mirrors the ``smibase`` instantiation layer (same classes,
same PV prefixes, same constructor kwargs), so a green run here means the
post-refactor device *classes* still bind to the live IOCs.  Add devices by
extending ``DEVICES``; keep every entry read-only and side-effect free.

There is no beam dependency: connecting to a PV and reading a readback works
whether or not the shutter is open.
"""
import pytest

from smiclasses import device_factory as df

_CONNECT_TIMEOUT = 5.0


# (name, import path "module:ClassName", prefix, kwargs) -- mirrors smibase/*.
# name is used only for the factory registry / test id.
DEVICES = [
    # detectors
    ("pil2M", "smiclasses.pilatus:SAXS_Detector", "XF:12ID2-ES{Pilatus:Det-2M}",
     {"asset_path": "pilatus2m-1"}),
    ("pil900KW", "smiclasses.pilatus:WAXS_Detector", "XF:12IDC-ES:2{Det:900KW}",
     {"asset_path": "pilatus900kw-1"}),
    # sample stack (Huber coarse + SmarAct fine)
    ("stage", "smiclasses.manipulators:STG_pseudo", "XF:12IDC-OP:2{HUB:Stg-Ax:", {}),
    ("piezo", "smiclasses.manipulators:SMARACT", "", {}),
    ("bdm", "smiclasses.manipulators:BDMStage", "XF:12IDC-ES:2:", {}),
    # energy (DCM pseudo-positioner)
    ("energy", "smiclasses.energy:Energy", "", {}),
    # flux / I0 / transmitted
    ("xbpm2", "smiclasses.electrometers:XBPM", "XF:12IDA-BI:2{EM:BPM2}", {}),
    ("xbpm3", "smiclasses.electrometers:XBPM", "XF:12IDB-BI:2{EM:BPM3}", {}),
    ("pin_diode", "nslsii.ad33:QuadEMV33", "XF:12ID:2{EM:Tetr1}", {}),
    # temperature
    ("ls", "smiclasses.electrometers:new_LakeShore", "XF:12ID-ES", {}),
    # shutters / gate valve
    ("ph_shutter", "smiclasses.shutter:TwoButtonShutter", "XF:12IDA-PPS:2{PSh}", {}),
    ("GV7", "smiclasses.shutter:TwoButtonShutter", "XF:12IDC-VA:2{Det:1M-GV:7}", {}),
    # a representative attenuator foil (the one smi-plans uses)
    ("att2_9", "smiclasses.attenuators:Attenuator", "XF:12IDC-OP:2{Fltr:2-9}", {}),
]


def _import(path):
    module_name, cls_name = path.split(":")
    mod = __import__(module_name, fromlist=[cls_name])
    return getattr(mod, cls_name)


@pytest.mark.parametrize("name,cls_path,prefix,kwargs",
                         DEVICES, ids=[d[0] for d in DEVICES])
def test_device_connects(name, cls_path, prefix, kwargs):
    """Build the REAL device and assert it connects (no motion, no triggering)."""
    cls = _import(cls_path)
    dev = df.make_device(cls, prefix, name=name, force=df.REAL,
                         register=False, **kwargs)
    dev.wait_for_connection(timeout=_CONNECT_TIMEOUT)
    assert dev.connected, "{} ({}) failed to connect".format(name, prefix)


def test_waxs_arc_readback_present():
    """The WAXS arc readback (used by the arc-block detector logic) is reachable."""
    cls = _import("smiclasses.pilatus:WAXS_Detector")
    waxs = df.make_device(cls, "XF:12IDC-ES:2{Det:900KW}", name="pil900KW",
                          force=df.REAL, register=False, asset_path="pilatus900kw-1")
    waxs.wait_for_connection(timeout=_CONNECT_TIMEOUT)
    # read-only: the arc position must be a number we can read
    pos = waxs.motors.arc.position
    assert pos is not None


def test_stage_backcompat_aliases_connect():
    """The Huber stage's legacy .th/.ph/.ch aliases resolve to connected axes."""
    cls = _import("smiclasses.manipulators:STG_pseudo")
    stage = df.make_device(cls, "XF:12IDC-OP:2{HUB:Stg-Ax:", name="stage",
                           force=df.REAL, register=False)
    stage.wait_for_connection(timeout=_CONNECT_TIMEOUT)
    # the Phase-0 aliases must point at the (connected) rotation pseudo-axes
    assert stage.th is stage.theta
    assert stage.ph is stage.phi
    assert stage.ch is stage.chi
    assert stage.th.position is not None
