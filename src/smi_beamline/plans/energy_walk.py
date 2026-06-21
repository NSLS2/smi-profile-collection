"""
smi_beamline.plans.energy_walk
==============================

Feedback-managed energy move (Part B) as a **message-pure RunEngine plan**.

``energy_walk(target_eV)`` choreographs a reliable energy change with the DCM beam-position
feedback:

1. **feedback OFF** (both pitch & roll);
2. **brake-confirmed energy move** to ``target_eV`` (uses the Part A ``InsertionDevice.move`` fix
   under the hood via ``bps.mv(energy, ...)``), then **verify** the energy actually moved;
3. **flux gate** -- BPM3 sum must exceed an *energy-dependent* threshold (``<8 keV`` -> ``>10``;
   ``<10 keV`` -> ``>5``; else ``>1``).  On failure: make sure the axes are in position, dwell a
   second, **revert to the previous energy**, and raise (a signal that smaller steps are needed);
4. **feedback ON**;
5. wait until ``OVAL`` (the PID control value / piezo command) **settles**;
6. per axis, if ``|OVAL| > oval_window`` (~3000), **slowly re-centre** with the coarse DCM motors
   (m68 roll / m67 pitch) -- small steps, ``<= 1/s``, judged on the *settled* OVAL direction, with
   a **wrong-way abort** -- until ``|OVAL| < oval_target`` (~400);
7. only then report success.

Message-pure: every read is ``bps.rd``, every move ``bps.mv``/``bps.abs_set``, every dwell
``bps.sleep`` -- no blocking ``.get()``/``time.sleep`` -- so it runs under the RunEngine and the
queueserver.  The whole thing is wrapped in ``finalize_wrapper`` so **feedback is left ON** even on
abort/Ctrl-C.

The live signals (energy, the two ``fast_pidX/Y.OVAL`` control values, the feedback enable bits,
m67/m68, BPM3 sum) and the verified per-axis sign / flux thresholds come from a
:class:`smi_beamline.plans.dcm_diag.DCMDiag` instance, so the PV wiring and Phase-0 calibration
live in one place.
"""
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp

from smi_beamline.plans.dcm_diag import flux_threshold


__all__ = ["energy_walk", "recenter_axis_plan", "settle_oval_plan"]


# ---------------------------------------------------------------- small message-pure helpers
def _rd(sig):
    """Read a signal's value inside a plan (float)."""
    val = yield from bps.rd(sig)
    return float(val)


def settle_oval_plan(diag, axis="both", oval_window=300.0, seconds=2.0, interval=0.2,
                     timeout=8.0):
    """Wait (message-pure) until ``OVAL`` of ``axis`` is peak-to-peak stable within
    ``oval_window`` for ``seconds``; return True if it settled, False on ``timeout``.

    Gates on OVAL (steady) rather than the very noisy beam-position CVAL.
    """
    axes = ("roll", "pitch") if axis == "both" else (axis,)
    recent = {a: [] for a in axes}
    elapsed = 0.0
    stable_for = 0.0
    nkeep = max(2, int(seconds / interval) + 1)
    while elapsed < timeout:
        for a in axes:
            v = yield from _rd(diag.oval[a])
            recent[a].append(v)
            recent[a][:] = recent[a][-nkeep:]
        enough = all(len(recent[a]) >= nkeep for a in axes)
        ptp = max((max(recent[a]) - min(recent[a])) for a in axes if recent[a])
        if enough and ptp <= oval_window:
            stable_for += interval
            if stable_for >= seconds:
                return True
        else:
            stable_for = 0.0
        yield from bps.sleep(interval)
        elapsed += interval
    return False


