import copy
from types import SimpleNamespace

import pytest
from ophyd import Signal
from bluesky import RunEngine
import bluesky.plan_stubs as bps

from smi_beamline.plans import beam_snapshot


class _Motor:
    def __init__(self, name, value):
        self.name = name
        self.parent = None
        self.prefix = name.upper()
        self.user_readback = Signal(value=value, name=name + "_rb")
        self.user_setpoint = Signal(value=value, name=name + "_sp")
        self.user_offset = Signal(value=0.0, name=name + "_off")
        self.low_limit = Signal(value=-1000.0, name=name + "_llm")
        self.high_limit = Signal(value=1000.0, name=name + "_hlm")
        self.velocity = Signal(value=2.5, name=name + "_velo")
        self.motor_egu = Signal(value="mm", name=name + "_egu")

    def set(self, value):
        return self.user_setpoint.set(value)


class _Device:
    pass


def _slit(prefix, start=0):
    dev = _Device()
    for i, axis in enumerate(("h", "hg", "v", "vg")):
        setattr(dev, axis, _Motor(prefix + "_" + axis, start + i))
    return dev


def _mirror(prefix, start=0):
    dev = _Device()
    for i, axis in enumerate(("x", "y", "th")):
        setattr(dev, axis, _Motor(prefix + "_" + axis, start + i))
    return dev


def _xbpm(prefix, start=0):
    dev = _Device()
    dev.x = _Motor(prefix + "_x", start)
    dev.y = _Motor(prefix + "_y", start + 1)
    return dev


def _voltage(prefix):
    dev = _Device()
    dev.name = prefix
    for i in range(beam_snapshot.N_BIMORPH_CH):
        setattr(dev, "ch{}".format(i), Signal(value=float(i), name="{}_ch{}".format(prefix, i)))
        setattr(dev, "ch{}_trg".format(i), Signal(value=float(i), name="{}_trg_write{}".format(prefix, i)))
        setattr(dev, "ch{}_trg_rb".format(i), Signal(value=float(i), name="{}_trg{}".format(prefix, i)))
        setattr(dev, "ch{}_status".format(i), Signal(value="On", name="{}_status{}".format(prefix, i)))

    def read_outputs():
        return [getattr(dev, "ch{}".format(i)).get() for i in range(beam_snapshot.N_BIMORPH_CH)]

    def set_targets(voltages):
        for i, value in enumerate(voltages):
            getattr(dev, "ch{}_trg".format(i)).put(value)
            getattr(dev, "ch{}_trg_rb".format(i)).put(value)
        yield from bps.null()

    def apply_and_wait():
        for i in range(beam_snapshot.N_BIMORPH_CH):
            getattr(dev, "ch{}".format(i)).put(getattr(dev, "ch{}_trg_rb".format(i)).get())
        yield from bps.null()

    dev.read_outputs = read_outputs
    dev.set_targets = set_targets
    dev.apply_and_wait = apply_and_wait
    return dev


def _namespace():
    energy = _Device()
    energy.energy = _Device()
    energy.energy.readback = Signal(name="energy_readback", value=10000.0)
    energy.pitch_feedback_disabled = Signal(name="pitch_feedback_disabled", value="0")
    energy.roll_feedback_disabled = Signal(name="roll_feedback_disabled", value="0")
    energy.bragg = _Motor("bragg", 1.0)
    energy.dcmgap = _Motor("dcmgap", 2.0)
    energy.ivugap = _Motor("ivugap", 3.0)
    dcm_config = _Device()
    dcm_config.pitch = _Motor("dcm_pitch", 4.0)
    dcm_config.roll = _Motor("dcm_roll", 5.0)
    xbpm3 = _Device()
    xbpm3.range = Signal(name="xbpm3_range", value=3)
    return {
        "mdsave": {},
        "wbs": _slit("wbs"),
        "ssa": _slit("ssa"),
        "eslit": _slit("eslit"),
        "cslit": _slit("cslit"),
        "energy": energy,
        "dcm_config": dcm_config,
        "xbpm3": xbpm3,
        "ph_shutter": Signal(name="ph_shutter", value="Open"),
        "xbpm2_pos": _xbpm("xbpm2"),
        "xbpm3_pos": _xbpm("xbpm3"),
        "hfm": _mirror("hfm"),
        "vfm": _mirror("vfm"),
        "vdm": _mirror("vdm"),
        "hfm_voltage": _voltage("hfm_voltage"),
        "vfm_voltage": _voltage("vfm_voltage"),
    }


