from ophyd import (
    PVPositioner,
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    Device,
    Signal,
    PseudoPositioner,
    PseudoSingle,
)
from ophyd.utils.epics_pvs import set_and_wait
from ophyd.status import DeviceStatus
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from ophyd import Component as Cpt
import logging
import threading

from . import _context
from . import _config
from . import attenuator_data as _ad

import math as _math
_math_isfinite = _math.isfinite
#: largest attenuation factor reported (beyond this the beam is effectively fully absorbed
#: and the reading is non-physical for a measurement); keeps documents finite/serializable.
_ad_MAX_FACTOR = 1e300

logger = logging.getLogger("bluesky")


class Attenuator(Device):
    """
    A single attenuator foil that is **unreliable at the hardware level** -- the actuation
    command often has to be re-issued, and the position read-back confirms the new state only
    after a delay.

    The previous ``set`` handled this with a blocking ``while`` loop that re-issued the command
    and **swallowed all errors / always reported success**.  That blocked the RunEngine and --
    worse -- could leave the foil in the wrong position while telling the plan it succeeded.

    This version is **non-blocking and subscription-driven**, and keeps the essential retry
    behavior, but with safe failure semantics:

    * The returned ``Status`` finishes (success) only when ``status`` actually reads the target
      value -- so ``yield from bps.mv(att, 'Insert')`` does not proceed until the foil confirms.
      The confirmation may arrive any time after the command (a real device delay); the
      subscription handles that without blocking -- no ``sleep().wait()`` needed.
    * The command is re-actuated up to ``max_retries`` times if the hardware does not confirm.
      Each attempt uses a short ``cmd_timeout``; **a single attempt timing out is expected** (the
      first few often do) and is swallowed -- only the *repeated* failure is reported.
    * **If it still has not confirmed after the retries / ``timeout`` seconds, the Status is
      marked FAILED (raises).**  A hard stop is the safe outcome: better to halt a run than to
      keep going with an attenuator in the wrong (potentially unsafe) position.

    Attributes:
        open_cmd (EpicsSignal): Command to open (insert) the attenuator.
        close_cmd (EpicsSignal): Command to close (retract) the attenuator.
        status (EpicsSignalRO): The attenuator's position read-back.
        fail_to_close / fail_to_open (EpicsSignalRO): hardware fault flags.
    """
    open_cmd = Cpt(EpicsSignal, "Cmd:Opn-Cmd", string=True)
    open_val = "Open"

    close_cmd = Cpt(EpicsSignal, "Cmd:Cls-Cmd", string=True)
    close_val = "Not Open"

    status = Cpt(EpicsSignalRO, "Pos-Sts", string=True)
    fail_to_close = Cpt(EpicsSignalRO, "Sts:FailCls-Sts", string=True)
    fail_to_open = Cpt(EpicsSignalRO, "Sts:FailOpn-Sts", string=True)

    # User-facing commands
    open_str = "Insert"
    close_str = "Retract"

    #: how many times to re-issue the actuation command before failing
    max_retries = 8
    #: hard wall-clock cap (s) after which the set FAILS if not confirmed
    timeout = 30.0
    #: delay (s) between re-actuation attempts (waited for via a timer, NOT a blocking sleep)
    retry_delay = 0.5
    #: per-attempt command-put timeout (s); a single attempt timing out is EXPECTED (the first
    #: few often do) and is swallowed -- only repeated failure (max_retries / `timeout`) raises.
    cmd_timeout = 1.0
    #: the read-back must stay at the target for this long (s) before the foil is considered "in
    #: position".  This DEBOUNCES the hardware's bounce-back: a foil can momentarily read the
    #: target and then fall back, so a single transient reading must NOT latch success.
    settle_time = 2

    _OPEN_ALIASES = ("Open", "Insert", "open", "insert", "in", 1, "1")
    _CLOSE_ALIASES = ("Close", "Retract", "close", "retract", "out", 0, "0", "Not Open")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_st = None
        self.read_attrs = ["status"]

    def set(self, val):
        """Drive the foil to ``val`` ('Insert'/'Retract' etc.), retrying until confirmed.

        Returns a ``DeviceStatus`` that finishes when ``status`` reads the target value, or
        **fails** (after ``max_retries`` re-actuations / ``timeout`` seconds) if the foil never
        confirms -- a flaky foil that cannot reach position raises rather than silently
        proceeding in the wrong state.  Non-blocking.
        """
        if self._set_st is not None:
            raise RuntimeError(
                "{}: trying to set while a set is in progress".format(self.name))

        if val in self._OPEN_ALIASES:
            cmd_sig, target = self.open_cmd, self.open_val
        elif val in self._CLOSE_ALIASES:
            cmd_sig, target = self.close_cmd, self.close_val
        else:
            raise ValueError(
                "{}: unknown attenuator state {!r} (use 'Insert'/'Retract')".format(
                    self.name, val))

        st = self._set_st = DeviceStatus(self)
        state = {"attempts": 0, "done": False, "timer": None, "watchdog": None,
                 "settle": None}

        def _cancel_settle():
            t = state.get("settle")
            if t is not None:
                try:
                    t.cancel()
                except Exception:
                    pass
            state["settle"] = None

        def _cleanup():
            state["done"] = True
            _cancel_settle()
            for key in ("timer", "watchdog"):
                t = state.get(key)
                if t is not None:
                    try:
                        t.cancel()
                    except Exception:
                        pass
            try:
                self.status.clear_sub(_status_cb)
            except Exception:
                pass
            self._set_st = None

        def _succeed():
            if state["done"]:
                return
            _cleanup()
            st.set_finished()

        def _fail():
            if state["done"]:
                return
            cur = self._safe_status()
            _cleanup()
            logger.error(
                "%s: failed to reach '%s' after %d attempts / %.0fs (status=%r); "
                "FAILING the set so the run halts rather than continue with the foil in the "
                "wrong position.", self.name, val, state["attempts"], self.timeout, cur)
            st.set_exception(
                TimeoutError("{}: attenuator did not reach {!r} (last status={!r})".format(
                    self.name, target, cur)))

        def _settle_confirm():
            # Fired settle_time after the status reached target; succeed only if it is STILL at
            # target (it did not bounce back).
            if state["done"]:
                return
            if str(self._safe_status()) == target:
                _succeed()
            else:
                _cancel_settle()   # bounced away; the retry loop will re-actuate

        def _status_cb(value, **kwargs):
            # status changed.  If it is at target, ARM the settle timer (don't succeed yet -- it
            # may bounce back).  If it moved away from target, cancel any pending settle.
            if state["done"]:
                return
            if str(value) == target:
                if state["settle"] is None:
                    t = threading.Timer(self.settle_time, _settle_confirm)
                    t.daemon = True
                    state["settle"] = t
                    t.start()
            else:
                _cancel_settle()

        def _retry():
            # Runs on a timer thread; re-actuate, then schedule the next check until confirmed
            # (settled), retries exhausted, or the watchdog fails us.  No blocking of the RE loop.
            if state["done"]:
                return
            # If we're currently at target, let the settle timer confirm it -- do NOT re-actuate
            # (and do not succeed here, since a momentary reading may bounce back).
            if str(self._safe_status()) == target:
                if state["settle"] is None:
                    t = threading.Timer(self.settle_time, _settle_confirm)
                    t.daemon = True
                    state["settle"] = t
                    t.start()
                # keep a (slow) heartbeat so we re-check if the settle timer was cancelled
                if not state["done"]:
                    hb = threading.Timer(self.settle_time + self.retry_delay, _retry)
                    hb.daemon = True
                    state["timer"] = hb
                    hb.start()
                return
            if state["attempts"] >= self.max_retries:
                _fail()
                return
            state["attempts"] += 1
            # Issue one actuation with a SHORT, bounded timeout.  A single attempt timing out is
            # EXPECTED for this flaky hardware (the first few often do) -- swallow it here; only
            # the repeated failure (max_retries / watchdog `timeout`) is reported upward via the
            # returned Status.  The bounded .wait() runs on this timer thread, never the RE loop.
            try:
                cmd_sig.set(1, timeout=self.cmd_timeout).wait()
            except Exception as exc:
                logger.debug("%s: actuation attempt %d to '%s' did not confirm in %.1fs (%r); "
                             "will retry", self.name, state["attempts"], val,
                             self.cmd_timeout, exc)
            if state["attempts"] > 1:
                logger.info("** %s: re-actuating to '%s' (attempt %d)",
                            self.name, val, state["attempts"])
            if not state["done"]:
                t = threading.Timer(self.retry_delay, _retry)
                t.daemon = True
                state["timer"] = t
                t.start()

        # Hard wall-clock cap: fail if not confirmed in time (covers a foil that accepts the
        # command but whose read-back is stuck).  Ensure the cap is comfortably larger than the
        # settle window, otherwise the watchdog could fire before a (settling) success can
        # confirm and EVERY move would spuriously fail.
        effective_timeout = max(self.timeout, self.settle_time + 2.0 * self.retry_delay + 1.0)
        watchdog = threading.Timer(effective_timeout, _fail)
        watchdog.daemon = True
        state["watchdog"] = watchdog
        watchdog.start()

        # If already at target, finish immediately; else subscribe + start the retry loop.
        self.status.subscribe(_status_cb, run=True)
        if not state["done"]:
            _retry()
        return st

    def _safe_status(self):
        try:
            return self.status.get()
        except Exception:
            return None


