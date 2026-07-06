"""
Empirical attenuator foil-thickness calibration plans.

The plan records ratio data for exact physical foil combinations across the
automated 5-24 keV energy range.  It does not fit foil thicknesses online; the
run documents are intended for offline fitting of one effective thickness per
physical foil, with harmonic leakage included as nuisance terms.
"""

import math

import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from ophyd import Signal

from smi_beamline.devices import attenuator_data as _ad
from smibase.beam import SMI as smi


__all__ = ["attenuator_thickness_calibration", "attenuator_two_pass_calibration"]


DEFAULT_ENERGIES_EV = (5000, 6500, 8000, 10000, 12000, 16000, 19000, 22000, 24000)
DEFAULT_HARMONIC_TARGET_FACTORS = (1e4, 1e5, 1e6)


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


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _foil_groups_by_material():
    groups = []
    seen = set()
    for label, (base, _mult) in _ad.FOIL_LAYOUT.items():
        if base in seen:
            continue
        labels = [k for k, (b, _m) in _ad.FOIL_LAYOUT.items() if b == base]
        labels = sorted(labels, key=_ad._foil_sort_key)
        groups.append((base, labels))
        seen.add(base)
    return groups


def _default_fixed_states():
    """Compact state list: open beam, every foil alone, and same-material pairs."""
    states = [("open", ())]
    for label in sorted(_ad.FOIL_LAYOUT, key=_ad._foil_sort_key):
        states.append(("single_att{}".format(label), (label,)))

    for base, labels in _foil_groups_by_material():
        short = base.replace("_", "")
        for a, b in zip(labels[:-1], labels[1:]):
            states.append(("pair_{}_att{}_att{}".format(short, a, b), (a, b)))
    return states


def _dynamic_harmonic_states(energy_eV, target_factors, max_foils):
    states = []
    for target in target_factors:
        labels, factor, _ok = _ad.select_foils(
            float(target), float(energy_eV), max_foils=int(max_foils), mode="atleast")
        if labels:
            states.append(("target_{:.0e}_actual_{:.2e}".format(float(target), factor), labels))
    return states


def _dedupe_states(states):
    out = []
    seen = set()
    for name, labels in states:
        labels = tuple(sorted(labels, key=_ad._foil_sort_key))
        if labels in seen:
            continue
        seen.add(labels)
        out.append((name, labels))
    return out


def _set_exact_foils(labels, attenuators1, attenuators2, settle_s):
    want1 = ["f{}".format(label.split("_", 1)[1]) for label in labels
             if label.split("_", 1)[0] == "1"]
    want2 = ["f{}".format(label.split("_", 1)[1]) for label in labels
             if label.split("_", 1)[0] == "2"]
    yield from bps.mv(attenuators1, want1, attenuators2, want2)
    if settle_s:
        yield from bps.sleep(float(settle_s))


def _safe_factor(labels, energy_eV):
    factor = _ad.attenuation_factor(labels, energy_eV)
    if not math.isfinite(factor):
        return 1e300
    return factor


def _check_saturation(readings, limit, readers):
    if limit is None:
        return
    limit = abs(float(limit))
    reader_names = [getattr(reader, "name", "") for reader in readers]
    for key, item in readings.items():
        if not any(key == name or key.startswith(name + "_") for name in reader_names):
            continue
        value = item.get("value") if isinstance(item, dict) else None
        try:
            value = abs(float(value))
        except Exception:
            continue
        if value >= limit:
            raise RuntimeError(
                "pin-diode reading {}={:.6g} reached saturation limit {:.6g}".format(
                    key, value, limit))