def test_beam_snapshot_saves_to_mdsave_and_indexes():
    ns = _namespace()
    snapshot = beam_snapshot.save_beam_position_snapshot(
        "test", note="unit", namespace=ns, store=ns["mdsave"])

    assert snapshot["snapshot_name"] == "test"
    assert len(snapshot["items"]) == 68
    assert "beam_position_snapshots:test" in ns["mdsave"]
    assert ns["mdsave"]["beam_position_snapshots:index"]["test"]["count"] == 68

    names = {item["name"] for item in snapshot["items"]}
    assert "energy.bragg" in names
    assert "xbpm2_pos.x" in names
    assert "hfm_voltage.ch15" in names
    assert "hfmslit.h" not in names
    assert "energy.dcmx" not in names
    assert next(item for item in snapshot["items"] if item["name"] == "wbs.h")["speed"] == 2.5


def test_beam_snapshot_compare_is_dry_run_and_reports_diff():
    ns = _namespace()
    beam_snapshot.save_beam_position_snapshot("test", namespace=ns, store=ns["mdsave"])
    ns["wbs"].h.user_readback.put(10.0)

    rows = beam_snapshot.compare_beam_position_snapshot(
        "test", namespace=ns, store=ns["mdsave"], print_table=False)

    row = next(row for row in rows if row["name"] == "wbs.h")
    assert row["status"] == "would move"
    assert row["current"] == 10.0
    assert row["snapshot"] == 0


def test_beam_snapshot_voltage_diff_is_restorable():
    ns = _namespace()
    beam_snapshot.save_beam_position_snapshot("test", namespace=ns, store=ns["mdsave"])
    ns["vfm_voltage"].ch0.put(99.0)

    rows = beam_snapshot.compare_beam_position_snapshot(
        "test", namespace=ns, store=ns["mdsave"], print_table=False)

    row = next(row for row in rows if row["name"] == "vfm_voltage.ch0")
    assert row["status"] == "would move"


def test_beam_snapshot_restore_defaults_to_dry_run():
    ns = _namespace()
    beam_snapshot.save_beam_position_snapshot("test", namespace=ns, store=ns["mdsave"])
    ns["wbs"].h.user_readback.put(10.0)

    rows = beam_snapshot.restore_beam_position_snapshot(
        "test", namespace=ns, store=ns["mdsave"], names=["wbs.h"], print_table=False)

    assert rows == [
        {
            "name": "wbs.h",
            "group": "slits",
            "target": 0,
            "current": 10.0,
            "units": "mm",
            "status": "would move",
            "delta": -10.0,
        }
    ]


def test_beam_snapshot_restore_moves_selected_motor_when_enabled():
    ns = _namespace()
    RE = RunEngine({})
    beam_snapshot.save_beam_position_snapshot("test", namespace=ns, store=ns["mdsave"])
    ns["wbs"].h.user_readback.put(10.0)
    ns["wbs"].v.user_readback.put(20.0)

    RE(beam_snapshot.restore_beam_position_snapshot(
        "test", namespace=ns, store=ns["mdsave"], names=["wbs.h"], dry_run=False,
        print_table=False))

    assert ns["wbs"].h.user_setpoint.get() == 0
    assert ns["wbs"].v.user_setpoint.get() == 2


