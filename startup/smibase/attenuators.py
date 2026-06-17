
from smi_beamline.devices.attenuators import Attenuator, make_attenuator_bank, AttenuatorSet
from smi_beamline.devices import _context


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

# Aggregate banks: move a whole combination of foils with ONE settled, all-or-nothing move
# (fixes the bounce-back when several foils are driven at once via bps.mv of the individual
# foils).  Foil children are f1..f12, addressing the SAME PVs as att1_*/att2_* above.
#   yield from bps.mv(attenuators2, ['f5', 'f6'])   # insert f5,f6; retract the rest of bank 2
#   yield from bps.mv(attenuators2, [])             # retract all of bank 2
Bank1 = make_attenuator_bank("Bank1", "XF:12IDC-OP:2{{Fltr:1-{}}}", range(1, 13))
Bank2 = make_attenuator_bank("Bank2", "XF:12IDC-OP:2{{Fltr:2-{}}}", range(1, 13))
attenuators1 = Bank1("", name="attenuators1")
attenuators2 = Bank2("", name="attenuators2")

# Energy-aware attenuation factor for the whole 24-foil set.  Reports an approximate
# attenuation factor (from CXRO transmission curves) + a text description of which foils
# are in, evaluated at the current beamline energy; and lets a user/plan REQUEST a factor:
#   yield from bps.mv(attenuation, 100)          # auto-pick fewest foils ~100x at current E
#   yield from bps.mv(attenuation, 1)            # retract all (no attenuation)
#   attenuation.set_for_energy(100, 12000)       # pre-stage 100x for a PLANNED 12 keV
# It is in the baseline (recorded at scan start/end) AND can be added to the detector list
# to be read at every point when energy or attenuation changes during a scan.
attenuation = AttenuatorSet("", name="attenuation", banks=[attenuators1, attenuators2],
                            bank_prefixes=["1", "2"])

_context.baseline_register([att1_1, att1_2, att1_3, att1_4, att1_5, att1_6, att1_7, att1_8, att1_9, att1_10, att1_11, att1_12])
_context.baseline_register([att2_1, att2_2, att2_3, att2_4, att2_5, att2_6, att2_7, att2_8, att2_9, att2_10, att2_11, att2_12])
_context.baseline_register([attenuation])