def attenuator_thickness_calibration(
        *,
        energies_eV=DEFAULT_ENERGIES_EV,
        energy=None,
        attenuators1=None,
        attenuators2=None,
        attenuation=None,
        pin_readers=None,
        pilatus_readers=None,
        extra_readers=None,
        fixed_states=None,
        harmonic_target_factors=DEFAULT_HARMONIC_TARGET_FACTORS,
        harmonic_max_foils=4,
        pilatus_min_factor=1e6,
        bracket_every=8,
        settle_s=0.5,
        pin_saturation_limit=None,
        restore_open=True,
        md=None):
    """Measure exact attenuator-foil states over 5-24 keV for offline fitting.

    Parameters
    ----------
    energies_eV : sequence
        Photon energies to visit.  The default spans the easy automated range,
        5-24 keV, while avoiding the Mo K edge at about 20 keV.
    energy : positioner, optional
        Beamline energy object.  Defaults to ``energy`` from the IPython namespace.
        Existing managed-energy-move preprocessing will handle large moves.
    attenuators1, attenuators2 : devices, optional
        Aggregate attenuator banks.  Defaults to the live namespace objects.
    attenuation : device, optional
        Energy-aware attenuation reporter.  If supplied/readable, it is included
        in every event and refreshed for the exact labels being measured.
    pin_readers : device or list, optional
        Pin-diode/current signals or devices to read for every state.  Defaults
        to ``pdcurrent`` from the live namespace if present.
    pilatus_readers : device or list, optional
        Pilatus direct-beam detector/ROI readers.  These are only read for states
        whose modeled attenuation factor is at least ``pilatus_min_factor``.
    fixed_states : list, optional
        Explicit ``[(name, labels), ...]`` state list.  Labels are strings like
        ``"2_6"``.  If omitted, the plan measures open beam, every foil alone,
        and adjacent same-material pairs.
    harmonic_target_factors : sequence
        Additional energy-dependent high-attenuation states selected at each
        energy.  These help expose 2x/3x harmonic leakage when the fundamental is
        strongly attenuated.
    pin_saturation_limit : float, optional
        Absolute reading limit.  If any pin-reader value reaches this limit, the
        plan raises rather than silently collecting saturated data.

    Notes
    -----
    Configure detector exposure time, direct-beam ROI, and Pilatus threshold/gain
    before running.  The plan deliberately records modeled transmission/factor
    only as metadata; the empirical effective thicknesses should be fitted from
    the measured ratios offline.
    """
    energy = _resolve("energy", energy)
    attenuators1 = _resolve("attenuators1", attenuators1)
    attenuators2 = _resolve("attenuators2", attenuators2)
    if attenuation is None:
        attenuation = _namespace().get("attenuation")

    ns = _namespace()
    if pin_readers is None:
        pin_readers = [ns["pdcurrent"]] if "pdcurrent" in ns else []
    else:
        pin_readers = _as_list(pin_readers)
    pilatus_readers = _as_list(pilatus_readers)
    extra_readers = _as_list(extra_readers)

    if fixed_states is None:
        fixed_states = _default_fixed_states()
    else:
        fixed_states = [(name, tuple(labels)) for name, labels in fixed_states]

    if not pin_readers and not pilatus_readers:
        raise ValueError("supply at least one pin_readers or pilatus_readers device/signal")

    state_index = Signal(name="attenuator_calibration_state_index", value=0, kind="normal")
    state_name = Signal(name="attenuator_calibration_state_name", value="", kind="normal")
    state_labels = Signal(name="attenuator_calibration_labels", value="", kind="normal")
    requested_energy = Signal(name="attenuator_calibration_energy_eV", value=0.0, kind="normal")
    modeled_factor = Signal(name="attenuator_calibration_modeled_factor", value=1.0, kind="normal")
    modeled_transmission = Signal(
        name="attenuator_calibration_modeled_transmission", value=1.0, kind="normal")
    calibration_signals = [
        state_index, state_name, state_labels, requested_energy,
        modeled_factor, modeled_transmission,
    ]
    if attenuation is not None:
        extra_readers = list(extra_readers) + [attenuation]

    plan_md = {
        "plan_name": "attenuator_thickness_calibration",
        "purpose": "empirical attenuator effective-thickness calibration",
        "energies_eV": [float(e) for e in energies_eV],
        "foil_layout": {label: list(value) for label, value in _ad.FOIL_LAYOUT.items()},
        "harmonic_target_factors": [float(v) for v in harmonic_target_factors],
        "pilatus_min_factor": float(pilatus_min_factor),
        "pin_saturation_limit": pin_saturation_limit,
    }
    if md:
        plan_md.update(md)

    staged = []
    for reader in pilatus_readers:
        if hasattr(reader, "stage") and hasattr(reader, "unstage"):
            yield from bps.stage(reader)
            staged.append(reader)

    uid = yield from bps.open_run(md=plan_md)
    try:
        idx = 0
        for energy_eV in energies_eV:
            energy_eV = float(energy_eV)
            if not 5000 <= energy_eV <= 24000:
                raise ValueError("energy {:.1f} eV is outside the intended 5-24 keV range".format(
                    energy_eV))
            print("attenuator calibration: moving to {:.1f} eV".format(energy_eV))
            yield from bps.mv(energy, energy_eV)

            states = list(fixed_states)
            states.extend(_dynamic_harmonic_states(
                energy_eV, harmonic_target_factors, harmonic_max_foils))
            states = _dedupe_states(states)

            for local_index, (name, labels) in enumerate(states):
                if bracket_every and local_index and local_index % int(bracket_every) == 0:
                    states_to_measure = [("open_bracket", ()), (name, labels)]
                else:
                    states_to_measure = [(name, labels)]

                for measure_name, measure_labels in states_to_measure:
                    idx += 1
                    factor = _safe_factor(measure_labels, energy_eV)
                    transmission = 1.0 / factor if factor else 0.0
                    label_text = ",".join(measure_labels)

                    print("  {:04d}: {} [{}] factor~{:.3g}".format(
                        idx, measure_name, label_text or "open", factor))
                    yield from _set_exact_foils(
                        measure_labels, attenuators1, attenuators2, settle_s)
                    if attenuation is not None and hasattr(attenuation, "compute"):
                        attenuation.compute(labels=measure_labels, energy_eV=energy_eV)

                    yield from bps.abs_set(state_index, idx, wait=True)
                    yield from bps.abs_set(state_name, measure_name, wait=True)
                    yield from bps.abs_set(state_labels, label_text, wait=True)
                    yield from bps.abs_set(requested_energy, energy_eV, wait=True)
                    yield from bps.abs_set(modeled_factor, factor, wait=True)
                    yield from bps.abs_set(modeled_transmission, transmission, wait=True)

                    pin_devices = list(pin_readers) + list(extra_readers) + calibration_signals
                    if pin_devices:
                        readings = yield from bps.trigger_and_read(pin_devices, name="pin_diode")
                        _check_saturation(readings, pin_saturation_limit, pin_readers)

                    if pilatus_readers and factor >= float(pilatus_min_factor):
                        pilatus_devices = (
                            list(pilatus_readers) + list(extra_readers) + calibration_signals)
                        yield from bps.trigger_and_read(pilatus_devices, name="pilatus_direct")

            idx += 1
            yield from _set_exact_foils((), attenuators1, attenuators2, settle_s)
            yield from bps.abs_set(state_index, idx, wait=True)
            yield from bps.abs_set(state_name, "open_end_energy", wait=True)
            yield from bps.abs_set(state_labels, "", wait=True)
            yield from bps.abs_set(requested_energy, energy_eV, wait=True)
            yield from bps.abs_set(modeled_factor, 1.0, wait=True)
            yield from bps.abs_set(modeled_transmission, 1.0, wait=True)
            readings = yield from bps.trigger_and_read(
                list(pin_readers) + list(extra_readers) + calibration_signals,
                name="pin_diode")
            _check_saturation(readings, pin_saturation_limit, pin_readers)
    finally:
        try:
            if restore_open:
                yield from _set_exact_foils((), attenuators1, attenuators2, settle_s)
        finally:
            try:
                yield from bps.close_run()
            finally:
                for reader in reversed(staged):
                    yield from bps.unstage(reader)

    return uid


