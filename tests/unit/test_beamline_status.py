"""Read-only overview contract, including offline operation and bounded output."""

import re
from types import SimpleNamespace, MethodType
from unittest.mock import Mock

import pytest

from smi_beamline.beamline_status import Reader, show_status, status_rows
from smi_beamline.motor_magics import _color
from smi_beamline.devices.shutter import TwoButtonShutter, FrontEndShutterReadback, SMIFastShutter
from smi_beamline.devices.waxschamber import Sample_Chamber
from smi_beamline.devices.crls import CRL
from smi_beamline.devices.pilatus import Pilatus, SAXS_Detector


def state_device(cls, **attributes):
    """Use real device semantics with strict read-only stand-in signals."""
    device = SimpleNamespace(**attributes)
    for name in ("read_state", "pressure_state", "read_lens_state", "energy_difference", "selected_beamstop_motors"):
        if hasattr(cls, name):
            setattr(device, name, MethodType(getattr(cls, name), device))
    for name in ("status_values", "pumped_below", "vented_above", "inserted_tolerance_mm", "energy_match_tolerance_eV"):
        if hasattr(cls, name):
            setattr(device, name, getattr(cls, name))
    return device


class ReadOnlySignal:
    def __init__(self, value, *, connected=True, units=None, enums=None):
        self.value = value
        self.connected = connected
        self.metadata = {"units": units, "enum_strs": enums}
        self.calls = []

    def get(self, **kwargs):
        assert 0 < kwargs["timeout"] <= 0.15
        assert kwargs["connection_timeout"] == kwargs["timeout"]
        self.calls.append(kwargs)
        return self.value

    def put(self, *args, **kwargs):
        pytest.fail("status must never write")

    set = put
    trigger = put
    read = put


def motor(value, units="mm", done=1):
    return SimpleNamespace(user_readback=ReadOnlySignal(value), motor_egu=ReadOnlySignal(units),
                           motor_done_move=ReadOnlySignal(done))


def valve(value="Open", *, open_val="Open", close_val="Not Open"):
    return state_device(TwoButtonShutter, status=ReadOnlySignal(value), open_val=open_val, close_val=close_val)


@pytest.fixture
def namespace():
    ns = {
        "RE": SimpleNamespace(state="paused"),
        "smi_shutter_enable": ReadOnlySignal(1),
        "mstr_shutter_enable": ReadOnlySignal(0),
        "ph_shutter": valve("Not Open"),
        "fs": state_device(SMIFastShutter, status_pv=ReadOnlySignal(7)),
        "ring": SimpleNamespace(current=ReadOnlySignal(400)),
        "energy": SimpleNamespace(
            energy=SimpleNamespace(readback=ReadOnlySignal(16150)),
            ivugap=motor(7000, "um"), bragg=motor(7, "deg"), dcmgap=motor(10),
            harmonic=ReadOnlySignal(9), pitch_feedback_disabled=ReadOnlySignal("0"),
            roll_feedback_disabled=ReadOnlySignal("1"),
        ),
        "dcm_config": SimpleNamespace(pitch=motor(1, "deg"), roll=motor(2, "deg")),
    }
    for name in ("hfm", "vfm", "vdm"):
        ns[name] = SimpleNamespace(x=motor(1), y=motor(2), th=motor(3, "mrad"))
    for name in ("xbpm2", "xbpm3"):
        ns[name + "_pos"] = SimpleNamespace(x=motor(1.25), y=motor(-2.5))
        ns[name] = SimpleNamespace(sumX=ReadOnlySignal(123.4, units="nA"))
    for bank in (1, 2):
        for i in range(1, 13):
            ns[f"att{bank}_{i}"] = valve("Open" if i % 2 else "Not Open")
    ns["crl"] = state_device(CRL, **{
        **{f"lens{i}": motor(i) for i in range(1, 13)},
        **{axis: motor(0) for axis in ("x", "y", "z", "ph", "th")},
    })
    ns["chamber_pressure"] = state_device(Sample_Chamber,
        waxs=ReadOnlySignal("LO"), maxs=ReadOnlySignal(0.005, units="Torr"),
        upstream_valve=valve(1, open_val="OPENED", close_val="CLOSED"),
        waxs_saxs_valve=valve("Not Open"), turbo_enable=ReadOnlySignal(1),
        det_power=ReadOnlySignal(0),
    )
    ns["chamber_pressure"].upstream_valve.status.metadata["enum_strs"] = ("CLOSED", "OPENED")
    for name in ("piezo", "stage"):
        ns[name] = SimpleNamespace(**{axis: motor(2) for axis in ("x", "y", "z", "th", "ph", "ch")})
    del ns["piezo"].ph
    for name, kev in (("pil900KW", 16.15), ("pil2M", 15)):
        ns[name] = state_device(SAXS_Detector if name == "pil2M" else Pilatus, cam=SimpleNamespace(
            detector_state=ReadOnlySignal(0, enums=("Idle", "Acquire", "Error")),
            acquire_time=ReadOnlySignal(0.5), num_images=ReadOnlySignal(3),
            cam_energy=ReadOnlySignal(kev), threshold_energy=ReadOnlySignal(8),
        ))
    ns["pil2M"].active_beamstop = ReadOnlySignal("rod")
    ns["pil2M"].beamstop = SimpleNamespace(x_rod=motor(6.8), y_rod=motor(0),
                                         x_pin=motor(-227), y_pin=motor(6.8))
    ns["attenuation"] = SimpleNamespace(read_state=Mock(return_value={
        "attenuation_factor": 20, "transmission": 0.05,
        "energy_eV": 16150, "inserted": ["1_3", "2_5"],
    }))
    return ns


