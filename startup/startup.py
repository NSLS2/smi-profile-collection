
from IPython import get_ipython
ipython = get_ipython()

if '__IPYTHON__' in globals():
    ipython.magic('load_ext autoreload')
    ipython.magic('autoreload 2')
    
from smibase.base import *
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
