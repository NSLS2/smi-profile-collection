print(f"Loading {__file__}")

from .base import sd
from ..smiclasses.amptek import SMIAmptek, AmptekPositions

# amptek_energy = Signal(name='amptek_energy', value=energy_channels)


amptek = SMIAmptek("XF:12IDC-ES:2{Det-Amptek:1}", name="amptek")
amptek.energy_channels.kind = "normal"

amptek_pos = AmptekPositions("XF:12IDC-ES:2{Det:Amptek-Ax:", name="amptek_pos")
sd.baseline.extend([amptek_pos])
