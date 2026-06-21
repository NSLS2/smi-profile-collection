"""Tier-2 (sim) tests for the IVU brake-confirm + verify/retry logic of ``InsertionDevice.move``.

These build a FAKE ``InsertionDevice`` (no Channel Access) and drive the *real* ``move`` method,
monkeypatching the underlying ``EpicsMotor.move`` (the ``super().move`` call) so each "attempt"
has a controllable outcome -- whether the readback reaches target.  This exercises the Part A
retry loop (re-issue the gap move if it didn't reach target) deterministically and fast, without
needing the live-speed sim IOC (that path is covered by the ``integration`` tier).

The brake-CONFIRM timing (wait for ``BrakesDisengaged-Sts``) is covered against the fake IOC in
``tests/integration/test_energy_iocs.py``.
"""
import threading

import pytest

from ophyd import EpicsMotor
from ophyd.status import StatusBase

from smi_beamline.devices import device_factory as df
from smi_beamline.devices.machine import InsertionDevice


@pytest.fixture
def fake_ivu(make_fake):
    """A fake InsertionDevice with the brake readback already 'disengaged' and fast tunables."""
    ivu = df.make_device(
        InsertionDevice, "SR:C12-ID:G1{IVU:1-Ax:Gap}-Mtr", name="ivu", force=df.FAKE)
    # Make the brake-confirm wait instant: the SP write mirrors onto the readback, and a fake
    # brake.put already updates brake.get(), so confirmation is immediate.
    ivu.brake_settle = 0.0
    ivu.brake_timeout = 2.0
    ivu.move_deadband = 5.0
    ivu.max_move_attempts = 2
    # brake.put should drive the readback (fake signal: put updates get()); start engaged.
    ivu.brake.sim_put(0)
    ivu.user_readback.sim_put(7400.0)
    ivu.user_setpoint.sim_put(7400.0)
    return ivu


def _instant_status():
    st = StatusBase()
    st.set_finished()
    return st


def test_move_succeeds_first_attempt(fake_ivu, monkeypatch):
    """A move whose readback reaches target on the first attempt finishes with no retry."""
    attempts = {"n": 0}

    def fake_super_move(self, position, wait=False, **kw):
        attempts["n"] += 1
        self.user_readback.sim_put(float(position))   # reaches target immediately
        return _instant_status()

    monkeypatch.setattr(EpicsMotor, "move", fake_super_move)

    st = fake_ivu.move(7600.0, wait=True, timeout=10)
    assert st.success
    assert attempts["n"] == 1                          # no retry needed
    assert fake_ivu.user_readback.get() == pytest.approx(7600.0)
    assert int(fake_ivu.brake.get()) == 1              # brake was disengaged


def test_move_retries_when_first_attempt_misses(fake_ivu, monkeypatch):
    """If the gap doesn't reach target (dropped command), move re-issues and succeeds (the
    automatic "move it twice")."""
    attempts = {"n": 0}

    def fake_super_move(self, position, wait=False, **kw):
        attempts["n"] += 1
        if attempts["n"] == 1:
            # first attempt: dropped -> readback stays put (still far from target)
            pass
        else:
            self.user_readback.sim_put(float(position))   # second attempt reaches target
        return _instant_status()

    monkeypatch.setattr(EpicsMotor, "move", fake_super_move)

    st = fake_ivu.move(7600.0, wait=True, timeout=10)
    assert st.success
    assert attempts["n"] == 2                          # exactly one retry
    assert fake_ivu.user_readback.get() == pytest.approx(7600.0)


def test_move_gives_up_after_max_attempts(fake_ivu, monkeypatch):
    """If every attempt misses, move fails after ``max_move_attempts`` (no infinite loop)."""
    fake_ivu.max_move_attempts = 3
    attempts = {"n": 0}

    def fake_super_move(self, position, wait=False, **kw):
        attempts["n"] += 1
        return _instant_status()                       # never moves the readback

    monkeypatch.setattr(EpicsMotor, "move", fake_super_move)

    st = fake_ivu.move(7600.0, wait=False, timeout=10)
    with pytest.raises(Exception):
        st.wait(timeout=10)                            # FailedStatus / RuntimeError
    assert attempts["n"] == 3                          # tried exactly the budget
    assert not st.success


def test_move_within_deadband_counts_as_reached(fake_ivu, monkeypatch):
    """A readback within move_deadband of target is 'reached' -> no retry."""
    attempts = {"n": 0}

    def fake_super_move(self, position, wait=False, **kw):
        attempts["n"] += 1
        self.user_readback.sim_put(float(position) - 3.0)   # 3 um short, deadband is 5
        return _instant_status()

    monkeypatch.setattr(EpicsMotor, "move", fake_super_move)

    st = fake_ivu.move(7600.0, wait=True, timeout=10)
    assert st.success
    assert attempts["n"] == 1                          # within deadband -> accepted, no retry


def test_move_disengages_brake_each_attempt(fake_ivu, monkeypatch):
    """The brake is (re-)disengaged before every attempt."""
    brake_writes = []
    orig_put = fake_ivu.brake.put

    def record_put(value, **kw):
        brake_writes.append(int(value))
        return orig_put(value, **kw)

    fake_ivu.brake.put = record_put

    attempts = {"n": 0}

    def fake_super_move(self, position, wait=False, **kw):
        attempts["n"] += 1
        if attempts["n"] >= 2:
            self.user_readback.sim_put(float(position))
        return _instant_status()

    monkeypatch.setattr(EpicsMotor, "move", fake_super_move)

    fake_ivu.move(7600.0, wait=True, timeout=10)
    # disengage (1) written once per attempt (2 attempts here)
    assert brake_writes.count(1) == 2


def test_move_returns_immediately_when_not_waiting(fake_ivu, monkeypatch):
    """wait=False returns a Status right away (non-blocking) for the Energy pseudo-positioner."""
    started = threading.Event()

    def fake_super_move(self, position, wait=False, **kw):
        started.set()
        self.user_readback.sim_put(float(position))
        return _instant_status()

    monkeypatch.setattr(EpicsMotor, "move", fake_super_move)

    st = fake_ivu.move(7600.0, wait=False)
    assert isinstance(st, StatusBase)
    assert st.wait(timeout=10) is None or st.success    # completes on the worker thread
    assert started.is_set()
