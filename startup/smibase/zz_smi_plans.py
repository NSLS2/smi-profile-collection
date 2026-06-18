"""
smibase.zz_smi_plans
====================

Wire the external ``smi_plans`` package (the curated A-O technique presets and the ``*_from_spec``
queue wrappers) into the live SMI session **and** the queueserver worker.

Why this module exists
----------------------
``smi_plans`` is written against the historical ``%run`` model: its ``technique_*`` / ``_core`` /
``_compose`` / ``_qserver`` modules reference beamline devices (``piezo``, ``energy``, ``pil2M``,
``waxs`` ...) and helpers (``bps``, ``np``, ``det_exposure_time``, ``alignement_gisaxs_hex`` ...) as
**bare module globals** that "the profile injects at runtime".  As an *installed package* each of
those modules has its **own** namespace, so simply ``import``-ing them is not enough -- the names
are undefined until we copy the live objects in.

This module does the two things needed to make the plans both **listed** by the queueserver and
actually **runnable**:

1. **Inject** the live session namespace into every imported ``smi_plans.*`` module (the same thing
   ``smi-plans``' own test ``conftest`` does with its sim devices).  After this, a technique plan's
   ``bps.mv(piezo.th, ...)`` resolves, and ``_qserver.resolve("pil2M_pos")`` finds the object.
2. **Expose** the curated queue surface (``smi_plans._qserver.__all__`` -- the ``A_*``/``B_*`` ...
   presets and the ``*_from_spec`` wrappers) back into the caller's namespace, so the queueserver
   introspects them into ``existing_plans_and_devices.yaml`` and the terminal user can call them.

It is loaded **after** the device factory (so the device globals exist) via
:func:`wire` from ``startup/startup.py``.  See ``smi-plans/docs/QSERVER_WIRING.md``.
"""
import sys


def _inject_namespace_into_smi_plans(ns):
    """Copy the live session names in ``ns`` into every imported ``smi_plans.*`` module.

    Mirrors ``smi-plans``' test ``conftest._inject``: device-dependent modules resolve their bare
    globals (devices + ``bps``/``np``/``Signal`` + helper plans like ``det_exposure_time``) out of
    their own module ``__dict__``, so we ``setattr`` the live objects onto each module.  Injecting
    the **whole** public session namespace (rather than a hand-maintained device list) means any
    name a technique module references resolves as long as the profile exports it -- exactly the
    old ``%run`` single-namespace behaviour -- with no list to drift out of sync with smi_plans.

    Only injects names already imported under ``smi_plans`` (``import smi_plans._qserver`` below
    pulls in the techniques/_core/_compose), and never clobbers a module's own ``__name__`` etc.
    """
    # The names worth injecting: public session names (devices, helper plans, bps/np/Signal/...).
    # Skip dunders and private helpers; skip the modules themselves to avoid shadowing imports.
    payload = {
        k: v for k, v in ns.items()
        if not k.startswith("_")
    }
    n_mods = 0
    for name, mod in list(sys.modules.items()):
        if not name.startswith("smi_plans") or mod is None:
            continue
        for k, v in payload.items():
            try:
                setattr(mod, k, v)
            except Exception:
                pass
        n_mods += 1
    return n_mods


def wire(ns, *, verbose=False):
    """Inject the live namespace into ``smi_plans`` and return its curated queue surface.

    Parameters
    ----------
    ns : dict
        The live session namespace (the profile's ``startup.py`` ``globals()``), holding the device
        instances and the bluesky helpers (``bps``/``bpp``/``np``/``Signal``/...).
    verbose : bool
        Print a one-line summary (modules injected, plans exposed).

    Returns
    -------
    dict
        ``{name: plan}`` for every public name in ``smi_plans._qserver.__all__`` -- merge this into
        the session namespace so the queueserver introspects them and the terminal can call them.
        Returns ``{}`` (and prints why, if ``verbose``) when ``smi_plans`` is not installed, so a
        missing package never blocks startup.
    """
    try:
        import smi_plans._qserver as _qs
    except Exception as exc:  # smi_plans not installed / import error -> degrade, never block
        if verbose:
            print(f"smi-plans: not wired ({type(exc).__name__}: {exc}); "
                  "no queue plans exposed (install the smi-plans pixi dep).")
        return {}

    n_mods = _inject_namespace_into_smi_plans(ns)

    names = [n for n in getattr(_qs, "__all__", []) if not n.startswith("_")]
    surface = {n: getattr(_qs, n) for n in names if hasattr(_qs, n)}

    if verbose:
        print(f"smi-plans: injected session namespace into {n_mods} module(s); "
              f"exposed {len(surface)} queue plan(s) "
              f"(presets + {sum(1 for n in surface if n.endswith('_from_spec'))} *_from_spec).")
    return surface
