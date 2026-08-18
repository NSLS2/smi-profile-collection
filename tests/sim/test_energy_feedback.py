"""Tier-2 (sim) test for the Energy.set feedback choreography on the ERROR path.

The full success path (move completes -> completion-callback re-enables feedback) needs real-speed
motors that actually finish, so it lives in the ``integration`` tier (fake ophyd EpicsMotors never
complete a move).  But the **error path** -- a move that fails to start -> ``Energy.set`` must
re-enable feedback before re-raising -- is testable fast with fakes (a fake EpicsMotor's
``check_value`` raises because its simulated limits are unset, which fails the move).

This guards the property you care about: an energy move inside a plan must never leave the DCM
pitch/roll feedback OFF.
"""
import warnings

import pytest

from bluesky import RunEngine
import bluesky.plan_stubs as bps

from smi_beamline.devices import device_factory as df
from smi_beamline.devices import _context
from smi_beamline.devices.energy import Energy, UNMANAGED_MOVE_WARN_eV


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


def test_energy_move_direct_call_toggles_feedback(fake_energy):
    """The feedback choreography must also run for a bare console ``energy.move(E)``.

    Regression guard: ``Energy`` overrides ``move`` (the chokepoint that ``set`` funnels through),
    NOT just ``set``.  Previously only ``set`` was overridden, so ``energy.move(E)`` -- which ophyd
    routes via ``PositionerBase.set -> self.move``, i.e. straight to ``PseudoPositioner.move`` --
    bypassed the feedback disable/re-enable entirely.  Feedback is disabled ("1") up front and, when
    the fake-motor move fails (unset limits), re-enabled ("0") -- never left OFF.
    """
    en = fake_energy
    hist = []
    en.pitch_feedback_disabled.subscribe(lambda value, **k: hist.append(str(value)), run=False)
    try:
        en.move(en.position.energy + 50)      # bare console move (blocking); default wait=True
    except Exception:
        pass                                   # fake motor never completes; only the toggling matters
    assert "1" in hist, ("feedback was never disabled -> energy.move bypassed the choreography", hist)
    assert str(en.pitch_feedback_disabled.get()) == "0", hist
    assert str(en.roll_feedback_disabled.get()) == "0"


# --------------------------------------------------------------------- unmanaged-move courtesy warning
# ``Energy.move`` (the chokepoint ``set`` funnels through) emits a single ``warnings.warn`` when a
# LARGE move (>= the warn threshold) is made *directly* (not through the RunEngine, so it skips the
# managed ``energy_walk``).  ``warnings.warn`` (not the "bluesky" logger, which is file-only on the
# live beamline) so the reminder is visible on the console.  Detection: the RE calls ``energy.set``
# (-> ``move``) from its own plan thread (``RE._th``); a console ``energy.move``/``set`` runs on the
# caller's (main) thread.  The seam must have the RE wired for the check to engage (see
# ``_running_under_run_engine``); tests/off-beamline stay silent.

def _wire_re(re):
    """Point the _context seam at ``re`` so the unmanaged-move detector can compare threads.

    The autouse ``_unconfigured_context`` fixture restores it to None afterwards.
    """
    _context.configure(run_engine=re)


def test_direct_large_move_warns_when_re_wired(fake_energy):
    """A big DIRECT move (main thread, RE wired) warns with the one-line unmanaged-move reminder."""
    en = fake_energy
    RE = RunEngine({})
    _wire_re(RE)

    start = en.position.energy
    target = start + UNMANAGED_MOVE_WARN_eV + 100.0   # comfortably over the threshold
    with pytest.warns(UserWarning, match="NOT going through the RunEngine"):
        try:
            st = en.set((target,))     # direct call on the main thread -> unmanaged
            st.wait(timeout=5)
        except Exception:
            pass                       # fake motor never completes; we only care about the warning
    # feedback still restored on the (failed) move -- the warning doesn't change the choreography
    assert str(en.pitch_feedback_disabled.get()) == "0"


def test_direct_large_MOVE_warns_when_re_wired(fake_energy):
    """The reminder must also fire via the bare ``energy.move(E)`` entry point (the original bug:
    the warning lived on ``set``, which ``energy.move`` never calls)."""
    en = fake_energy
    RE = RunEngine({})
    _wire_re(RE)

    target = en.position.energy + UNMANAGED_MOVE_WARN_eV + 100.0
    with pytest.warns(UserWarning, match="NOT going through the RunEngine"):
        try:
            en.move(target)            # bare console move (blocking) -> unmanaged, must warn
        except Exception:
            pass                       # fake motor never completes; we only care about the warning
    assert str(en.pitch_feedback_disabled.get()) == "0"


def test_direct_small_move_does_not_warn(fake_energy):
    """A small direct move stays silent (small moves aren't managed anyway)."""
    en = fake_energy
    RE = RunEngine({})
    _wire_re(RE)

    with warnings.catch_warnings():
        warnings.simplefilter("error")               # any warning -> test failure
        try:
            st = en.set((en.position.energy + 50.0,))   # 50 eV << threshold
            st.wait(timeout=5)
        except Warning:
            raise                                    # a spurious courtesy warning: fail
        except Exception:
            pass                                     # fake-motor move failure is fine


def test_in_plan_large_move_does_not_warn(fake_energy, recwarn):
    """The SAME big move run through the RunEngine (bps.mv) must NOT warn -- it is the managed path
    (the preprocessor would route it through energy_walk on the live beamline)."""
    en = fake_energy
    RE = RunEngine({})
    _wire_re(RE)

    target = en.position.energy + UNMANAGED_MOVE_WARN_eV + 100.0
    try:
        RE(bps.mv(en, target))     # runs energy.set on the RE's plan thread -> managed
    except Exception:
        pass                       # fake motor never completes; only the warning matters here
    assert not any("NOT going through the RunEngine" in str(w.message) for w in recwarn.list)

def test_direct_large_move_silent_when_no_re_wired(fake_energy, recwarn):
    """With no RE wired (default test/off-beamline state) the detector can't tell console from
    plan, so it stays quiet -- no spurious warnings for a bare device."""
    en = fake_energy                    # _unconfigured_context leaves _context._run_engine = None
    target = en.position.energy + UNMANAGED_MOVE_WARN_eV + 100.0
    try:
        st = en.set((target,))
        st.wait(timeout=5)
    except Exception:
        pass
    assert not any("NOT going through the RunEngine" in str(w.message) for w in recwarn.list)
