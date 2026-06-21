"""Tier-2 (sim) test for the Energy.set feedback choreography on the ERROR path.

The full success path (move completes -> completion-callback re-enables feedback) needs real-speed
motors that actually finish, so it lives in the ``integration`` tier (fake ophyd EpicsMotors never
complete a move).  But the **error path** -- a move that fails to start -> ``Energy.set`` must
re-enable feedback before re-raising -- is testable fast with fakes (a fake EpicsMotor's
``check_value`` raises because its simulated limits are unset, which fails the move).

This guards the property you care about: an energy move inside a plan must never leave the DCM
pitch/roll feedback OFF.
"""
import pytest

from bluesky import RunEngine
import bluesky.plan_stubs as bps

from smi_beamline.devices import device_factory as df
from smi_beamline.devices.energy import Energy


def _seed(sig, value):
    (sig.sim_put if hasattr(sig, "sim_put") else sig.put)(value)


@pytest.fixture
def fake_energy():
    en = df.make_device(Energy, "", name="energy", force=df.FAKE,
                        read_attrs=["energy", "ivugap", "bragg", "harmonic"],
                        configuration_attrs=["enableivu", "enabledcmgap", "target_harmonic"])
    _seed(en.bragg.user_readback, 12.7)      # ~9 keV so forward()/inverse() are valid
    _seed(en.harmonic, 7)
    _seed(en.target_harmonic, 7)
    _seed(en.ivugap.user_readback, 7400)
    _seed(en.pitch_feedback_disabled, "0")   # feedback ON
    _seed(en.roll_feedback_disabled, "0")
    return en


def test_energy_set_disables_then_reenables_feedback_on_failed_move(fake_energy):
    """RE(bps.mv(energy, E)) (the in-plan path): feedback is disabled up front and, when the move
    fails (fake-motor limits), re-enabled -- never left OFF."""
    en = fake_energy
    hist = {"pitch": [], "roll": []}
    en.pitch_feedback_disabled.subscribe(
        lambda value, **k: hist["pitch"].append(str(value)), run=False)
    en.roll_feedback_disabled.subscribe(
        lambda value, **k: hist["roll"].append(str(value)), run=False)

    RE = RunEngine({})
    # The fake EpicsMotor move raises (unset simulated limits) -> Energy.set error path runs.
    try:
        RE(bps.mv(en, en.position.energy + 50))
    except Exception:
        pass

    # feedback was disabled ("1") up front ...
    assert "1" in hist["pitch"] and "1" in hist["roll"], hist
    # ... and is back ON ("0") -- the error path re-enabled it.
    assert str(en.pitch_feedback_disabled.get()) == "0", hist["pitch"]
    assert str(en.roll_feedback_disabled.get()) == "0", hist["roll"]


def test_energy_set_direct_call_reenables_on_failure(fake_energy):
    """Same property via a direct energy.set(...) call (not under the RE)."""
    en = fake_energy
    try:
        st = en.set((en.position.energy + 50,))
        st.wait(timeout=5)
    except Exception:
        pass
    assert str(en.pitch_feedback_disabled.get()) == "0"
    assert str(en.roll_feedback_disabled.get()) == "0"
