
from smiclasses.mirrors import MIR
from smiclasses.bimorph import VFM_voltage, HFM_voltage
from smiclasses import _config
import bluesky.plan_stubs as bps


hfm = MIR("XF:12IDA-OP:2{Mir:HF-Ax:", name="hfm")
vfm = MIR("XF:12IDA-OP:2{Mir:VF-Ax:", name="vfm")
vdm = MIR("XF:12IDA-OP:2{Mir:VD-Ax:", name="vdm")


vfm_voltage = VFM_voltage("VFM:", name="vfm_voltage")

hfm_voltage = HFM_voltage("HFM:", name="hfm_voltage")


# ---------------------------------------------------------------------------
# Named bimorph states: save / recall known-good voltage sets per mirror, persisted in the
# Redis-backed config (mdsave) under the key "bimorph_states":
#     {name: {"hfm": [16 V], "vfm": [16 V]}}
#
# Mechanism (CAENels controller, verified on hardware): a two-step stage-then-apply.
#   1. write SET-VTRGT<n> to stage each per-channel target -- does NOT move the mirror;
#   2. write SET-ALLTRGT = 1 (the apply trigger) -- ramps the staged targets onto the outputs,
#      with each GET-STATUS<n> going On -> Busy -> On.
# load_bimorph stages then applies and waits for all channels to leave Busy.
# ---------------------------------------------------------------------------
_BIMORPH_MIRRORS = {"hfm": hfm_voltage, "vfm": vfm_voltage}


def save_bimorph(name):
    """Snapshot the live output voltages of BOTH bimorph mirrors as the named state ``name``.

    Reads each mirror's GET-VOUT, stores them in mdsave["bimorph_states"][name], and syncs each
    mirror's SET-VTRGT targets to those outputs (so the staged state matches reality).  This is a
    PLAN (``RE(save_bimorph('tender'))``) -- the target sync is done with messages.
    """
    states = dict(_config.load("bimorph_states"))
    snapshot = {}
    for key, dev in _BIMORPH_MIRRORS.items():
        outs = dev.read_outputs()
        snapshot[key] = outs
        yield from dev.set_targets(outs)   # sync targets to current outputs (no motion)
    states[name] = snapshot
    _config.persist({"bimorph_states": states})
    print("saved bimorph state {!r}: hfm[0]={:.1f} vfm[0]={:.1f}".format(
        name, snapshot["hfm"][0], snapshot["vfm"][0]))


def list_bimorph_states():
    """Return the dict of saved bimorph states (name -> {'hfm':[...], 'vfm':[...]})."""
    states = _config.load("bimorph_states")
    for nm, snap in states.items():
        print("  {:20s} hfm[0]={:7.1f}  vfm[0]={:7.1f}".format(
            nm, snap.get("hfm", [float('nan')])[0], snap.get("vfm", [float('nan')])[0]))
    return states


def delete_bimorph_state(name):
    """Delete the named bimorph state from the persistent config."""
    states = dict(_config.load("bimorph_states"))
    if name not in states:
        raise KeyError("no saved bimorph state named {!r}; have {}".format(
            name, sorted(states)))
    del states[name]
    _config.persist({"bimorph_states": states})
    print("deleted bimorph state {!r}".format(name))


def stage_bimorph(name):
    """PLAN: stage the saved state ``name`` onto both mirrors' SET-VTRGT targets (NO motion).

    Writes the targets only; does not apply, so the mirror does not move.  Follow with
    ``apply_bimorph()`` (or use ``load_bimorph`` which does both).
    """
    states = _config.load("bimorph_states")
    if name not in states:
        raise KeyError("no saved bimorph state named {!r}; have {}".format(
            name, sorted(states)))
    snap = states[name]
    for key, dev in _BIMORPH_MIRRORS.items():
        if key in snap:
            yield from dev.set_targets(snap[key])
    print("staged bimorph state {!r} onto SET-VTRGT (not yet applied)".format(name))


def apply_bimorph(settle=1.0, timeout=120.0):
    """PLAN: apply the currently-staged targets on BOTH mirrors and wait until they settle."""
    for dev in _BIMORPH_MIRRORS.values():
        yield from dev.apply_and_wait(settle=settle, timeout=timeout)


def load_bimorph(name, settle=1.0, timeout=120.0):
    """PLAN: stage the saved state ``name`` and apply it (ramp both mirrors), waiting to settle.

    ``RE(load_bimorph('tender'))``.  Stages SET-VTRGT (safe, no motion), then triggers the apply
    and polls GET-STATUS until every channel leaves 'Busy'.
    """
    yield from stage_bimorph(name)
    yield from apply_bimorph(settle=settle, timeout=timeout)
    print("loaded bimorph state {!r}".format(name))



from smiclasses import _context

_context.baseline_register([ vfm_voltage, hfm_voltage, hfm, vdm, vfm,])