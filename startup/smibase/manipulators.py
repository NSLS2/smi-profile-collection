print(f"Loading {__file__}")

from smiclasses.manipulators import BDMStage, STG, SMPL, HEXAPOD, SMARACT
from ophyd import EpicsMotor


bdm = BDMStage("XF:12IDC-ES:2:", name="bdm")


stage = STG("XF:12IDC-OP:2{HEX:Stg-Ax:", name="stage")
sample = SMPL("XF:12IDC-OP:2{HEX:Sam-Ax:", name="sample")
hp140 = HEXAPOD("XF:12IDC-OP:2{HEX:140-Ax:", name="hp140")
hp430 = HEXAPOD("XF:12IDC-OP:2{HEX:430-Ax:", name="hp430")
piezo = SMARACT("XF:12IDC-ES:2{MCS:1-Ax:", name="piezo")


for hp in [stage, sample, hp140, hp430]:
    hp.configuration_attrs = hp.read_attrs

for pz in [piezo]:
    pz.configuration_attrs = pz.read_attrs

prs = EpicsMotor("XF:12IDC-OP:2{HEX:PRS-Ax:Rot}Mtr", name="prs", labels=["prs"])

for pr in [prs]:
    pr.configuration_attrs = pr.read_attrs



from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([stage,  prs, piezo,])