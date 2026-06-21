
# Phase 4: put the smi_beamline package (src/) on the import path so the smibase modules can reach
# the relocated device classes via the smiclasses shim.  startup.py lives in <repo>/startup/, so
# the package is at <repo>/src.  (Works whether this file is run by IPython --profile-dir=. or
# exec'd by the queueserver; falls back to the profile dir / cwd if __file__ is unavailable.)
import os as _os
import sys as _sys
try:
    _repo = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
except NameError:
    _repo = _os.path.dirname(_os.path.abspath(_os.getcwd()))
_src = _os.path.join(_repo, "src")
if _os.path.isdir(_src) and _src not in _sys.path:
    _sys.path.insert(0, _src)

from IPython import get_ipython
ipython = get_ipython()

if '__IPYTHON__' in globals():
    ipython.magic('load_ext autoreload')
    ipython.magic('autoreload 2')

# --- Bootstrap: create the session (RE/sd/bec/db/mdsave) and wire the device-class seam. ---
# These two modules ARE the bootstrap: importing them creates RE/db/bec/sd via
# nslsii.configure_base, opens Tiled/Redis, sets the prompt, and configures
# smi_beamline.devices._context with RE/sd/bec/db.  They run first (before the factory) and expose
# the session objects (RE, sd, bec, db, mdsave, ...) into this namespace via ``import *``.
from smibase.base import *
from smibase.base_dev import *

# --- Factory: build the beamline devices, with a timed per-module load report (Option C). ---
# make_devices imports the device modules in dependency order, times each, reports ok/fail, and
# returns the namespace they export.  We merge that into globals() so all the device instances and
# plans land in the IPython user namespace exactly as the old flat ``from smibase.X import *`` did.
from smi_beamline.devices import _context as _seam
from smi_beamline.instances import make_devices as _make_devices

_ctx = {"RE": _seam.get_re(), "sd": _seam.get_sd(),
        "bec": _seam.get_bec(), "db": _seam.get_db(), "mdsave": mdsave}
_devices_ns = _make_devices(_ctx, verbose=True)
globals().update({_k: _v for _k, _v in _devices_ns.items() if not _k.startswith("_")})

# --- smi-plans queue surface (technique presets + *_from_spec wrappers). ---
# Wire the external smi_plans package: inject THIS namespace (devices + bps/np/Signal/...) into the
# smi_plans modules so their bare-global device references resolve, and merge the curated queue
# surface (smi_plans._qserver.__all__) into globals() so the queueserver introspects the plans and
# the terminal user can call them.  Runs AFTER the factory so the device globals exist; guarded so
# a missing smi-plans package never blocks startup.  See smi-plans/docs/QSERVER_WIRING.md.
try:
    from smibase.zz_smi_plans import wire as _wire_smi_plans

    _smi_plans_ns = _wire_smi_plans(globals(), verbose=True)
    globals().update(_smi_plans_ns)
    if _smi_plans_ns:
        print(f"\u2713 smi-plans queue surface exposed ({len(_smi_plans_ns)} plans)")
except Exception as _exc:  # noqa: BLE001 -- never let smi-plans wiring block the session
    print(f"\u2717 smi-plans queue surface NOT exposed: "
          f"{type(_exc).__name__}: {_exc}")

# --- Default scan-naming preprocessor (recorded-field filename templating). ---
# Append the modern replacement for get_scan_md() to RE.preprocessors so EVERY plan run through
# the RunEngine gets its run-scoped sample_name extended with a recorded-field template
# (energy/WAXS-arc/SDD by default), and those fields are read into each data-taking run's primary
# stream for the downstream symlink/readout worker to fill.  The existing RE.md['sample_name']
# (user/proposal prefix) is APPENDED TO, never overwritten.
#
# We pass this module's globals() as the device namespace: tokens are resolved by device VARIABLE
# NAME, so adding/removing signals or whole measurement sets is done entirely in
# smi_beamline.plans.scan_naming (MEASUREMENT_SETS / DEFAULT_SETS) -- THIS call never needs to
# change.  Runs after the factory so the devices exist; guarded so a missing device never blocks
# startup (an unresolved token is simply skipped).
try:
    from smi_beamline.plans.scan_naming import install_default_scan_naming as _install_scan_naming

    _install_scan_naming(_seam.get_re(), globals(), verbose=True)
    print("\u2713 default scan-naming preprocessor installed "
          "(sample_name += recorded-field template)")
except Exception as _exc:  # noqa: BLE001 -- never let naming setup block the session
    print(f"\u2717 default scan-naming preprocessor NOT installed: "
          f"{type(_exc).__name__}: {_exc}")

# --- RE-busy signal (cross-process lock-out flag for the GUI). ---
# Append a preprocessor that holds a "RE is busy" flag high in Redis (db=3, key
# 'swaxsstatus:re_busy') for the duration of every plan, so the out-of-process alignment GUI can
# poll it and disable the small motor moves it would otherwise make while the RunEngine drives the
# beamline.  The flag is heartbeat-refreshed with a short TTL and cleared in a finally, so it can
# never latch (it auto-expires even on a hard kill of the worker).  Guarded so a Redis hiccup never
# blocks the session.  See smi_beamline.plans.re_status.
try:
    from smi_beamline.plans.re_status import install_re_busy_signal as _install_re_busy

    _install_re_busy(_seam.get_re(), verbose=True)
    print("\u2713 RE-busy signal preprocessor installed "
          "(Redis 'swaxsstatus:re_busy' held while plans run)")
except Exception as _exc:  # noqa: BLE001 -- never let the busy signal block the session
    print(f"\u2717 RE-busy signal preprocessor NOT installed: "
          f"{type(_exc).__name__}: {_exc}")

# --- Managed energy-move preprocessor (feedback-managed large energy moves). ---
# Append a preprocessor so EVERY plan energy move (scans, bps.mv(energy, E), queued multi-edge
# plans) larger than 500 eV is routed through the feedback-managed ``energy_walk`` in 500 eV
# sub-steps -- feedback off -> brake-confirmed move -> per-energy BPM3 range -> flux gate ->
# feedback on -> OVAL settle -> coarse-pitch/roll recentre -- while small moves (<=500 eV, e.g.
# fine scan steps) stay fast as a plain ``set``.  One warning line per large move; silent
# otherwise; leaves feedback ON on any exit.  Live-validated 8 -> 16.1 keV up and down.
# Guarded so a BPM3 CA hiccup never blocks the session; ``disable_managed_energy_moves()`` removes
# it at the console.  See smi_beamline.plans.energy_move_preprocessor / smibase.energy.
try:
    from smibase.energy import enable_managed_energy_moves as _enable_managed_energy_moves

    _enable_managed_energy_moves()   # prints its own "energy-move preprocessor installed" line
except Exception as _exc:  # noqa: BLE001 -- never let managed energy moves block the session
    print(f"\u2717 managed energy-move preprocessor NOT installed: "
          f"{type(_exc).__name__}: {_exc}")

