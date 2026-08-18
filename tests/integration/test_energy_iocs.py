"""Integration tests: drive the REAL Energy / InsertionDevice logic against a fake IOC.

These spin up the local caproto ``tests/iocs/sim_energy_ioc.py`` (sandbox prefix ``SMIsim:``,
loopback only) which serves DCM + undulator motors that **move at finite, configurable speeds**.
We then point lightweight subclasses of the real :class:`smi_beamline.devices.energy.Energy` /
:class:`smi_beamline.devices.machine.InsertionDevice` at that IOC and exercise the actual move
choreography that ``ophyd.sim`` cannot (instantaneous fakes have no readback ramp):

* ``set`` / ``move`` -- DCM feedback is disabled during the move and re-enabled after (Status
  chaining; H1).
* ``InsertionDevice.move`` -- the IVU brake is disengaged before the gap moves (H2).
* ``small_move`` -- bragg and IVU finish *together* because the faster axis is slowed to match
  the slower one, and the original speeds are restored afterwards.

Marked ``integration``; opt in with ``--run-iocs`` (off by default, like the hardware tier, so a
normal ``pixi run -e test test`` stays pure unit+sim).  The IOC is loopback-only and uses a
sandbox prefix, so it never touches the real beamline.
"""
import os
import sys
import time
import signal
import socket
import subprocess

import pytest

pytestmark = pytest.mark.integration

from ophyd import Component as Cpt, EpicsSignal, EpicsMotor

# Import the real classes under test.
from smi_beamline.devices.energy import Energy
from smi_beamline.devices.machine import InsertionDevice

PREFIX = "SMIsim:"
_IOC_PATH = os.path.join(os.path.dirname(__file__), "..", "iocs", "sim_energy_ioc.py")


# ---------------------------------------------------------------------------
# Test device subclasses: same logic as the real classes, PVs -> the fake IOC.
# ---------------------------------------------------------------------------
class SimInsertionDevice(InsertionDevice):
    """InsertionDevice whose brake/gap_speed point at the sandbox IOC (keeps move() logic).

    The brake / gap-speed PVs are *absolute* (``add_prefix=()``) so they are not prefixed by the
    parent IVU-motor prefix -- mirroring the real device, where ``IVUBrakeCpt`` / ``gap_speed``
    splice their own absolute PV rather than appending to the motor prefix.
    """
    brake = Cpt(EpicsSignal, PREFIX + "ivu:brake:RB", write_pv=PREFIX + "ivu:brake",
                add_prefix=())
    gap_speed = Cpt(EpicsSignal, PREFIX + "ivu:gapspeed:RB", write_pv=PREFIX + "ivu:gapspeed",
                    add_prefix=())


class SimEnergy(Energy):
    """Energy with all real motors/feedback pointed at the sandbox IOC (keeps all logic)."""
    dcmgap = Cpt(EpicsMotor, "dcmgap", read_attrs=["user_readback"])
    bragg = Cpt(EpicsMotor, "bragg", read_attrs=["user_readback"])
    # Feedback-disable signals: string channels matching the real device (writes "0"/"1").
    pitch_feedback_disabled = Cpt(EpicsSignal, "fbk:pitch", string=True)
    roll_feedback_disabled = Cpt(EpicsSignal, "fbk:roll", string=True)
    ivugap = Cpt(SimInsertionDevice, "ivu", read_attrs=["user_readback"],
                 add_prefix=("suffix",))