def test_overview_units_states_and_order(namespace):
    rows = status_rows(namespace)
    data = {label: {f.label: f.value for f in fields} for label, fields in rows}
    assert data["Hutch A"] == {"FE": "N/A"}
    assert data["Hutch B"] == {"photon": "NOT OPEN"}
    assert data["Hutch C"] == {"fast": "NOT OPEN"}
    assert data["Accelerator / FE"] == {"ring": "400.0 mA", "IVU gap": "7000.0 um", "FE permit": "ENABLED"}
    assert data["HFM"]["pitch"] == "3.000 mrad"
    assert data["xbpm2"] == {"x": "1.250 mm", "y": "-2.500 mm", "sumX": "123.4 nA"}
    assert data["xbpm3"] == data["xbpm2"]
    assert "DCM feedback" not in data
    assert data["Foils IN"][""] == "1_3,2_5"
    assert data["Attenuation"]["factor"] == "20x"
    assert data["CRLs IN"][""] == "1, 2"
    assert data["SAXS beamstop"] == {"selected": "rod", "x": "6.800 mm", "y": "0.000 mm"}
    assert "pitch" not in data["DCM motors"]
    assert data["Sample vacuum"]["WAXS"] == "LO raw"
    assert data["Sample vacuum"]["MAXS"] == "5.00e-03 Torr"
    assert data["Sample vacuum"]["upstream"] == "OPEN"
    assert data["piezo angles"]["ph"] == "N/A"
    assert data["stage XYZ"]["x"] == "2.000 mm"
    assert data["pil2M energy"]["energy"] == "15000.0 eV"
    assert data["pil2M energy"]["threshold"] == "8000.0 eV"
    assert data["pil2M energy"]["delta E"] == "MISMATCH -1150.0 eV"
    assert data["pil900KW"]["state"] == "Idle"
    labels = [label for label, fields in rows]
    ordered = ["Accelerator / FE", "Hutch A", "WBS slits", "Monochromator", "HFM", "VFM", "VDM", "xbpm2",
               "Hutch B", "SSA slits", "xbpm3", "Hutch C", "ESLIT slits",
               "Attenuation", "CRLs IN", "CSLIT slits", "Sample vacuum", "piezo XYZ", "pil900KW", "pil2M"]
    assert [labels.index(label) for label in ordered] == sorted(labels.index(label) for label in ordered)


@pytest.mark.parametrize("empty", [False, True])
def test_compact_aligned_display(namespace, capsys, monkeypatch, empty):
    monkeypatch.delenv("NO_COLOR", raising=False)
    shell = SimpleNamespace(user_ns={} if empty else namespace, colors="linux")
    show_status(shell, _color)
    colored = capsys.readouterr().out
    plain = re.sub(r"\x1b\[[0-9;]*m", "", colored)
    lines = plain.splitlines()
    assert len(lines) == 36
    assert max(map(len, lines)) <= 132
    accelerator = next(line for line in lines if "Accelerator / FE" in line)
    if not empty:
        assert "400.0 mA" in accelerator
        assert "FE permit" in accelerator and "ENABLED" in accelerator
    else:
        assert accelerator.count("N/A") == 3
    box = [line for line in lines if line.startswith(("│", "┌", "└", "├"))]
    assert len(set(map(len, box))) == 1
    assert "\033[93m" in colored
    if not empty:
        assert "\033[1;91mMISMATCH" in colored
    monkeypatch.setenv("NO_COLOR", "1")
    show_status(shell, _color)
    assert "\033[" not in capsys.readouterr().out


def test_offline_timeout_budget_and_caching():
    signal = ReadOnlySignal(5)
    reader = Reader({"value": signal})
    assert reader.get("value") == reader.get("value") == 5
    assert len(signal.calls) == 1
    offline = ReadOnlySignal(0, connected=False)
    with pytest.raises(ConnectionError):
        Reader({"value": offline}).get("value")
    assert not offline.calls
    deferred = ReadOnlySignal(0)
    with pytest.raises(TimeoutError, match="BUDGET"):
        Reader({"value": deferred}, budget=0).get("value")
    assert not deferred.calls
    signal = Mock(connected=True)
    signal.get.side_effect = TimeoutError("offline")
    reader = Reader({"value": signal})
    for _ in range(2):
        with pytest.raises(TimeoutError):
            reader.get("value")
    signal.get.assert_called_once()


