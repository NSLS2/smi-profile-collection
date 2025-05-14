
print(f"Loading {__file__}")

from smiclasses.ioLogik import ioLogik1240, ioLogik1241, Diag_Module


moxa_in = ioLogik1241("XF:12IDC-ES:2{IO}AO:", name="moxa_in")
moxa_out = ioLogik1240("XF:12IDC-ES:2{IO}AI:", name="moxa_out")

moxa_in.ch1_read.kind = "hinted"
moxa_out.ch1_read.kind = "hinted"
moxa_in.ch1_sp.kind = "hinted"

diagA_pos = Diag_Module('XF:12ID2A-DM{DM1-IOL1:E1213}:',name='Hutch_A_Diag_pos')
diagB_pos = Diag_Module('XF:12ID2B-DM{DM2-IOL1:E1213}:',name='Hutch_B_Diag_pos')
