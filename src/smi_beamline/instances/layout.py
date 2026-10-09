"""SMI installation metadata, independent of imports that construct hardware.

Classes describe what they are; these instance entries describe where they are.
Orders are relative beam-path positions, not physical distances in metres.
"""

from dataclasses import dataclass

from smi_beamline.devices.status import STATUS_PROFILES


@dataclass(frozen=True)
class BeamlineLocation:
    hutch: str
    order: float
    label: str
    profile: str
    boundary: str = ""
    short_label: str = ""


DEFAULT_LAYOUT = {
    "ring": BeamlineLocation("FE", 0, "Accelerator / FE", "accelerator"),
    "fe_shutter": BeamlineLocation("A", 10, "Hutch A", "shutter", "FE shutter", "FE"),
    "wbs": BeamlineLocation("A", 20, "WBS slits", "slits"),
    "energy": BeamlineLocation("A", 30, "Monochromator", "energy"),
    "hfm": BeamlineLocation("A", 40, "HFM", "mirror"),
    "vfm": BeamlineLocation("A", 50, "VFM", "mirror"),
    "vdm": BeamlineLocation("A", 60, "VDM", "mirror"),
    "hfm_voltage": BeamlineLocation("A", 65, "Bimorph outputs", "bimorph"),
    "xbpm2": BeamlineLocation("A", 70, "xbpm2", "xbpm"),
    "ph_shutter": BeamlineLocation("B", 80, "Hutch B", "shutter", "Photon shutter", "photon"),
    "ssa": BeamlineLocation("B", 90, "SSA slits", "slits"),
    "xbpm3": BeamlineLocation("B", 100, "xbpm3", "xbpm"),
    "fs": BeamlineLocation("C", 110, "Hutch C", "shutter", "Fast shutter", "fast"),
    "eslit": BeamlineLocation("C", 120, "ESLIT slits", "slits"),
    "attenuation": BeamlineLocation("C", 130, "Attenuation", "attenuation"),
    "crl": BeamlineLocation("C", 140, "CRLs IN", "crl"),
    "cslit": BeamlineLocation("C", 150, "CSLIT slits", "slits"),
    "chamber_pressure": BeamlineLocation("C", 160, "Sample vacuum", "chamber"),
    "piezo": BeamlineLocation("C", 170, "piezo", "piezo"),
    "stage": BeamlineLocation("C", 180, "stage", "stage"),
    "pil900KW": BeamlineLocation("C", 190, "pil900KW", "waxs"),
    "pil2M": BeamlineLocation("C", 200, "pil2M", "saxs"),
}


def configure_layout(namespace):
    """Attach location/description metadata to existing objects; never read PVs.

    Preserve explicit instance overrides. Called by the device factory after its
    imports, and safe to call when upgrading an existing interactive session.
    """
    for name, location in DEFAULT_LAYOUT.items():
        device = namespace.get(name)
        if device is None:
            continue
        if not hasattr(device, "beamline_location"):
            device.beamline_location = location
        if not hasattr(device, "status_description"):
            device.status_description = STATUS_PROFILES[location.profile]


def status_entries(namespace):
    """Yield located devices in beam order, deduplicating aliases by identity.

    Missing expected devices get pure-data descriptions so N/A remains visible.
    New objects with beamline_location/status_description participate automatically.
    """
    entries, seen = [], set()
    for name, default in DEFAULT_LAYOUT.items():
        device = namespace.get(name)
        location = getattr(device, "beamline_location", default)
        if device is not None:
            if id(device) in seen:
                continue
            seen.add(id(device))
        description = getattr(device, "status_description", None)
        if description is None:
            description = STATUS_PROFILES.get(location.profile, ())
        entries.append((name, location, description))
    for name, device in namespace.items():
        if name in DEFAULT_LAYOUT or id(device) in seen:
            continue
        location = getattr(device, "beamline_location", None)
        if not isinstance(location, BeamlineLocation):
            continue
        description = getattr(device, "status_description", ())
        seen.add(id(device))
        entries.append((name, location, description))
    return sorted(entries, key=lambda entry: entry[1].order)