@pytest.mark.parametrize("debug", [False, True])
def test_beam_snapshot_restore_moves_selected_bimorph_channel_when_enabled(debug):
    ns = _namespace()
    RE = RunEngine({})
    beam_snapshot.save_beam_position_snapshot("test", namespace=ns, store=ns["mdsave"])
    ns["hfm_voltage"].ch0.put(99.0)
    ns["hfm_voltage"].ch1.put(88.0)
    calls = []
    dev = ns["hfm_voltage"]
    original_stage = dev.set_targets
    original_apply = dev.apply_and_wait

    def stage(targets, **kwargs):
        calls.append(("stage", kwargs))
        yield from original_stage(targets)

    def apply(**kwargs):
        calls.append(("apply", kwargs))
        yield from original_apply()

    dev.set_targets = stage
    dev.apply_and_wait = apply

    RE(beam_snapshot.restore_beam_position_snapshot(
        "test", namespace=ns, store=ns["mdsave"], names=["hfm_voltage.ch0"],
        dry_run=False, print_table=False, bimorph_debug=debug))

    assert ns["hfm_voltage"].ch0.get() == 0.0
    assert ns["hfm_voltage"].ch1.get() == 88.0
    assert ns["hfm_voltage"].ch1_trg_rb.get() == 88.0
    options = {"debug": True} if debug else {}
    assert calls == [("stage", options), ("apply", options)]


@pytest.mark.parametrize("legacy", [False, True])
def test_xbpm_positions_restore_and_compare_including_old_snapshots(legacy):
    ns = _namespace()
    snapshot = beam_snapshot.save_beam_position_snapshot("test", namespace=ns)
    names = ["xbpm2_pos.x", "xbpm2_pos.y", "xbpm3_pos.x", "xbpm3_pos.y"]
    for item in snapshot["items"]:
        if item["name"] in names:
            assert item["restore"] is True
            if legacy:
                item["restore"] = False
            dev, axis = item["name"].split(".")
            motor = getattr(ns[dev], axis)
            motor.user_readback.put(20.0)
            motor.user_setpoint.put(20.0)
    original = copy.deepcopy(snapshot)

    compared = beam_snapshot.compare_beam_position_snapshot(
        snapshot, namespace=ns, print_table=False)
    assert all(row["status"] == "would move" for row in compared if row["name"] in names)
    dry_rows = beam_snapshot.restore_beam_position_snapshot(
        snapshot, namespace=ns, names=names, groups=["diagnostics"], print_table=False)
    assert {row["name"] for row in dry_rows} == set(names)
    assert all(row["status"] == "would move" for row in dry_rows)

    RE = RunEngine({}, call_returns_result=True)
    result = RE(beam_snapshot.restore_beam_position_snapshot(
        snapshot, namespace=ns, names=names, groups=["diagnostics"], dry_run=False, print_table=False))
    assert all(row["status"] == "moved" for row in result.plan_result)
    for dev in ("xbpm2_pos", "xbpm3_pos"):
        assert ns[dev].x.user_setpoint.get() == 0
        assert ns[dev].y.user_setpoint.get() == 1
    assert snapshot == original


def test_restore_starts_each_motor_batch_before_waiting_and_keeps_read_only_axes():
    ns = _namespace()
    snapshot = beam_snapshot.save_beam_position_snapshot("test", namespace=ns)
    for item in snapshot["items"]:
        if item["kind"] == "motor":
            dev, axis = item["name"].split(".")
            motor = getattr(ns[dev], axis)
            motor.user_readback.put(50.0)
            motor.user_setpoint.put(50.0)

    messages = []
    RE = RunEngine({}, call_returns_result=True)
    RE.msg_hook = messages.append
    result = RE(beam_snapshot.restore_beam_position_snapshot(
        snapshot, namespace=ns, dry_run=False, print_table=False))

    # All sets in a batch must precede its wait, and share that wait's group.
    batches = []
    pending = []
    for msg in messages:
        if msg.command == "set":
            pending.append(msg)
        elif msg.command == "wait":
            assert pending
            assert all(move.kwargs["group"] == msg.kwargs["group"] for move in pending)
            batches.append({move.obj.name for move in pending})
            pending = []
    assert not pending
    assert batches == [
        {"pitch_feedback_disabled", "roll_feedback_disabled"},
        {"ph_shutter"},
        {"dcm_pitch", "dcm_roll"},
        {dev + "_" + axis for dev in ("wbs", "ssa", "eslit", "cslit") for axis in ("h", "v")},
        {dev + "_" + axis for dev in ("wbs", "ssa", "eslit", "cslit") for axis in ("hg", "vg")},
        {dev + "_" + axis for dev in ("hfm", "vfm", "vdm") for axis in ("x", "y")},
        {dev + "_th" for dev in ("hfm", "vfm", "vdm")},
        {dev + "_" + axis for dev in ("xbpm2", "xbpm3") for axis in ("x", "y")},
    ]
    rows = {row["name"]: row for row in result.plan_result}
    for item in snapshot["items"]:
        if item["kind"] != "motor":
            continue
        dev, axis = item["name"].split(".")
        if item["restore"]:
            assert getattr(ns[dev], axis).user_setpoint.get() == item["readback"]
            assert rows[item["name"]]["status"] == "moved"
        else:
            assert getattr(ns[dev], axis).user_setpoint.get() == 50.0
            assert rows[item["name"]]["status"] == "skipped read-only"


