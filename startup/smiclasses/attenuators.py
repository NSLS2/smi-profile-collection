from ophyd import (
    PVPositioner,
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    Device,
    Signal,
    PseudoPositioner,
    PseudoSingle,
)
from ophyd.utils.epics_pvs import set_and_wait
from ophyd.status import DeviceStatus
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from ophyd import Component as Cpt


class Attenuator(Device):
    """
    Class representing a single attenuator.

    Attributes:
        open_cmd (EpicsSignal): Command to open the attenuator.
        close_cmd (EpicsSignal): Command to close the attenuator.
        status (EpicsSignalRO): Read-only signal for the attenuator's status.
        fail_to_close (EpicsSignalRO): Signal indicating failure to close.
        fail_to_open (EpicsSignalRO): Signal indicating failure to open.
    """
    open_cmd = Cpt(EpicsSignal, "Cmd:Opn-Cmd", string=True)
    open_val = "Open"

    close_cmd = Cpt(EpicsSignal, "Cmd:Cls-Cmd", string=True)
    close_val = "Not Open"

    status = Cpt(EpicsSignalRO, "Pos-Sts", string=True)
    fail_to_close = Cpt(EpicsSignalRO, "Sts:FailCls-Sts", string=True)
    fail_to_open = Cpt(EpicsSignalRO, "Sts:FailOpn-Sts", string=True)

    # User-facing commands
    open_str = "Insert"
    close_str = "Retract"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_st = None
        self.read_attrs = ["status"]

    def set(self, val):
        """
        Set the attenuator to the desired state.

        Parameters:
            val (str or int): Desired state ('Open', 'Close', etc.).

        Returns:
            DeviceStatus: Status of the operation.
        """
        st = self._set_st = DeviceStatus(self)

        if val in ['Open', 'Insert', 'open', 'insert', 'in', 1]:
            while self.status.get() != 'Open':
                try:
                    self.open_cmd.set(1,timeout=1).wait()
                except: # what is the error, a timeout error?  status error?  for now any error
                    pass

        elif val in ['Close', 'Retract', 'close', 'retract', 'out', 0]:
            while self.status.get() != 'Not Open':
                try:
                    self.close_cmd.set(1,timeout=1).wait()
                except:
                    pass

        st.set_finished()
        return st


# Uncomment and complete the following class if needed
# class Attenuation(PseudoPositioner):
#     """
#     PseudoPositioner for controlling multiple attenuators.
#     """
#     # Synthetic axis
#     attenuation = Cpt(PseudoSingle, kind="hinted")

#     # Real axes
#     att1_1 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:1-1}")
#     att1_2 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:1-2}")
#     ...
#     att2_12 = Cpt(Attenuator, "XF:12IDC-OP:2{Fltr:2-12}")

#     @real_position_argument
#     def inverse(self, r_pos):
#         """
#         Convert real positions to pseudo positions.
#         """
#         return self.PseudoPosition(attenuation=...)

#     @pseudo_position_argument
#     def forward(self, p_pos):
#         """
#         Convert pseudo positions to real positions.
#         """
#         return self.RealPosition(
#             att1_1=att1_1_calc,
#             att1_2=att1_2_calc,
#             ...
#             att2_12=att2_12_calc,
#         )