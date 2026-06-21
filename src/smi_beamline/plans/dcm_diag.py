"""
DCM feedback / energy-move PHASE-0 DIAGNOSTIC (read-only first, tiny supervised nudges)
=======================================================================================

Run from the bluesky IPython console **with live beam**, supervised, abort with Ctrl-C.

Purpose
-------
Characterise the DCM beam-position feedback so the automated energy-move choreography
(``energy_walk``, Part B) can be built and trusted.  Specifically:

* read-only logging of BPM3 flux, both PID **control values** (``OVAL``), beam position errors
  (``CVAL``), the coarse DCM motors (m67 pitch / m68 roll), and energy;
* the **energy-dependent flux gate** the move will use;
* a **single, supervised** coarse-motor step (:func:`DCMDiag.recenter_once`) and a slow,
  guarded loop (:func:`DCMDiag.recenter`) to verify -- on the real system -- that moving
  roll/pitch drives ``OVAL`` toward zero (the single most safety-critical unknown) and that
  ``|OVAL|`` converges.

**Polarity assumption (to be verified by this script):** moving ROLL (m68) **+** moves its
control value **+**; PITCH (m67) is the opposite (**+** move -> control value **-**).  Every
nudge checks the **signed direction** of the OVAL *change* (toward 0), so over-correcting through
zero is fine; it **aborts only** if OVAL moved the *opposite* of intended (genuine wrong sign /
coupling change) -- so a wrong sign cannot drive the piezo into the rail.

Observed on the live system (10 keV): OVAL is steady (roll ~+207, pitch ~+1005) while the
beam-position **CVAL is very noisy** (swings +/-20000 sample-to-sample).  So OVAL is the
meaningful signal -- ``settled()`` gates on OVAL stability, not CVAL.  These coarse motors also
have **hysteresis / are not reproducible**, so the per-step OVAL response varies; the loop
re-measures the gain every step and only relies on its *sign*, with small steps (default 0.0001
EGU) clamped to ``max_step``.

Nothing here is wired into the RunEngine or any plan.  The moves are plain blocking
``motor.move(rel, wait=True)`` console calls (Ctrl-C aborts), each small (default 0.0001 EGU) and
rate-limited (>=1 s apart).

Quick use
---------
>>> d = DCMDiag(energy_source=energy)   # builds the PV handles
>>> d.snapshot()                  # one read-only line: flux / OVAL / CVAL / motors / energy
>>> d.monitor(seconds=20)         # log a few times a second for 20 s (read-only)
>>> d.flux_ok()                   # is BPM3 flux above the energy-dependent threshold right now?
>>> d.measure_gain('roll')        # ONE small step; report d(OVAL)/d(m68) sign+magnitude (no abort)
>>> d.recenter_once('roll')       # ONE small step on m68; abort only if OVAL moves the WRONG way
>>> d.recenter('roll')            # slow adaptive loop: step roll until |OVAL_roll| < 400
>>> d.recenter('pitch')           # same for pitch (m67)
"""
import time

from ophyd import EpicsSignal, EpicsSignalRO, EpicsMotor


# --------------------------------------------------------------------------- flux gate
#: BPM3-sum flux thresholds vs photon energy (keV).  ``(max_energy_keV, min_sum)`` rows, checked
#: in order; the first row whose ``max_energy_keV`` the current energy is **below** applies.  Last
#: row is the high-energy floor.  Edit here (or pass ``flux_table=`` to :class:`DCMDiag`).
DEFAULT_FLUX_TABLE = [
    (8.0, 10.0),     # E < 8 keV    -> sum must be > 10
    (10.0, 5.0),     # 8 <= E < 10  -> sum must be > 5
    (12.0, 1.0),     # 10 <= E < 12 -> sum must be > 1
    (float("inf"), 0.1),   # E >= 12 keV -> sum must be > 0.1
]


def flux_threshold(energy_keV, table=None):
    """Return the minimum acceptable BPM3 sum for ``energy_keV`` from ``table``."""
    table = table or DEFAULT_FLUX_TABLE
    for max_e, min_sum in table:
        if energy_keV < max_e:
            return min_sum
    return table[-1][1]


