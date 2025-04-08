
print(f"Loading {__file__}")

from smiclasses.ioLogik import ioLogik1240, ioLogik1241


moxa_in = ioLogik1241("XF:12IDC-ES:2{IO}AO:", name="moxa_in")
moxa_out = ioLogik1240("XF:12IDC-ES:2{IO}AI:", name="moxa_out")

moxa_in.ch1_read.kind = "hinted"
moxa_out.ch1_read.kind = "hinted"
moxa_in.ch1_sp.kind = "hinted"

