
from ophyd import (
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    Device,
)
from ophyd import Component


class Ring(Device):
    current = EpicsSignalRO("SR:C03-BI{DCCT:1}I:Real-I", name="ring_current")
    lifetime = EpicsSignalRO("SR:OPS-BI{DCCT:1}Lifetime-I", name="ring_lifetime")
    energy = EpicsSignalRO("SR{}Energy_SRBend", name="ring_energy")
    mode = EpicsSignal("SR-OPS{}Mode-Sts", name="ring_ops", string=True)
    filltarget = EpicsSignalRO("SR-HLA{}FillPattern:DesireImA", name="ring_filltarget")

class IVUBrakeCpt(Component):
    def maybe_add_prefix(self, instance, kw, suffix):
        if kw not in self.add_prefix:
            return suffix

        prefix = "".join(instance.prefix.partition("IVU:1")[:2]) + "}"
        return prefix + suffix


class InsertionDevice(EpicsMotor):
    # SR:C12-ID:G1{IVU:1}BrakesDisengaged-SP
    # SR:C12-ID:G1{IVU:1}BrakesDisengaged-Sts
    brake = IVUBrakeCpt(
        EpicsSignal,
        write_pv="BrakesDisengaged-SP",
        read_pv="BrakesDisengaged-Sts",
        add_prefix=("read_pv", "write_pv", "suffix"),
    )
    gap_speed = Component(EpicsSignal,
        write_pv = "SR:C12-ID:G1{IVU:1}GapSpeed-SP",
        read_pv = "SR:C12-ID:G1{IVU:1}GapSpeed-RB",
        add_prefix = (),
    )

    def move(self, position, wait=True, **kwargs):
        """Disengage the IVU brake, then move the gap.

        The brake **must** be disengaged before the gap can move.  The brake is written with a
        non-blocking ``put`` (a single CA put) immediately before delegating to the normal
        ``EpicsMotor.move``; the returned Status is the gap-move status, so ``wait``/timeout
        semantics are unchanged from a plain motor move and this composes correctly with the
        ``Energy`` pseudo-positioner.
        """
        # Disengage the brake (1 = disengaged) and wait for the put to complete so the brake is
        # provably released before motion starts.  A single quick CA put; put(wait=True) (not
        # set().wait()) avoids spawning a worker thread and works on the main or a worker thread.
        self.brake.put(1, wait=True)
        return super().move(position, wait=wait, **kwargs)
