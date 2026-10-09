"""Uniform-shift selection and actual-output confirmation without hardware."""

import threading

import numpy as np
import pytest
from bluesky import RunEngine, plan_stubs as bps
from ophyd import Signal

from smi_beamline.devices.bimorph import _BimorphChannels, HFM_voltage, VFM_voltage


class Mirror(_BimorphChannels):
    def __init__(self, *, accept=True, delay=0, error=False):
        self.name = "sim_mirror"
        self.shifts = []
        self.stages = []
        self.applies = 0
        self.timer = None
        self.shift_rel = Signal(name="shift", value=0)
        self.shift_rel.pvname = "SIM:SET-ALLSHIFT"
        self.shift_rel.put = self.shift
        self.accept, self.delay, self.error = accept, delay, error
        for i in range(16):
            setattr(self, f"ch{i}", Signal(name=f"output{i}", value=100 + i * 10))
            setattr(self, f"ch{i}_status", Signal(name=f"state{i}", value="On"))

    def shift(self, value, **kwargs):
        self.shifts.append(value)
        targets = np.asarray(self.read_outputs()) + value
        def finish():
            if self.accept:
                for i, target in enumerate(targets):
                    getattr(self, f"ch{i}").put(target)
        if self.delay:
            self.timer = threading.Timer(self.delay, finish)
            self.timer.start()
        else:
            finish()
        if self.error:
            raise RuntimeError("ambiguous write result")

    def set_targets(self, targets, **kwargs):
        self.stages.append(list(targets))
        yield from bps.null()

    def apply_and_wait(self, **kwargs):
        self.applies += 1
        if self.accept:
            for i, target in enumerate(self.stages[-1]):
                getattr(self, f"ch{i}").put(target)
        yield from bps.null()


@pytest.fixture
def engine():
    return RunEngine({}, context_managers=[])


def move(engine, mirror, targets, **kwargs):
    engine(mirror.move_voltages(targets, settle=0, poll=0.005, timeout=0.15, **kwargs))


@pytest.mark.parametrize("delta", [50, -80])
def test_uniform_offsets_shift_once_with_no_staging(engine, delta):
    mirror = Mirror()
    messages = []
    engine.msg_hook = lambda msg: messages.append(msg.command)
    targets = np.asarray(mirror.read_outputs()) + delta
    move(engine, mirror, targets)
    assert mirror.shifts == [delta]
    assert mirror.stages == [] and mirror.applies == 0
    assert mirror.read_outputs() == list(targets)
    assert "clear_checkpoint" in messages
    # Sending the same relative command again must not be skipped as equal PV value.
    move(engine, mirror, targets + delta)
    assert mirror.shifts == [delta, delta]


def test_small_readback_noise_uses_absolute_tolerance(engine):
    mirror = Mirror()
    targets = np.asarray(mirror.read_outputs()) + 80
    targets[0] += 0.4
    move(engine, mirror, targets)
    assert len(mirror.shifts) == 1
    assert np.max(np.abs(np.asarray(mirror.read_outputs()) - targets)) <= 0.5


@pytest.mark.parametrize("disabled", [False, True])
def test_nonuniform_or_disabled_uses_stage_apply(engine, disabled):
    mirror = Mirror()
    targets = np.asarray(mirror.read_outputs()) + 30
    if not disabled:
        targets[5] += 2
    move(engine, mirror, targets, use_shift=not disabled)
    assert mirror.shifts == []
    assert mirror.stages == [list(targets)] and mirror.applies == 1
    assert mirror.read_outputs() == list(targets)


def test_already_at_target_is_noop(engine):
    mirror = Mirror()
    move(engine, mirror, mirror.read_outputs())
    assert not mirror.shifts and not mirror.stages and not mirror.applies


def test_waits_for_outputs_even_when_states_never_show_busy(engine):
    mirror = Mirror(delay=0.04)
    targets = np.asarray(mirror.read_outputs()) + 50
    try:
        move(engine, mirror, targets)
        assert mirror.read_outputs() == list(targets)
    finally:
        mirror.timer.join()


