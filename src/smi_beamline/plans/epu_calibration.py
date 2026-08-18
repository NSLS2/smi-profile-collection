"""
Human-run EPU lookup-table calibration plan.

This plan deliberately writes only a dated candidate table to ``mdsave``.  It never
modifies the production energy/IVU lookup-table configuration.
"""

from datetime import datetime
import math

import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from ophyd import Signal

from smi_beamline.devices import _context
from smi_beamline.plans.energy_walk import recenter_axis_plan, settle_oval_plan


__all__ = ["calibrate_epu_lookup", "EPUCalibrationLivePlot"]


GAP_MIN_UM = 6200.0
GAP_MAX_UM = 15100.0


def _namespace():
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None:
            return ip.user_ns
    except Exception:
        pass
    return {}


def _resolve(name, value):
    if value is not None:
        return value
    ns = _namespace()
    if name in ns:
        return ns[name]
    raise ValueError("{} was not supplied and is not present in the IPython namespace".format(name))


def _energy_grid(start_energy, stop_energy, energy_step):
    start = float(start_energy)
    stop = float(stop_energy)
    step = abs(float(energy_step))
    if step <= 0:
        raise ValueError("energy_step must be positive")
    direction = -1.0 if stop < start else 1.0
    values = []
    cur = start
    for _ in range(100000):
        values.append(cur)
        if (direction < 0 and cur <= stop) or (direction > 0 and cur >= stop):
            break
        cur = cur + direction * step
        if direction < 0:
            cur = max(cur, stop)
        else:
            cur = min(cur, stop)
    return values


def _gap_grid(center, *, half_width, step, gap_min, gap_max):
    step = abs(float(step))
    if step <= 0:
        raise ValueError("gap_step must be positive")
    start = max(float(gap_min), float(center) - float(half_width))
    stop = min(float(gap_max), float(center) + float(half_width))
    if stop < start:
        # The requested center is too far outside the usable range.  Still take one
        # boundary point so the operator gets an explicit measured result.
        return [float(gap_min if center < gap_min else gap_max)]
    n = int(math.floor((stop - start) / step + 1e-9))
    points = [start + i * step for i in range(n + 1)]
    if not points or abs(points[-1] - stop) > step * 0.25:
        points.append(stop)
    return points


def _dcm_gap_for_energy(energy_obj, energy_eV):
    target_bragg = energy_obj.energy_to_bragg(float(energy_eV))
    dcm_offset = 25.0
    target_dcm_gap = (dcm_offset / 2.0) / math.cos(math.radians(target_bragg))
    return target_bragg, target_dcm_gap


def _pilatus_threshold_settings(en_ev, thresh_ev=None, gain=1):
    """Same threshold/gain table used by ``set_energy_cam`` / ``set_energy``."""
    en = float(en_ev) / 1000.0
    thresh = float(thresh_ev) / 1000.0 if thresh_ev is not None else None
    gain = int(gain)

    if not thresh:
        if en < 2:
            en = 16.1
            gain = 1
        elif en < 4:
            gain = 3
        elif en < 7:
            gain = 2
        elif en < 20:
            gain = 1
        else:
            gain = 0

        if en < 2.6:
            thresh = 1.6
        elif en < 3.5:
            thresh = 1.7
        elif en < 4:
            thresh = 1.8
        elif en < 5:
            thresh = 2.0
        else:
            thresh = en / 2.0
    return en, thresh, gain


def _detector_signal(detector, detector_attr, cam_attr):
    if hasattr(detector, detector_attr):
        return getattr(detector, detector_attr)
    cam = getattr(detector, "cam", None)
    if cam is not None and hasattr(cam, cam_attr):
        return getattr(cam, cam_attr)
    raise AttributeError("{} has neither .{} nor .cam.{}".format(
        getattr(detector, "name", detector), detector_attr, cam_attr))