def test_unknown_shutter_does_not_guess_polarity(namespace):
    namespace["fs"].status_pv.value = 5
    namespace["ph_shutter"].status.value = 1  # no enum metadata
    data = {label: {f.label: f.value for f in fields} for label, fields in status_rows(namespace)}
    assert data["Hutch C"]["fast"] == "UNKNOWN(5)"
    assert data["Hutch B"]["photon"] == "UNKNOWN(1)"


def test_crl_boundaries_and_unknowns(namespace):
    for i, value in enumerate((-3, -2.999, 0, 2.999, 3, float("nan")), 1):
        namespace["crl"].__dict__[f"lens{i}"] = motor(value)
    rows = dict(status_rows(namespace))
    assert rows["CRLs IN"][0].value == "2, 3, 4; UNKNOWN: 6"


@pytest.mark.parametrize("selected", ["pin", "pin_removed", "none"])
def test_selected_beamstop(namespace, selected):
    namespace["pil2M"].active_beamstop.value = selected
    fields = {f.label: f.value for f in dict(status_rows(namespace))["SAXS beamstop"]}
    assert fields["selected"] == selected
    assert fields["x"] == ("N/A" if selected == "none" else "-227.000 mm")


def test_status_numbers_and_text_have_consistent_colors(namespace, capsys, monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    show_status(SimpleNamespace(user_ns=namespace, colors="linux"), _color)
    output = capsys.readouterr().out
    assert "\033[94m1.000\033[0m" in output
    assert "\033[94m2.000\033[0m" in output
    assert "\033[94m3.000\033[0m" in output
    assert "\033[1;91m[ Fast shutter: CLOSED ]" in output
    assert "\033[92mIdle\033[0m" in output
    assert "\033[94m3.000\033[0m mrad" in output
    assert "\033[95m" not in output


@pytest.mark.parametrize("value,expected", [(7, "NOT OPEN"), (7.0, "NOT OPEN"), ("7", "NOT OPEN"),
                                            ("7.0", "NOT OPEN"), (0.0, "OPEN"), (3, "UNKNOWN(3)")])
def test_fast_shutter_numeric_mapping_overrides_enum_metadata(namespace, value, expected):
    namespace["fs"].status_pv.value = value
    namespace["fs"].status_pv.metadata["enum_strs"] = tuple(str(i) for i in range(8))
    data = {f.label: f.value for f in dict(status_rows(namespace))["Hutch C"]}
    assert data["fast"] == expected


@pytest.mark.parametrize("value,expected", [(0, "OPEN"), (1, "NOT OPEN"), (1.0, "NOT OPEN"), (2, "UNKNOWN(2)")])
def test_front_end_closed_status_bit(namespace, value, expected):
    namespace["fe_shutter"] = state_device(FrontEndShutterReadback, status=ReadOnlySignal(value))
    data = {f.label: f.value for f in dict(status_rows(namespace))["Hutch A"]}
    assert data["FE"] == expected


def test_open_and_unknown_hutch_openings(namespace, capsys, monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    namespace["fe_shutter"] = state_device(FrontEndShutterReadback, status=ReadOnlySignal(0))
    namespace["fs"].status_pv.value = 5
    show_status(SimpleNamespace(user_ns=namespace, colors="linux"), _color)
    output = capsys.readouterr().out
    assert "\033[1;92m[ FE shutter: OPEN ]" in output
    assert "\033[1;91m[ Photon shutter: CLOSED ]" in output
    assert "\033[1;93m[ Fast shutter: UNKNOWN(5) ]" in output


@pytest.mark.parametrize("value,expected", [
    (7001, "Vented"), (7000, "7.00e+03 Torr"),
    (0.0049, "Pumped"), (0.005, "5.00e-03 Torr"), (1, "1.00e+00 Torr"),
])
def test_pressure_state_thresholds(namespace, value, expected):
    namespace["chamber_pressure"].maxs.value = value
    fields = {f.label: f.value for f in dict(status_rows(namespace))["Sample vacuum"]}
    assert fields["MAXS"] == expected


def test_pressure_state_colors(namespace, capsys, monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    namespace["chamber_pressure"].maxs.value = 10000
    namespace["chamber_pressure"].waxs.value = 0.001
    show_status(SimpleNamespace(user_ns=namespace, colors="linux"), _color)
    output = capsys.readouterr().out
    assert "\033[91mVented\033[0m" in output
    assert "\033[92mPumped\033[0m" in output


def test_long_ioc_strings_cannot_break_layout(namespace, capsys):
    namespace["pil2M"].cam.detector_state.value = "Error\n" + "X" * 500
    show_status(SimpleNamespace(user_ns=namespace, colors="nocolor"), _color)
    output = capsys.readouterr().out
    assert "…" in output
    assert max(map(len, output.splitlines())) <= 132