# ---------------------------------------------------------------------------
# IOC fixture
# ---------------------------------------------------------------------------
def _free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="module")
def sim_ioc():
    """Launch the loopback-only fake energy IOC for the module; tear it down after."""
    ioc_env = dict(os.environ)
    ioc_env["EPICS_CAS_INTF_ADDR_LIST"] = "127.0.0.1"
    ioc_env["EPICS_CAS_BEACON_ADDR_LIST"] = "127.0.0.1"

    proc = subprocess.Popen(
        [sys.executable, _IOC_PATH, "--prefix", PREFIX, "--interfaces", "127.0.0.1"],
        env=ioc_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )

    # Point THIS process's CA client at the loopback IOC (before ophyd connects).
    os.environ["EPICS_CA_ADDR_LIST"] = "127.0.0.1"
    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"

    # Wait until a known PV is reachable (or fail fast with the IOC output).
    deadline = time.time() + 25
    ready = False
    from caproto.sync.client import read
    while time.time() < deadline:
        if proc.poll() is not None:
            pytest.fail("sim IOC exited early:\n" + proc.stdout.read())
        try:
            read(PREFIX + "bragg.RBV", timeout=1)
            ready = True
            break
        except Exception:
            time.sleep(0.5)
    if not ready:
        proc.send_signal(signal.SIGINT)
        out = ""
        try:
            proc.wait(timeout=3)
            out = proc.stdout.read()
        except Exception:
            proc.kill()
        pytest.fail("sim IOC did not become ready in time. IOC output:\n" + out)

    yield PREFIX
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=10)
    except Exception:
        proc.kill()


@pytest.fixture
def energy(sim_ioc):
    en = SimEnergy(prefix=sim_ioc, name="energy",
                   read_attrs=["energy", "ivugap", "bragg", "harmonic"],
                   configuration_attrs=["enableivu", "enabledcmgap", "target_harmonic"])
    en.wait_for_connection(timeout=10)

    en.harmonic.put(7)
    en.target_harmonic.put(7)
    # feedback starts enabled ("0")
    en.pitch_feedback_disabled.put("0")
    en.roll_feedback_disabled.put("0")

    # Put the stack at a self-consistent starting point for ~9.4 keV.  Use fast velocities and
    # move the real motors directly (bypassing the energy pseudo) so setup is quick + reliable.
    en.bragg.velocity.put(20.0)
    en.dcmgap.velocity.put(20.0)
    en.ivugap.gap_speed.put(20000.0)   # also drives the ivu motor VELO (IOC putter)
    import time as _t
    _t.sleep(0.3)
    start_bragg = en.energy_to_bragg(9400.0)
    start_ivu = en.energy_to_gap(9400.0, 7)
    en.bragg.move(start_bragg, timeout=15)
    en.ivugap.move(start_ivu, timeout=15)
    # leave the axes at a moderate speed so a move is observably non-instant
    en.bragg.velocity.put(2.0)
    en.ivugap.gap_speed.put(2000.0)
    _t.sleep(0.2)
    yield en


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_ioc_motor_moves_at_finite_speed(energy):
    """Sanity: a sim motor actually ramps (not instantaneous)."""
    start = energy.bragg.position
    energy.bragg.velocity.put(0.5)
    st = energy.bragg.set(start + 1.0)
    # immediately after issuing, it should NOT be done yet (finite speed)
    time.sleep(0.1)
    moving_seen = not st.done
    st.wait(timeout=20)
    assert abs(energy.bragg.position - (start + 1.0)) < 0.05
    assert moving_seen, "motor appeared to move instantly (IOC not simulating speed?)"


def test_set_toggles_feedback_around_move(energy):
    """energy.set disables feedback during the move and re-enables it after (H1)."""
    hist = []
    energy.pitch_feedback_disabled.subscribe(
        lambda value, **k: hist.append(str(value)), run=False)

    # Slow the axes right down so the move takes long enough to observe "feedback disabled"
    # mid-flight (a fast move would re-enable before we can sample it).  Confirm the velocity
    # actually took effect on the IOC before proceeding.
    energy.bragg.velocity.put(0.02, wait=True)
    energy.ivugap.gap_speed.put(200.0, wait=True)
    for _ in range(20):
        if abs(energy.bragg.velocity.get() - 0.02) < 1e-6:
            break
        time.sleep(0.1)
    assert abs(energy.bragg.velocity.get() - 0.02) < 1e-6, "bragg velocity did not slow"

    target = energy.position[0] + 30.0   # a small but real energy step (eV)
    st = energy.set((target,))
    # while moving, feedback must be disabled
    time.sleep(0.4)
    assert str(energy.pitch_feedback_disabled.get()) == "1", (
        "feedback not disabled during move (or move already finished); hist=%s" % hist)
    st.wait(timeout=60)
    # after the move, feedback must be back on
    time.sleep(0.5)
    assert str(energy.pitch_feedback_disabled.get()) == "0"
    # sequence saw a disable ("1") then a re-enable ("0")
    assert "1" in hist and hist[-1] == "0", hist


