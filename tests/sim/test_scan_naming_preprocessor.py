"""Tier-2 (sim) tests: the default scan-name preprocessor against FAKE devices under a RunEngine.

No hardware is touched.  These exercise the message-level behaviour of
``smi_beamline.devices._plan_helpers.scan_name_preprocessor`` and the beamline wiring in
``smi_beamline.plans.scan_naming`` -- the recorded-field replacement for the old ``get_scan_md``.
"""
import pytest

pytest.importorskip("bluesky")
from bluesky import RunEngine  # noqa: E402
import bluesky.plans as bp  # noqa: E402
from ophyd.sim import det, SynAxis  # noqa: E402

from smi_beamline.devices._plan_helpers import scan_name_preprocessor  # noqa: E402
from smi_beamline.plans import scan_naming as sn  # noqa: E402


# --------------------------------------------------------------------------- helpers / fixtures
def _seed(sig, value):
    (sig.sim_put if hasattr(sig, "sim_put") else sig.put)(value)


@pytest.fixture
def energy_dev(make_fake):
    """A fake Energy with a seeded bragg readback so ``energy.read()`` (inverse) yields a value."""
    from smi_beamline.devices.energy import Energy

    en = make_fake(Energy, name="energy", prefix="")
    _seed(en.bragg.user_readback, 12.7)
    _seed(en.harmonic, 7)
    return en


@pytest.fixture
def waxs_dev(make_fake):
    """A fake WAXS motor bank with the ``waxs_arc`` rename applied (as the instance module does)."""
    from smi_beamline.devices.pilatus import WAXS_Detector

    w = make_fake(WAXS_Detector, name="pil900KW", prefix="XF:12IDC-ES:2{Det:900KW}",
                  asset_path="p9k").motors
    w.arc.user_readback.name = "waxs_arc"
    _seed(w.arc.user_readback, 20.0)
    return w


@pytest.fixture
def sdd_dev(make_fake):
    """A fake SAXS detector-position device (``pil2M.motor``); records ``pil2M_motor_z`` (SDD)."""
    from smi_beamline.devices.pilatus import SAXS_Detector

    p = make_fake(SAXS_Detector, name="pil2M", prefix="XF:12ID2-ES{Pilatus:Det-2M}",
                  asset_path="p2m").motor
    _seed(p.z.user_readback, 8300.0)
    return p


def _collect():
    """Return (callback, names_list, events_list) capturing start sample_name + event data."""
    names, events = [], []

    def cb(name, doc):
        if name == "start":
            names.append(doc.get("sample_name"))
        elif name == "event":
            events.append(doc["data"])

    return cb, names, events


# --------------------------------------------------------------------------- core append behaviour
def test_appends_template_to_base_name(energy_dev, waxs_dev, sdd_dev):
    """No per-run name -> append default template to the base (RE.md prefix)."""
    RE = RunEngine({})
    RE.md["sample_name"] = "SMI_user"
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, events = _collect()
    RE(bp.count([det], num=1), cb)

    assert names[-1] == "SMI_user_" + sn.DEFAULT_SCAN_NAME_TEMPLATE
    # the referenced fields are recorded so the worker can fill them
    for key in ("energy_energy", "waxs_arc", "pil2M_motor_z"):
        assert key in events[-1]
    # the global md prefix is untouched (no leak into later runs)
    assert RE.md["sample_name"] == "SMI_user"


def test_appends_to_explicit_per_run_name(energy_dev, waxs_dev, sdd_dev):
    """A plan that passes its own sample_name -> template appends to THAT, not the base."""
    RE = RunEngine({})
    RE.md["sample_name"] = "SMI_user"
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, _ = _collect()
    RE(bp.count([det], num=1, md={"sample_name": "myfilm"}), cb)

    assert names[-1] == "myfilm_" + sn.DEFAULT_SCAN_NAME_TEMPLATE


# --------------------------------------------- user-supplied token template -> skip the default
def test_user_token_template_is_used_verbatim(energy_dev, waxs_dev, sdd_dev):
    """A per-run name that already has {tokens} is taken as-is; the default is NOT appended."""
    RE = RunEngine({})
    RE.md["sample_name"] = "SMI_user"
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, events = _collect()
    custom = "test_{energy_energy}eV_{waxs_arc}wa"  # the user's own template (no format spec)
    RE(bp.count([det], num=1, md={"sample_name": custom}), cb)

    assert names[-1] == custom  # verbatim, default NOT appended
    # ...and the fields it references ARE recorded, so the worker can fill them
    assert "energy_energy" in events[-1] and "waxs_arc" in events[-1]
    # a token the user did NOT reference (sdd) is not force-recorded
    assert "pil2M_motor_z" not in events[-1]


