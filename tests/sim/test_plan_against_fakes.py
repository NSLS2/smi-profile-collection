"""Tier-2 demonstration: run real Bluesky plans against FAKE devices.

No hardware is touched -- the devices are ``ophyd.sim`` fakes built through the
factory, and the RunEngine drives them entirely in memory.  This is the level
at which a chronically-faked device (or the whole instrument) can be exercised
for plan-logic regressions while the real hardware is unavailable.
"""
import pytest

pytest.importorskip("bluesky")
from bluesky import RunEngine  # noqa: E402
import bluesky.plan_stubs as bps  # noqa: E402
import bluesky.plans as bp  # noqa: E402


def test_run_engine_sets_a_fake_signal(make_fake):
    """Drive a plan that sets an EpicsSignal-backed value on a fake device.

    (We use an EpicsSignal rather than an EpicsMotor: a fake EpicsMotor's move
    status does not auto-complete, so ``bps.mv`` on one would hang under the RE.
    Signals complete immediately, which is what plans like det_exposure_time do.)
    """
    from smiclasses.pilatus import PilatusDetectorCamV33

    cam = make_fake(PilatusDetectorCamV33, name="cam", prefix="FAKE:cam1:")
    RE = RunEngine({})
    RE(bps.mv(cam.acquire_time, 0.3, cam.num_images, 5))
    assert cam.acquire_time.get() == pytest.approx(0.3)
    assert cam.num_images.get() == 5


def test_run_engine_counts_a_fake_device(make_fake):
    from smiclasses.beamstop import SAXSBeamStops

    bs = make_fake(SAXSBeamStops, name="bs")
    docs = {"start": 0, "event": 0, "stop": 0}

    def collect(name, doc):
        if name in docs:
            docs[name] += 1

    RE = RunEngine({})
    RE(bp.count([bs], num=3), collect)
    assert docs["start"] == 1
    assert docs["event"] == 3
    assert docs["stop"] == 1
