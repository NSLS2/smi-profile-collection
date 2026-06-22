
from smi_beamline.devices.energy import Energy, DCMInternals
from ophyd import EpicsMotor

energy = Energy(
    prefix="",
    name="energy",
    read_attrs=["energy", "ivugap", "bragg", "harmonic"],
    configuration_attrs=["enableivu", "enabledcmgap", "target_harmonic"],
)
energy.settle_time = 1

# Provide the live beamline energy to the device-class seam (used by e.g. the Pilatus
# ``energyset`` so it can remember the energy for camserver-restart threshold resets) without
# the device classes importing smibase.energy.  Runs after `energy` exists and before the
# detector modules are imported by startup.py.
from smi_beamline.devices import _context as _smiclasses_context
_smiclasses_context.configure(energy_source=energy)

dcm = energy
ivugap = energy.ivugap
dcm_gap = dcm.dcmgap  # Height in CSS # EpicsMotor('XF:12ID:m66', name='p2h')
dcm_pitch = EpicsMotor("XF:12ID:m67", name="dcm_pitch")
bragg = dcm.bragg  # Theta in CSS  # EpicsMotor('XF:12ID:m65', name='bragg')

dcm_config = DCMInternals("", name="dcm_config")

bragg.read_attrs = ["user_readback"]


# Hinting: plot ONLY the photon energy.  By default the EpicsMotor `user_readback` of bragg/ivugap
# (and the PseudoSingle energy) are all kind='hinted', which gives the device 3 hinted fields and
# makes the BestEffortCallback raise "we do not know how to pick out a single value".  Make the
# synthetic `energy` axis the sole hinted field; keep bragg/ivugap/dcmgap readbacks and `harmonic`
# recorded but kind='normal' (in every event, just not auto-plotted).  Do this AFTER the
# `bragg.read_attrs = [...]` reassignment above (which would otherwise re-hint bragg.user_readback).
energy.energy.kind = "hinted"
energy.bragg.user_readback.kind = "normal"
energy.ivugap.user_readback.kind = "normal"
energy.dcmgap.user_readback.kind = "normal"
energy.harmonic.kind = "normal"


_smiclasses_context.baseline_register([energy, dcm_config, ivugap, bragg])



manual_PID_disable_pitch = energy.pitch_feedback_disabled
manual_PID_disable_roll = energy.roll_feedback_disabled


def feedback(action=None):
    allowed_actions = ["on", "off"]
    assert (
        action in allowed_actions
    ), f'Wrong action: {action}, must choose: {" or ".join(allowed_actions)}'
    if action == "off":
        manual_PID_disable_pitch.set("1")
        manual_PID_disable_roll.set("1")
    elif action == "on":
        manual_PID_disable_pitch.set("0")
        manual_PID_disable_roll.set("0")


import bluesky.plan_stubs as bps


def move_energy(target_energy):
    """Plan: move the DCM energy to ``target_energy`` (eV) -- the message-pure path.

    Use this inside a Bluesky plan instead of ``energy.move(target_energy)``.

    Background
    ----------
    * ``energy.move(target_energy)`` is the **blocking convenience** for the console / scripts:
      it sets the energy and *waits* for the move to finish before returning.  It still works
      and is fine to type interactively, but it must NOT be used inside a plan (a blocking call
      in a plan stalls the RunEngine).
    * ``yield from move_energy(target_energy)`` (equivalently ``yield from bps.mv(energy,
      target_energy)``) is the message form for plans.  The DCM pitch/roll feedback is disabled
      for the move and re-enabled afterwards automatically -- that choreography now lives in the
      ``Energy.set`` ophyd device (wired with Status callbacks, non-blocking), so the plan needs
      to do nothing special.

    Migrating a script: replace ``energy.move(E)`` with ``yield from move_energy(E)`` (and make
    the enclosing function a generator / run it under ``RE``).
    """
    yield from bps.mv(energy, target_energy)


