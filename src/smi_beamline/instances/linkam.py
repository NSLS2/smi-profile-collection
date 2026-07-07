from smi_beamline.devices.linkam import LinkamTensile, LinkamThermal


LThermal = LinkamThermal("XF:12ID-ES{LINKAM}:", name="LinkamThermal")
LTensile = LinkamTensile("XF:12ID-ES:{LINKAM}:", name="LinkamTensile")
