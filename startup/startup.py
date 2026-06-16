
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
from smiclasses import _context as _seam
from smi_beamline.instances import make_devices as _make_devices

_ctx = {"RE": _seam.get_re(), "sd": _seam.get_sd(),
        "bec": _seam.get_bec(), "db": _seam.get_db(), "mdsave": mdsave}
_devices_ns = _make_devices(_ctx, verbose=True)
globals().update({_k: _v for _k, _v in _devices_ns.items() if not _k.startswith("_")})
