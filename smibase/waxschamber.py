print(f"Loading {__file__}")


from ..smiclasses.waxschamber import sample_chamber_pressure

def get_chamber_pressure(signal):
    value = signal.get()
    try:
        return float(value)
    except:
        if isinstance(value, str) and value.startswith("LO"):
            return float("1E-03")
        raise


chamber_pressure = sample_chamber_pressure(
    "XF:12IDC-VA:2", name="chamber_pressure"
)  # Change PVs
chamber_pressure.waxs.kind = "hinted"
chamber_pressure.maxs.kind = "hinted"



from .base import sd

sd.baseline.extend([ chamber_pressure])
