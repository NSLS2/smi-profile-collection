
from smi_beamline.devices.amptek import SMIAmptek, AmptekPositions

# Initialize the Amptek detector
amptek = SMIAmptek("XF:12IDC-ES:2{Det-Amptek:1}", name="amptek")
amptek.energy_channels.kind = "normal"

# Initialize the Amptek positions
amptek_pos = AmptekPositions("XF:12IDC-ES:2{Det:Amptek-Ax:", name="amptek_pos")

# Add Amptek positions to the baseline
#sd.baseline.extend([amptek_pos])