def test_set_toggles_feedback_under_runengine(energy):
    """The SAME feedback choreography must work when energy is moved INSIDE A PLAN (the scan path):
    ``RE(bps.mv(energy, E))`` -> Msg('set', energy) -> Energy.set under the RunEngine.

    This is the path a scan / queued plan uses (NOT the direct ``energy.set()`` call), and the
    re-enable runs from the move-Status completion callback while the RE drives the move.  We
    assert feedback is disabled ("1") at some point and is back ON ("0") after the run completes.
    """
    from bluesky import RunEngine
    import bluesky.plan_stubs as bps

    # start with feedback ON
    energy.pitch_feedback_disabled.put("0", wait=True)
    energy.roll_feedback_disabled.put("0", wait=True)

    hist = {"pitch": [], "roll": []}
    energy.pitch_feedback_disabled.subscribe(
        lambda value, **k: hist["pitch"].append(str(value)), run=False)
    energy.roll_feedback_disabled.subscribe(
        lambda value, **k: hist["roll"].append(str(value)), run=False)

    # moderate speeds so the move completes in a few seconds (the IOC motors actually ramp)
    energy.bragg.velocity.put(2.0, wait=True)
    energy.ivugap.gap_speed.put(2000.0, wait=True)

    target = energy.position[0] + 30.0
    RE = RunEngine({})
    RE(bps.mv(energy, target))        # <-- the in-plan move path

    time.sleep(0.5)                   # let the completion callback's re-enable land
    # feedback was disabled at some point during the move
    assert "1" in hist["pitch"] and "1" in hist["roll"], hist
    # and is back ON now that the run finished
    assert str(energy.pitch_feedback_disabled.get()) == "0", hist["pitch"]
    assert str(energy.roll_feedback_disabled.get()) == "0", hist["roll"]
    # the energy actually moved
    assert abs(energy.position[0] - target) < 2.0


def test_set_reenables_feedback_on_failed_move_under_runengine(energy):
    """If the move FAILS inside a plan, feedback must still be re-enabled (not left off).

    We force a failure by commanding past a real-motor soft limit; the RE raises, and the
    finalize/completion path must leave feedback ON.
    """
    from bluesky import RunEngine
    import bluesky.plan_stubs as bps

    energy.pitch_feedback_disabled.put("0", wait=True)
    energy.roll_feedback_disabled.put("0", wait=True)

    # Command an energy whose bragg target is outside the sim bragg limits (-30..30 deg) so the
    # underlying move is rejected -> Energy.set's error path must re-enable feedback.
    RE = RunEngine({})
    bad_energy = 1.0e6   # absurd -> forward() bragg far out of range / move rejected
    try:
        RE(bps.mv(energy, bad_energy))
    except Exception:
        pass  # expected to fail

    time.sleep(0.3)
    assert str(energy.pitch_feedback_disabled.get()) == "0", "feedback left OFF after a failed move"
    assert str(energy.roll_feedback_disabled.get()) == "0", "feedback left OFF after a failed move"



def test_ivu_brake_disengaged_before_move(energy):
    """InsertionDevice.move disengages the brake before the gap moves, and reaches target (H2)."""
    brake_hist = []
    energy.ivugap.brake.subscribe(
        lambda value, **k: brake_hist.append(value), run=False)

    start = energy.ivugap.position
    st = energy.ivugap.move(start + 200.0, wait=False)
    st.wait(timeout=10)
    assert any(int(v) == 1 for v in brake_hist), "brake was never disengaged"
    # the gap actually REACHED the target (not just "Status succeeded")
    assert abs(energy.ivugap.position - (start + 200.0)) <= energy.ivugap.move_deadband


