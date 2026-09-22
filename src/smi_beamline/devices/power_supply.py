from ophyd import Component as Cpt
from ophyd import Device, EpicsSignal, EpicsSignalRO


class PowerSupply(Device):
    current = Cpt(EpicsSignalRO, "I-I", kind="hinted", metadata={"units": "A"})
    # EpicsSignal supplies metadata internally; passing metadata= here raises a
    # duplicate-keyword TypeError. Writable PV units come from the IOC's EGU.
    max_current = Cpt(EpicsSignal, "I-Lim", kind="omitted")
    out_main_readback = Cpt(
        EpicsSignalRO,
        "E:OutMain-RB",
        kind="hinted",
        metadata={"units": "V"},
    )
    out_main_setpoint = Cpt(
        EpicsSignal,
        "E:OutMain-SP",
        kind="omitted",
    )
    lock_command = Cpt(EpicsSignal, "Enbl:Lock-Cmd", kind="omitted")
    lock_status = Cpt(EpicsSignalRO, "Enbl:Lock-Sts", kind="omitted")
    out_main_command = Cpt(EpicsSignal, "Enbl:OutMain-Cmd", kind="omitted")
    out_main_status = Cpt(EpicsSignalRO, "Enbl:OutMain-Sts", kind="omitted")
    operating_status_bc = Cpt(EpicsSignalRO, "Sts:Opr-Sts.BC", kind="omitted")
    operating_status_bd = Cpt(EpicsSignalRO, "Sts:Opr-Sts.BD", kind="omitted")

    def output(self, voltage, *, current_max=None):
        """Set output voltage, and optionally set the current limit."""
        status = None
        if current_max is not None:
            status = self.max_current.set(current_max)
        voltage_status = self.out_main_setpoint.set(voltage)
        if status is not None:
            return status & voltage_status
        return voltage_status

    def describe(self):
        description = super().describe()
        description[self.current.name]["units"] = "A"
        description[self.out_main_readback.name]["units"] = "V"
        return description

    def on(self):
        """Enable the main output."""
        return self.out_main_command.set(1)

    def off(self):
        """Disable the main output."""
        return self.out_main_command.set(0)