def recenter_axis_plan(diag, axis, target=400.0, step=0.0001, settle=1.5, rate=1.0,
                       max_steps=200, max_step=0.002, oval_abort=None, deadband=10.0,
                       sample_interval=0.15, adapt=True, verbose=True,
                       rail_step_factor=10.0, rail_max_steps=3):
    """Message-pure version of ``DCMDiag.recenter``: step the coarse motor for ``axis`` until
    ``|OVAL[axis]| < target``, judging on the **settled** OVAL direction (waits ``settle`` s so a
    brief wrong-way transient does not abort), with an adaptive step and a wrong-way abort.

    At-the-rail behaviour: when ``|OVAL|`` is saturated at the rail, the small adaptive steps barely
    register (the loop is clamped), so the step is enlarged by ``rail_step_factor`` (default 10x,
    still clamped to ``rail_step_factor * max_step``) to decisively pull OVAL off the rail; only
    ``rail_max_steps`` (default 3) such rail steps are allowed before aborting (vs. many ineffective
    small ones).

    Raises ``RuntimeError`` on a *settled* wrong-way step, on ``|OVAL|`` reading *beyond* the axis
    hardware rail, or if ``max_steps``/``rail_max_steps`` is hit without progress.
    """
    # Default abort = the axis rail + margin (per-axis: roll ~+/-4095, pitch ~+/-8191).  Being AT
    # the rail is allowed -- that's when stepping toward 0 matters; only a reading clearly beyond
    # the rail is treated as invalid.
    rail = diag.rail(axis) if hasattr(diag, "rail") else diag.OVAL_RANGE
    margin = getattr(diag, "OVAL_RAIL_MARGIN", 200.0)
    oval_abort = (rail + margin) if oval_abort is None else oval_abort
    period = 1.0 / max(rate, 1e-6)
    per_step_settle = max(settle, period)
    sign = diag.assumed_sign[axis]
    sig = diag.oval[axis]
    mot = diag.motor[axis]
    cur_step = abs(step)
    rail_steps = 0          # how many enlarged "at the rail" steps we've taken

    for i in range(1, max_steps + 1):
        cur = yield from _rd(sig)
        if abs(cur) < target:
            if verbose:
                print(f"recenter {axis}: |OVAL|={abs(cur):.1f} < {target:.0f}  DONE ({i-1} steps)")
            return True
        if abs(cur) > oval_abort:
            raise RuntimeError(
                f"{axis} OVAL {cur:.1f} reads beyond the hardware rail (+/-{rail:.0f}); "
                "treating as invalid -- aborting recenter (check PV/connection).")

        before = cur
        at_rail = abs(before) >= (rail - margin)        # OVAL is saturated at the rail
        want = -1.0 if cur > 0 else 1.0                 # desired sign of dOVAL (toward 0)
        # At the rail, take a decisive enlarged step (small steps don't move a saturated loop).
        if at_rail:
            rail_steps += 1
            if rail_steps > rail_max_steps:
                raise RuntimeError(
                    f"{axis}: OVAL still at the rail (~{before:+.0f}) after {rail_max_steps} "
                    f"enlarged steps -- not coming off (wrong sign? / piezo cannot recover).  "
                    "Aborting; re-check by hand.")
            # 10x the BASE step (not the adapted one), bounded by max_step.
            step_mag = min(abs(step) * rail_step_factor, abs(max_step))
        else:
            step_mag = min(abs(cur_step), abs(max_step))
        motor_delta = (want / sign) * step_mag
        if verbose:
            railnote = f" [at rail, enlarged step {rail_steps}/{rail_max_steps}]" if at_rail else ""
            print(f"{axis}: OVAL {before:+.1f} -> step {mot.name} {motor_delta:+.5f} EGU; "
                  f"settling {per_step_settle:.1f}s ...{railnote}")
        yield from bps.mv(mot, mot.position + motor_delta)

        # settle: poll OVAL for the window; judge on the mean of the final third.
        samples = []
        waited = 0.0
        while waited < per_step_settle:
            samples.append((yield from _rd(sig)))
            yield from bps.sleep(sample_interval)
            waited += sample_interval
        if not samples:
            samples = [(yield from _rd(sig))]
        tail = samples[max(1, 2 * len(samples) // 3):] or samples[-1:]
        after = sum(tail) / len(tail)
        delta_oval = after - before
        gain = (delta_oval / motor_delta) if motor_delta else 0.0
        moved = abs(delta_oval) > deadband
        correct = (not moved) or (delta_oval * want > 0)
        if verbose:
            print(f"{axis}: OVAL {before:+.1f} -> {after:+.1f} settled "
                  f"(dOVAL={delta_oval:+.1f}, gain~{gain:+.0f} OVAL/EGU, "
                  f"{'toward 0' if correct else 'WRONG WAY'})")
        if not correct:
            raise RuntimeError(
                f"{axis}: settled OVAL moved the WRONG way ({before:+.1f} -> {after:+.1f}) after "
                f"a {motor_delta:+.5f} step on {mot.name} -- sign/coupling not as assumed; "
                "aborting before the piezo is driven into the rail.")

        # Once OVAL has come off the rail, reset the rail-step counter and resume normal adapt.
        if not (abs(after) >= (rail - margin)):
            rail_steps = 0
            if adapt and abs(gain) > 1e-9:
                want_dOVAL = -0.5 * after                # aim halfway to 0 (damped)
                cur_step = max(min(abs(want_dOVAL / gain), max_step), abs(step) * 0.25)

    raise RuntimeError(
        f"recenter {axis}: hit max_steps={max_steps} without reaching |OVAL| < {target:.0f}.")


# ---------------------------------------------------------------- the main plan
def energy_walk(target_eV, *, diag=None, energy=None,
                flux_settle=1.0, oval_settle_s=3.0, oval_settle_window=300.0,
                oval_window=None, oval_target=None, recenter_step=0.0001,
                recenter_rate=1.0, recenter_settle=1.5, move_tol_eV=1.0, verbose=True):
    """Plan: feedback-managed move of the photon energy to ``target_eV`` (eV).

    Parameters
    ----------
    target_eV : float
        Target photon energy in eV.
    diag : DCMDiag, optional
        The feedback signal/calibration holder (PVs + verified signs + flux thresholds).  If
        ``None``, one is built (``DCMDiag(energy_source=energy)``).
    energy : positioner, optional
        The ``energy`` pseudo-positioner.  If ``None``, taken from ``diag._energy_source``.
    flux_settle : float
        Dwell (s) before the flux re-check / before reverting on flux failure.
    oval_settle_s, oval_settle_window : float
        After feedback ON, wait until OVAL is peak-to-peak within ``oval_settle_window`` for
        ``oval_settle_s`` (or a timeout).
    oval_window : float, optional
        Re-centre an axis only if ``|OVAL| > oval_window``.  If ``None`` (default), uses the
        per-axis trigger from the diag (``diag.recenter_window(axis)`` -- roll ~2000, pitch ~4000,
        well inside the rails 4095 / 8191 to avoid the nonlinear edge).  A scalar overrides both
        axes.
    oval_target : float, optional
        Re-centre drives ``|OVAL|`` below this; ``None`` (default) uses ``diag.OVAL_TARGET`` (~400).
    recenter_step, recenter_rate, recenter_settle : float
        Coarse-motor step (EGU), max steps/s, and per-step settle for the recenter loop.
    move_tol_eV : float
        Tolerance for "the energy actually moved / reached target".

    Raises
    ------
    RuntimeError
        If the energy did not move/reach target, if the flux gate fails (after reverting), or if a
        recenter step goes the wrong way.  On any exit, **feedback is left ON**.
    """
    from smi_beamline.plans.dcm_diag import DCMDiag

    if diag is None:
        diag = DCMDiag(energy_source=energy)
    if energy is None:
        energy = diag._energy_source
    if energy is None:
        raise ValueError("energy_walk needs an `energy` positioner (pass energy= or a diag with "
                         "an energy_source).")

    def _emit(msg):
        if verbose:
            print(msg)

    def _body():
        start_eV = float(energy.position) if not hasattr(energy.position, "energy") \
            else float(energy.position.energy)
        _emit(f"energy_walk: {start_eV:.2f} -> {target_eV:.2f} eV")

        # 1) feedback OFF (both)
        _emit("  feedback OFF")
        yield from bps.mv(diag.fb_disable["roll"], "1", diag.fb_disable["pitch"], "1")

        # 2) brake-confirmed energy move (Part A path), then verify it moved/reached target
        _emit("  moving energy (brake-confirmed) ...")
        yield from bps.mv(energy, float(target_eV))
        now_eV = float(energy.position) if not hasattr(energy.position, "energy") \
            else float(energy.position.energy)
        if abs(now_eV - target_eV) > move_tol_eV:
            raise RuntimeError(
                f"energy did not reach target: at {now_eV:.2f} eV, wanted {target_eV:.2f} eV "
                f"(|diff| {abs(now_eV - target_eV):.2f} > {move_tol_eV}).")
        _emit(f"  energy at {now_eV:.2f} eV")

        # 3) flux gate (energy-dependent).  On failure: settle, revert, raise.
        flux = yield from _rd(diag.sumY)
        thr = flux_threshold(now_eV / 1000.0, diag.flux_table)
        _emit(f"  flux sumY={flux:.3f}  threshold(@{now_eV/1000:.2f}keV)={thr:.3f}")
        if flux <= thr:
            _emit("  FLUX LOW -> settling, then reverting energy")
            yield from bps.sleep(flux_settle)
            flux = yield from _rd(diag.sumY)               # one more chance after settle
            if flux <= thr:
                yield from bps.mv(energy, start_eV)        # revert to previous energy
                raise RuntimeError(
                    f"energy_walk: BPM3 flux {flux:.3f} below threshold {thr:.3f} at "
                    f"{now_eV:.2f} eV -- reverted to {start_eV:.2f} eV.  Use smaller energy steps.")

        # 4) feedback ON (both)
        _emit("  feedback ON")
        yield from bps.mv(diag.fb_disable["roll"], "0", diag.fb_disable["pitch"], "0")

        # 5) wait for OVAL to settle
        settled = yield from settle_oval_plan(
            diag, axis="both", oval_window=oval_settle_window, seconds=oval_settle_s,
            timeout=max(oval_settle_s * 3, 6.0))
        _emit(f"  OVAL {'settled' if settled else 'did NOT settle (continuing)'}")

        # 6) per-axis recenter if |OVAL| exceeds the axis trigger window (well inside the rail).
        for axis in ("roll", "pitch"):
            win = oval_window if oval_window is not None else diag.recenter_window(axis)
            tgt = oval_target if oval_target is not None else getattr(diag, "OVAL_TARGET", 400.0)
            ov = yield from _rd(diag.oval[axis])
            if abs(ov) > win:
                _emit(f"  {axis}: |OVAL|={abs(ov):.1f} > {win:.0f} -> recentering to <{tgt:.0f}")
                yield from recenter_axis_plan(
                    diag, axis, target=tgt, step=recenter_step, settle=recenter_settle,
                    rate=recenter_rate, verbose=verbose)
            else:
                _emit(f"  {axis}: |OVAL|={abs(ov):.1f} within +/-{win:.0f} (no recenter)")

        _emit(f"energy_walk: DONE at {now_eV:.2f} eV")

    def _restore_feedback_on():
        # Always leave feedback ON, even on abort/error.
        yield from bps.mv(diag.fb_disable["roll"], "0", diag.fb_disable["pitch"], "0")

    return (yield from bpp.finalize_wrapper(_body(), _restore_feedback_on()))
