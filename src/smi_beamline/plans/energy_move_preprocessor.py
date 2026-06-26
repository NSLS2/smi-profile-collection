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
* ``|target - current| <= threshold_eV``: plain, fast ``set`` (fine scan steps stay untouched).
  But if a ``diag`` is available, after the move each axis' settled ``OVAL`` is checked against its
  recentre window and, if a run of small moves has let it **drift toward the piezo rail**, the
  coarse motor is recentred (feedback stays ON) -- so fine-step scans can't creep into the rail.
* below the validated floor (``low_energy_warn_eV``, default 2100 eV = the beamline minimum; start
  or target): still runs, but prints a **warning**.  The managed move is live-validated across the
  full 2.1 -> 16.1 keV range, so this normally never fires.
* the ``energy_walk`` sub-plan's own internal energy moves are <= ``step_eV`` (== threshold), so
  they pass straight through and never re-trigger this preprocessor (a re-entry guard backs this
  up regardless).

Not covered: a bare console ``energy.move(E)`` (no RunEngine) cannot run a plan, so it stays a
plain blocking move.  Use ``RE(move_energy(E))`` / ``RE(energy_walk(E))`` for the managed path at
the console.
"""
import warnings

import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp

from smi_beamline.plans.energy_walk import (
    energy_walk, recenter_axis_plan, LOW_ENERGY_STEP_BELOW_eV, LOW_ENERGY_STEP_eV)


__all__ = ["energy_move_preprocessor", "install_energy_move_preprocessor"]

#: Warn (but still run) when a managed move starts/ends below this (eV).  The managed move is
#: live-validated across the full 2.1 -> 16.1 keV range down to the 2100 eV beamline minimum, so
#: this is effectively "below the validated floor" and normally never fires.
LOW_ENERGY_WARN_eV = 2100.0


def energy_move_preprocessor(plan, energy, *, threshold_eV=500.0, step_eV=500.0,
                             low_energy_warn_eV=LOW_ENERGY_WARN_eV, walk_kwargs=None,
                             verbose_walk=False, diag=None, check_drift=True,
                             drift_window=None, drift_target=400.0,
                             low_below=LOW_ENERGY_STEP_BELOW_eV, low_step=LOW_ENERGY_STEP_eV):
    """Plan preprocessor: route ``Msg('set', energy, target)`` with ``|target-current| >
    threshold_eV`` through :func:`energy_walk` (``step_eV`` sub-steps); pass smaller moves through.

    Small-move drift guard
    ----------------------
    Small moves (``<= threshold_eV``) stay plain and fast, but a *succession* of them can slowly
    walk the DCM pitch/roll feedback toward its piezo rail without ever triggering the managed
    recentre.  So after each small move (``check_drift``, default on, and a ``diag`` is available),
    each axis' settled ``OVAL`` is checked against its recentre window (``drift_window`` or
    ``diag.recenter_window(axis)`` -- roll ~2000, pitch ~4000); if exceeded, a one-line warning is
    printed and the coarse motor is recentred (feedback stays ON throughout) back under
    ``drift_target``.  This is the same recentre the managed walk uses, applied opportunistically so
    fine-step scans cannot creep into the rail unnoticed.

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
        Warn (but still run) when the start or target is below this (default 2100 eV = the beamline
        minimum).  The managed move is live-validated across the full 2.1 -> 16.1 keV range, so this
        is effectively "below the validated floor" and normally never fires.
    walk_kwargs : dict, optional
        Extra kwargs forwarded to ``energy_walk`` (e.g. ``oval_window``, ``recenter_settle``).
    verbose_walk : bool
        If True, let ``energy_walk`` print its per-step detail (default False -> silent, just the
        one-line large-move warning).
    diag : DCMDiag, optional
        The feedback/OVAL holder used for the small-move drift check.  If omitted, falls back to
        ``walk_kwargs['diag']``; with no diag available the drift check is skipped.
    check_drift : bool
        If true (default), run the small-move OVAL drift check / recentre described above.
    drift_window : float, optional
        OVAL magnitude that triggers a small-move recentre.  ``None`` (default) uses the per-axis
        ``diag.recenter_window(axis)``.
    drift_target : float
        Recentre the drifting axis back under this ``|OVAL|`` (default 400).
    """
    walk_kwargs = dict(walk_kwargs or {})
    if diag is None:
        diag = walk_kwargs.get("diag")
    walking = {"active": False}    # re-entry guard: don't re-wrap sets emitted by our own walk

    def _current():
        p = energy.position
        return float(p.energy) if hasattr(p, "energy") else float(p)

    def _drift_check():
        """After a small move: recentre any axis whose settled OVAL has drifted out of its window."""
        for axis in ("roll", "pitch"):
            win = drift_window if drift_window is not None else diag.recenter_window(axis)
            oval = float((yield from bps.rd(diag.oval[axis])))
            if abs(oval) > win:
                warnings.warn(
                    f"energy: {axis} OVAL {oval:+.0f} drifted past its window ({win:.0f}) over small "
                    f"moves -- recentring the coarse {axis} motor (feedback stays ON).",
                    stacklevel=2,
                )
                yield from recenter_axis_plan(
                    diag, axis, target=drift_target, verbose=verbose_walk, flux_floor=None)

    def _needs_managed(cur, target):
        """True if this move should go through ``energy_walk`` (sub-stepped): either the jump
        exceeds ``threshold_eV``, or it is in/into the low-energy region (<= ``low_below``) with a
        span larger than the low-energy sub-step (so the finer 50 eV stepping is enforced there)."""
        span = abs(target - cur)
        if span > threshold_eV:
            return True
        if min(cur, target) <= low_below and span > low_step:
            return True
        return False

    def _mutate(msg):
        if walking["active"]:
            return None, None      # inside our energy_walk / re-emitted set -> leave it alone
        if msg.command != "set" or msg.obj is not energy or not msg.args:
            return None, None
        target = float(msg.args[0])
        cur = _current()
        if not _needs_managed(cur, target):
            if not (check_drift and diag is not None):
                return None, None      # small move -> plain set, untouched
            # Small move: do the plain set, then opportunistically recentre if OVAL has drifted.

            def _small_then_check():
                walking["active"] = True
                try:
                    yield msg                       # the original set, re-emitted verbatim
                finally:
                    walking["active"] = False
                yield from _drift_check()
                return None

            return _small_then_check(), None

        # Managed move -> energy_walk.  One warning line (sensible at scan start / edge change).
        lo = min(cur, target)
        low_note = (f"  ({low_step:g} eV sub-steps below {low_below:g} eV.)"
                    if lo <= low_below else "")
        warnings.warn(
            f"energy: managed move {cur:.1f} -> {target:.1f} eV via energy_walk in {step_eV:g} eV "
            f"steps with DCM feedback management." + low_note
            + ("  NOTE: below {:.0f} eV -- below the validated feedback range."
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
    smaller moves stay plain (but, if a ``diag`` is supplied and ``check_drift`` is on, a small move
    that has let pitch/roll OVAL drift past its window triggers an opportunistic recentre).  Tagged
    ``_smi_energy_move`` so re-installing de-dups.  Extra ``**kwargs`` (``diag``, ``walk_kwargs``,
    ``check_drift``, ``drift_window``, ``drift_target``, ``verbose_walk`` ...) pass through to
    :func:`energy_move_preprocessor`.

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
