print(f"Loading {__file__}")

from ..smiclasses.attenuators import Attenuator

from .base import sd


att1_1 = Attenuator("XF:12IDC-OP:2{Fltr:1-1}", name="att1_1")
att1_2 = Attenuator("XF:12IDC-OP:2{Fltr:1-2}", name="att1_2")
att1_3 = Attenuator("XF:12IDC-OP:2{Fltr:1-3}", name="att1_3")
att1_4 = Attenuator("XF:12IDC-OP:2{Fltr:1-4}", name="att1_4")
att1_5 = Attenuator("XF:12IDC-OP:2{Fltr:1-5}", name="att1_5")
att1_6 = Attenuator("XF:12IDC-OP:2{Fltr:1-6}", name="att1_6")
att1_7 = Attenuator("XF:12IDC-OP:2{Fltr:1-7}", name="att1_7")
att1_8 = Attenuator("XF:12IDC-OP:2{Fltr:1-8}", name="att1_8")
att1_9 = Attenuator("XF:12IDC-OP:2{Fltr:1-9}", name="att1_9")
att1_10 = Attenuator("XF:12IDC-OP:2{Fltr:1-10}", name="att1_10")
att1_11 = Attenuator("XF:12IDC-OP:2{Fltr:1-11}", name="att1_11")
att1_12 = Attenuator("XF:12IDC-OP:2{Fltr:1-12}", name="att1_12")

att2_1 = Attenuator("XF:12IDC-OP:2{Fltr:2-1}", name="att2_1")
att2_2 = Attenuator("XF:12IDC-OP:2{Fltr:2-2}", name="att2_2")
att2_3 = Attenuator("XF:12IDC-OP:2{Fltr:2-3}", name="att2_3")
att2_4 = Attenuator("XF:12IDC-OP:2{Fltr:2-4}", name="att2_4")
att2_5 = Attenuator("XF:12IDC-OP:2{Fltr:2-5}", name="att2_5")
att2_6 = Attenuator("XF:12IDC-OP:2{Fltr:2-6}", name="att2_6")
att2_7 = Attenuator("XF:12IDC-OP:2{Fltr:2-7}", name="att2_7")
att2_8 = Attenuator("XF:12IDC-OP:2{Fltr:2-8}", name="att2_8")
att2_9 = Attenuator("XF:12IDC-OP:2{Fltr:2-9}", name="att2_9")
att2_10 = Attenuator("XF:12IDC-OP:2{Fltr:2-10}", name="att2_10")
att2_11 = Attenuator("XF:12IDC-OP:2{Fltr:2-11}", name="att2_11")
att2_12 = Attenuator("XF:12IDC-OP:2{Fltr:2-12}", name="att2_12")

sd.baseline.extend([att1_1, att1_2, att1_3, att1_4, att1_5, att1_6, att1_7, att1_8, att1_9, att1_10, att1_11, att1_12])
sd.baseline.extend([att2_1, att2_2, att2_3, att2_4, att2_5, att2_6, att2_7, att2_8, att2_9, att2_10, att2_11, att2_12])
