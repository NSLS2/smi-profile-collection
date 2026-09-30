import pytest
from bluesky import RunEngine
from ophyd import Signal

from smi_beamline.devices.bimorph import _BimorphChannels, N_BIMORPH_CH


class _Target(Signal):
    def __init__(self, readback, *, accept, **kwargs):
        super().__init__(**kwargs)
        self.readback = readback
        self.accept = accept
        self.writes = []

    def set(self, value):
        self.writes.append(value)
        if self.accept:
            self.readback.put(value)
        return super().set(value)


class _Mirror(_BimorphChannels):
    def __init__(self, *, accept=True):
        self.name = "test_mirror"
        self.apply_sig = Signal(name="apply", value=0)
        self.apply_sig.pvname = "TEST:SET-ALLTRGT"
        for i in range(N_BIMORPH_CH):
            rb = Signal(name="rb{}".format(i), value=0)
            rb.pvname = "TEST:GET-VTRGT{}".format(i)
            target = _Target(rb, accept=accept, name="target{}".format(i), value=0)
            target.pvname = "TEST:SET-VTRGT{}".format(i)
            setattr(self, "ch{}_trg_rb".format(i), rb)
            setattr(self, "ch{}_trg".format(i), target)
            setattr(self, "ch{}_status".format(i), Signal(name="state{}".format(i), value="On"))


@pytest.mark.parametrize("debug", [False, True])
def test_staging_diagnostics_preserve_writes_and_do_not_apply(debug, capsys):
    mirror = _Mirror()
    RE = RunEngine({})
    RE(mirror.set_targets_sequential(range(N_BIMORPH_CH), stable_reads=1, debug=debug))
    assert mirror.read_targets() == list(range(N_BIMORPH_CH))
    assert mirror.apply_sig.get() == 0
    for i in range(N_BIMORPH_CH):
        assert getattr(mirror, "ch{}_trg".format(i)).writes == [float(i)]
    output = capsys.readouterr().err
    if debug:
        assert "test_mirror: STAGE begin" in output
        assert "STAGE ch15 attempt 1/3 WRITE pv=TEST:SET-VTRGT15 target=15.000V" in output
        assert "READ pv=TEST:GET-VTRGT15 value=15.000V" in output
        assert "stable=1/1" in output
        assert "WRITE status complete: success=True exception=None" in output
        assert "STAGE complete" in output
    else:
        assert output == ""


def test_staging_diagnostics_identify_stale_target_and_retry(capsys):
    mirror = _Mirror(accept=False)
    RE = RunEngine({})
    with pytest.raises(TimeoutError, match="ch0 target readback did not reach"):
        RE(mirror.set_targets_sequential([20] * N_BIMORPH_CH,
                                        timeout=-1, attempts=2, stable_reads=1, debug=True))
    assert mirror.ch0_trg.writes == [20.0, 20.0]
    assert mirror.ch1_trg.writes == []
    assert mirror.apply_sig.get() == 0
    output = capsys.readouterr().err
    assert "delta=-20.000V stable=0/1" in output
    assert "attempt 1/2 verification TIMEOUT; retrying" in output
    assert "attempt 2/2 verification TIMEOUT; attempts exhausted" in output
    assert "STAGE complete" not in output


def test_apply_diagnostics_distinguish_apply_from_staging(capsys):
    mirror = _Mirror()
    RE = RunEngine({})
    RE(mirror.apply_and_wait(settle=0, poll=0, debug=True))
    assert mirror.apply_sig.get() == 1
    output = capsys.readouterr().err
    assert "APPLY WRITE pv=TEST:SET-ALLTRGT value=1" in output
    assert "APPLY poll" in output
    assert "APPLY settled" in output
    assert "STAGE" not in output
