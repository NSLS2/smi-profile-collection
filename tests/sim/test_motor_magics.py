"""Exercise actual IPython parsing and RE moves, without beamline startup."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from bluesky import RunEngine
from bluesky import plan_stubs as bps
from IPython.core.error import UsageError
from IPython.core.interactiveshell import InteractiveShell
from ophyd import Signal, SoftPositioner
from ophyd.sim import SynAxis, SynSignal
from ophyd.utils.errors import LimitError
from traitlets.config import Config

from smi_beamline.motor_magics import load_ipython_extension


AXES = ("x", "y", "z", "th", "ph", "ch")


@pytest.fixture
def console():
    ns = {"RE": RunEngine({}, context_managers=[])}
    for device in ("piezo", "stage"):
        ns[device] = SimpleNamespace(**{
            axis: SynAxis(name=f"{device}_{axis}", value=10) for axis in AXES
        })
    for name in ("pil2M", "pil900KW"):
        detector = SynSignal(name=name, func=lambda: 1)
        detector.cam = SimpleNamespace(
            acquire_time=Signal(name=name + "_time", value=0.1),
            acquire_period=Signal(name=name + "_period", value=0.101),
            num_images=Signal(name=name + "_images", value=3),
            cam_energy=Signal(name=name + "_energy", value=16.15),
        )
        ns[name] = detector
    ns["det_exposure_time"] = Mock(side_effect=lambda *args: bps.null())
    shell = InteractiveShell(
        user_ns=ns, config=Config({"HistoryManager": {"hist_file": ":memory:"}})
    )
    load_ipython_extension(shell)
    yield shell
    shell.history_manager.end_session()


@pytest.mark.parametrize("axis", AXES)
@pytest.mark.parametrize("prefix,device", [("", "piezo"), ("s", "stage")])
def test_moves_and_automagic(console, axis, prefix, device):
    command = prefix + axis
    assert command not in console.user_ns
    result = console.run_cell(f"{command} -1.25e0")
    assert result.success
    assert getattr(console.user_ns[device], axis).position == pytest.approx(8.75)
    result = console.run_cell(f"%{command} a 2.5")
    assert result.success
    assert getattr(console.user_ns[device], axis).position == pytest.approx(2.5)
    # Only the selected device/axis moved.
    for other_device in ("piezo", "stage"):
        for other_axis in AXES:
            if (other_device, other_axis) != (device, axis):
                assert getattr(console.user_ns[other_device], other_axis).position == 10


@pytest.mark.parametrize("line", [
    "a", "a 1 2", "1 2", "r 2", "NaN", "inf", "-inf", "1e999",
    "a nan", "1+2", "1 mm", "1 # comment", "1; sx 2", "$distance",
    "{side_effect()}",
])
def test_invalid_input_never_calls_re(console, line):
    re = Mock(state="idle")
    side_effect = Mock(return_value=1)
    console.user_ns.update(RE=re, distance=1, side_effect=side_effect)
    result = console.run_cell(f"%x {line}")
    assert isinstance(result.error_in_exec, UsageError)
    re.assert_not_called()
    side_effect.assert_not_called()


@pytest.mark.parametrize("line", ["%x", "%x --help", "%x?", "x"])
def test_help_never_moves(console, line):
    re = Mock(state="idle")
    console.user_ns["RE"] = re
    assert console.run_cell(line).success
    re.assert_not_called()


def test_shadowing_and_registration_preserve_variables(console):
    console.user_ns["x"] = "user data"
    load_ipython_extension(console)
    assert console.user_ns["x"] == "user data"
    assert console.run_cell("%x 1").success
    assert console.user_ns["piezo"].x.position == 11
    # IPython gives variables precedence over bare magics.
    assert not console.run_cell("x 1").success
    assert console.user_ns["piezo"].x.position == 11
    assert console.run_cell("del x").success
    assert console.run_cell("x 1").success
    assert console.user_ns["piezo"].x.position == 12


@pytest.mark.parametrize("state", ["running", "paused", "aborting"])
def test_busy_re_is_rejected(console, state):
    re = Mock(state=state)
    console.user_ns["RE"] = re
    result = console.run_cell("%sx 1")
    assert isinstance(result.error_in_exec, UsageError)
    assert "must be idle" in str(result.error_in_exec)
    re.assert_not_called()


@pytest.mark.parametrize("missing", ["RE", "piezo", "ph"])
def test_missing_session_objects(console, missing):
    if missing == "ph":
        del console.user_ns["piezo"].ph
    else:
        del console.user_ns[missing]
    result = console.run_cell("%ph 1")
    assert isinstance(result.error_in_exec, UsageError)


@pytest.mark.parametrize("source", [
    "def jog():\n    %x 1\njog()",
    "def jog():\n    get_ipython().run_line_magic('x', '1')\njog()",
    "def plan():\n    %x 1\n    yield\nnext(plan())",
    "def plan():\n    %x 1\n    yield\nRE(plan())",
])
def test_nested_commands_are_rejected(console, source):
    result = console.run_cell(source)
    assert isinstance(result.error_in_exec, UsageError)
    assert "standalone" in str(result.error_in_exec)
    assert console.user_ns["piezo"].x.position == 10


@pytest.mark.parametrize("line", ["%x a 1000", "%x 11"])
def test_device_limits_and_errors_propagate(console, line):
    motor = SoftPositioner(name="limited_x", init_pos=10, limits=(-20, 20))
    console.user_ns["piezo"].x = motor
    result = console.run_cell(line)
    assert isinstance(result.error_in_exec, LimitError)
    assert "not within limits" in str(result.error_in_exec)
    assert motor.position == 10
    assert console.user_ns["RE"].state == "idle"


def test_worker_registration_is_rejected(console):
    console.user_ns["IS_QS_WORKER"] = True
    with pytest.raises(UsageError, match="QueueServer"):
        load_ipython_extension(console)


def test_extension_manager_loading(console):
    console.extension_manager.load_extension("smi_beamline.motor_magics")
    assert console.run_cell("sx 0.001").success
    assert console.user_ns["stage"].x.position == pytest.approx(10.001)


@pytest.mark.parametrize("axis", AXES)
@pytest.mark.parametrize("style,device", [("piezo", "piezo"), ("prefix", "stage"), ("suffix", "stage")])
@pytest.mark.parametrize("relative", [False, True])
def test_scans_record_positions_and_restore_relative(console, axis, style, device, relative):
    stem = axis if style == "piezo" else ("s" + axis if style == "prefix" else axis + "s")
    command = stem + ("rscan" if relative else "scan")
    documents = []
    console.user_ns["RE"].subscribe(lambda name, doc: documents.append((name, doc)))
    args = "2 3" if relative else "-2 2 3"
    assert console.run_cell(f"{command} {args}").success
    events = [doc for name, doc in documents if name == "event"]
    expected = [8, 10, 12] if relative else [-2, 0, 2]
    assert [event["data"][f"{device}_{axis}"] for event in events] == expected
    assert all("pil2M" in event["data"] and "pil900KW" not in event["data"] for event in events)
    assert getattr(console.user_ns[device], axis).position == (10 if relative else 2)


@pytest.mark.parametrize("command,names", [
    ("snaps", ["pil2M"]), ("snapw", ["pil900KW"]), ("snapsw", ["pil2M", "pil900KW"]),
])
def test_snapshot_detectors_and_run_metadata(console, command, names):
    re = console.user_ns["RE"]
    re.md["sample_name"] = "original sample"
    documents = []
    re.subscribe(lambda name, doc: documents.append((name, doc)))
    assert console.run_cell(command).success
    start = next(doc for name, doc in documents if name == "start")
    assert start["sample_name"] == "snapshot"
    events = [doc for name, doc in documents if name == "event"]
    assert len(events) == 1
    assert set(events[0]["data"]) == set(names)
    assert re.md["sample_name"] == "original sample"


@pytest.mark.parametrize("args,expected", [("0.5", (0.5, 0.5)), ("0.5 2", (0.5, 2))])
def test_exposure_plan_dispatch_and_readback(console, capsys, args, expected):
    # Different actual readbacks demonstrate that output is read from detectors,
    # rather than inferred from arguments passed to the existing exposure plan.
    console.user_ns["pil900KW"].cam.acquire_time.put(0.25)
    console.user_ns["pil900KW"].cam.num_images.put(7)
    assert console.run_cell(f"exp {args}").success
    console.user_ns["det_exposure_time"].assert_called_once_with(*expected)
    output = capsys.readouterr().out
    assert "pil2M" in output and "pil900KW" in output
    assert "0.25" in output and "7" in output and "Images/trigger" in output


@pytest.mark.parametrize("line", [
    "xscan 1 2", "xscan 1 2 1", "xscan 1 2 3.5", "xscan nan 2 3", "xscan 1 inf 3",
    "xrscan -1 3", "xrscan 0 3", "xrscan 2 0", "xrscan 1e999 3", "xrscan 1 3 extra",
    "exp 0", "exp -1", "exp 1 0.5", "exp nan", "exp 1 inf", "exp 1 2 3",
    "exp 1e-300 1e300", "wh extra", "snaps 1", "snapw extra", "snapsw 2",
])
def test_invalid_new_commands_never_call_re(console, line):
    re = Mock(state="idle")
    console.user_ns["RE"] = re
    result = console.run_cell("%" + line)
    assert isinstance(result.error_in_exec, UsageError)
    re.assert_not_called()
    console.user_ns["det_exposure_time"].assert_not_called()


@pytest.mark.parametrize("command", ["x", "xscan", "xrscan", "xsscan", "syscan", "wh", "exp", "snaps", "snapw", "snapsw"])
@pytest.mark.parametrize("args", ["?", "123 ?", "--help"])
def test_help_for_all_commands_never_reads_or_executes(console, capsys, command, args):
    re = Mock(state="idle")
    console.user_ns["RE"] = re
    # Help should not require any live devices.
    for name in ("piezo", "stage", "pil2M", "pil900KW"):
        del console.user_ns[name]
    assert console.run_cell(f"%{command} {args}").success
    assert f"%{command}" in capsys.readouterr().out
    re.assert_not_called()


@pytest.mark.parametrize("command", ["x", "wh", "exp"])
def test_readouts_without_re(console, capsys, command):
    del console.user_ns["RE"]
    assert console.run_cell(command).success
    output = capsys.readouterr().out
    assert "┌" in output and "└" in output
    if command != "exp":
        assert "10.0000 um" in output
    if command == "wh":
        assert "10.0000 mm" in output and "10.0000 deg" in output


def test_wh_missing_axis_preserves_other_readouts(console, capsys):
    del console.user_ns["piezo"].ph
    assert console.run_cell("wh").success
    output = capsys.readouterr().out
    assert "N/A" in output and "piezo.ph" in output and "10.0000 mm" in output


def test_exposure_missing_detector_preserves_other_readout(console, capsys):
    del console.user_ns["pil2M"]
    assert console.run_cell("exp").success
    output = capsys.readouterr().out
    assert "N/A" in output and "pil900KW" in output and "0.101" in output


@pytest.mark.parametrize("line", ["xscan -1 1 3", "xrscan 1 3", "exp 1", "snaps", "snapw", "snapsw"])
def test_new_actions_reject_paused_re(console, line):
    re = Mock(state="paused")
    console.user_ns["RE"] = re
    result = console.run_cell("%" + line)
    assert isinstance(result.error_in_exec, UsageError)
    assert "must be idle" in str(result.error_in_exec)
    re.assert_not_called()


@pytest.mark.parametrize("line", ["xscan -1 1 3", "xrscan 1 3", "exp 1", "snaps", "wh", "exp"])
def test_new_commands_reject_nested_use(console, line):
    re = Mock(state="idle")
    console.user_ns["RE"] = re
    result = console.run_cell(f"def action():\n    %{line}\naction()")
    assert isinstance(result.error_in_exec, UsageError)
    assert "standalone" in str(result.error_in_exec)
    re.assert_not_called()


def test_color_and_plain_output(console, capsys, monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    console.colors = "linux"
    assert console.run_cell("wh").success
    assert "\033[" in capsys.readouterr().out
    monkeypatch.setenv("NO_COLOR", "1")
    assert console.run_cell("wh").success
    assert "\033[" not in capsys.readouterr().out


@pytest.mark.parametrize("command,plan_name", [
    ("so", "shopen"), ("sopen", "shopen"), ("sc", "shclose"), ("sclose", "shclose"),
])
def test_shutter_aliases(console, command, plan_name):
    state = Signal(name="shutter_state", value=0)
    plan = Mock(side_effect=lambda: bps.mv(state, 1))
    console.user_ns[plan_name] = plan
    assert console.run_cell(command).success
    plan.assert_called_once_with()
    assert state.get() == 1


def test_stop_paused_run(console):
    from bluesky.utils import RunEngineInterrupted

    re = console.user_ns["RE"]
    documents = []
    re.subscribe(lambda name, doc: documents.append((name, doc)))

    def pausing_plan():
        yield from bps.open_run()
        yield from bps.pause()
        yield from bps.close_run()

    with pytest.raises(RunEngineInterrupted):
        re(pausing_plan())
    assert re.state == "paused"
    assert console.run_cell("stop").success
    assert re.state == "idle"
    assert next(doc for name, doc in documents if name == "stop")["exit_status"] == "success"


@pytest.mark.parametrize("command", ["so", "sopen", "sc", "sclose", "stop", "help"])
def test_control_commands_reject_arguments_and_nested_calls(console, command):
    re = Mock(state="idle")
    console.user_ns["RE"] = re
    for source in (f"%{command} extra", f"def action():\n    %{command}\naction()"):
        result = console.run_cell(source)
        assert isinstance(result.error_in_exec, UsageError)
    re.assert_not_called()
    re.stop.assert_not_called()


@pytest.mark.parametrize("command", ["so", "sopen", "sc", "sclose"])
def test_shutter_aliases_reject_paused_re(console, command):
    re = Mock(state="paused")
    console.user_ns["RE"] = re
    result = console.run_cell(command)
    assert isinstance(result.error_in_exec, UsageError)
    assert "must be idle" in str(result.error_in_exec)
    re.assert_not_called()


@pytest.mark.parametrize("command", ["so", "sopen", "sc", "sclose", "stop", "help"])
def test_control_help_without_re(console, capsys, command):
    del console.user_ns["RE"]
    assert console.run_cell(f"%{command} ?").success
    assert command in capsys.readouterr().out


@pytest.mark.parametrize("source", ["help", "%help", "help ?", "%help ?"])
def test_boxed_guide(console, capsys, source):
    del console.user_ns["RE"]
    assert console.run_cell(source).success
    output = capsys.readouterr().out
    assert "┌" in output and "└" in output
    for command in ("xscan", "xrscan", "wh", "exp", "snapsw", "sopen", "sclose", "stop"):
        assert command in output


def test_help_preserves_python_help_and_user_variables(console, capsys):
    import builtins

    original_help = builtins.help
    assert console.run_cell("help(int)").success
    assert "class int" in capsys.readouterr().out
    assert builtins.help is original_help
    console.user_ns["help"] = "user help"
    assert console.run_cell("help").result == "user help"
    assert console.run_cell("%help").success


def test_reloading_does_not_duplicate_help_transform(console):
    load_ipython_extension(console)
    load_ipython_extension(console)
    assert sum(bool(getattr(t, "_smi_bare_help", False)) for t in console.input_transformers_cleanup) == 1


def test_energy_move_then_detector_settings(console):
    energy = SynAxis(name="energy", value=16000)
    sequence = []
    console.user_ns["RE"].msg_hook = lambda msg: sequence.append(msg.command)

    def set_energy(value):
        assert energy.position == value == 16150
        assert console.user_ns["RE"].state == "idle"
        sequence.append("set_energy")

    console.user_ns.update(energy=energy, set_energy=Mock(side_effect=set_energy))
    assert console.run_cell("e 16150").success
    console.user_ns["set_energy"].assert_called_once_with(16150)
    assert sequence.index("set") < sequence.index("wait") < sequence.index("set_energy")


def test_energy_readback_from_pseudo_position(console, capsys):
    from collections import namedtuple

    position = namedtuple("EnergyPseudoPosition", "energy")(16150.125)
    console.user_ns["energy"] = SimpleNamespace(position=position)
    del console.user_ns["RE"]
    assert console.run_cell("e").success
    assert "16150.12 eV" in capsys.readouterr().out


@pytest.mark.parametrize("args", ["0", "-1", "nan", "inf", "1e999", "a 16150", "16150 2", "1+2"])
def test_energy_invalid_input_never_moves(console, args):
    engine = Mock(state="idle")
    update = Mock()
    console.user_ns.update(RE=engine, set_energy=update)
    result = console.run_cell(f"%e {args}")
    assert isinstance(result.error_in_exec, UsageError)
    engine.assert_not_called()
    update.assert_not_called()


@pytest.mark.parametrize("failure", ["limits", "paused", "missing_helper", "nested"])
def test_energy_failures_skip_detector_update(console, failure):
    energy = SoftPositioner(name="energy", init_pos=16000, limits=(15000, 16100))
    update = Mock()
    console.user_ns.update(energy=energy, set_energy=update)
    source = "%e 16150"
    if failure == "paused":
        console.user_ns["RE"] = Mock(state="paused")
    elif failure == "missing_helper":
        del console.user_ns["set_energy"]
    elif failure == "nested":
        source = "def action():\n    %e 16150\naction()"
    result = console.run_cell(source)
    assert not result.success
    update.assert_not_called()
    assert energy.position == 16000


def test_energy_detector_update_error_propagates(console):
    energy = SynAxis(name="energy", value=16000)
    update = Mock(side_effect=RuntimeError("detector update failed"))
    console.user_ns.update(energy=energy, set_energy=update)
    result = console.run_cell("e 16150")
    assert isinstance(result.error_in_exec, RuntimeError)
    assert energy.position == 16150
    update.assert_called_once_with(16150)


def test_energy_help_without_hardware(console, capsys):
    del console.user_ns["RE"]
    assert console.run_cell("e ?").success
    output = capsys.readouterr().out
    assert "set_energy" in output and "eV" in output


@pytest.mark.parametrize("offset,status", [
    (0, "OK"), (99.9, "OK"), (100, "OK"), (-100, "OK"),
    (100.1, "MISMATCH"), (-100.1, "MISMATCH"),
])
def test_detector_energy_comparison(console, capsys, monkeypatch, offset, status):
    monkeypatch.delenv("NO_COLOR", raising=False)
    console.colors = "linux"
    console.user_ns["energy"] = SynAxis(name="energy", value=16150)
    console.user_ns["pil2M"].cam.cam_energy.put((16150 + offset) / 1000)
    del console.user_ns["RE"]
    assert console.run_cell("e").success
    output = capsys.readouterr().out
    row = next(line for line in output.splitlines() if "pil2M" in line)
    assert f"{16150 + offset:.2f} eV" in row
    assert f"{offset:+.2f} eV" in row
    assert status in row
    assert ("\033[1;91m" in row) == (status == "MISMATCH")
    assert "OK" in next(line for line in output.splitlines() if "pil900KW" in line)


@pytest.mark.parametrize("failure", ["missing", "timeout", "nan"])
def test_detector_energy_unavailable(console, capsys, failure):
    console.user_ns["energy"] = SynAxis(name="energy", value=16150)
    if failure == "missing":
        del console.user_ns["pil2M"]
    elif failure == "timeout":
        console.user_ns["pil2M"].cam.cam_energy = Mock()
        console.user_ns["pil2M"].cam.cam_energy.get.side_effect = TimeoutError("offline")
    else:
        console.user_ns["pil2M"].cam.cam_energy.put(float("nan"))
    assert console.run_cell("e").success
    output = capsys.readouterr().out
    row = next(line for line in output.splitlines() if "pil2M" in line)
    assert "UNKNOWN" in row and "N/A" in row
    assert "16150.00 eV" in output
    assert "OK" in next(line for line in output.splitlines() if "pil900KW" in line)


def test_energy_move_displays_actual_detector_settings(console, capsys):
    console.user_ns.update(energy=SynAxis(name="energy", value=16000), set_energy=Mock())
    console.user_ns["pil2M"].cam.cam_energy.put(15)
    assert console.run_cell("e 16150").success
    output = capsys.readouterr().out
    row = next(line for line in output.splitlines() if "pil2M" in line)
    assert "15000.00 eV" in row and "MISMATCH" in row


def test_syntax_colors_match_argument_order(console, capsys, monkeypatch):
    from smi_beamline.motor_magics import _syntax

    monkeypatch.delenv("NO_COLOR", raising=False)
    console.colors = "linux"
    assert _syntax(console, "xscan -1000 1000 21") == (
        "\033[1;36mxscan\033[0m \033[94m-1000\033[0m "
        "\033[92m1000\033[0m \033[95m21\033[0m"
    )
    assert "\033[94m1e-3\033[0m" in _syntax(console, "x a 1e-3")
    # Each example starts argument numbering anew.
    assert "\033[94m0.5\033[0m \033[92m2\033[0m" in _syntax(console, "exp 0.5 / exp 0.5 2")
    assert console.run_cell("help").success
    output = capsys.readouterr().out
    assert "\033[1;36mxscan\033[0m \033[94m-1000\033[0m" in output
    assert "\033[1;36me\033[0m \033[94m16150\033[0m" in output
    assert console.run_cell("xscan -1 1 3").success
    assert "\033[1;36mxscan\033[0m \033[94m-1\033[0m \033[92m1\033[0m \033[95m3\033[0m" in capsys.readouterr().out
    monkeypatch.setenv("NO_COLOR", "1")
    assert _syntax(console, "xscan -1000 1000 21") == "xscan -1000 1000 21"
