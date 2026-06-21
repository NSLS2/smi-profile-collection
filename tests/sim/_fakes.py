"""Shared fake DCM-feedback model for the energy_walk / energy-move-preprocessor sim tests.

A lightweight stand-in for ``smi_beamline.plans.dcm_diag.DCMDiag`` with the same attribute surface
the plans use (``oval`` / ``fb_disable`` / ``motor`` / ``sumY`` / ``assumed_sign`` /
``flux_table`` / rails / windows), plus a simple feedback coupling: when feedback is ON, moving a
coarse motor changes the corresponding OVAL by ``gain * motor_delta`` (verified signs), clamped at
the per-axis rail to model piezo-DAC saturation.

Importable as ``from _fakes import FakeDiag`` (pytest puts each test directory on ``sys.path``).
"""
from ophyd import Signal
from ophyd.sim import SynAxis


class FakeOval(Signal):
    """OVAL coupled to a coarse motor; clamped at +/-rail to model DAC saturation."""
    def __init__(self, name, motor, fb_disable, gain, rail=4095.0):
        super().__init__(name=name, value=0.0)
        self._motor = motor
        self._fb = fb_disable           # "0" = feedback ON
        self._gain = gain
        self._rail = rail
        self._last_motor = float(motor.position)

    def get(self):
        cur_m = float(self._motor.position)
        dm = cur_m - self._last_motor
        self._last_motor = cur_m
        if dm and str(self._fb.get()) == "0":
            v = float(super().get()) + self._gain * dm
            v = max(-self._rail, min(self._rail, v))
            super().put(v)
        return super().get()


def _make_range_signals(initial=0):
    """A BPM3 range setpoint + readback pair where writing the setpoint echoes into the readback
    (like the IOC), without overriding ``Signal.set``/``put`` (so ``bps.mv`` Status stays clean)."""
    readback = Signal(name="bpm3_range_rb", value=int(initial))
    setpoint = Signal(name="bpm3_range_sp", value=int(initial))
    setpoint.subscribe(lambda value, **k: readback.put(int(value)), run=False)
    return setpoint, readback


class FakeDiag:
    OVAL_RANGE = 8192.0
    OVAL_RAIL = {"roll": 4095.0, "pitch": 8191.0}
    OVAL_RAIL_MARGIN = 200.0
    OVAL_RECENTER_WINDOW = {"roll": 2000.0, "pitch": 4000.0}
    OVAL_TARGET = 400.0

    def rail(self, axis):
        return self.OVAL_RAIL.get(axis, self.OVAL_RANGE)

    def recenter_window(self, axis):
        return self.OVAL_RECENTER_WINDOW.get(axis, 0.5 * self.rail(axis))

    def __init__(self, energy, sumY=10.0, gains=None, flux_table=None, oval0=None):
        gains = gains or {"roll": 600000.0, "pitch": -600000.0}     # verified signs
        self._energy_source = energy
        self.assumed_sign = {"roll": +1.0, "pitch": -1.0}
        self.flux_table = flux_table
        self.motor = {"roll": SynAxis(name="m68"), "pitch": SynAxis(name="m67")}
        self.fb_disable = {"roll": Signal(name="fb_roll", value="0"),
                           "pitch": Signal(name="fb_pitch", value="0")}
        self.oval = {
            a: FakeOval(f"oval_{a}", self.motor[a], self.fb_disable[a], gains[a],
                        rail=self.OVAL_RAIL[a])
            for a in ("roll", "pitch")
        }
        if oval0:
            for a, v in oval0.items():
                self.oval[a].put(v)
        self.sumY = Signal(name="sumY", value=sumY)

        # BPM3 electrometer range (gain): writing the setpoint echoes into the readback, like the
        # IOC.  Seed the readback to an index that will differ from the table so tests see a switch.
        self.range_sp, self.range_rb = _make_range_signals(initial=0)

    def range_index(self, energy_keV):
        from smi_beamline.plans.dcm_diag import range_index
        return range_index(energy_keV)