def test_batched_restore_respects_selection_exclusions_and_tolerance():
    ns = _namespace()
    snapshot = beam_snapshot.save_beam_position_snapshot("test", namespace=ns)
    names = ["wbs.h", "wbs.hg", "ssa.h", "ssa.v", "hfm.x", "xbpm2_pos.x"]
    for name in names:
        dev, axis = name.split(".")
        motor = getattr(ns[dev], axis)
        motor.user_readback.put(50.0)
        motor.user_setpoint.put(50.0)
    ns["ssa"].v.user_readback.put(2.01)
    messages = []
    RE = RunEngine({}, call_returns_result=True)
    RE.msg_hook = messages.append
    result = RE(beam_snapshot.restore_beam_position_snapshot(
        snapshot, namespace=ns, names=names, groups=["slits", "diagnostics"],
        exclude=["ssa.h"], tolerance=0.1, dry_run=False, print_table=False))

    assert [msg.obj.name for msg in messages if msg.command == "set"] == [
        "pitch_feedback_disabled", "roll_feedback_disabled", "ph_shutter",
        "wbs_h", "wbs_hg", "xbpm2_x"]
    assert sum(msg.command == "wait" for msg in messages) == 5
    rows = {row["name"]: row for row in result.plan_result}
    assert set(rows) == {"wbs.h", "wbs.hg", "ssa.v", "xbpm2_pos.x"}
    assert rows["ssa.v"]["status"] == "already there"


def test_energy_restore_records_harmonic_with_feedback_off_before_gain():
    ns = _namespace()
    en = ns["energy"]
    en.enabledcmgap = Signal(name="enabledcmgap", value=True)
    en.enableivu = Signal(name="enableivu", value=True)
    en.harmonic = Signal(name="harmonic", value=7)
    en.PseudoPosition = SimpleNamespace
    en._harmonic_and_gap = lambda value: (5, 8000.0)
    def forward(pos):
        assert pos.energy == 10000
        assert en.pitch_feedback_disabled.get() == "1"
        assert en.roll_feedback_disabled.get() == "1"
        assert ns["ph_shutter"].get() == "Close"
        return SimpleNamespace(bragg=11.0, dcmgap=12.0, ivugap=8000.0)
    en.forward = forward
    snapshot = beam_snapshot.save_beam_position_snapshot("test", namespace=ns)
    en.energy.readback.put(9000)
    ns["xbpm3"].range.put(4)
    engine = RunEngine({})
    messages = []
    engine.msg_hook = messages.append
    engine(beam_snapshot.restore_beam_position_snapshot(
        snapshot, namespace=ns, dry_run=False, print_table=False,
        names=["energy.energy", "xbpm3.range"], tolerance=2))
    assert [msg.obj.name for msg in messages if msg.command == "set"] == [
        "pitch_feedback_disabled", "roll_feedback_disabled", "ph_shutter",
        "bragg", "dcmgap", "ivugap", "harmonic", "xbpm3_range"]
    assert en.harmonic.get() == 5
    assert en.ivugap.user_setpoint.get() == 8000
    assert ns["xbpm3"].range.get() == 3  # enum change is not swallowed by tolerance
    assert en.pitch_feedback_disabled.get() == "1"
    assert en.roll_feedback_disabled.get() == "1"
    assert ns["ph_shutter"].get() == "Close"
