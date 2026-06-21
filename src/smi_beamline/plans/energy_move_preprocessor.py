"""
smi_beamline.plans.energy_move_preprocessor
===========================================

An ``RE.preprocessor`` that routes **large** energy moves through the feedback-managed
:func:`smi_beamline.plans.energy_walk.energy_walk` -- uniformly, for every energy move in any plan
run through the RunEngine (scans, ``bps.mv(energy, E)``, queued multi-edge plans), while leaving
**small** moves as plain, fast ``set`` operations.

Why a preprocessor (and not ``Energy.set``)
-------------------------------------------
``Energy.set`` returns a ``Status`` synchronously and cannot *run a plan*; the managed move is a
plan (flux reads, OVAL settle, recenter loops, sleeps) that needs the RunEngine.  A preprocessor
is the clean way to make every plan-driven energy move go through that plan: it intercepts each
``Msg('set', energy, target)`` and, when the jump exceeds ``threshold_eV``, replaces it with the
``energy_walk`` sub-plan (which itself steps in ``step_eV`` increments).  Moves at or below the
threshold pass straight through unchanged, so fine scan steps and small nudges stay plain and fast.

Behaviour
---------
* ``|target - current| > threshold_eV`` (default 500): replace with
  ``energy_walk(target, step_eV=step_eV, verbose=False)`` -- silent (so a 500-point scan does not
  spam the console), with a single one-line **warning** that a managed large move is starting
  (sensible at the start of a scan / at an edge change).
* below 8 keV (start or target): still runs, but prints a **warning** that the feedback
  signs/gains/rails were characterised only >= 8 keV.
* the ``energy_walk`` sub-plan's own internal energy moves are <= ``step_eV`` (== threshold), so
  they pass straight through and never re-trigger this preprocessor (a re-entry guard backs this
  up regardless).

Not covered: a bare console ``energy.move(E)`` (no RunEngine) cannot run a plan, so it stays a
plain blocking move.  Use ``RE(move_energy(E))`` / ``RE(energy_walk(E))`` for the managed path at
the console.
"""
import warnings

import bluesky.preprocessors as bpp

from smi_beamline.plans.energy_walk import energy_walk


__all__ = ["energy_move_preprocessor", "install_energy_move_preprocessor"]

LOW_ENERGY_WARN_eV = 8000.0


def energy_move_preprocessor(plan, energy, *, threshold_eV=500.0, step_eV=500.0,
                             low_energy_warn_eV=LOW_ENERGY_WARN_eV, walk_kwargs=None,
                             verbose_walk=False):
    """Plan preprocessor: route ``Msg('set', energy, target)`` with ``|target-current| >
    threshold_eV`` through :func:`energy_walk` (``step_eV`` sub-steps); pass smaller moves through.

    Parameters
    ----------
    plan : generator
        The plan to wrap (the RunEngine passes this when installed on ``RE.preprocessors``).
    energy : positioner
        The ``energy`` pseudo-positioner whose ``set`` messages are intercepted (matched by
        identity).
    threshold_eV : float
        Jump size above which the managed walk engages (default 500).
    step_eV : float
        Sub-step size handed to ``energy_walk`` (default 500).
    low_energy_warn_eV : float
        Warn (but still run) when the start or target is below this (default 8000 eV; the feedback
        calibration is validated only >= 8 keV).
    walk_kwargs : dict, optional
        Extra kwargs forwarded to ``energy_walk`` (e.g. ``oval_window``, ``recenter_settle``).
    verbose_walk : bool
        If True, let ``energy_walk`` print its per-step detail (default False -> silent, just the
        one-line large-move warning).
    """
    walk_kwargs = dict(walk_kwargs or {})
    walking = {"active": False}    # re-entry guard: don't re-wrap sets emitted by our own walk

    def _current():
        p = energy.position
        return float(p.energy) if hasattr(p, "energy") else float(p)

    def _mutate(msg):
        if walking["active"]:
            return None, None      # inside our energy_walk -> leave its sets alone
        if msg.command != "set" or msg.obj is not energy or not msg.args:
            return None, None
        target = float(msg.args[0])
        cur = _current()
        if abs(target - cur) <= threshold_eV:
            return None, None      # small move -> plain set, untouched

        # Large move -> managed walk.  One warning line (sensible at scan start / edge change).
        lo = min(cur, target)
        warnings.warn(
            f"energy: managed large move {cur:.1f} -> {target:.1f} eV (>{threshold_eV:g} eV) via "
            f"energy_walk in {step_eV:g} eV steps with DCM feedback management."
            + ("  NOTE: below {:.0f} eV -- feedback calibration is validated only >= 8 keV."
               .format(low_energy_warn_eV) if lo < low_energy_warn_eV else ""),
            stacklevel=2,
        )

        def _walk():
            walking["active"] = True
            try:
                ret = yield from energy_walk(
                    target, energy=energy, step_eV=step_eV, verbose=verbose_walk, **walk_kwargs)
            finally:
                walking["active"] = False
            # ``set`` is expected to return a status-like to the host plan; energy_walk's last
            # internal move already left us at target, so a no-op completion is fine -- the host
            # plan's subsequent ``wait`` sees nothing pending.
            return ret

        return _walk(), None

    return (yield from bpp.plan_mutator(plan, _mutate))


def install_energy_move_preprocessor(RE, energy, *, threshold_eV=500.0, step_eV=500.0,
                                     replace=True, verbose=False, **kwargs):
    """Append the energy-move preprocessor to ``RE.preprocessors`` (the beamline default wiring).

    After this, **every** energy move in any plan run through ``RE`` with ``|target-current| >
    threshold_eV`` goes through the feedback-managed ``energy_walk`` (in ``step_eV`` sub-steps);
    smaller moves stay plain.  Tagged ``_smi_energy_move`` so re-installing de-dups.

    Returns the installed preprocessor.
    """
    if replace:
        RE.preprocessors[:] = [
            pp for pp in RE.preprocessors if not getattr(pp, "_smi_energy_move", False)
        ]

    def _pp(plan):
        return (yield from energy_move_preprocessor(
            plan, energy, threshold_eV=threshold_eV, step_eV=step_eV, **kwargs))

    try:
        _pp._smi_energy_move = True
        _pp._smi_threshold_eV = threshold_eV
        _pp._smi_step_eV = step_eV
    except (AttributeError, TypeError):
        pass

    RE.preprocessors.append(_pp)
    if verbose:
        print(f"\u2713 energy-move preprocessor installed: moves > {threshold_eV:g} eV use "
              f"energy_walk in {step_eV:g} eV steps")
    return _pp
