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

# Provide the live beamline energy to the device-class seam (used by e.g. the Pilatus
# ``energyset`` so it can remember the energy for camserver-restart threshold resets) without
# the device classes importing smibase.energy.  Runs after `energy` exists and before the
# detector modules are imported by startup.py.
from smiclasses import _context as _smiclasses_context
_smiclasses_context.configure(energy_source=energy)

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



manual_PID_disable_pitch = energy.pitch_feedback_disabled
manual_PID_disable_roll = energy.roll_feedback_disabled


def feedback(action=None):
    allowed_actions = ["on", "off"]
    assert (
        action in allowed_actions
    ), f'Wrong action: {action}, must choose: {" or ".join(allowed_actions)}'
    if action == "off":
        manual_PID_disable_pitch.set("1")
        manual_PID_disable_roll.set("1")
    elif action == "on":
        manual_PID_disable_pitch.set("0")
        manual_PID_disable_roll.set("0")