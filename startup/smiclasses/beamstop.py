from ophyd import (
    EpicsMotor,
    Device,
    Component as Cpt,
)
import bluesky.plan_stubs as bps


class SAXSBeamStops(Device):
    x_rod = Cpt(EpicsMotor, "IBB}Mtr")
    y_rod = Cpt(EpicsMotor, "IBM}Mtr")
    x_pin = Cpt(EpicsMotor, "OBB}Mtr")
    y_pin = Cpt(EpicsMotor, "OBM}Mtr")

    def rod_in(self, x_pos=1.5):
        if self.x_rod.position > 0:
            print("bs rod already in")
            yield from bps.mv(self.x_rod, x_pos)

        else:
            # Move the pindiode out of the way to avoid collision
            yield from self.pin_out()

            # move the bs rod in
            yield from bps.mv(self.x_rod, x_pos)

    def rod_out(self):
        yield from bps.mv(self.x_rod, -205)

    def pin_in(self, x_pos=-199.5):
        if self.x_pin.position < -180:
            print("pindiode already in")
        else:
            # make sure that the pil1M bs is out of the way to avoid collision
            yield from self.rod_out()

            # move the pindiode in
            yield from bps.mv(self.x_pin, x_pos)

    def pin_out(self):
        yield from bps.mv(self.x, 0)

