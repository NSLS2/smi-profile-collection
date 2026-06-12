print(f"Loading {__file__}")

from smiclasses.manipulators import BDMStage, STG, SMARACT


bdm = BDMStage("XF:12IDC-ES:2:", name="bdm")


stage = STG("XF:12IDC-OP:2{HUB:Stg-Ax:", name="stage")
piezo = SMARACT("", name="piezo")


for hp in [stage]:
    hp.configuration_attrs = hp.read_attrs

for pz in [piezo]:
    pz.configuration_attrs = pz.read_attrs

from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([stage,  piezo,])