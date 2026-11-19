"""Overlay bindings and startup wiring, with fake devices and no Channel Access."""

import importlib
import sys

import pytest
from ophyd.sim import make_fake_device

from smi_beamline.devices.diagnostic_cameras import (
    OAV_PLUGIN_PREFIXES,
    DiagnosticCamera,
    OAVConfiguration,
)
from smi_beamline.instances import DEVICE_MODULES, make_devices


@pytest.mark.parametrize("number", [9, 10])
def test_all_overlay_fields_and_prefixes(number):
    prefix = f"XF:12ID2-OP{{GigE-Cam:{number}}}"
    camera = make_fake_device(DiagnosticCamera)(prefix, name=f"cam{number}")
    assert camera.component_names == ("over1",)
    assert len(camera.over1.component_names) == 8
    fields = {
        "blue": "Blue",
        "center_x": "CenterX",
        "center_y": "CenterY",
        "draw_mode": "DrawMode",
        "green": "Green",
        "overlay_portname": "Name",
        "position_x": "PositionX",
        "position_y": "PositionY",
        "red": "Red",
        "shape": "Shape",
        "size_x": "SizeX",
        "size_y": "SizeY",
        "use": "Use",
        "width_x": "WidthX",
        "width_y": "WidthY",
    }
    for index in range(1, 9):
        overlay = getattr(camera.over1, f"overlay_{index}")
        assert overlay.prefix == prefix + f"Over1:{index}:"
        for attr, suffix in fields.items():
            assert overlay._sig_attrs[attr].suffix == suffix
            signal = getattr(overlay, attr)
            value = "beam reference" if attr == "overlay_portname" else 17
            signal.sim_put(value)
            assert signal.get() == value
        assert not overlay.stage_sigs
    assert not camera.stage_sigs
    assert not camera.over1.stage_sigs
    camera.over1.overlay_3.use.sim_put(0)
    camera.stage()
    camera.unstage()
    assert camera.over1.overlay_3.use.get() == 0


def test_profile_exports_fake_cameras(monkeypatch):
    module = "smi_beamline.instances.diagnostic_cameras"
    monkeypatch.setenv("SMI_FAKE_DEVICES", "cam9,cam10,OAV_config")
    monkeypatch.delenv("SMI_REAL_DEVICES", raising=False)
    previous = sys.modules.pop(module, None)
    try:
        # Only import the new instance module, never profile startup.
        entry = next(item for item in DEVICE_MODULES if item[1] == module)
        namespace = make_devices(modules=[entry], verbose=False, halt_on_error=True)
        for name, number in (("cam9", 9), ("cam10", 10)):
            camera = namespace[name]
            assert camera.prefix == f"XF:12ID2-OP{{GigE-Cam:{number}}}"
            camera.over1.overlay_3.width_x.sim_put(4)
            assert camera.over1.overlay_3.width_x.get() == 4
        assert namespace["OAV_config"].prefix == "XF:12IDC-BI{Cam:SAM}"
        assert set(namespace) == {"cam9", "cam10", "OAV_config", "_load_report"}
    finally:
        sys.modules.pop(module, None)
        parent = importlib.import_module("smi_beamline.instances")
        if previous is None:
            parent.__dict__.pop("diagnostic_cameras", None)
        else:
            sys.modules[module] = previous
            parent.diagnostic_cameras = previous


def test_oav_routing_is_exactly_the_requested_plugins_and_fields():
    camera = make_fake_device(OAVConfiguration)(
        "XF:12IDC-BI{Cam:SAM}", name="OAV_config"
    )
    assert set(camera.component_names) == {"plugins", "trans1"}
    assert not camera._signals  # Both containers are lazy at construction.
    assert set(camera.plugins.component_names) == {
        p.lower() for p in OAV_PLUGIN_PREFIXES
    }
    assert len(OAV_PLUGIN_PREFIXES) == 33
    for prefix in OAV_PLUGIN_PREFIXES:
        plugin = getattr(camera.plugins, prefix.lower())
        assert plugin.prefix == camera.prefix + prefix + ":"
        assert set(plugin.component_names) == {"enable", "nd_array_port", "port_name"}
        assert plugin._sig_attrs["enable"].suffix == "EnableCallbacks"
        assert plugin._sig_attrs["nd_array_port"].suffix == "NDArrayPort"
        assert plugin._sig_attrs["port_name"].suffix == "PortName_RBV"
        plugin.enable.sim_put(0)
        plugin.nd_array_port.sim_put("CAM")
        plugin.port_name.sim_put(prefix)
        assert plugin.port_name.get() == prefix
        assert not plugin.stage_sigs
    assert camera.trans1.prefix == camera.prefix + "Trans1:"
    assert camera.trans1._sig_attrs["type_"].suffix == "Type"
    camera.trans1.type_.sim_put("Rot90")
    camera.stage()
    camera.unstage()
    assert camera.trans1.type_.get() == "Rot90"
    for prefix in OAV_PLUGIN_PREFIXES:
        plugin = getattr(camera.plugins, prefix.lower())
        assert plugin.enable.get() == 0
        assert plugin.nd_array_port.get() == "CAM"
