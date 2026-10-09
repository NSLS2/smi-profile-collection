"""Status layout is instance data; state meaning belongs to the device."""

from dataclasses import replace
from types import SimpleNamespace

from smi_beamline.beamline_status import status_rows
from smi_beamline.devices.status import StatusRow, number
from smi_beamline.instances.layout import BeamlineLocation, configure_layout, status_entries


def test_location_override_moves_device_and_preserves_description():
    ssa = SimpleNamespace()
    ns = {"ssa": ssa}
    configure_layout(ns)
    assert ssa.beamline_location.hutch == "B"
    ssa.beamline_location = replace(ssa.beamline_location, hutch="C", order=125, label="Moved SSA")
    ssa.status_description = (StatusRow("{label}", (number("value", "missing"),)),)
    configure_layout(ns)
    rows = [row.label for row in status_rows(ns)]
    assert rows.index("Hutch C") < rows.index("Moved SSA") < rows.index("Attenuation")
    assert "SSA slits" not in rows
    assert ssa.beamline_location.hutch == "C"


def test_new_device_participates_and_aliases_are_deduplicated():
    device = SimpleNamespace(
        beamline_location=BeamlineLocation("B", 95, "New monitor", ""),
        status_description=(StatusRow("{label}", (number("value", "signal"),)),),
        signal=SimpleNamespace(connected=True, get=lambda **kw: 42),
    )
    ns = {"monitor": device, "alias": device}
    entries = status_entries(ns)
    assert sum(location.label == "New monitor" for _, location, _ in entries) == 1
    rows = status_rows(ns)
    labels = [row.label for row in rows]
    assert labels.index("SSA slits") < labels.index("New monitor") < labels.index("xbpm3")
    assert dict(rows)["New monitor"][0].value == "42"


def test_class_description_override_is_used():
    class Custom:
        status_description = (StatusRow("class-provided", (number("value", "absent"),)),)

    ns = {"hfm": Custom()}
    configure_layout(ns)
    assert "class-provided" in dict(status_rows(ns))
