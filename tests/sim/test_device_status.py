"""Device-level state APIs operate directly on fake signals, with no display."""

import pytest
from ophyd.sim import make_fake_device

from smi_beamline.devices.shutter import FrontEndShutterReadback, SMIFastShutter, TwoButtonShutter
from smi_beamline.devices.waxschamber import Sample_Chamber
from smi_beamline.devices.crls import CRL
from smi_beamline.devices.bimorph import HFM_voltage, VFM_voltage


@pytest.mark.parametrize("cls", [HFM_voltage, VFM_voltage])
def test_bimorph_summary_includes_first_voltage(cls):
    device = make_fake_device(cls)("FAKE:", name="mirror_voltage")
    for i in range(16):
        getattr(device, f"ch{i}").sim_put(100 + i * 10)
        getattr(device, f"ch{i}_status").sim_put("On")
    device.ch0.sim_put(175)
    state = device.read_output_state()
    assert state == {"state": "ON", "first": 175, "min": 110, "max": 250, "units": "V"}


def test_fast_shutter_reads_live_state_without_updating_software_cache():
    device = make_fake_device(SMIFastShutter)(name="fs")
    device.status.put("old cached state")
    for raw, expected in [(7.0, "NOT OPEN"), (0, "OPEN"), (3, "UNKNOWN(3)")]:
        device.status_pv.sim_put(raw)
        assert device.read_state() == expected
        assert device.status.get() == "old cached state"


def test_front_end_and_valve_polarity():
    fe = make_fake_device(FrontEndShutterReadback)("FAKE:", name="fe")
    fe.status.sim_put(1)
    assert fe.read_state() == "NOT OPEN"
    valve = make_fake_device(TwoButtonShutter)("FAKE:", name="valve")
    valve.open_val, valve.close_val = "ReverseOpen", "ReverseClosed"
    valve.status.sim_put("ReverseOpen")
    assert valve.read_state() == "OPEN"
    valve.status.sim_put("ReverseClosed")
    assert valve.read_state() == "CLOSED"


def test_pressure_thresholds_are_device_configuration():
    chamber = make_fake_device(Sample_Chamber)(name="chamber")
    chamber.maxs.sim_put(0.006)
    assert chamber.pressure_state("maxs")["state"] == "INTERMEDIATE"
    chamber.pumped_below = 0.01
    assert chamber.pressure_state("maxs")["state"] == "Pumped"
    chamber.maxs.sim_put(8000)
    assert chamber.pressure_state("maxs")["state"] == "Vented"
    chamber.maxs.sim_put("LO")
    assert chamber.pressure_state("maxs")["state"] == "UNKNOWN"
    with pytest.raises(ValueError):
        chamber.pressure_state("nonexistent")


def test_crl_insertion_tolerance_is_device_configuration():
    crl = make_fake_device(CRL)("FAKE:", name="crl")
    crl.lens1.user_readback.sim_put(3)
    assert crl.read_lens_state()[1] == "OUT"
    crl.inserted_tolerance_mm = 4
    assert crl.read_lens_state()[1] == "IN"
    crl.lens2.user_readback.sim_put(float("nan"))
    assert crl.read_lens_state()[2] == "UNKNOWN"
