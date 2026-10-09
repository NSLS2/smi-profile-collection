"""Shared read-only status primitives. No devices, GUI, or EPICS connections.

Device methods accept ``read_signal`` so callers can impose timeouts/caching.
The default remains useful directly at the console without invoking a RunEngine.
"""

import math
from dataclasses import dataclass


def read_signal(signal):
    return signal.get(timeout=0.15, connection_timeout=0.15)


def enum_value(signal, read=read_signal):
    value = read(signal)
    if not isinstance(value, str):
        enums = signal.metadata.get("enum_strs")
        if enums and int(value) == value and 0 <= int(value) < len(enums):
            return enums[int(value)]
    return value


def numeric_state(value, mapping):
    """Interpret explicit numeric states, never guess an unknown polarity."""
    try:
        number = float(value)
        if math.isfinite(number) and number.is_integer() and int(number) in mapping:
            return mapping[int(number)]
    except (TypeError, ValueError):
        pass
    return f"UNKNOWN({value})"


def finite_number(value):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("non-finite readback")
    return value


@dataclass(frozen=True)
class StatusField:
    """One read-only field: paths are relative to the owning device; @ is absolute."""
    label: str
    path: str
    kind: str = "number"
    units: str | None = ""
    precision: str = "g"
    scale: float = 1
    reference: str = ""


@dataclass(frozen=True)
class StatusRow:
    label: str
    fields: tuple
    wide: bool = False


def compare_energy(detector_energy_eV, beamline_energy_eV, tolerance_eV=100.0):
    """Common eV comparison for device clients, including the console magics."""
    difference = finite_number(detector_energy_eV) - finite_number(beamline_energy_eV)
    matches = abs(difference) <= tolerance_eV or math.isclose(
        abs(difference), tolerance_eV, rel_tol=0, abs_tol=1e-9)
    return {"difference_eV": difference, "matches": matches}


def motor(label, path, units=None, precision=3):
    return StatusField(label, path, "motor", units, f".{precision}f")


def number(label, path, units="", precision="g", scale=1):
    return StatusField(label, path, units=units, precision=precision, scale=scale)


def state(label, path=""):
    return StatusField(label, path, "state")


# These immutable descriptions are shared by device classes and missing-device
# placeholders. They describe values, not ANSI colors, widgets, or table borders.
MIRROR_STATUS = (StatusRow("{label}", (motor("x", "x"), motor("y", "y"), motor("pitch", "th"))),)
SLIT_STATUS = (StatusRow("{label}", (
    motor("H gap", "hg"), motor("V gap", "vg"),
    StatusField("center H/V", "h", "motor_pair", reference="v"),
)),)
XBPM_STATUS = (StatusRow("{label}", (
    motor("x", "@{name}_pos.x"), motor("y", "@{name}_pos.y"),
    number("sumX", "sumX", units=None, precision=".4g"),
)),)
ENERGY_STATUS = (
    StatusRow("Monochromator", (number("energy", "energy.readback", "eV", ".1f"), number("harmonic", "harmonic"))),
    StatusRow("DCM motors", (motor("bragg", "bragg"), motor("gap", "dcmgap"))),
)
ACCELERATOR_STATUS = (StatusRow("Accelerator / FE", (
    number("ring", "current", "mA", ".1f"), motor("IVU gap", "@energy.ivugap", "um", 1),
    StatusField("FE permit", "@smi_shutter_enable", "permit"),
)),)
SHUTTER_STATUS = (StatusRow("{label}", (state("{short_label}"),)),)
BIMORPH_STATUS = (StatusRow("Bimorph outputs", (
    StatusField("HFM", "", "bimorph"), StatusField("VFM", "@vfm_voltage", "bimorph"),
)),)
CRL_STATUS = (StatusRow("CRLs IN", (StatusField("", "", "lenses"),), wide=True),)
ATTENUATION_STATUS = (
    StatusRow("Attenuation", (
        StatusField("factor", "", "attenuation_factor", reference="@energy.energy.readback"),
        StatusField("transmit", "", "attenuation_transmission", reference="@energy.energy.readback"),
        StatusField("at energy", "", "attenuation_energy", reference="@energy.energy.readback"),
    )),
    StatusRow("Foils IN", (StatusField("", "", "attenuation_foils", reference="@energy.energy.readback"),), wide=True),
)
CHAMBER_STATUS = (
    StatusRow("Sample vacuum", (
        StatusField("WAXS", "", "pressure", reference="waxs"),
        StatusField("MAXS", "", "pressure", reference="maxs"), state("upstream", "upstream_valve"),
    )),
    StatusRow("Vacuum valves", (
        state("WAXS/SAXS", "waxs_saxs_valve"), state("turbo", "turbo_valve"), state("cooling", "turbo_cooling_valve"),
    )),
    StatusRow("Vacuum controls", (
        StatusField("turbo cmd", "turbo_enable", "on_off"), StatusField("power cmd", "det_power", "on_off"),
    )),
)


def sample_status(units):
    return (
        StatusRow("{label} XYZ", tuple(motor(axis, axis, units) for axis in ("x", "y", "z"))),
        StatusRow("{label} angles", tuple(motor(axis, axis, "deg") for axis in ("th", "ph", "ch"))),
    )


DETECTOR_STATUS = (
    StatusRow("{label}", (
        StatusField("state", "cam.detector_state", "enum"),
        number("exposure", "cam.acquire_time", "s"), number("images", "cam.num_images"),
    )),
    StatusRow("{label} energy", (
        number("energy", "cam.cam_energy", "eV", ".1f", 1000),
        number("threshold", "cam.threshold_energy", "eV", ".1f", 1000),
        StatusField("delta E", "", "energy_difference", reference="@energy.energy.readback"),
    )),
)
WAXS_STATUS = DETECTOR_STATUS + (StatusRow("WAXS position", (
    motor("arc", "motors.arc", "deg"), motor("BS x", "motors.bs_x"), motor("BS y", "motors.bs_y"),
)),)
SAXS_STATUS = DETECTOR_STATUS + (
    StatusRow("SAXS position", tuple(motor(axis, "motor." + axis, "mm") for axis in ("x", "y", "z"))),
    StatusRow("SAXS beamstop", (
        StatusField("selected", "active_beamstop", "text"),
        StatusField("x", "", "beamstop_motor", reference="x"),
        StatusField("y", "", "beamstop_motor", reference="y"),
    )),
)

# Pure-data defaults allow a missing device to remain visible in the overview.
STATUS_PROFILES = {
    "accelerator": ACCELERATOR_STATUS, "shutter": SHUTTER_STATUS, "slits": SLIT_STATUS,
    "energy": ENERGY_STATUS, "mirror": MIRROR_STATUS, "bimorph": BIMORPH_STATUS,
    "xbpm": XBPM_STATUS, "attenuation": ATTENUATION_STATUS, "crl": CRL_STATUS,
    "chamber": CHAMBER_STATUS, "piezo": sample_status("um"), "stage": sample_status("mm"),
    "waxs": WAXS_STATUS, "saxs": SAXS_STATUS,
}
