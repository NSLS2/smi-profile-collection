"""Tier-2 (sim) tests for the unreliable-attenuator retry logic.

The real attenuator foils need the actuation command re-issued before they confirm; a foil that
never confirms must FAIL the set (so a run halts rather than continue with the foil in the wrong
position).  We exercise :meth:`smiclasses.attenuators.Attenuator.set` against a fake device,
driving the (fake) ``status`` signal to simulate the hardware confirming -- or never confirming.
"""
import pytest

from ophyd.sim import make_fake_device

from smiclasses.attenuators import Attenuator, make_attenuator_bank


def _fast_fake_attenuator(name="att"):
    att = make_fake_device(Attenuator)("FAKE:", name=name)
    # short timings so the give-up path is quick (set settle_time explicitly so the test does
    # not depend on the class default, which is tuned for real hardware).
    att.settle_time = 0.3
    att.max_retries = 3
    att.timeout = 3.0
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


# ---------------------------------------------------------------------------
# Aggregate bank (Attenuators) -- moves a combination of foils as ONE unit,
# with settle-debounce so a foil that bounces back does not latch success.
# ---------------------------------------------------------------------------
import threading
import time


def _fake_bank(indices=(5, 6, 9), name="att"):
    Bank = make_attenuator_bank("BankT", "XF:12IDC-OP:2{{Fltr:2-{}}}", indices)
    bank = make_fake_device(Bank)("", name=name)
    for n in bank.component_names:
        f = getattr(bank, n)
        f.settle_time = 0.3
        f.max_retries = 5
        f.timeout = 8.0
        f.retry_delay = 0.2
        f.cmd_timeout = 0.3
        f.status.sim_put("Not Open")
    return bank


def _reliable_open(foil):
    foil.open_cmd.subscribe(lambda value, **k: foil.status.sim_put("Open"), run=False)


def _reliable_foil(foil):
    """Make a fake foil respond reliably to both open and close commands."""
    foil.open_cmd.subscribe(lambda value, **k: foil.status.sim_put("Open"), run=False)
    foil.close_cmd.subscribe(lambda value, **k: foil.status.sim_put("Not Open"), run=False)


def test_aggregate_inserts_requested_retracts_rest():
    bank = _fake_bank()
    for n in bank.component_names:
        _reliable_foil(getattr(bank, n))
    # start with f9 already open so we can see it get retracted
    bank.f9.status.sim_put("Open")

    st = bank.set(["f5", "f6"])
    st.wait(timeout=8)
    assert st.success
    assert bank.f5.status.get() == "Open"
    assert bank.f6.status.get() == "Open"
    assert bank.f9.status.get() == "Not Open"   # not requested -> retracted
    assert sorted(bank.inserted_foils()) == ["f5", "f6"]


def test_aggregate_debounces_bounce_back():
    """A foil that momentarily reads target then bounces back must be re-actuated, not latched."""
    bank = _fake_bank(indices=(5, 6))
    _reliable_open(bank.f6)

    # f5 bounces back after the first actuation (reads Open, then falls back within settle_time),
    # and only stays Open from the 2nd actuation on.
    n = {"f5": 0}

    def _f5_open(value, **kwargs):
        n["f5"] += 1
        bank.f5.status.sim_put("Open")
        if n["f5"] < 2:
            threading.Timer(0.1, lambda: bank.f5.status.sim_put("Not Open")).start()

    bank.f5.open_cmd.subscribe(_f5_open, run=False)

    st = bank.set(["f5", "f6"])
    st.wait(timeout=10)
    assert st.success
    assert bank.f5.status.get() == "Open"
    assert bank.f6.status.get() == "Open"
    assert n["f5"] >= 2          # the bounce was caught: f5 had to be re-actuated


def test_aggregate_fails_if_a_foil_never_settles():
    """If one foil keeps bouncing back, the whole aggregate FAILS (safe halt)."""
    bank = _fake_bank(indices=(5, 6))
    for f in (bank.f5, bank.f6):
        f.max_retries = 3
        f.timeout = 3.0
    _reliable_open(bank.f6)

    def _f5_open(value, **kwargs):
        bank.f5.status.sim_put("Open")
        threading.Timer(0.1, lambda: bank.f5.status.sim_put("Not Open")).start()

    bank.f5.open_cmd.subscribe(_f5_open, run=False)

    st = bank.set(["f5", "f6"])
    with pytest.raises(Exception):
        st.wait(timeout=8)
    assert not st.success


def test_aggregate_resolves_objects_and_names():
    bank = _fake_bank(indices=(5, 6, 9))
    want = bank._resolve_foils(["f5", bank.f9])
    assert {getattr(f, "name") for f in want} == {"att_f5", "att_f9"}


def test_aggregate_unknown_foil_raises():
    bank = _fake_bank(indices=(5, 6))
    with pytest.raises(ValueError):
        bank.set(["f99"])
