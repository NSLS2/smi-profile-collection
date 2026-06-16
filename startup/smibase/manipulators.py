print(f"Loading {__file__}")

from smiclasses.manipulators import BDMStage, SMARACT, STG_pseudo


bdm = BDMStage("XF:12IDC-ES:2:", name="bdm")


# The Huber sample stack, driven through the STG_pseudo PseudoPositioner
# (laboratory-frame x/y/z/theta/chi/phi with rotation-center compensation).
stage = STG_pseudo("XF:12IDC-OP:2{HUB:Stg-Ax:", name="stage")
piezo = SMARACT("", name="piezo")


for hp in [stage]:
    hp.configuration_attrs = hp.read_attrs

for pz in [piezo]:
    pz.configuration_attrs = pz.read_attrs

from smiclasses import _context

_context.baseline_register([stage,  piezo,])