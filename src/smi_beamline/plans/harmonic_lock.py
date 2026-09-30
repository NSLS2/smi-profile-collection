"""Scan-scoped harmonic selection; no live devices are imported by this module."""
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from bluesky.utils import Msg

def with_harmonic_lock(plan, start, stop, *, energy, harmonic=None,
                       max_harmonic=None, gap_margin_um=0):
    """Run ``plan`` on one harmonic covering ``start`` through ``stop`` (eV).

    Select/validate before motion. With no existing lock, approach ``start`` in automatic
    mode, then establish the selected harmonic at that energy before running the plan.
    An existing lock is respected for the approach (including nested wrappers).
    Restore the prior lock on completion/error/RE abort; restoration causes no motion.
    Each open_run receives ``harmonic_lock`` metadata. Returns the wrapped plan's result.

    ``energy`` is the energy device. ``harmonic`` requests an exact
    choice; otherwise select the highest valid odd harmonic <= ``max_harmonic`` (default
    ``energy.target_harmonic``). Requires IVU movement enabled. See
    ``docs/ENERGY_SCAN_HARMONICS.md`` for plan-writing examples and cleanup semantics.
    """
    if energy is None:
        raise ValueError("with_harmonic_lock requires an energy device.")
    selected = energy.harmonic_for_range(
        start, stop, harmonic=harmonic, max_harmonic=max_harmonic,
        gap_margin_um=gap_margin_um)
    if not (yield from bps.rd(energy.enableivu)):
        raise RuntimeError("A harmonic-locked scan requires enableivu=True.")
    previous = yield from bps.rd(energy.locked_harmonic)
    metadata = {"harmonic": selected, "start_eV": float(start), "stop_eV": float(stop),
                "gap_margin_um": float(gap_margin_um)}

    def add_metadata(msg):
        if msg.command == "open_run":
            return Msg(msg.command, msg.obj, *msg.args, run=msg.run,
                       **dict(msg.kwargs, harmonic_lock=metadata))
        return msg

    def body():
        yield from bps.mv(energy, float(start))
        yield from bps.mv(energy.locked_harmonic, selected)
        # Required even when Bragg is already at start: the IVU may be on another harmonic.
        yield from bps.mv(energy, float(start))
        return (yield from bpp.msg_mutator(plan, add_metadata))

    def restore():
        yield from bps.mv(energy.locked_harmonic, previous)

    return (yield from bpp.finalize_wrapper(body(), restore()))