def test_user_token_template_records_only_its_tokens(energy_dev, waxs_dev, sdd_dev):
    """An energy-only user template records energy but not waxs/sdd."""
    RE = RunEngine({})
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, events = _collect()
    RE(bp.count([det], num=1, md={"sample_name": "just_{energy_energy:.0f}"}), cb)

    assert names[-1] == "just_{energy_energy:.0f}"
    assert "energy_energy" in events[-1]
    assert "waxs_arc" not in events[-1] and "pil2M_motor_z" not in events[-1]


def test_user_token_template_worker_render(energy_dev, waxs_dev, sdd_dev):
    """The user's own bare-token template fills correctly through the worker's str.format."""
    RE = RunEngine({})
    RE.md["sample_name"] = "SMI_user"
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, events = _collect()
    RE(bp.count([det], num=1, md={"sample_name": "film_{waxs_arc}wa"}), cb)

    single = dict(events[-1])
    tt = "{det_name}/" + names[-1] + "_id7_{N:06d}_{det_type}.tif"
    out = tt.format(det_name="2M", N=0, det_type="SAXS", **single).format(**single)
    assert out == "2M/film_20.0wa_id7_000000_SAXS.tif"


def test_no_base_and_no_per_run_name_uses_template_alone(energy_dev, waxs_dev, sdd_dev):
    RE = RunEngine({})  # no RE.md['sample_name']
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, _ = _collect()
    RE(bp.count([det], num=1), cb)
    assert names[-1] == sn.DEFAULT_SCAN_NAME_TEMPLATE


def test_worker_render_roundtrip(energy_dev, waxs_dev, sdd_dev):
    """The recorded values fill the template via str.format exactly as the symlink worker does."""
    RE = RunEngine({})
    RE.md["sample_name"] = "SMI_user"
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, events = _collect()
    RE(bp.count([det], num=1), cb)

    single_doc_data = dict(events[-1])  # {data_key: value}
    target_template = "{det_name}/" + names[-1] + "_id7_{N:06d}_{det_type}.tif"
    out = target_template.format(det_name="2M", N=0, det_type="SAXS",
                                 **single_doc_data).format(**single_doc_data)
    # arc seeded 20.0, sdd seeded 8300.0; energy is whatever inverse() gives (just check structure)
    assert out.startswith("2M/SMI_user_")
    assert "eV_wa20.0_sdd8300.0mm_id7_000000_SAXS.tif" in out
    assert "{" not in out and "}" not in out  # everything got filled


# --------------------------------------------------------------------------- detectors-only guard
def test_no_primary_bundle_run_records_nothing(energy_dev, waxs_dev, sdd_dev):
    """A run with no ``primary`` Event gets no injected reads (and writes no file).

    A bare move opens no ``primary`` bundle, so the preprocessor injects nothing.  (We move a
    plain ``SynAxis`` rather than a fake ``EpicsMotor``, whose simulated limits are unset.)
    """
    import bluesky.plan_stubs as bps

    RE = RunEngine({})
    RE.md["sample_name"] = "SMI_user"
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    knob = SynAxis(name="knob")

    def move_in_a_run():
        # open/close a run around a move -> a run with NO primary Event bundle
        yield from bps.open_run()
        yield from bps.mv(knob, 1)
        yield from bps.close_run()

    cb, names, events = _collect()
    RE(move_in_a_run(), cb)
    assert events == []  # no primary bundle -> nothing recorded
    # the name is still appended (harmless; this run writes no file anyway)
    assert names[-1] == "SMI_user_" + sn.DEFAULT_SCAN_NAME_TEMPLATE


# --------------------------------------------------------------------------- idempotency
def test_idempotent_when_name_already_has_suffix(energy_dev, waxs_dev, sdd_dev):
    RE = RunEngine({})
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, _ = _collect()
    already = "myfilm_" + sn.DEFAULT_SCAN_NAME_TEMPLATE
    RE(bp.count([det], num=1, md={"sample_name": already}), cb)
    assert names[-1] == already  # not double-appended