def test_ivu_move_waits_for_brake_confirm(energy):
    """With a brake that takes time to *confirm* disengaged, the gap must not start moving until
    BrakesDisengaged-Sts reads disengaged -- and must still reach target.

    This is the core of the Part A fix: the old code wrote the brake SP and (CA-ack only) issued
    the gap immediately, so the gap could be commanded while still braked.  The sim IOC's
    ``ivu:brake:delay`` holds the Sts readback "engaged" for a while after the SP write.
    """
    brake_delay = EpicsSignal(PREFIX + "ivu:brake:delay", name="brake_delay")
    brake_delay.wait_for_connection(timeout=5)
    brake_delay.put(0.8, wait=True)            # brake confirms ~0.8 s after the SP write
    try:
        # Slow the gap so motion is observable; park the brake engaged first.
        energy.ivugap.gap_speed.put(2000.0, wait=True)
        energy.ivugap.brake.put(0, wait=True)  # engaged
        time.sleep(0.2)

        start = energy.ivugap.position
        st = energy.ivugap.move(start + 300.0, wait=False)

        # At 0.4 s the brake has NOT yet confirmed (delay 0.8 s) -> the gap must not have moved.
        time.sleep(0.4)
        moved_early = abs(energy.ivugap.position - start) > energy.ivugap.move_deadband
        assert not moved_early, (
            "gap moved before the brake confirmed disengaged (pos moved %.1f um)"
            % (energy.ivugap.position - start))

        st.wait(timeout=10)
        # ...but it does reach target once the brake confirms.
        assert abs(energy.ivugap.position - (start + 300.0)) <= energy.ivugap.move_deadband
    finally:
        brake_delay.put(0.0, wait=True)        # restore instant-brake for other tests



def test_small_move_axes_finish_together(energy):
    """small_move slows the faster axis so bragg + IVU arrive together; speeds restored."""
    import threading
    from bluesky import RunEngine

    orig_bragg_v = energy.bragg.velocity.get()
    orig_ivu_v = energy.ivugap.gap_speed.get()
    start_bragg = energy.bragg.position
    start_ivu = energy.ivugap.position

    # Record the time each axis reports done-moving (DMOV 0->1) during the small move.
    done_times = {}

    def _watch(name, motor):
        def _cb(value, **k):
            # DMOV goes 1 (idle) -> 0 (moving) -> 1 (done); capture the *done* edge after motion
            if int(value) == 1 and name in done_times.get("_moving", set()):
                done_times[name] = time.time()
        return _cb

    done_times["_moving"] = set()

    def _moving_cb(name):
        def _cb(value, **k):
            if int(value) == 0:
                done_times["_moving"].add(name)
        return _cb

    cb_b = energy.bragg.motor_done_move.subscribe(_watch("bragg", energy.bragg), run=False)
    cb_i = energy.ivugap.motor_done_move.subscribe(_watch("ivu", energy.ivugap), run=False)
    mb = energy.bragg.motor_is_moving.subscribe(_moving_cb("bragg"), run=False)
    mi = energy.ivugap.motor_is_moving.subscribe(_moving_cb("ivu"), run=False)

    target = energy.position[0] + 20.0   # small step
    RE = RunEngine({})
    RE(energy.small_move(target))

    # both axes actually moved
    assert abs(energy.bragg.position - start_bragg) > 1e-6
    assert abs(energy.ivugap.position - start_ivu) > 1.0

    # they finished reasonably close together (the point of matching speeds): without matching,
    # the fast IVU would finish ~seconds before the slow bragg; with matching they are within ~1s
    # (residual gap is acceleration ramps + gap-speed propagation in the sim).
    if "bragg" in done_times and "ivu" in done_times:
        assert abs(done_times["bragg"] - done_times["ivu"]) < 1.2, (
            "axes did not finish together: bragg@%.3f ivu@%.3f"
            % (done_times["bragg"], done_times["ivu"]))

    # speeds restored to originals (the finalize ran with wait=True)
    assert energy.bragg.velocity.get() == pytest.approx(orig_bragg_v, rel=1e-3)
    assert energy.ivugap.gap_speed.get() == pytest.approx(orig_ivu_v, rel=1e-3)
