"""Helpers for the SMI profile startup bootstrap."""

import sys


def _inject_namespace_into_smi_plans(ns):
    """Copy public live-session names into every imported ``smi_plans.*`` module."""
    payload = {k: v for k, v in ns.items() if not k.startswith("_")}
    n_mods = 0
    for name, mod in list(sys.modules.items()):
        if not name.startswith("smi_plans") or mod is None:
            continue
        for key, value in payload.items():
            try:
                setattr(mod, key, value)
            except Exception:
                pass
        n_mods += 1
    return n_mods


def wire_smi_plans(ns, *, verbose=False):
    """Inject the live namespace into ``smi_plans`` and return its curated queue surface."""
    try:
        import smi_plans._qserver as qs
    except Exception as exc:
        if verbose:
            print(f"smi-plans: not wired ({type(exc).__name__}: {exc}); "
                  "no queue plans exposed (install the smi-plans pixi dep).")
        return {}

    n_mods = _inject_namespace_into_smi_plans(ns)
    names = [name for name in getattr(qs, "__all__", []) if not name.startswith("_")]
    surface = {name: getattr(qs, name) for name in names if hasattr(qs, name)}

    if verbose:
        print(f"smi-plans: injected session namespace into {n_mods} module(s); "
              f"exposed {len(surface)} queue plan(s) "
              f"(presets + {sum(1 for name in surface if name.endswith('_from_spec'))} "
              "*_from_spec).")
    return surface