# --------------------------------------------------------------------------- collision safety
def test_token_device_already_in_detector_list_does_not_crash():
    """If the plan already reads a token device, the PP must not read it twice (would raise).

    Bluesky raises ``ValueError`` on a duplicate read of the same object within one Event, so the
    preprocessor must skip a token device the plan itself already reads.
    """
    RE = RunEngine({})
    RE.md["sample_name"] = "u"
    energy = SynAxis(name="energy")
    waxs = SynAxis(name="waxs")
    RE.preprocessors.append(
        lambda plan: scan_name_preprocessor(
            plan,
            template="{energy:.1f}eV_wa{waxs:.1f}",
            token_devices={"energy": energy, "waxs": waxs},
            base_name="u",
        )
    )

    cb, names, events = _collect()
    # waxs is BOTH a detector (in the list) and a token device (in the template)
    RE(bp.count([det, waxs], num=1), cb)
    assert len(events) == 1
    assert "waxs" in events[-1] and "energy" in events[-1]


# --------------------------------------------------------------------------- baseline interleaving
# Regression for IllegalMessageSequence ("A second 'create' ... until ... 'save'/'drop'"): the
# preprocessor must coexist with SupplementalData's baseline stream (which opens its own
# create/save bundles at run open/close).  This is the real beamline config (sd.baseline holds
# pil2m_pos/waxs, which are ALSO token devices).
def _primary_events(plan, baseline, token_devices, template):
    """Run ``plan`` with sd.baseline + the naming PP; return the PRIMARY-stream event data dicts."""
    from bluesky.preprocessors import SupplementalData

    RE = RunEngine({})
    RE.preprocessors.append(SupplementalData(baseline=baseline))
    RE.preprocessors.append(
        lambda p: scan_name_preprocessor(
            p, template=template, token_devices=token_devices, base_name="u")
    )
    desc, prim, stop = {}, [], []

    def cb(name, doc):
        if name == "descriptor":
            desc[doc["uid"]] = doc.get("name")
        elif name == "event" and desc.get(doc["descriptor"]) == "primary":
            prim.append(doc["data"])
        elif name == "stop":
            stop.append(doc)

    RE(plan, cb)
    assert stop and stop[-1]["exit_status"] == "success"  # run closed cleanly, no IMS
    return prim


def test_runs_cleanly_with_baseline_stream():
    energy = SynAxis(name="energy")
    waxs = SynAxis(name="waxs")
    sdd = SynAxis(name="sdd")
    td = {"energy": energy, "waxs": waxs, "sdd": sdd}
    tmpl = "{energy:.1f}_{waxs:.1f}_{sdd:.1f}"

    # baseline holds devices that are ALSO token devices (the SMI config)
    prim = _primary_events(bp.count([det], num=2), [waxs, sdd], td, tmpl)
    assert len(prim) == 2
    for ev in prim:
        # injected token fields are present in the PRIMARY events
        assert "energy" in ev and "waxs" in ev and "sdd" in ev


def test_collision_with_baseline_records_field_once():
    energy = SynAxis(name="energy")
    waxs = SynAxis(name="waxs")
    sdd = SynAxis(name="sdd")
    td = {"energy": energy, "waxs": waxs, "sdd": sdd}
    tmpl = "{energy:.1f}_{waxs:.1f}_{sdd:.1f}"

    # energy is in the detector list (plan reads it) AND a token; baseline holds waxs/sdd.
    prim = _primary_events(bp.count([det, energy], num=1), [waxs, sdd], td, tmpl)
    keys = list(prim[0])
    assert keys.count("energy") == 1          # recorded exactly once (not double-read)
    assert "det" in keys and "waxs" in keys and "sdd" in keys


def test_scan_over_a_token_device_records_it_once():
    """Scanning a motor that is also a token device must not double-read it."""
    energy = SynAxis(name="energy")
    waxs = SynAxis(name="waxs")
    sdd = SynAxis(name="sdd")
    td = {"energy": energy, "waxs": waxs, "sdd": sdd}
    tmpl = "{energy:.1f}_{waxs:.1f}_{sdd:.1f}"

    # scan OVER waxs (it is the motor) -> waxs recorded once by the scan; energy/sdd injected
    prim = _primary_events(bp.scan([det], waxs, 0, 1, 3), [sdd], td, tmpl)
    assert len(prim) == 3
    for ev in prim:
        assert list(ev).count("waxs") == 1
        assert "energy" in ev and "sdd" in ev and "det" in ev


