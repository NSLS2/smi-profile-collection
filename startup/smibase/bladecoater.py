
print(f"Loading {__file__}")

from smiclasses.bladecoater import bladecoater_smaract, syringe_pump

bc_smaract = bladecoater_smaract("XF:12ID2-ES{DDSM100-Ax:", name="bc_smaract")

syringe_pu = syringe_pump("XF:12ID2-ES{Pmp:1}", name="syringe_pu")