def _set_pilatus_energy(detector, en_ev, *, thresh_ev=None, gain=1,
                        timeout=10.0, poll=0.25, settle=0.5):
    en, thresh, gain = _pilatus_threshold_settings(en_ev, thresh_ev=thresh_ev, gain=gain)

    cam_energy = _detector_signal(detector, "cam_energy", "cam_energy")
    threshold = _detector_signal(detector, "threshold", "threshold_energy")
    gain_signal = _detector_signal(detector, "gain", "gain_menu")
    apply_signal = _detector_signal(detector, "apply", "threshold_apply")

    print("EPU calibration: setting {} sensitivity to {:.3f} keV "
          "(threshold {:.3f} keV, gain {}).".format(detector.name, en, thresh, gain))
    yield from bps.mv(cam_energy, en, threshold, thresh, gain_signal, gain, apply_signal, 1)

    cam = getattr(detector, "cam", None)
    if cam is not None and hasattr(cam, "energyset"):
        yield from bps.abs_set(cam.energyset, en, wait=True)

    energy_read = getattr(detector, "energy_read", None)
    threshold_read = getattr(detector, "threshold_read", None)
    gain_read = getattr(detector, "gain_read", None)
    skipped_readbacks = set()

    def _read_or_skip(signal):
        try:
            return (yield from bps.rd(signal))
        except Exception as exc:
            name = getattr(signal, "name", str(signal))
            if name not in skipped_readbacks:
                print("EPU calibration: warning - skipping disconnected {} "
                      "readback ({}: {}).".format(name, type(exc).__name__, exc))
                skipped_readbacks.add(name)
            return None

    elapsed = 0.0
    while elapsed < float(timeout):
        ok = True
        if energy_read is not None:
            value = yield from _read_or_skip(energy_read)
            ok = ok and (value is None or abs(float(value) - en) <= 0.05)
        if threshold_read is not None:
            value = yield from _read_or_skip(threshold_read)
            ok = ok and (value is None or abs(float(value) - thresh) <= 0.05)
        if gain_read is not None:
            value = yield from _read_or_skip(gain_read)
            ok = ok and (value is None or int(float(value)) == int(gain))
        if ok:
            break
        yield from bps.sleep(poll)
        elapsed += poll
    else:
        print("EPU calibration: warning - {} sensitivity readbacks did not confirm "
              "within {:.1f} s; continuing after requested write.".format(detector.name, timeout))
    yield from bps.sleep(settle)
    return {"energy_keV": en, "threshold_keV": thresh, "gain": gain}


def _feedback_off(diag):
    yield from bps.mv(diag.fb_disable["roll"], "1", diag.fb_disable["pitch"], "1")


def _feedback_on(diag):
    yield from bps.mv(diag.fb_disable["roll"], "0", diag.fb_disable["pitch"], "0")


def _center_with_feedback(diag, *, oval_settle_s, oval_settle_window,
                          recenter_target, recenter_step, recenter_rate,
                          recenter_settle, verbose):
    yield from _feedback_on(diag)
    yield from settle_oval_plan(
        diag, axis="both", oval_window=oval_settle_window, seconds=oval_settle_s,
        timeout=max(oval_settle_s * 3.0, 6.0))
    for axis in ("roll", "pitch"):
        win = diag.recenter_window(axis) if hasattr(diag, "recenter_window") else oval_settle_window
        target = recenter_target
        oval = float((yield from bps.rd(diag.oval[axis])))
        if abs(oval) > win:
            print("EPU calibration: {} OVAL {:+.0f} outside {:.0f}; centering to <{:.0f}.".
                  format(axis, oval, win, target))
            yield from recenter_axis_plan(
                diag, axis, target=target, step=recenter_step, rate=recenter_rate,
                settle=recenter_settle, verbose=verbose, flux_floor=None)


def _direct_dcm_move(energy_obj, target_eV):
    bragg, dcm_gap = _dcm_gap_for_energy(energy_obj, target_eV)
    yield from bps.mv(energy_obj.bragg, bragg, energy_obj.dcmgap, dcm_gap)
    return bragg, dcm_gap