def test_parent_detector_with_child_token_does_not_collide():
    """Plan reads a PARENT detector whose CHILD sub-device is a token (the real pil900KW/waxs case).

    Reading ``pil900KW`` already records its ``.motors`` child's ``waxs_arc`` key, so the
    preprocessor must NOT also inject the ``waxs`` (== ``pil900KW.motors``) token -- that would
    collide on ``waxs_arc``.  Exercised here with a generic parent/child device.
    """
    from ophyd import Device, Component as Cpt, Signal
    from ophyd.sim import SynSignal

    class _Child(Device):
        arc = Cpt(Signal, value=20.0)

    class _Parent(Device):
        motors = Cpt(_Child)
        val = Cpt(Signal, value=1.0)

    parent = _Parent(name="pil900KW_like")
    parent.motors.arc.name = "waxs_arc"          # renamed key, like smibase does
    waxs = parent.motors                          # token device is the CHILD sub-device
    energy = SynSignal(name="energy", func=lambda: 9000.0)

    td = {"waxs_arc": waxs, "energy": energy}
    tmpl = "{waxs_arc:.1f}_{energy:.0f}"

    # 1) plan reads the PARENT; baseline ALSO holds the child (the full SMI shape)
    prim = _primary_events(bp.count([parent], num=2), [waxs], td, tmpl)
    assert len(prim) == 2
    for ev in prim:
        assert list(ev).count("waxs_arc") == 1    # recorded once (via the parent), not doubled
        assert "energy" in ev                      # energy still injected

    # 2) plan reads the CHILD directly while energy token is injected
    prim = _primary_events(bp.count([det, waxs], num=1), [], td, tmpl)
    assert list(prim[0]).count("waxs_arc") == 1
    assert "energy" in prim[0] and "det" in prim[0]


# --------------------------------------------------------------------------- only-referenced reads
def test_only_referenced_devices_are_injected():
    """A template that names only energy must not force a WAXS/SDD read."""
    RE = RunEngine({})
    energy = SynAxis(name="energy")
    waxs = SynAxis(name="waxs")
    token_devices = {"energy": energy, "waxs": waxs}

    RE.preprocessors.append(
        lambda plan: scan_name_preprocessor(
            plan, template="{energy:.1f}eV", token_devices=token_devices, base_name="u")
    )

    cb, names, events = _collect()
    RE(bp.count([det], num=1), cb)
    assert "energy" in events[-1]
    assert "waxs" not in events[-1]  # waxs not referenced -> not read


# --------------------------------------------------------------------------- sanitization of base
def test_base_name_is_sanitized_but_template_braces_preserved():
    RE = RunEngine({})
    energy = SynAxis(name="energy")
    RE.preprocessors.append(
        lambda plan: scan_name_preprocessor(
            plan, template="{energy:.1f}eV", token_devices={"energy": energy},
            base_name="my film 1")
    )
    cb, names, _ = _collect()
    RE(bp.count([det], num=1), cb)
    # spaces in the base -> underscores; the template's braces/colon survive
    assert names[-1] == "my_film_1_{energy:.1f}eV"


# --------------------------------------------------------------------------- multi-point scans
def test_scan_records_tokens_at_every_point(energy_dev, waxs_dev, sdd_dev):
    RE = RunEngine({})
    RE.md["sample_name"] = "u"
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    cb, names, events = _collect()
    m = SynAxis(name="m")
    RE(bp.scan([det], m, 0, 1, 3), cb)
    assert len(events) == 3
    for ev in events:
        assert "energy_energy" in ev and "waxs_arc" in ev and "pil2M_motor_z" in ev