# ---------------------------------------------------------------------------------------------
# Feedback-managed energy move (Part B).  The full choreography (feedback off -> brake-confirmed
# move -> per-energy BPM3 range -> flux gate -> feedback on -> OVAL settle -> recenter coarse
# pitch/roll if |OVAL|>3000).  Run a single move explicitly with ``RE(energy_walk(E))``; >500 eV
# moves in any plan go through this automatically via the managed-move preprocessor (below).
# ---------------------------------------------------------------------------------------------
from smi_beamline.plans.energy_walk import energy_walk as _energy_walk_plan

#: Lazily-built DCMDiag (holds the BPM3/OVAL/feedback/m67-m68 PVs + verified signs).  Built on
#: first use so importing this module never blocks on a CA connect to BPM3.
_dcm_diag = None


def _get_dcm_diag():
    global _dcm_diag
    if _dcm_diag is None:
        from smi_beamline.plans.dcm_diag import DCMDiag
        _dcm_diag = DCMDiag(energy_source=energy)
    return _dcm_diag


def energy_walk(target_eV, **kwargs):
    """Plan: feedback-managed move of the photon energy to ``target_eV`` (eV).

    Thin wrapper over :func:`smi_beamline.plans.energy_walk.energy_walk` that supplies the live
    ``energy`` positioner and a (lazily-built, cached) ``DCMDiag``.  See that function for the full
    choreography and parameters.  Run as ``RE(energy_walk(E))``.

    The managed-move preprocessor (installed by default) already routes >500 eV moves in any plan
    through this; call this directly to run a single managed move explicitly at the console.
    """
    diag = kwargs.pop("diag", None) or _get_dcm_diag()
    return (yield from _energy_walk_plan(target_eV, diag=diag, energy=energy, **kwargs))


def dcm_diag():
    """Return the live :class:`DCMDiag` (build on first call).  For console diagnostics:
    ``dcm_diag().snapshot()`` / ``.measure_gain('roll')`` / ``.recenter('pitch')``."""
    return _get_dcm_diag()


# ---------------------------------------------------------------------------------------------
# Managed-energy-move PREPROCESSOR -- makes large energy moves in ANY plan (scans, bps.mv(energy,E),
# queued multi-edge plans) go through energy_walk in 500 eV steps; small moves stay plain.
# Installed by default at startup (startup.py calls enable_managed_energy_moves()); call
# disable_managed_energy_moves() at the console to turn it off for a session.
# ---------------------------------------------------------------------------------------------
def enable_managed_energy_moves(threshold_eV=500.0, step_eV=500.0, **kwargs):
    """Install the energy-move preprocessor on ``RE``: every plan energy move with
    ``|target-current| > threshold_eV`` is routed through the feedback-managed ``energy_walk`` in
    ``step_eV`` sub-steps (silent unless it errors, with one warning line per large move); smaller
    moves pass through as plain ``set`` (fine scan steps stay fast), but a small move that has let
    pitch/roll OVAL drift past its recentre window triggers an opportunistic coarse recentre
    (feedback stays ON) so fine-step scans can't creep into the piezo rail.

    Installed by default at startup; call this again to change ``threshold_eV``/``step_eV``.
    Idempotent (re-installing de-dups).  ``disable_managed_energy_moves()`` removes it.
    """
    from smi_beamline.plans.energy_move_preprocessor import install_energy_move_preprocessor
    RE = _smiclasses_context.get_re()
    diag = kwargs.pop("diag", None) or _get_dcm_diag()
    walk_kwargs = dict(kwargs.pop("walk_kwargs", {}))
    walk_kwargs.setdefault("diag", diag)
    return install_energy_move_preprocessor(
        RE, energy, threshold_eV=threshold_eV, step_eV=step_eV,
        diag=diag, walk_kwargs=walk_kwargs, verbose=True, **kwargs)


def disable_managed_energy_moves():
    """Remove the energy-move preprocessor from ``RE`` (energy moves go back to plain ``set``)."""
    RE = _smiclasses_context.get_re()
    before = len(RE.preprocessors)
    RE.preprocessors[:] = [
        pp for pp in RE.preprocessors if not getattr(pp, "_smi_energy_move", False)]
    removed = before - len(RE.preprocessors)
    print(f"managed energy moves: {'removed' if removed else 'were not installed'}")