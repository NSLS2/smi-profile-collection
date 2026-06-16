
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
    
from smibase.base import *
from smibase.base_dev import *
from smibase.waxschamber import *
from smibase.shutter import *
from smibase.beamstop import *
from smibase.machine import *
from smibase.attenuators import *
from smibase.crls import *
from smibase.manipulators import *
from smibase.mirrors import *
from smibase.motors import *
from smibase.slits import *
from smibase.energy import *
from smibase.xbpms import *
from smibase.ioLogik import *
from smibase.electrometers import *
from smibase.amptek import *
from smibase.pilatus import *
from smibase.prosilica import *
from smibase.beam import *
from smibase.alignment import *
from smibase.config import *
from smibase.bladecoater import *
from smibase.humidity_cell import *
from smibase.linkam import *
from smibase.suspenders import *
from smibase.utils import *
