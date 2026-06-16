"""Unit tests for the device factory (smi_beamline.instances.make_devices).

These exercise the orchestration/timing/reporting logic with stand-in modules (real importable
modules + a deliberately-missing one), so they need no live beamline/IPython.
"""
import pytest

from smi_beamline import instances


def test_make_devices_collects_public_names_and_reports(capsys):
    # use real importable modules as stand-ins; collect their public names
    mods = [("math lib", "math"), ("string lib", "string")]
    ns = instances.make_devices(modules=mods, verbose=True)

    # public names from the modules are present
    import math
    assert ns["pi"] == math.pi
    assert "ascii_lowercase" in ns

    # a per-module report is attached
    report = ns["_load_report"]
    assert [r["label"] for r in report] == ["math lib", "string lib"]
    assert all(r["status"] == "ok" for r in report)
    assert all(r["seconds"] >= 0 for r in report)

    # Option-C timed output was printed
    out = capsys.readouterr().out
    assert "Building SMI devices" in out
    assert "math lib" in out and "ok" in out
    assert "device groups built" in out


def test_make_devices_continues_on_error_by_default(capsys):
    mods = [("good", "math"), ("broken", "this_module_does_not_exist_xyz"), ("good2", "string")]
    ns = instances.make_devices(modules=mods, verbose=True)

    report = {r["label"]: r for r in ns["_load_report"]}
    assert report["good"]["status"] == "ok"
    assert report["broken"]["status"] == "FAIL"
    assert isinstance(report["broken"]["error"], Exception)
    assert report["good2"]["status"] == "ok"          # continued past the failure

    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "1 FAILED: broken" in out


def test_make_devices_halt_on_error_raises():
    mods = [("good", "math"), ("broken", "this_module_does_not_exist_xyz")]
    with pytest.raises(ModuleNotFoundError):
        instances.make_devices(modules=mods, verbose=False, halt_on_error=True)


def test_make_devices_quiet(capsys):
    instances.make_devices(modules=[("m", "math")], verbose=False)
    assert capsys.readouterr().out == ""


def test_default_device_modules_excludes_bootstrap():
    # the factory must NOT import base/base_dev (those are the bootstrap, run before the factory)
    names = [m for _, m in instances.DEVICE_MODULES]
    assert "smibase.base" not in names
    assert "smibase.base_dev" not in names
    # but it should cover the real device modules
    assert "smibase.pilatus" in names
    assert "smibase.energy" in names
    assert "smibase.suspenders" in names
