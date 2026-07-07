from smi_beamline.devices import _context
from smi_beamline.devices.waxschamber import Sample_Chamber


def get_chamber_pressure(signal):
    value = signal.get()
    try:
        return float(value)
    except Exception:
        if isinstance(value, str) and value.startswith("LO"):
            return float("1E-03")
        if isinstance(value, str) and value.startswith("NO"):
            return 10000.0
        raise


chamber_pressure = Sample_Chamber("", name="chamber")
chamber_pressure.waxs.kind = "hinted"
chamber_pressure.maxs.kind = "hinted"

_context.baseline_register([chamber_pressure])
