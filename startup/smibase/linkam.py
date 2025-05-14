print(f"Loading {__file__}")

from smiclasses.linkam import Linkam, LinkamTensile, LinkamThermal

LThermal = LinkamThermal("XF:12ID-ES{LINKAM}:", name="LinkamThermal")
LTensile = LinkamTensile("XF:12ID-ES:{LINKAM}:", name="LinkamTensile")