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
    energy.bragg = _Motor("bragg", 1.0)
    energy.dcmgap = _Motor("dcmgap", 2.0)
    energy.ivugap = _Motor("ivugap", 3.0)
    dcm_config = _Device()
    dcm_config.pitch = _Motor("dcm_pitch", 4.0)
    dcm_config.roll = _Motor("dcm_roll", 5.0)
    return {
        "mdsave": {},
        "wbs": _slit("wbs"),
        "ssa": _slit("ssa"),
        "eslit": _slit("eslit"),
        "cslit": _slit("cslit"),
        "energy": energy,
        "dcm_config": dcm_config,
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
    assert len(snapshot["items"]) == 66
    assert "beam_position_snapshots:test" in ns["mdsave"]
    assert ns["mdsave"]["beam_position_snapshots:index"]["test"]["count"] == 66

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


def test_beam_snapshot_restore_moves_selected_bimorph_channel_when_enabled():
    ns = _namespace()
    RE = RunEngine({})
    beam_snapshot.save_beam_position_snapshot("test", namespace=ns, store=ns["mdsave"])
    ns["hfm_voltage"].ch0.put(99.0)
    ns["hfm_voltage"].ch1.put(88.0)

    RE(beam_snapshot.restore_beam_position_snapshot(
        "test", namespace=ns, store=ns["mdsave"], names=["hfm_voltage.ch0"],
        dry_run=False, print_table=False))

    assert ns["hfm_voltage"].ch0.get() == 0.0
    assert ns["hfm_voltage"].ch1.get() == 88.0
    assert ns["hfm_voltage"].ch1_trg_rb.get() == 88.0
