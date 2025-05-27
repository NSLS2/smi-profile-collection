print(f"Loading {__file__}")

from IPython import get_ipython
from smiclasses.amptek import SMIAmptek, AmptekPositions

# Retrieve the scan dictionary from the IPython namespace
sd = get_ipython().user_ns['sd']

# Initialize the Amptek detector
amptek = SMIAmptek("XF:12IDC-ES:2{Det-Amptek:1}", name="amptek")
amptek.energy_channels.kind = "normal"

# Initialize the Amptek positions
amptek_pos = AmptekPositions("XF:12IDC-ES:2{Det:Amptek-Ax:", name="amptek_pos")

# Add Amptek positions to the baseline
#sd.baseline.extend([amptek_pos])