class Attenuators(Device):
    """An aggregate over a bank of :class:`Attenuator` foils that moves them **as one unit**.

    Why this exists
    ---------------
    Moving several foils with one ``bps.mv(att2_5, 'Insert', att2_6, 'Insert', ...)`` was
    observed to misbehave on the real hardware: the foils all actuate, but one or more *bounce
    back* out of position while the overall move still reports success.  Driving them through a
    single device fixes this because:

    * the per-foil :class:`Attenuator` now requires the read-back to be **stable** (settled) for
      ``Attenuator.settle_time`` before it counts as in-position, so a transient correct reading
      that bounces back no longer latches success; and
    * this aggregate's ``set`` does not finish until **every** foil's settled-confirmation has
      completed (and re-actuates any that fall back), so the combined move is only "done" when
      the whole requested combination is genuinely in place.

    Usage
    -----
    ``set`` takes the foils that should be **inserted**; every other foil in the bank is
    **retracted**.  Accepts foil child-attribute names or the foil objects themselves::

        yield from bps.mv(attenuators, ['f5', 'f6'])         # insert f5,f6; retract the rest
        yield from bps.mv(attenuators, [attenuators.f5])     # by object
        yield from bps.mv(attenuators, [])                   # retract all (no attenuation)

    The returned Status finishes only when all 12 foils confirm; if any foil cannot reach
    position it FAILS (the foil's own safe-fail), halting the run rather than running with the
    wrong attenuation.
    """

    def set(self, inserted):
        """Insert the foils in ``inserted`` and retract all others; finish when all confirm.

        Parameters
        ----------
        inserted : iterable
            Foil child-attribute names (e.g. ``'f5'``) and/or foil objects that should end up
            INSERTED.  Everything else in the bank is RETRACTED.
        """
        want_in = self._resolve_foils(inserted)

        statuses = []
        for name in self.component_names:
            foil = getattr(self, name)
            if not isinstance(foil, Attenuator):
                continue
            target = "Insert" if foil in want_in else "Retract"
            statuses.append(foil.set(target))

        if not statuses:
            # nothing to do -> an already-finished status
            st = DeviceStatus(self)
            st.set_finished()
            return st

        # Combine: the aggregate is done only when EVERY foil's (settled) status is done; it
        # fails if any foil fails.
        combined = statuses[0]
        for s in statuses[1:]:
            combined = combined & s
        return combined

    def _resolve_foils(self, inserted):
        """Return the set of foil objects requested to be inserted (from names or objects)."""
        foils_by_name = {name: getattr(self, name) for name in self.component_names
                         if isinstance(getattr(self, name), Attenuator)}
        by_obj = set(foils_by_name.values())
        want = set()
        for item in (inserted or []):
            if isinstance(item, Attenuator):
                if item not in by_obj:
                    raise ValueError(
                        "{}: {!r} is not a foil of this bank".format(self.name, item))
                want.add(item)
            elif item in foils_by_name:
                want.add(foils_by_name[item])
            else:
                raise ValueError(
                    "{}: unknown foil {!r}; expected one of {}".format(
                        self.name, item, sorted(foils_by_name)))
        return want

    def inserted_foils(self):
        """Return the child-attribute names of the foils currently reading 'Open'."""
        out = []
        for name in self.component_names:
            foil = getattr(self, name)
            if isinstance(foil, Attenuator) and foil._safe_status() == foil.open_val:
                out.append(name)
        return out