# --------------------------------------------------------------------------- BPM3 range (gain)
#: BPM3 electrometer **range enum index** vs photon energy (keV).  ``(max_energy_keV, range_idx)``
#: rows, checked in order; the first row whose ``max_energy_keV`` the energy is **below** applies.
#: Index map is 0-based (confirmed live: "100 uA" reads back as 2): ``1 = 10 uA``, ``2 = 100 uA``,
#: ``3 = 1000 uA`` (full-scale current; smaller index -> more sensitive).  Low energy has more BPM3
#: flux -> a less sensitive (larger full-scale) range; high energy less flux -> more sensitive.
DEFAULT_RANGE_TABLE = [
    (10.0, 3),     # E < 10 keV    -> 1000 uA (index 3)
    (12.0, 2),     # 10 <= E < 12  -> 100 uA  (index 2)
    (float("inf"), 1),   # E >= 12 keV -> 10 uA (index 1)
]


def range_index(energy_keV, table=None):
    """Return the BPM3 electrometer range enum index for ``energy_keV`` from ``table``."""
    table = table or DEFAULT_RANGE_TABLE
    for max_e, idx in table:
        if energy_keV < max_e:
            return idx
    return table[-1][1]


# --------------------------------------------------------------------------- the diagnostic
class DCMDiag:
    """Read-only DCM-feedback diagnostics + supervised single-step coarse re-centring.

    Parameters
    ----------
    bpm3_prefix : str
        BPM3 / PID record prefix (default ``"XF:12IDB-BI:2{EM:BPM3}"``).
    energy_source : object, optional
        Something with ``.position`` in **eV** (the live ``energy`` positioner).  If ``None``, the
        diagnostic still works but ``energy_keV`` / the flux gate read 0 / the lowest threshold.
    flux_table : list, optional
        Override :data:`DEFAULT_FLUX_TABLE`.
    """

    #: Per-axis OVAL hardware rail (|OVAL| saturates here -- the piezo DAC limit).  MEASURED on
    #: the live system: roll rails at ~+/-4095 (12-bit), pitch at ~+/-8191.  Being AT the rail is
    #: exactly when re-centring (toward 0) matters most, so the loop steps from the rail; it only
    #: refuses a value that reads *beyond* the rail by ``OVAL_RAIL_MARGIN`` (a garbage/disconnected
    #: reading).  ``OVAL_RANGE`` is kept as a back-compat fallback for any axis not in the dict.
    OVAL_RANGE = 8192.0
    OVAL_RAIL = {"roll": 4095.0, "pitch": 8191.0}
    OVAL_RAIL_MARGIN = 200.0   # allow readings up to rail+margin before calling them invalid

    #: Per-axis recenter-TRIGGER threshold: re-centre an axis when |OVAL| exceeds this.  Set well
    #: inside the rail (~half) to stay out of the nonlinear region near the edge -- roll ~2000 (rail
    #: 4095), pitch ~4000 (rail 8191).  ``OVAL_TARGET`` is how far in we then drive it.
    OVAL_RECENTER_WINDOW = {"roll": 2000.0, "pitch": 4000.0}
    OVAL_TARGET = 400.0

    def rail(self, axis):
        """The OVAL saturation limit (|OVAL|) for ``axis``."""
        return self.OVAL_RAIL.get(axis, self.OVAL_RANGE)

    def recenter_window(self, axis):
        """The |OVAL| above which ``axis`` should be re-centred (per-axis, well inside the rail)."""
        return self.OVAL_RECENTER_WINDOW.get(axis, 0.5 * self.rail(axis))

    def __init__(self, bpm3_prefix="XF:12IDB-BI:2{EM:BPM3}", energy_source=None, flux_table=None):
        p = bpm3_prefix
        self.flux_table = flux_table or DEFAULT_FLUX_TABLE
        self._energy_source = energy_source

        # --- per-axis PID records: X = roll, Y = pitch (confirmed convention) ----------------
        # Control value (piezo command) -- the thing kept within +/-3000 then driven to <400.
        self.oval = {
            "roll":  EpicsSignalRO(f"{p}fast_pidX.OVAL", name="oval_roll"),
            "pitch": EpicsSignalRO(f"{p}fast_pidY.OVAL", name="oval_pitch"),
        }
        # Beam-position error process value (CVAL) and setpoint (VAL): error = CVAL - VAL.
        self.cval = {
            "roll":  EpicsSignalRO(f"{p}fast_pidX.CVAL", name="cval_roll"),
            "pitch": EpicsSignalRO(f"{p}fast_pidY.CVAL", name="cval_pitch"),
        }
        self.setp = {
            "roll":  EpicsSignalRO(f"{p}fast_pidX.VAL", name="vsp_roll"),
            "pitch": EpicsSignalRO(f"{p}fast_pidY.VAL", name="vsp_pitch"),
        }
        # Feedback enable/disable bits bluesky already uses ("0"=on / "1"=off).
        self.fb_disable = {
            "roll":  EpicsSignal(f"{p}fast_pidX_incalc.CLCN", name="fb_dis_roll", string=True),
            "pitch": EpicsSignal(f"{p}fast_pidY_incalc.CLCN", name="fb_dis_pitch", string=True),
        }

        # --- BPM3 flux + position --------------------------------------------------------------
        self.sumX = EpicsSignalRO(f"{p}SumX:MeanValue_RBV", name="bpm3_sumX")
        self.sumY = EpicsSignalRO(f"{p}SumY:MeanValue_RBV", name="bpm3_sumY")
        self.posX = EpicsSignalRO(f"{p}PosX:MeanValue_RBV", name="bpm3_posX")
        self.posY = EpicsSignalRO(f"{p}PosY:MeanValue_RBV", name="bpm3_posY")

        # --- BPM3 electrometer range / gain (mbbo set + mbbi readback) -------------------------
        # Index map is 0-based (confirmed on the live IOC: "100 uA" reads back as 2):
        #   1 = 10 uA, 2 = 100 uA, 3 = 1000 uA (full-scale current; smaller -> more sensitive).
        self.range_sp = EpicsSignal(f"{p}Range", name="bpm3_range_sp")
        self.range_rb = EpicsSignalRO(f"{p}Range_RBV", name="bpm3_range_rb")

        # --- coarse in-vacuum DCM motors: roll = m68, pitch = m67 -----------------------------
        self.motor = {
            "roll":  EpicsMotor("XF:12ID:m68", name="dcm_roll_m68"),
            "pitch": EpicsMotor("XF:12ID:m67", name="dcm_pitch_m67"),
        }

        #: Sign of d(OVAL)/d(motor) per axis.  **MEASURED on the live system @ 10 keV** (settled,
        #: via measure_gain): roll d(OVAL)/d(m68) ~ +6e5 OVAL/EGU (so +move -> +OVAL); pitch
        #: d(OVAL)/d(m67) ~ -5e5..-7e5 OVAL/EGU (so +move -> -OVAL).  Only the SIGN is used (the
        #: magnitude varies with energy/hysteresis and is re-measured every step); confirm with
        #: measure_gain() at a new energy before trusting the loop there.
        self.assumed_sign = {"roll": +1.0, "pitch": -1.0}

        self.connect()

    # ---------------------------------------------------------------- connection / reads
    def connect(self, timeout=5.0):
        """Connect all signals (short timeout; raises if the IOC is unreachable)."""
        sigs = (list(self.oval.values()) + list(self.cval.values()) + list(self.setp.values())
                + list(self.fb_disable.values()) + list(self.motor.values())
                + [self.sumX, self.sumY, self.posX, self.posY, self.range_sp, self.range_rb])
        for s in sigs:
            s.wait_for_connection(timeout=timeout)
        return self

    def range_index(self, energy_keV):
        """The BPM3 electrometer range **enum index** for ``energy_keV`` from
        :data:`DEFAULT_RANGE_TABLE` (or ``self.range_table``)."""
        return range_index(energy_keV, getattr(self, "range_table", None))

    def energy_keV(self):
        """Current photon energy in keV (0.0 if no energy source wired)."""
        if self._energy_source is None:
            return 0.0
        try:
            return float(self._energy_source.position) / 1000.0
        except Exception:
            try:
                return float(self._energy_source.position.energy) / 1000.0
            except Exception:
                return 0.0

    def flux(self):
        """Current BPM3 sum (use sumY -- the pitch/vertical sum -- as the flux proxy)."""
        return float(self.sumY.get())

    def flux_min(self):
        """The energy-dependent minimum acceptable BPM3 sum right now."""
        return flux_threshold(self.energy_keV(), self.flux_table)

    def flux_ok(self, verbose=True):
        """True if the current BPM3 flux is above the energy-dependent threshold."""
        f, fmin, e = self.flux(), self.flux_min(), self.energy_keV()
        ok = f > fmin
        if verbose:
            print(f"flux: sumY={f:.3f}  threshold(@{e:.2f}keV)={fmin:.3f}  -> {'OK' if ok else 'LOW'}")
        return ok

    def read(self):
        """Return a dict snapshot of everything (read-only)."""
        return {
            "energy_keV": self.energy_keV(),
            "sumX": float(self.sumX.get()), "sumY": float(self.sumY.get()),
            "posX": float(self.posX.get()), "posY": float(self.posY.get()),
            "oval_roll": float(self.oval["roll"].get()),
            "oval_pitch": float(self.oval["pitch"].get()),
            "cval_roll": float(self.cval["roll"].get()),
            "cval_pitch": float(self.cval["pitch"].get()),
            "m68_roll": float(self.motor["roll"].position),
            "m67_pitch": float(self.motor["pitch"].position),
            "fb_roll_off": str(self.fb_disable["roll"].get()),
            "fb_pitch_off": str(self.fb_disable["pitch"].get()),
        }

    def snapshot(self):
        """Print one compact read-only line."""
        r = self.read()
        print(
            "E={energy_keV:6.2f}keV | sumY={sumY:8.3f} (min {fmin:.1f}) | "
            "OVAL roll={oval_roll:+7.1f} pitch={oval_pitch:+7.1f} | "
            "CVAL roll={cval_roll:+7.3f} pitch={cval_pitch:+7.3f} | "
            "m68={m68_roll:.4f} m67={m67_pitch:.4f} | fb off r/p={fb_roll_off}/{fb_pitch_off}"
            .format(fmin=self.flux_min(), **r)
        )
        return r

    def monitor(self, seconds=20, interval=0.5):
        """Read-only: print a snapshot every ``interval`` s for ``seconds`` (Ctrl-C to stop)."""
        t_end = time.time() + seconds
        try:
            while time.time() < t_end:
                self.snapshot()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("monitor: stopped by user")

    # ---------------------------------------------------------------- feedback helpers (read/toggle)
    def feedback(self, action):
        """Turn the DCM pitch+roll feedback ``"on"``/``"off"`` (writes the enable bits)."""
        val = "1" if action == "off" else "0"
        if action not in ("on", "off"):
            raise ValueError("action must be 'on' or 'off'")
        self.fb_disable["roll"].put(val, wait=True)
        self.fb_disable["pitch"].put(val, wait=True)
        print(f"feedback {action} (roll+pitch)")

    def settled(self, axis="both", oval_window=200.0, seconds=2.0, interval=0.2):
        """Block (<= ``seconds`` after first stability) until the **OVAL** of ``axis`` stays within a
        peak-to-peak ``oval_window`` for the whole dwell; return True if it settled, else False.

        Read-only.  Gates on OVAL, not CVAL: on the live system the beam-position CVAL is very
        noisy (swings ±20000 sample-to-sample) while OVAL is steady, so OVAL stability is the
        meaningful "is the loop holding?" criterion.  (Use :meth:`settled_cval` for the raw
        position-error gate if you really want it.)
        """
        axes = ("roll", "pitch") if axis == "both" else (axis,)
        deadline = time.time() + 4 * max(seconds, interval)   # overall cap
        recent = {a: [] for a in axes}
        stable_since = None
        while time.time() < deadline:
            for a in axes:
                recent[a].append(float(self.oval[a].get()))
                recent[a][:] = recent[a][-int(max(seconds, interval) / interval) - 1:]
            ptp = max((max(v) - min(v)) for v in recent.values() if v)
            enough = all(len(v) >= max(2, seconds / interval) for v in recent.values())
            if enough and ptp <= oval_window:
                stable_since = stable_since or time.time()
                if time.time() - stable_since >= seconds:
                    return True
            else:
                stable_since = None
            time.sleep(interval)
        return False

    def settled_cval(self, axis="both", pos_window=10000.0, seconds=2.0, interval=0.2):
        """Like :meth:`settled` but on the raw beam-position error ``|CVAL - VAL|`` (very noisy on
        the live system -- prefer :meth:`settled`)."""
        axes = ("roll", "pitch") if axis == "both" else (axis,)
        deadline = time.time() + 4 * max(seconds, interval)
        stable_since = None
        while time.time() < deadline:
            err = max(abs(float(self.cval[a].get()) - float(self.setp[a].get())) for a in axes)
            if err <= pos_window:
                stable_since = stable_since or time.time()
                if time.time() - stable_since >= seconds:
                    return True
            else:
                stable_since = None
            time.sleep(interval)
        return False

    # ---------------------------------------------------------------- supervised re-centring
    def recenter_once(self, axis, step=0.0001, settle=1.5, require_correct_direction=True,
                      oval_abort=None, deadband=None, max_step=0.002, sample_interval=0.15):
        """Take **one** small coarse-motor step that should drive ``OVAL[axis]`` toward 0, then
        **wait ``settle`` s and judge on the settled value** (not the instantaneous read).  Returns
        a dict with ``before``/``after``/``delta_oval``/``motor_delta``/``gain``/``overshot``.

        Why we wait before judging
        --------------------------
        The fast loop reacts to the coarse-motor step with a brief **transient dip the wrong way**,
        then settles in the intended direction.  Judging on the *immediate* read would false-abort
        on that dip (observed on pitch: a +0.0001 step read +25 wrong-way at t~0 but recovers).  So
        after the step we poll OVAL for ``settle`` seconds and take ``after`` as the **settled**
        value (mean of the final third of samples).  Direction is then judged on that settled
        value: correct iff ``sign(after - before) == want`` (toward 0).  Overshoot through zero is
        still correct (it over-corrected).  Only a *settled* move the opposite of intended -- by
        more than ``deadband`` -- raises ``RuntimeError`` (genuine wrong sign).

        These motors have hysteresis / are not reproducible, so magnitude varies; we only rely on
        the *settled sign* and re-measure the gain every step.

        Safety:
        * ``step`` is a small RELATIVE move (default 0.0001 EGU) on m68 (roll) / m67 (pitch), clamped
          to ``max_step``; direction comes from :attr:`assumed_sign`.
        * ``oval_abort`` (default: the axis rail + margin): refuse to step only if ``|OVAL|`` reads
          *beyond* the hardware rail (a garbage/disconnected value).  Being AT the rail is allowed
          -- that is exactly when stepping toward 0 matters.
        """
        if axis not in ("roll", "pitch"):
            raise ValueError("axis must be 'roll' or 'pitch'")
        # Default abort threshold = the axis hardware rail + a margin.  At/near the rail we still
        # step (toward 0); only a reading clearly beyond the rail is treated as invalid.
        oval_abort = (self.rail(axis) + self.OVAL_RAIL_MARGIN) if oval_abort is None else oval_abort
        deadband = (10.0 if deadband is None else deadband)   # OVAL units of noise to ignore
        sig = self.oval[axis]
        mot = self.motor[axis]

        before = float(sig.get())
        if abs(before) > oval_abort:
            raise RuntimeError(
                f"{axis} OVAL {before:.1f} reads beyond the hardware rail "
                f"(+/-{self.rail(axis):.0f}); treating as invalid -- investigate (PV/connection?) "
                "before stepping.")

        want = -1.0 if before > 0 else 1.0       # desired sign of delta_oval (toward 0)
        motor_dir = want / self.assumed_sign[axis]
        motor_delta = motor_dir * min(abs(step), abs(max_step))

        print(f"{axis}: OVAL {before:+.1f} -> stepping {mot.name} by {motor_delta:+.5f} EGU "
              f"(want OVAL {'-' if want < 0 else '+'}); settling {settle:.1f}s ...")
        mot.move(mot.position + motor_delta, wait=True)

        # Poll OVAL over the settle window so a brief wrong-way transient doesn't trigger a verdict.
        samples = []
        t_end = time.time() + max(settle, sample_interval)
        while time.time() < t_end:
            samples.append(float(sig.get()))
            time.sleep(sample_interval)
        if not samples:
            samples = [float(sig.get())]
        # settled value = mean of the final third (denoise).
        tail = samples[max(1, 2 * len(samples) // 3):] or samples[-1:]
        after = sum(tail) / len(tail)

        delta_oval = after - before
        gain = (delta_oval / motor_delta) if motor_delta else float("nan")  # d(OVAL)/d(motor)
        correct = (abs(delta_oval) <= deadband) or (delta_oval * want > 0)  # settled intended sign
        overshot = abs(after) > deadband and (after * before < 0)           # crossed through 0

        tag = "toward 0" if (correct and not overshot) else (
            "overshot through 0" if overshot else "WRONG WAY (settled)")
        early = ""
        if samples and (samples[0] - before) * want < -deadband:
            early = f"  [early transient dip to {samples[0]:+.1f}, recovered]"
        print(f"{axis}: OVAL {before:+.1f} -> {after:+.1f} settled  (dOVAL={delta_oval:+.1f}, "
              f"gain~{gain:+.0f} OVAL/EGU, {tag}){early}")

        if require_correct_direction and not correct:
            raise RuntimeError(
                f"{axis}: settled OVAL moved the WRONG way ({before:+.1f} -> {after:+.1f}, "
                f"dOVAL={delta_oval:+.1f}) after a {motor_delta:+.5f} step on {mot.name} (waited "
                f"{settle:.1f}s) -- sign/coupling is NOT as assumed.  Aborting before this drives "
                "the piezo into the rail.  Re-check assumed_sign / wiring.")
        return {"before": before, "after": after, "delta_oval": delta_oval,
                "motor_delta": motor_delta, "gain": gain, "overshot": overshot,
                "samples": samples}

    def measure_gain(self, axis, step=0.0001, settle=1.5):
        """Read-then-one-small-step characterisation of ``d(OVAL)/d(motor)`` for ``axis``.

        Prints and returns the measured (settled) gain (OVAL units per motor EGU) and the implied
        sign.  Use this to confirm the polarity / rough magnitude on the live system before running
        the loop -- these motors have hysteresis, so treat the magnitude as approximate and
        per-step.  Settles ``settle`` s before reading so the brief wrong-way transient is excluded.
        """
        info = self.recenter_once(axis, step=step, settle=settle, require_correct_direction=False)
        sign = "+" if info["gain"] > 0 else "-"
        print(f"{axis}: measured gain ~ {info['gain']:+.0f} OVAL/EGU  (sign {sign}; "
              f"assumed_sign[{axis}]={self.assumed_sign[axis]:+.0f})")
        return info["gain"]

    def recenter(self, axis, target=400.0, step=0.0001, settle=1.5, rate=1.0, max_steps=200,
                 max_step=0.002, oval_abort=None, adapt=True):
        """Slow, guarded loop: step ``axis`` until ``|OVAL[axis]| < target``.  Each step settles
        ``settle`` s (>= the loop period) before judging direction / re-measuring gain, so a brief
        wrong-way transient never aborts.  Adapts the step from the measured gain to converge
        without overshooting far, clamped to ``max_step``.

        Stops on: ``|OVAL| < target`` reached, ``max_steps`` exhausted, a *settled* wrong-way step
        (``recenter_once`` raises), ``|OVAL|`` beyond ``oval_abort``, or Ctrl-C.  Supervised.
        """
        period = 1.0 / max(rate, 1e-6)
        per_step_settle = max(settle, period)     # always wait >= settle before judging
        cur_step = abs(step)
        print(f"recenter {axis}: driving |OVAL| < {target:.0f}  (start step {cur_step} EGU, "
              f"max {max_step} EGU, settle {per_step_settle:.1f}s/step, max {max_steps} steps).  "
              "Ctrl-C to stop.")
        try:
            for i in range(1, max_steps + 1):
                cur = abs(float(self.oval[axis].get()))
                if cur < target:
                    print(f"recenter {axis}: |OVAL|={cur:.1f} < {target:.0f}  DONE in {i-1} steps")
                    return True
                info = self.recenter_once(axis, step=cur_step, settle=per_step_settle,
                                          oval_abort=oval_abort, max_step=max_step)
                if adapt and info["gain"] and abs(info["gain"]) > 1e-9:
                    # size the next step to land ~halfway to 0 from the new OVAL (damped), so we
                    # close in without overshooting far; clamp to max_step.
                    want_dOVAL = -0.5 * info["after"]
                    nxt = abs(want_dOVAL / info["gain"])
                    cur_step = max(min(nxt, max_step), abs(step) * 0.25)
            print(f"recenter {axis}: hit max_steps={max_steps} without reaching target "
                  f"(|OVAL|={abs(float(self.oval[axis].get())):.1f})")
            return False
        except KeyboardInterrupt:
            print(f"recenter {axis}: stopped by user at |OVAL|="
                  f"{abs(float(self.oval[axis].get())):.1f}")
            return False

