from smi_beamline.devices.manipulators import BDMStage, SMARACT, STG_pseudo, STG_temps


bdm = BDMStage("XF:12IDC-ES:2:", name="bdm")


# The Huber sample stack, driven through the STG_pseudo PseudoPositioner
# (laboratory-frame x/y/z/theta/chi/phi with rotation-center compensation).
stage = STG_pseudo("XF:12IDC-OP:2{HUB:Stg-Ax:", name="stage")
stage_temps = STG_temps("XF:12ID2C-ES{IOLOGIK1:E1262}:Avg-I:TC",name='Huber')
piezo = SMARACT("", name="piezo")


for hp in [stage]:
    hp.configuration_attrs = hp.read_attrs

for pz in [piezo]:
    pz.configuration_attrs = pz.read_attrs

from smi_beamline.devices import _context

_context.baseline_register([stage,  piezo,])