# --------------------------------------------------------------------------- "flux" set (xbpm)
def test_flux_set_extends_template_and_records_sum(make_fake):
    from smi_beamline.devices.electrometers import XBPM
    from smi_beamline.devices.energy import Energy

    en = make_fake(Energy, name="energy", prefix="")
    _seed(en.bragg.user_readback, 12.7)
    _seed(en.harmonic, 7)
    xbpm2 = make_fake(XBPM, name="xbpm2", prefix="XF:12IDA-BI:2{EM:BPM2}")
    _seed(xbpm2.sumX, 1.234)

    RE = RunEngine({})
    RE.md["sample_name"] = "u"
    # activate the optional "flux" set in addition to the energy default
    sn.install_default_scan_naming(RE, energy=en, xbpm2=xbpm2, sets=["energy", "flux"])

    cb, names, events = _collect()
    RE(bp.count([det], num=1), cb)
    assert "xbpm{xbpm2_sumX:.3f}" in names[-1]
    assert "xbpm2_sumX" in events[-1]


def test_enable_disable_set_toggles_live(make_fake):
    """enable_set/disable_set rebuild the installed preprocessor without restart."""
    from smi_beamline.devices.electrometers import XBPM
    from smi_beamline.devices.energy import Energy

    en = make_fake(Energy, name="energy", prefix="")
    _seed(en.bragg.user_readback, 12.7)
    _seed(en.harmonic, 7)
    xbpm2 = make_fake(XBPM, name="xbpm2", prefix="XF:12IDA-BI:2{EM:BPM2}")
    _seed(xbpm2.sumX, 1.234)

    RE = RunEngine({})
    RE.md["sample_name"] = "u"
    ns = {"energy": en, "xbpm2": xbpm2}
    # install with just energy, then turn flux on, then off again
    sn.install_default_scan_naming(RE, ns, sets=["energy"])

    cb, names, events = _collect()
    RE(bp.count([det], num=1), cb)
    assert "xbpm2_sumX" not in events[-1]

    sn.enable_set("flux", RE=RE)  # uses the namespace captured at install
    names.clear(); events.clear()
    RE(bp.count([det], num=1), cb)
    assert "xbpm{xbpm2_sumX:.3f}" in names[-1] and "xbpm2_sumX" in events[-1]
    # exactly one naming preprocessor remains (rebuilt, not stacked)
    assert sum(1 for pp in RE.preprocessors if getattr(pp, "_smi_scan_naming", False)) == 1

    sn.disable_set("flux", RE=RE)
    names.clear(); events.clear()
    RE(bp.count([det], num=1), cb)
    assert "xbpm2_sumX" not in events[-1]


# --------------------------------------------------------------------------- re-install dedup
def test_reinstall_does_not_stack_preprocessors(energy_dev):
    RE = RunEngine({})
    sn.install_default_scan_naming(RE, energy=energy_dev)
    sn.install_default_scan_naming(RE, energy=energy_dev)
    n = sum(1 for pp in RE.preprocessors if getattr(pp, "_smi_scan_naming", False))
    assert n == 1


# --------------------------------------------------------------------------- coexists with decorator
def test_coexists_with_sample_name_decorator(energy_dev, waxs_dev, sdd_dev):
    """sample_name_decorator sets the per-run name inside the plan; the global PP appends to it."""
    from smi_beamline.devices._plan_helpers import sample_name_decorator

    RE = RunEngine({})
    RE.md["sample_name"] = "SMI_user"
    sn.install_default_scan_naming(RE, energy=energy_dev, waxs=waxs_dev, pil2m_pos=sdd_dev)

    @sample_name_decorator("alignment_scan")
    def aligned():
        yield from bp.count([det], num=1)

    cb, names, _ = _collect()
    RE(aligned(), cb)
    # decorator name wins as the base, template appended by the global PP
    assert names[-1] == "alignment_scan_" + sn.DEFAULT_SCAN_NAME_TEMPLATE


# --------------------------------------------------------------------------- skip_if_tokens=False
def test_skip_if_tokens_false_always_appends():
    """With skip_if_tokens=False the default is appended even to a token-bearing user name."""
    RE = RunEngine({})
    energy = SynAxis(name="energy")
    RE.preprocessors.append(
        lambda plan: scan_name_preprocessor(
            plan, template="{energy:.1f}eV", token_devices={"energy": energy},
            base_name=None, skip_if_tokens=False)
    )
    cb, names, _ = _collect()
    RE(bp.count([det], num=1, md={"sample_name": "user_{energy}raw"}), cb)
    # token name is NOT treated as complete -> default appended (and the base is sanitized,
    # which here turns the user's own braces into underscores -- that is the documented
    # consequence of opting out of skip_if_tokens)
    assert names[-1].endswith("_{energy:.1f}eV")
    assert names[-1] != "user_{energy}raw"