def _scan_gap_stream(stream_name, *, energy_obj, detector, intensity_signal,
                     read_devices, gaps, gap_settle, target_eV, harmonic):
    points = []
    intensity_key = getattr(intensity_signal, "name", "")
    gap_key = getattr(energy_obj.ivugap, "name", "")
    for i, gap in enumerate(gaps, 1):
        print("EPU calibration: E={:.1f} eV h{} gap {:.1f} um ({}/{})".format(
            target_eV, int(harmonic), gap, i, len(gaps)))
        yield from bps.mv(energy_obj.ivugap, gap)
        if gap_settle:
            yield from bps.sleep(gap_settle)
        readings = yield from bps.trigger_and_read(read_devices, name=stream_name)
        try:
            intensity = float(readings[intensity_key]["value"])
        except Exception:
            intensity = float((yield from bps.rd(intensity_signal)))
        try:
            actual_gap = float(readings[gap_key]["value"])
        except Exception:
            actual_gap = float((yield from bps.rd(energy_obj.ivugap.user_readback)))
        points.append({"gap_um": actual_gap, "intensity": intensity})
    if not points:
        raise RuntimeError("No gap points were measured for stream {}".format(stream_name))
    best = max(points, key=lambda p: p["intensity"])
    return points, best


def _unique_candidate_key(store, prefix="epu_lookup_candidate"):
    stamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    base = "{}_{}".format(prefix, stamp)
    key = base
    i = 1
    while key in store:
        key = "{}_{:02d}".format(base, i)
        i += 1
    return key


def _write_candidate_table(store, table):
    key = _unique_candidate_key(store)
    store[key] = table
    index_key = "epu_lookup_candidate_index"
    index = list(store.get(index_key, []))
    index.append(key)
    store[index_key] = index
    return key


