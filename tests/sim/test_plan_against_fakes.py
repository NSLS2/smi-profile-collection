"""Tier-2 demonstration: run real Bluesky plans against FAKE devices.

No hardware is touched -- the devices are ``ophyd.sim`` fakes built through the
factory, and the RunEngine drives them entirely in memory.  This is the level
at which a chronically-faked device (or the whole instrument) can be exercised
for plan-logic regressions while the real hardware is unavailable.
"""
import pytest

pytest.importorskip("bluesky")
from bluesky import RunEngine  # noqa: E402
import bluesky.plan_stubs as bps  # noqa: E402
import bluesky.plans as bp  # noqa: E402


def test_run_engine_sets_a_fake_signal(make_fake):
    """Drive a plan that sets an EpicsSignal-backed value on a fake device.

    (We use an EpicsSignal rather than an EpicsMotor: a fake EpicsMotor's move
    status does not auto-complete, so ``bps.mv`` on one would hang under the RE.
    Signals complete immediately, which is what plans like det_exposure_time do.)
    """
    from smiclasses.pilatus import PilatusDetectorCamV33

    cam = make_fake(PilatusDetectorCamV33, name="cam", prefix="FAKE:cam1:")
    RE = RunEngine({})
    RE(bps.mv(cam.acquire_time, 0.3, cam.num_images, 5))
    assert cam.acquire_time.get() == pytest.approx(0.3)
    assert cam.num_images.get() == 5


def test_run_engine_counts_a_fake_device(make_fake):
    from smiclasses.beamstop import SAXSBeamStops

    bs = make_fake(SAXSBeamStops, name="bs")
    docs = {"start": 0, "event": 0, "stop": 0}

    def collect(name, doc):
        if name in docs:
            docs[name] += 1

    RE = RunEngine({})
    RE(bp.count([bs], num=3), collect)
    assert docs["start"] == 1
    assert docs["event"] == 3
    assert docs["stop"] == 1


def _seed(sig, value):
    (sig.sim_put if hasattr(sig, "sim_put") else sig.put)(value)


def _make_energy(make_fake):
    """A fake Energy with seeded readbacks/speeds suitable for a small move."""
    from smiclasses.energy import Energy

    en = make_fake(Energy, name="energy", prefix="")
    _seed(en.bragg.user_readback, 12.7)      # ~8980 eV
    _seed(en.bragg.velocity, 0.5)            # deg/s
    _seed(en.ivugap.user_readback, 7400)     # gap units
    _seed(en.ivugap.gap_speed, 50.0)
    _seed(en.harmonic, 7)
    return en


def test_small_move_message_stream(make_fake):
    """small_move sets matched speeds, moves both axes together, and restores speeds."""
    en = _make_energy(make_fake)
    msgs = list(en.small_move(8985.0))
    cmds = [m.command for m in msgs]

    # speeds are set before and restored after the move
    assert cmds.count("set") >= 4
    # the bragg + ivu move share one group (moved together)
    move_groups = {m.kwargs.get("group") for m in msgs
                   if m.command == "set" and getattr(m.obj, "name", "") in
                   ("energy_bragg", "energy_ivugap")}
    assert len(move_groups) == 1 and None not in move_groups

    # the last two sets restore the ORIGINAL speeds
    set_speed = [m for m in msgs if m.command == "set" and getattr(m.obj, "name", "")
                 in ("energy_bragg_velocity", "energy_ivugap_gap_speed")]
    restored = {getattr(m.obj, "name"): m.args[0] for m in set_speed[-2:]}
    assert restored["energy_bragg_velocity"] == pytest.approx(0.5)
    assert restored["energy_ivugap_gap_speed"] == pytest.approx(50.0)


def test_small_move_restores_speed_on_abort(make_fake):
    """If the move is interrupted, the finalize still restores the original speeds."""
    en = _make_energy(make_fake)
    gen = en.small_move(8985.0)
    seen = []
    try:
        m = next(gen)
        while True:
            seen.append((m.command, getattr(m.obj, "name", None)))
            if m.command == "set" and getattr(m.obj, "name", "") == "energy_bragg":
                m = gen.throw(RuntimeError("simulated abort during move"))
            else:
                m = gen.send(None)
    except StopIteration:
        pass
    except RuntimeError:
        pass  # expected to propagate after cleanup

    # restore of both speeds must appear AFTER the aborted move
    tail = seen[seen.index(("set", "energy_bragg")):]
    restored = {n for c, n in tail if c == "set"
                and n in ("energy_bragg_velocity", "energy_ivugap_gap_speed")}
    assert restored == {"energy_bragg_velocity", "energy_ivugap_gap_speed"}


def test_small_move_out_of_range_raises(make_fake):
    """A target whose IVU gap is out of range refuses (use the normal move path)."""
    en = _make_energy(make_fake)
    with pytest.raises(RuntimeError):
        list(en.small_move(2100.0))  # far from the seeded harmonic -> gap out of range


def test_sample_name_decorator_injects_run_scoped_name(make_fake):
    """sample_name_decorator tags every nested run, without touching RE.md (replaces sample_id)."""
    from smiclasses._plan_helpers import sample_name_decorator
    from smiclasses.beamstop import SAXSBeamStops

    bs = make_fake(SAXSBeamStops, name="bs")

    @sample_name_decorator("alignment_gisaxs")
    def two_runs():
        yield from bp.count([bs], num=1)
        yield from bp.count([bs], num=1)

    names = []
    RE = RunEngine({})
    RE(two_runs(), {"start": lambda n, d: names.append(d.get("sample_name"))})

    assert names == ["alignment_gisaxs", "alignment_gisaxs"]
    assert "sample_name" not in RE.md  # no global mutation


def test_sample_name_decorator_sanitizes_and_respects_explicit(make_fake):
    """Human labels are sanitized; an inner explicit sample_name is not overridden."""
    from smiclasses._plan_helpers import sample_name_decorator, sanitize_name
    from smiclasses.beamstop import SAXSBeamStops

    assert sanitize_name("alignment height scan") == "alignment_height_scan"

    bs = make_fake(SAXSBeamStops, name="bs")
    names = []
    RE = RunEngine({})

    # 1) a human label is sanitized into the run's sample_name
    @sample_name_decorator("my label here")
    def plain():
        yield from bp.count([bs], num=1)

    RE(plain(), {"start": lambda n, d: names.append(d.get("sample_name"))})
    assert names == ["my_label_here"]

    # 2) an inner scan's explicit sample_name wins (set-default semantics)
    @sample_name_decorator("outer")
    def inner_explicit():
        yield from bp.count([bs], num=1, md={"sample_name": "inner_wins"})

    names.clear()
    RE(inner_explicit(), {"start": lambda n, d: names.append(d.get("sample_name"))})
    assert names == ["inner_wins"]
