"""Tier-2 (sim) tests for the unreliable-attenuator retry logic.

The real attenuator foils need the actuation command re-issued before they confirm; a foil that
never confirms must FAIL the set (so a run halts rather than continue with the foil in the wrong
position).  We exercise :meth:`smiclasses.attenuators.Attenuator.set` against a fake device,
driving the (fake) ``status`` signal to simulate the hardware confirming -- or never confirming.
"""
import pytest

from ophyd.sim import make_fake_device

from smiclasses.attenuators import Attenuator


def _fast_fake_attenuator(name="att"):
    att = make_fake_device(Attenuator)("FAKE:", name=name)
    # short timings so the give-up path is quick
    att.max_retries = 3
    att.timeout = 2.0
    att.retry_delay = 0.2
    att.cmd_timeout = 0.3
    return att


def test_flaky_foil_retries_then_succeeds():
    """A foil that only confirms after a couple of re-actuations: set() retries and SUCCEEDS."""
    att = _fast_fake_attenuator()
    att.status.sim_put("Not Open")

    # Simulate the flaky hardware: confirm "Open" only on the 2nd actuation.
    state = {"n": 0}

    def _on_open(value, **kwargs):
        state["n"] += 1
        if state["n"] >= 2:
            att.status.sim_put("Open")

    att.open_cmd.subscribe(_on_open, run=False)

    st = att.set("Insert")
    st.wait(timeout=5)
    assert st.success
    assert att.status.get() == "Open"
    assert state["n"] >= 2            # it really had to retry


def test_stuck_foil_fails_safely():
    """A foil that never confirms: set() FAILS (raises) rather than silently succeeding."""
    att = _fast_fake_attenuator(name="stuck")
    att.status.sim_put("Not Open")   # never changes

    st = att.set("Insert")
    with pytest.raises(Exception):
        st.wait(timeout=6)
    assert not st.success
    assert att.status.get() != "Open"


def test_already_in_position_succeeds_immediately():
    """Setting to the state the foil is already in finishes (success) right away."""
    att = _fast_fake_attenuator(name="att2")
    att.status.sim_put("Open")
    st = att.set("Insert")
    st.wait(timeout=2)
    assert st.success


def test_unknown_state_raises():
    att = _fast_fake_attenuator()
    att.status.sim_put("Not Open")
    with pytest.raises(ValueError):
        att.set("sideways")


def test_concurrent_set_rejected():
    """A second set while one is in progress is rejected (the foil is single-actuation)."""
    att = _fast_fake_attenuator()
    att.status.sim_put("Not Open")   # stays unconfirmed so the first set is still 'in progress'
    st1 = att.set("Insert")
    try:
        with pytest.raises(RuntimeError):
            att.set("Retract")
    finally:
        # let the first set time out / finish so we don't leak the timer threads
        try:
            st1.wait(timeout=4)
        except Exception:
            pass