def calibrate_epu_lookup(start_energy, stop_energy, energy_step, *,
                         start_harmonic=None, energy=None, pil2M=None,
                         attenuation=None, intensity_signal=None, diag=None,
                         store=None, attenuation_factor=1e7,
                         gap_half_width=200.0, gap_step=5.0,
                         gap_min=GAP_MIN_UM, gap_max=GAP_MAX_UM,
                         gap_settle=0.25, pilatus_confirm_timeout=10.0,
                         pilatus_settle=0.5, thresh_ev=None, pilatus_gain=1,
                         auto_harmonic=21,
                         oval_settle_s=3.0, oval_settle_window=300.0,
                         recenter_target=400.0, recenter_step=0.0001,
                         recenter_rate=1.0, recenter_settle=1.5,
                         verbose_centering=True, md=None):
    """Calibrate candidate EPU gap peaks from high to low energy.

    The first energy move uses the normal managed ``energy`` move with feedback on.
    Every later energy step moves the real DCM axes directly with feedback off, so
    the current lookup table cannot change the harmonic or IVU gap behind the
    calibration plan's back.
    """
    energy = _resolve("energy", energy)
    detector = _resolve("pil2M", pil2M)
    attenuation = _resolve("attenuation", attenuation)
    if intensity_signal is None:
        intensity_signal = detector.stats1.total
    if store is None:
        store = _context.get_config()
    if diag is None:
        from smi_beamline.plans.dcm_diag import DCMDiag
        diag = DCMDiag(energy_source=energy)

    energies = _energy_grid(start_energy, stop_energy, energy_step)
    read_devices = [detector, energy.ivugap, attenuation]
    if intensity_signal not in read_devices:
        read_devices.append(intensity_signal)
    rows = []
    run_uids = []
    active = {"harmonic": start_harmonic}
    candidate_key = {"key": None}
    decision_energy = Signal(name="epu_calibration_energy_eV", value=0.0)
    decision_harmonic = Signal(name="epu_calibration_harmonic", value=0)
    decision_gap = Signal(name="epu_calibration_gap_um", value=0.0)
    decision_intensity = Signal(name="epu_calibration_intensity", value=0.0)

    plan_md = {
        "plan_name": "calibrate_epu_lookup",
        "calibration_type": "epu_lookup_candidate",
        "start_energy_eV": float(start_energy),
        "stop_energy_eV": float(stop_energy),
        "energy_step_eV": float(energy_step),
        "attenuation_factor_requested": float(attenuation_factor),
        "gap_half_width_um": float(gap_half_width),
        "gap_step_um": float(gap_step),
        "gap_min_um": float(gap_min),
        "gap_max_um": float(gap_max),
        "auto_harmonic_restore": int(auto_harmonic),
        "intensity_signal": getattr(intensity_signal, "name", str(intensity_signal)),
    }
    if md:
        plan_md.update(md)

    def _one_energy(target_eV, index):
        first = index == 0
        if first:
            print("EPU calibration: starting at {:.1f} eV with managed energy move.".format(target_eV))
            yield from _feedback_on(diag)
            if active["harmonic"] is not None:
                yield from bps.mv(energy.target_harmonic, int(active["harmonic"]))
            yield from bps.mv(energy, float(target_eV))
            active["harmonic"] = int((yield from bps.rd(energy.harmonic)))
            print("EPU calibration: initial managed move reports harmonic {}.".format(
                active["harmonic"]))
        else:
            print("EPU calibration: feedback OFF; moving DCM directly to {:.1f} eV "
                  "without LUT IVU/harmonic selection.".format(target_eV))
            yield from _feedback_off(diag)
            yield from _direct_dcm_move(energy, target_eV)

        yield from bps.mv(energy.target_harmonic, int(active["harmonic"]),
                          energy.harmonic, int(active["harmonic"]))
        print("EPU calibration: setting attenuation factor {:.4g} at {:.1f} eV.".format(
            attenuation_factor, target_eV))
        yield from bps.mv(attenuation, float(attenuation_factor))
        pilatus_settings = yield from _set_pilatus_energy(
            detector, target_eV, thresh_ev=thresh_ev, gain=pilatus_gain,
            timeout=pilatus_confirm_timeout, settle=pilatus_settle)

        yield from _feedback_off(diag)

        run_md = dict(plan_md)
        run_md.update({
            "target_energy_eV": float(target_eV),
            "active_harmonic": int(active["harmonic"]),
            "energy_index": int(index),
        })
        uid = yield from bps.open_run(md=run_md)
        run_uids.append(uid)
        detector_staged = False
        try:
            yield from bps.stage(detector)
            detector_staged = True
            current_h = int(active["harmonic"])
            center = energy.energy_to_gap(target_eV, current_h)
            gaps = _gap_grid(center, half_width=gap_half_width, step=gap_step,
                             gap_min=gap_min, gap_max=gap_max)
            stream = "harmonic_{}".format(current_h)
            print("EPU calibration: scanning harmonic {} centered at {:.1f} um.".format(
                current_h, center))
            points, best = yield from _scan_gap_stream(
                stream, energy_obj=energy, detector=detector,
                intensity_signal=intensity_signal, read_devices=read_devices,
                gaps=gaps, gap_settle=gap_settle, target_eV=target_eV,
                harmonic=current_h)

            trial = None
            selected = dict(best)
            selected_h = current_h
            decision = "peak"
            at_lower_limit = abs(best["gap_um"] - float(gap_min)) <= abs(float(gap_step)) * 0.51
            if at_lower_limit:
                trial_h = current_h - 2
                if trial_h >= 1:
                    print("EPU calibration: strongest point is at {:.1f} um; "
                          "testing lower harmonic {}.".format(gap_min, trial_h))
                    trial_center = energy.energy_to_gap(target_eV, trial_h)
                    trial_gaps = _gap_grid(trial_center, half_width=gap_half_width,
                                           step=gap_step, gap_min=gap_min, gap_max=gap_max)
                    trial_points, trial_best = yield from _scan_gap_stream(
                        "harmonic_{}".format(trial_h), energy_obj=energy,
                        detector=detector, intensity_signal=intensity_signal,
                        read_devices=read_devices, gaps=trial_gaps,
                        gap_settle=gap_settle, target_eV=target_eV,
                        harmonic=trial_h)
                    trial = {
                        "harmonic": trial_h,
                        "center_gap_um": trial_center,
                        "points": trial_points,
                        "best": trial_best,
                    }
                    if trial_best["intensity"] > best["intensity"]:
                        selected = dict(trial_best)
                        selected_h = trial_h
                        active["harmonic"] = trial_h
                        decision = "switched_to_lower_harmonic"
                        print("EPU calibration: lower harmonic {} is stronger; switching.".format(
                            trial_h))
                    else:
                        decision = "kept_current_harmonic_at_gap_min"
                        print("EPU calibration: current harmonic {} at {:.1f} um remains stronger.".
                              format(current_h, gap_min))
                else:
                    decision = "gap_min_no_lower_harmonic"

            print("EPU calibration: selected E={:.1f} eV h{} gap {:.1f} um "
                  "intensity {:.6g}.".format(
                      target_eV, int(selected_h), selected["gap_um"], selected["intensity"]))
            command_gap = min(max(float(selected["gap_um"]), float(gap_min)), float(gap_max))
            if command_gap != float(selected["gap_um"]):
                print("EPU calibration: clamping selected gap {:.3f} um to {:.3f} um "
                      "for motor limits.".format(float(selected["gap_um"]), command_gap))
            yield from bps.mv(energy.target_harmonic, int(selected_h),
                              energy.harmonic, int(selected_h),
                              energy.ivugap, command_gap)

            row = {
                "energy_eV": float(target_eV),
                "harmonic": int(selected_h),
                "gap_um": float(selected["gap_um"]),
                "command_gap_um": float(command_gap),
                "max_intensity": float(selected["intensity"]),
                "decision": decision,
                "run_uid": uid,
                "current_harmonic": int(current_h),
                "current_center_gap_um": float(center),
                "current_best_gap_um": float(best["gap_um"]),
                "current_best_intensity": float(best["intensity"]),
                "trial": trial,
                "pilatus": pilatus_settings,
            }
            rows.append(row)

            yield from bps.abs_set(decision_energy, float(target_eV), wait=True)
            yield from bps.abs_set(decision_harmonic, int(selected_h), wait=True)
            yield from bps.abs_set(decision_gap, float(selected["gap_um"]), wait=True)
            yield from bps.abs_set(decision_intensity, float(selected["intensity"]), wait=True)
            yield from bps.create(name="decision")
            yield from bps.read(decision_energy)
            yield from bps.read(decision_harmonic)
            yield from bps.read(decision_gap)
            yield from bps.read(decision_intensity)
            yield from bps.save()
        finally:
            if detector_staged:
                yield from bps.unstage(detector)
            yield from bps.close_run()

        print("EPU calibration: feedback ON; centering DCM roll/pitch before next energy.")
        yield from _center_with_feedback(
            diag, oval_settle_s=oval_settle_s, oval_settle_window=oval_settle_window,
            recenter_target=recenter_target, recenter_step=recenter_step,
            recenter_rate=recenter_rate, recenter_settle=recenter_settle,
            verbose=verbose_centering)

    def _body():
        for index, target_eV in enumerate(energies):
            yield from _one_energy(target_eV, index)

    def _cleanup():
        yield from _feedback_on(diag)
        print("EPU calibration: restoring automatic harmonic search start to {}.".format(
            int(auto_harmonic)))
        yield from bps.mv(energy.target_harmonic, int(auto_harmonic),
                          energy.harmonic, int(auto_harmonic))
        table = {
            "created": datetime.now().isoformat(timespec="seconds"),
            "inputs": plan_md,
            "run_uids": list(run_uids),
            "rows": rows,
        }
        candidate_key["key"] = _write_candidate_table(store, table)
        print("EPU calibration: saved candidate table to mdsave['{}'] "
              "({} rows).".format(candidate_key["key"], len(rows)))

    yield from bpp.finalize_wrapper(_body(), _cleanup())
    return candidate_key["key"]