def attenuator_two_pass_calibration(
        *,
        energies_eV=DEFAULT_ENERGIES_EV,
        energy=None,
        attenuators1=None,
        attenuators2=None,
        attenuation=None,
        pin_readers=None,
        pilatus_readers=None,
        extra_readers=None,
        pin_fixed_states=None,
        pilatus_fixed_states=None,
        pin_harmonic_target_factors=(),
        pilatus_harmonic_target_factors=DEFAULT_HARMONIC_TARGET_FACTORS,
        harmonic_max_foils=4,
        pilatus_min_factor=1e6,
        bracket_every=8,
        settle_s=0.5,
        pin_saturation_limit=None,
        restore_open=True,
        technique="gisaxs",
        md=None):
    """Run attenuator calibration once with the pin diode and once with Pilatus.

    The beamline is put into alignment geometry once, so the SAXS beamstop is
    moved out for the pin diode/direct-beam measurements and restored in a
    finalizer via ``smi.modeMeasurement()``.
    """
    ns = _namespace()
    energy = _resolve("energy", energy)
    attenuators1 = _resolve("attenuators1", attenuators1)
    attenuators2 = _resolve("attenuators2", attenuators2)
    if attenuation is None:
        attenuation = ns.get("attenuation")
    if pin_readers is None:
        pin_readers = [ns["pdcurrent"]] if "pdcurrent" in ns else []
    else:
        pin_readers = _as_list(pin_readers)
    if pilatus_readers is None:
        pilatus_readers = [ns["pil2M"]] if "pil2M" in ns else []
    else:
        pilatus_readers = _as_list(pilatus_readers)
    extra_readers = _as_list(extra_readers)

    if not pin_readers:
        raise ValueError("pin_readers is empty; supply a pin diode/current signal")
    if not pilatus_readers:
        raise ValueError("pilatus_readers is empty; supply pil2M or another Pilatus reader")

    base_md = {"calibration_wrapper": "attenuator_two_pass_calibration"}
    if md:
        base_md.update(md)

    def _body():
        yield from smi.modeAlignment(technique=technique)
        yield from smi.setDirectBeamROI(technique=technique)

        print("attenuator two-pass calibration: pin-diode pass")
        pin_uid = yield from attenuator_thickness_calibration(
            energies_eV=energies_eV,
            energy=energy,
            attenuators1=attenuators1,
            attenuators2=attenuators2,
            attenuation=attenuation,
            pin_readers=pin_readers,
            pilatus_readers=[],
            extra_readers=extra_readers,
            fixed_states=pin_fixed_states,
            harmonic_target_factors=pin_harmonic_target_factors,
            harmonic_max_foils=harmonic_max_foils,
            pilatus_min_factor=pilatus_min_factor,
            bracket_every=bracket_every,
            settle_s=settle_s,
            pin_saturation_limit=pin_saturation_limit,
            restore_open=restore_open,
            md={**base_md, "attenuator_calibration_pass": "pin_diode"},
        )

        print("attenuator two-pass calibration: high-attenuation Pilatus pass")
        pilatus_uid = yield from attenuator_thickness_calibration(
            energies_eV=energies_eV,
            energy=energy,
            attenuators1=attenuators1,
            attenuators2=attenuators2,
            attenuation=attenuation,
            pin_readers=[],
            pilatus_readers=pilatus_readers,
            extra_readers=extra_readers,
            fixed_states=pilatus_fixed_states,
            harmonic_target_factors=pilatus_harmonic_target_factors,
            harmonic_max_foils=harmonic_max_foils,
            pilatus_min_factor=pilatus_min_factor,
            bracket_every=bracket_every,
            settle_s=settle_s,
            pin_saturation_limit=pin_saturation_limit,
            restore_open=restore_open,
            md={**base_md, "attenuator_calibration_pass": "pilatus_high_attenuation"},
        )

        return {"pin_uid": pin_uid, "pilatus_uid": pilatus_uid}

    return (yield from bpp.finalize_wrapper(_body(), smi.modeMeasurement()))
