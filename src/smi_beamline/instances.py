"""smi_beamline.instances -- the device FACTORY.

``make_devices(context)`` builds the live beamline device objects and returns them as one
namespace dict.  It is called by the thin ``startup/startup.py`` bootstrap *after* the bootstrap
has created the session objects (``RE``/``sd``/``bec``/``db``/``mdsave``) and wired the
``smi_beamline.devices._context`` seam.

Why "orchestrate imports" (Phase 4, chosen approach)
----------------------------------------------------
The ``smibase.*`` modules currently build their instances as an import side effect (e.g.
``pil2M = SAXS_Detector(...)`` runs when ``smibase.pilatus`` is imported).  Now that the
``get_ipython()`` grabs are gone from those modules (they take what they need from the injected
seam), the factory's job is to **drive that import sequence explicitly**: import each module in
dependency order, time it, report ok/fail (so a stuck/broken device is obvious instead of a
cryptic hang), and collect the built instances into a single namespace.  Individual modules can
later be converted to explicit ``make_X(context)`` builders incrementally; the factory API does
not change.
"""
import importlib
import time

# The device/instance modules, in dependency order (mirrors the historical startup.py order, MINUS
# the bootstrap modules base/base_dev which the thin startup runs first to create the session).
# Each entry: (label, module_name).
DEVICE_MODULES = [
    ("sample chamber", "smibase.waxschamber"),
    ("shutters",       "smibase.shutter"),
    ("beamstop",       "smibase.beamstop"),
    ("machine/ring",   "smibase.machine"),
    ("attenuators",    "smibase.attenuators"),
    ("CRLs",           "smibase.crls"),
    ("manipulators",   "smibase.manipulators"),
    ("mirrors",        "smibase.mirrors"),
    ("motors",         "smibase.motors"),
    ("slits",          "smibase.slits"),
    ("energy",         "smibase.energy"),
    ("xbpms",          "smibase.xbpms"),
    ("ioLogik",        "smibase.ioLogik"),
    ("electrometers",  "smibase.electrometers"),
    ("amptek",         "smibase.amptek"),
    ("pilatus",        "smibase.pilatus"),
    ("prosilica",      "smibase.prosilica"),
    ("beam modes",     "smibase.beam"),
    ("alignment",      "smi_beamline.plans.alignment"),
    ("config",         "smi_beamline.plans.config"),
    ("scan naming",    "smi_beamline.plans.scan_naming"),
    ("blade coater",   "smibase.bladecoater"),
    ("humidity cell",  "smi_beamline.plans.humidity_cell"),
    ("linkam",         "smibase.linkam"),
    ("suspenders",     "smibase.suspenders"),
    ("utils",          "smi_beamline.plans.utils"),
]


def _public_names(module):
    """The names a ``from module import *`` would export (respecting ``__all__`` if present)."""
    if hasattr(module, "__all__"):
        return list(module.__all__)
    return [n for n in vars(module) if not n.startswith("_")]


def make_devices(context=None, *, modules=None, verbose=True, halt_on_error=False):
    """Build the beamline devices by importing the device modules in order, with timing.

    Parameters
    ----------
    context : mapping, optional
        Session objects (``RE``/``sd``/``bec``/``db``/...).  The modules currently read what they
        need from the ``smi_beamline.devices._context`` seam (wired by the bootstrap), so this is
        accepted for forward-compatibility and reporting; it is not required to be used yet.
    modules : list[(label, module_name)], optional
        Override the default :data:`DEVICE_MODULES` (e.g. for tests).
    verbose : bool
        Print the per-module timed progress (Option C).  Set False for a quiet/headless build.
    halt_on_error : bool
        If True, re-raise the first module that fails to build (stops the load).  If False
        (default), report the failure and continue, so one broken device does not block the rest.

    Returns
    -------
    dict
        ``{name: object}`` of every public name exported by the built modules (the namespace the
        bootstrap pushes into ``user_ns``), plus ``"_load_report"`` -> list of per-module results.
    """
    modules = modules if modules is not None else DEVICE_MODULES
    namespace = {}
    report = []

    if verbose:
        print("\nBuilding SMI devices...")

    t_start = time.monotonic()
    n_ok = 0
    for label, mod_name in modules:
        t0 = time.monotonic()
        status = "ok"
        err = None
        try:
            module = importlib.import_module(mod_name)
            for name in _public_names(module):
                namespace[name] = getattr(module, name)
            n_ok += 1
        except Exception as exc:  # noqa: BLE001 -- we want to report ANY device build failure
            status = "FAIL"
            err = exc
        dt = time.monotonic() - t0
        report.append({"label": label, "module": mod_name, "status": status,
                       "seconds": dt, "error": err})
        if verbose:
            dots = "." * max(1, 20 - len(label))
            line = "  {} {} {:>4}   {:4.1f}s".format(label, dots, status, dt)
            if err is not None:
                line += "   {}: {}".format(type(err).__name__, err)
            print(line)
        if err is not None and halt_on_error:
            raise err

    total = time.monotonic() - t_start
    n_fail = len(modules) - n_ok
    if verbose:
        mark = "\u2713" if n_fail == 0 else "\u2717"
        msg = "{} {} device groups built in {:.1f}s".format(mark, n_ok, total)
        if n_fail:
            failed = ", ".join(r["label"] for r in report if r["status"] == "FAIL")
            msg += "  ({} FAILED: {})".format(n_fail, failed)
        print(msg)

    namespace["_load_report"] = report
    return namespace