def make_attenuator_bank(class_name, prefix_fmt, foil_indices):
    """Build an :class:`Attenuators` subclass with foils ``f<i>`` for ``i`` in ``foil_indices``.

    ``prefix_fmt`` is a format string taking the foil index, e.g.
    ``"XF:12IDC-OP:2{{Fltr:2-{}}}"``.  Returns the new class (instantiate with ``name=...``).
    """
    body = {"f{}".format(i): Cpt(Attenuator, prefix_fmt.format(i), add_prefix=("suffix",))
            for i in foil_indices}
    return type(class_name, (Attenuators,), body)


class AttenuatorSet(Device):
    """Energy-aware attenuation factor for the whole 24-foil filter set.

    This is the user-/plan-facing handle on attenuation.  It does three things:

    1. **Reports** an approximate attenuation factor (and the equivalent transmission)
       for whatever foils are currently inserted, evaluated at the **current beamline
       energy** -- using the CXRO transmission curves embedded in
       :mod:`smi_beamline.devices.attenuator_data`.  It also reports a plain-text
       ``description`` naming every inserted foil (e.g. ``att1_3``), its material and
       thickness.  These are recorded as ``configuration``-/``hinted``-kind signals, so
       the factor lands in **baseline** (start & end of every scan) and -- because this
       is a readable ``Device`` -- can also be added to the detector list to be read at
       **every point** when energy or attenuation changes during a scan.

    2. **Sets** a requested attenuation factor: ``yield from bps.mv(attenuation, 100)``
       picks the foil combination whose factor is closest to 100 at the current (or a
       planned) energy, using as **few foils as possible** (more foils are harder to
       normalize and scatter more), inserts them via the settled, all-or-nothing bank
       moves, and records the **actual achieved** factor (never the request).  If it
       cannot get within tolerance with ``max_foils`` foils it still applies the best
       combination, logs a warning, and the recorded factor reflects what was applied.

    3. Lets a plan **pre-compute** for a *planned* energy (before moving the mono) via
       :meth:`set_for_energy`, so attenuation can be staged for the energy a scan is
       about to use.

    Because attenuation depends on energy, the reported factor is only meaningful
    alongside the energy at which it was computed; the energy used is recorded in
    ``energy_eV`` so the baseline/primary reading is self-describing.

    Parameters
    ----------
    banks : sequence of :class:`Attenuators`
        The aggregate foil banks (``attenuators1``, ``attenuators2``).  Used both to read
        the currently-inserted foils and to drive new combinations.
    bank_prefixes : sequence of str, optional
        The bank label of each entry in ``banks`` ("1", "2"), used to translate between
        global foil labels ("2_5") and a bank's child foils ("f5").  Defaults to
        ("1", "2", ...).
    """

    # --- reported (computed) values -------------------------------------------
    #: attenuation factor 1/T (>= 1) at ``energy_eV`` for the inserted foils.  hinted so
    #: it shows up in the live table / baseline.
    attenuation_factor = Cpt(Signal, value=1.0, kind="hinted")
    #: transmission 0-1 (== 1 / attenuation_factor).
    transmission = Cpt(Signal, value=1.0, kind="normal")
    #: photon energy (eV) at which the factor/transmission were computed.
    energy_eV = Cpt(Signal, value=0.0, kind="normal")
    #: comma-separated text naming each inserted foil + material + thickness.
    description = Cpt(Signal, value="none", kind="normal")
    #: list of inserted foil labels (e.g. ['1_3', '2_5']).
    inserted = Cpt(Signal, value=[], kind="normal")
    #: the most recently *requested* factor (0 -> never set via this device).
    requested_factor = Cpt(Signal, value=0.0, kind="config")
    #: True if the achieved factor was within ``tolerance`` of the last request.
    within_tolerance = Cpt(Signal, value=True, kind="config")

    # --- selection policy (config; recorded with every run) -------------------
    #: hard cap on how many foils a requested factor may use (fewer = less scatter).
    max_foils = Cpt(Signal, value=_config.load("attenuator_max_foils"), kind="config")
    #: relative tolerance on the requested factor before a warning is emitted.
    tolerance = Cpt(Signal, value=_config.load("attenuator_tolerance"), kind="config")
    #: "closest" (match either side) or "atleast" (never less attenuation than asked).
    select_mode = Cpt(Signal, value=_config.load("attenuator_select_mode"), kind="config")

    #: the ``RE.md`` key under which the current attenuation state is mirrored, so it lands
    #: in the **start document** of the next run (bluesky snapshots ``RE.md`` at open_run).
    #: This complements the baseline registration (which records the device's signals at
    #: start & end of every run); the start-doc copy is refreshed whenever attenuation is
    #: set/changed/read so a run started after a change carries the up-to-date value.
    md_key = "beamline_attenuators"

    def __init__(self, *args, banks, bank_prefixes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._banks = list(banks)
        if bank_prefixes is None:
            bank_prefixes = [str(i + 1) for i in range(len(self._banks))]
        self._bank_prefixes = list(bank_prefixes)
        if len(self._bank_prefixes) != len(self._banks):
            raise ValueError("banks and bank_prefixes must be the same length")
        # map global foil label ("2_5") -> (bank object, child attr "f5")
        self._label_to_bank = {}
        for bank, pfx in zip(self._banks, self._bank_prefixes):
            for name in bank.component_names:
                child = getattr(bank, name)
                if isinstance(child, Attenuator) and name.startswith("f"):
                    self._label_to_bank["{}_{}".format(pfx, name[1:])] = (bank, name)
        self.read_attrs = ["attenuation_factor", "transmission", "energy_eV",
                           "description", "inserted"]

    # ----------------------------------------------------------------- helpers
    def _current_energy(self, energy_eV=None):
        """Resolve the energy (eV) to evaluate at: explicit arg, else live beamline."""
        if energy_eV is not None:
            return float(energy_eV)
        e = _context.current_energy_eV()
        if e is None:
            # off-beamline / energy source unavailable: fall back to last value, else mid-range
            e = self.energy_eV.get() or (
                0.5 * (_ad.ENERGY_MIN_EV + _ad.ENERGY_MAX_EV))
        return float(e)

    def _read_inserted_labels(self):
        """Return the sorted global labels of foils currently reading 'Open'."""
        labels = []
        for bank, pfx in zip(self._banks, self._bank_prefixes):
            for name in bank.inserted_foils():        # child attrs like 'f5'
                labels.append("{}_{}".format(pfx, name[1:]))
        return tuple(sorted(labels, key=_ad._foil_sort_key))

    def compute(self, labels=None, energy_eV=None):
        """Compute (and store) factor/transmission/description for ``labels`` at energy.

        With ``labels=None`` the *currently inserted* foils are used.  Returns a dict of
        the computed values; also writes them into the component Signals so a subsequent
        ``read()`` / baseline reflects them.
        """
        energy = self._current_energy(energy_eV)
        if labels is None:
            labels = self._read_inserted_labels()
        labels = tuple(sorted(labels, key=_ad._foil_sort_key))

        factor = _ad.attenuation_factor(labels, energy)
        trans = _ad.transmission(labels, energy)
        desc = self._describe(labels)

        # Guard against non-finite values reaching the document stream when the beam is
        # essentially fully absorbed (transmission underflows): report a large-but-finite
        # factor instead of inf.  Such a reading is non-physical for a real measurement
        # anyway; the description still names the (very thick) foils responsible.
        if not _math_isfinite(factor):
            factor = _ad_MAX_FACTOR
        if trans <= 0.0:
            trans = 1.0 / _ad_MAX_FACTOR

        self.energy_eV.put(energy)
        self.attenuation_factor.put(factor)
        self.transmission.put(trans)
        self.description.put(desc)
        self.inserted.put(list(labels))

        state = {"attenuation_factor": factor, "transmission": trans,
                 "energy_eV": energy, "description": desc, "inserted": list(labels)}
        # Mirror into RE.md so a run started after this change carries the up-to-date value
        # in its START document (bluesky snapshots RE.md at open_run).  Never let a metadata
        # write break a compute() that runs mid-scan.
        try:
            self._update_run_md(state, labels)
        except Exception:
            logger.exception("%s: failed to mirror attenuation state into RE.md", self.name)
        return state

    def state_md(self, labels=None, energy_eV=None):
        """Return the attenuation-state dict that gets written to ``RE.md[md_key]``.

        Same shape used in the start document: per-foil ``{att1_3: {material, thickness}}``
        plus the overall ``attenuation_factor`` / ``transmission`` / ``energy_eV`` /
        ``description``.  Computes from the live foils/energy if ``labels`` is None.
        """
        info = self.compute(labels=labels, energy_eV=energy_eV)
        return self._build_md(info, tuple(info["inserted"]))

    @staticmethod
    def _build_md(state, labels):
        """Build the RE.md attenuation dict (per-foil materials + overall factor) from a
        computed ``state`` dict and the inserted ``labels``."""
        foils = {}
        for label in labels:
            base, mult = _ad.FOIL_LAYOUT[label]
            base_info = _ad.BASE_FOILS[base]
            foils["att{}".format(label)] = {
                "material": "{}_{:g}um".format(base_info["formula"], base_info["thickness_um"]),
                "thickness": "{}x".format(mult),
            }
        return {
            "foils": foils,
            "attenuation_factor": state.get("attenuation_factor"),
            "transmission": state.get("transmission"),
            "energy_eV": state.get("energy_eV"),
            "description": state.get("description"),
        }

    def _update_run_md(self, state, labels):
        """Write the current attenuation state into ``RE.md[md_key]`` (via the context seam).

        No-op off the beamline (``get_md()`` returns a throwaway dict).  Assigns the WHOLE
        key (not a nested mutation) so a Redis-backed ``RE.md`` persists the change.
        """
        md = _context.get_md()
        if md is None:
            return
        md[self.md_key] = self._build_md(state, labels)

    @staticmethod
    def _describe(labels):
        """Plain-text description naming each inserted foil, material and thickness."""
        if not labels:
            return "none (no attenuation)"
        return "; ".join(_ad.foil_description(l) for l in labels)

    def describe_factor(self, target_factor, energy_eV=None):
        """Preview (without moving anything) the foils that would be selected.

        Returns ``(labels, achieved_factor, within_tol, energy_eV)``.  Useful from a plan
        to decide on attenuation before committing the move.
        """
        energy = self._current_energy(energy_eV)
        labels, factor, ok = _ad.select_foils(
            float(target_factor), energy,
            candidates=list(self._label_to_bank.keys()),
            max_foils=int(self.max_foils.get()),
            tolerance=float(self.tolerance.get()),
            mode=str(self.select_mode.get()),
        )
        return labels, factor, ok, energy

    # --------------------------------------------------------------- readable
    def trigger(self):
        """Recompute from the live foil states + energy (so per-point reads are fresh)."""
        self.compute()
        st = DeviceStatus(self)
        st.set_finished()
        return st

    def read(self):
        # make sure the computed values reflect the present state at read time
        self.compute()
        return super().read()

    # ------------------------------------------------------------------- set
    def set(self, target_factor, energy_eV=None):
        """Insert the foil combination giving ~``target_factor`` and record what was applied.

        ``target_factor`` is the desired attenuation factor (1/T).  ``<= 1`` retracts all
        foils (no attenuation).  Optionally evaluate at a *planned* ``energy_eV`` instead
        of the current energy (useful to pre-stage attenuation for an energy a scan is
        about to move to).  Returns a Status that finishes when all foils confirm (it
        inherits the banks' settled, all-or-nothing, safe-fail behavior).
        """
        target_factor = float(target_factor)
        energy = self._current_energy(energy_eV)
        self.requested_factor.put(target_factor)

        labels, predicted, ok = _ad.select_foils(
            target_factor, energy,
            candidates=list(self._label_to_bank.keys()),
            max_foils=int(self.max_foils.get()),
            tolerance=float(self.tolerance.get()),
            mode=str(self.select_mode.get()),
        )
        self.within_tolerance.put(bool(ok))

        if not ok:
            logger.warning(
                "%s: requested attenuation factor %.4g at %.0f eV could not be matched "
                "within %.0f%% using <=%d foils; applying closest = %.4g (%+.1f%%) with "
                "foils %s.  The recorded factor reflects what was applied.",
                self.name, target_factor, energy, 100 * float(self.tolerance.get()),
                int(self.max_foils.get()), predicted,
                (predicted / target_factor - 1.0) * 100.0 if target_factor else float("nan"),
                ["att" + l for l in labels])
        else:
            logger.info(
                "%s: attenuation factor %.4g at %.0f eV -> %d foil(s) %s (achieved ~%.4g, "
                "%+.1f%%).", self.name, target_factor, energy, len(labels),
                ["att" + l for l in labels], predicted,
                (predicted / target_factor - 1.0) * 100.0 if target_factor else 0.0)

        # Drive each bank to exactly the requested subset (insert chosen, retract rest).
        statuses = []
        for bank, pfx in zip(self._banks, self._bank_prefixes):
            want = ["f{}".format(l.split("_", 1)[1])
                    for l in labels if l.split("_", 1)[0] == pfx]
            statuses.append(bank.set(want))

        combined = statuses[0]
        for s in statuses[1:]:
            combined = combined & s

        # Return a wrapper Status that finishes only AFTER the reported values have been
        # refreshed from the (now actual) foil state -- so a caller that waits on the move
        # is guaranteed to see the updated factor/description (no callback-vs-wait race).
        wrapper = DeviceStatus(self)

        def _on_done(*a, **k):
            try:
                self.compute(labels=labels, energy_eV=energy)
            except Exception:
                logger.exception("%s: failed to refresh reported factor after move",
                                 self.name)
            exc = None
            try:
                exc = combined.exception()
            except Exception:
                pass
            if exc is not None:
                wrapper.set_exception(exc)
            else:
                wrapper.set_finished()

        combined.add_callback(_on_done)
        return wrapper

    def set_for_energy(self, target_factor, energy_eV):
        """Convenience: :meth:`set` evaluated for a specific *planned* energy (eV)."""
        return self.set(target_factor, energy_eV=energy_eV)


# Uncomment and complete the following class if needed
# class Attenuation(PseudoPositioner):
#     """
#     PseudoPositioner for controlling multiple attenuators.
#     """
#     # Synthetic axis
#     attenuation = Cpt(PseudoSingle, kind="hinted")

#     # Real axes
#     att1_1 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:1-1}")
#     att1_2 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:1-2}")
#     ...
#     att2_12 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:2-12}")

#     @real_position_argument
#     def inverse(self, r_pos):
#         """
#         Convert real positions to pseudo positions.
#         """
#         return self.PseudoPosition(attenuation=...)

#     @pseudo_position_argument
#     def forward(self, p_pos):
#         """
#         Convert pseudo positions to real positions.
#         """
#         return self.RealPosition(
#             att1_1=att1_1_calc,
#             att1_2=att1_2_calc,
#             ...
#             att2_12=att2_12_calc,
#         )