@pytest.mark.parametrize("uniform", [False, True])
def test_stale_outputs_fail_without_retry_or_fallback(engine, uniform):
    mirror = Mirror(accept=False)
    targets = np.asarray(mirror.read_outputs()) + 50
    if not uniform:
        targets[0] += 10
    with pytest.raises(TimeoutError, match="outputs did not reach"):
        move(engine, mirror, targets)
    assert len(mirror.shifts) == int(uniform)
    assert len(mirror.stages) == int(not uniform)


def test_ambiguous_shift_write_does_not_repeat(engine):
    mirror = Mirror(error=True)
    targets = np.asarray(mirror.read_outputs()) + 50
    with pytest.raises(RuntimeError, match="ambiguous"):
        move(engine, mirror, targets)
    assert mirror.shifts == [50] and not mirror.stages


def test_one_wrong_output_cannot_pass_verification(engine):
    mirror = Mirror()
    original = mirror.shift_rel.put
    def partial_shift(value, **kwargs):
        original(value, **kwargs)
        mirror.ch15.put(mirror.ch15.get() - 2)
    mirror.shift_rel.put = partial_shift
    with pytest.raises(TimeoutError, match="outputs did not reach"):
        move(engine, mirror, np.asarray(mirror.read_outputs()) + 50)
    assert mirror.shifts == [50] and not mirror.stages


def test_fault_after_shift_cannot_pass_matching_outputs(engine):
    mirror = Mirror()
    original = mirror.shift_rel.put
    def faulting_shift(value, **kwargs):
        original(value, **kwargs)
        mirror.ch5_status.put("Fault")
    mirror.shift_rel.put = faulting_shift
    with pytest.raises(TimeoutError, match="outputs did not reach"):
        move(engine, mirror, np.asarray(mirror.read_outputs()) + 50)
    assert mirror.shifts == [50]


def test_named_load_uses_combined_move_and_validates_both_first(engine):
    # Load only the named helper, not the module's live device constructors.
    import ast
    from pathlib import Path
    from types import SimpleNamespace

    path = Path(__file__).parents[2] / "src/smi_beamline/instances/mirrors.py"
    tree = ast.parse(path.read_text())
    fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "load_bimorph")
    hfm, vfm = Mirror(), Mirror()
    snapshots = {"test": {"hfm": np.asarray(hfm.read_outputs()) + 10,
                          "vfm": np.asarray(vfm.read_outputs()) - 20}}
    ns = {"_config": SimpleNamespace(load=lambda key: snapshots), "_BIMORPH_MIRRORS": {"hfm": hfm, "vfm": vfm}}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(path), "exec"), ns)
    engine(ns["load_bimorph"]("test", settle=0))
    assert hfm.shifts == [10] and vfm.shifts == [-20]
    snapshots["test"]["vfm"] = [1] * 15
    with pytest.raises(ValueError):
        engine(ns["load_bimorph"]("test", settle=0))
    assert hfm.shifts == [10]  # no partial load before discovering malformed VFM data


@pytest.mark.parametrize("state", ["Busy", "Off", "Fault"])
def test_non_idle_channels_prevent_any_write(engine, state):
    mirror = Mirror()
    mirror.ch15_status.put(state)
    with pytest.raises(RuntimeError, match="all channels On"):
        move(engine, mirror, np.asarray(mirror.read_outputs()) + 50)
    assert not mirror.shifts and not mirror.stages


@pytest.mark.parametrize("targets", [[1] * 15, [float("nan")] * 16, [float("inf")] * 16])
def test_invalid_targets_prevent_any_write(engine, targets):
    mirror = Mirror()
    with pytest.raises(ValueError, match="finite scalar voltages"):
        move(engine, mirror, targets)
    assert not mirror.shifts and not mirror.stages


@pytest.mark.parametrize("cls", [HFM_voltage, VFM_voltage])
def test_shift_component_is_action_pv_without_put_completion(cls):
    assert cls.shift_rel.suffix == "SET-ALLSHIFT"
    assert cls.shift_rel.kwargs["put_complete"] is False