class EPUCalibrationLivePlot:
    """Small Bokeh callback for the EPU calibration plan.

    Use at the console before running the plan::

        cb = EPUCalibrationLivePlot()
        token = RE.subscribe(cb)

    The callback opens one Bokeh browser window and reuses it for subsequent events.
    """

    def __init__(self):
        from bokeh.io import output_notebook, show
        from bokeh.layouts import column
        from bokeh.models import ColumnDataSource
        from bokeh.plotting import figure

        self._descriptors = {}
        self._starts = {}
        self._current = ColumnDataSource({"gap": [], "intensity": [], "stream": []})
        self._table = ColumnDataSource({"energy": [], "gap": [], "intensity": [], "harmonic": []})

        scan = figure(title="Current EPU Gap Scan", x_axis_label="IVU gap (um)",
                      y_axis_label="SAXS stats1 total", width=900, height=420)
        scan.scatter("gap", "intensity", source=self._current, size=7, alpha=0.8)
        table = figure(title="Candidate EPU Table", x_axis_label="Energy (eV)",
                       y_axis_label="Selected IVU gap (um)", width=900, height=420)
        table.line("energy", "gap", source=self._table, line_width=2)
        table.scatter("energy", "gap", source=self._table, size=8, alpha=0.9)
        self._scan_plot = scan
        self._table_plot = table
        output_notebook(hide_banner=True)
        self._handle = show(column(scan, table), notebook_handle=True)

    def __call__(self, name, doc):
        if name == "start":
            self._starts[doc["uid"]] = doc
            if doc.get("plan_name") == "calibrate_epu_lookup":
                self._current.data = {"gap": [], "intensity": [], "stream": []}
                e = doc.get("target_energy_eV")
                h = doc.get("active_harmonic")
                self._scan_plot.title.text = "Current EPU Gap Scan: E={} eV h{}".format(e, h)
                self._push()
        elif name == "descriptor":
            self._descriptors[doc["uid"]] = doc
        elif name == "event":
            desc = self._descriptors.get(doc.get("descriptor"), {})
            stream = desc.get("name", "")
            data = doc.get("data", {})
            gap = _first_matching_value(data, "energy_ivugap", "ivugap", "gap")
            intensity = _first_matching_value(data, "pil2M_stats1_total", "stats1_total")
            if gap is not None and intensity is not None and stream.startswith("harmonic_"):
                self._current.stream({"gap": [gap], "intensity": [intensity], "stream": [stream]})
                self._push()
            if stream == "decision":
                e = data.get("epu_calibration_energy_eV")
                h = data.get("epu_calibration_harmonic")
                gap = data.get("epu_calibration_gap_um")
                intensity = data.get("epu_calibration_intensity")
            if stream == "decision" and gap is not None and intensity is not None:
                start = self._starts.get(desc.get("run_start"), {})
                self._table.stream({
                    "energy": [e if e is not None else start.get("target_energy_eV", len(self._table.data["energy"]))],
                    "gap": [gap],
                    "intensity": [intensity],
                    "harmonic": [h if h is not None else start.get("active_harmonic", 0)],
                })
                self._push()

    def _push(self):
        try:
            from bokeh.io import push_notebook
            push_notebook(handle=self._handle)
        except Exception:
            pass


def _first_matching_value(data, *tokens):
    for token in tokens:
        if token in data:
            return data[token]
    lowered = {str(k).lower(): k for k in data}
    for token in tokens:
        token = str(token).lower()
        for low, key in lowered.items():
            if token in low:
                return data[key]
    return None
