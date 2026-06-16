#!/usr/bin/env python3
"""A self-contained caproto IOC that serves fake DCM + undulator motors for tests.

It provides, under a **sandbox prefix** (default ``SMIsim:``), the records/signals that the
real :class:`smi_beamline.devices.energy.Energy` pseudo-positioner and
:class:`smi_beamline.devices.machine.InsertionDevice` drive, but as *simulated motors that move at finite,
configurable speeds* (via caproto's ``record='motor'`` simulator).  This lets the energy move
choreography -- feedback disable/enable, IVU-brake-then-move, and ``small_move`` speed-matching
-- be tested against real Channel Access with motion that actually takes time, which
``ophyd.sim.make_fake_device`` (instantaneous, no readback ramp) cannot do.

PVs (relative to the prefix), chosen so simple test subclasses can point the real device classes
here:

* ``bragg``   -- motor record  (Bragg angle; *slow* by default)
* ``dcmgap``  -- motor record  (DCM gap)
* ``ivu``     -- motor record  (undulator gap; *fast* by default)
* ``ivu:brake`` / ``ivu:brake:RB``  -- the IVU brake SP / readback
* ``ivu:gapspeed`` / ``ivu:gapspeed:RB`` -- the IVU gap-speed SP / readback
* ``fbk:pitch`` -- DCM pitch feedback-disable signal ("0"/"1")
* ``fbk:roll``  -- DCM roll feedback-disable signal ("0"/"1")

Run standalone (loopback only, safe)::

    python -m tests.iocs.sim_energy_ioc --prefix SMIsim: --interfaces 127.0.0.1
"""
from textwrap import dedent

from caproto.server import PVGroup, SubGroup, ioc_arg_parser, pvproperty, run
from caproto.ioc_examples.fake_motor_record import FakeMotor


class SimEnergyIOC(PVGroup):
    """DCM + undulator simulated motors, plus brake / gap-speed / feedback signals.

    The default speeds are deliberately mismatched (bragg slow, IVU fast) so the
    ``small_move`` speed-matching logic has something real to do.
    """

    # --- motors (record='motor'); RBV ramps toward VAL at VELO ---------------------------
    # bragg: small angular range.  (Speeds here are starting points; tests set VELO explicitly.)
    bragg = SubGroup(FakeMotor, velocity=2.0, precision=5,
                     user_limits=(-30.0, 30.0), prefix="bragg")
    # DCM gap: small.
    dcmgap = SubGroup(FakeMotor, velocity=2.0, precision=4,
                      user_limits=(0.0, 50.0), prefix="dcmgap")
    # undulator gap: large range (um), fast -- so it is the *slower-in-energy* axis only by
    # virtue of the larger distance, exercising small_move's speed-matching.
    ivu = SubGroup(FakeMotor, velocity=2000.0, precision=2,
                   user_limits=(5000.0, 16000.0), prefix="ivu")

    # --- IVU brake: SP (settable) + readback ---------------------------------------------
    ivu_brake_sp = pvproperty(value=0, name="ivu:brake", dtype=int)
    ivu_brake_rb = pvproperty(value=0, name="ivu:brake:RB", dtype=int)

    @ivu_brake_sp.putter
    async def ivu_brake_sp(self, instance, value):
        # mirror the SP onto the readback so BrakesDisengaged-Sts reflects the command
        await self.ivu_brake_rb.write(value)
        return value

    # --- IVU gap speed: SP + readback ----------------------------------------------------
    ivu_gapspeed_sp = pvproperty(value=50.0, name="ivu:gapspeed")
    ivu_gapspeed_rb = pvproperty(value=50.0, name="ivu:gapspeed:RB")

    @ivu_gapspeed_sp.putter
    async def ivu_gapspeed_sp(self, instance, value):
        await self.ivu_gapspeed_rb.write(value)
        # also drive the simulated IVU motor's VELO so the gap actually moves at this speed
        try:
            await self.ivu.motor.fields["velocity"].write(value)
        except Exception:
            pass
        return value

    # --- DCM feedback disable signals ("0" enabled / "1" disabled) -----------------------
    # String PVs matching the real device, which writes the strings "0"/"1".  Long enough
    # max_length so the "0"/"1" strings round-trip.
    fbk_pitch = pvproperty(value="0", name="fbk:pitch", dtype=str, max_length=8)
    fbk_roll = pvproperty(value="0", name="fbk:roll", dtype=str, max_length=8)


if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(
        default_prefix="SMIsim:",
        desc=dedent(SimEnergyIOC.__doc__ or ""),
    )
    ioc = SimEnergyIOC(**ioc_options)
    run(ioc.pvdb, **run_options)
