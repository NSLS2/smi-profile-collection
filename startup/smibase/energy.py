print(f"Loading {__file__}")

from smiclasses.energy import Energy, DCMInternals
from ophyd import EpicsMotor

energy = Energy(
    prefix="",
    name="energy",
    read_attrs=["energy", "ivugap", "bragg", "harmonic"],
    configuration_attrs=["enableivu", "enabledcmgap", "target_harmonic"],
)
energy.settle_time = 1
dcm = energy
ivugap = energy.ivugap
dcm_gap = dcm.dcmgap  # Height in CSS # EpicsMotor('XF:12ID:m66', name='p2h')
dcm_pitch = EpicsMotor("XF:12ID:m67", name="dcm_pitch")
bragg = dcm.bragg  # Theta in CSS  # EpicsMotor('XF:12ID:m65', name='bragg')

dcm_config = DCMInternals("", name="dcm_config")

bragg.read_attrs = ["user_readback"]


dcm_theta = EpicsMotor("XF:12ID:m65", name="dcm_theta")



from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([energy, dcm_config, ivugap, bragg])