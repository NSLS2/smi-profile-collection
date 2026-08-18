"""Unit tests for :mod:`smi_beamline.devices.device_factory` mode resolution.

Pure logic only -- no devices are constructed here (that is exercised in the
``sim`` tier).  Covers the documented priority order:
force > SMI_REAL_DEVICES > SMI_FAKE_DEVICES > in-process overrides > file > default.
"""
import pytest

from smi_beamline.devices import device_factory as df


@pytest.fixture(autouse=True)
def _clear_env(monkeypatch):
    monkeypatch.delenv("SMI_FAKE_DEVICES", raising=False)
    monkeypatch.delenv("SMI_REAL_DEVICES", raising=False)
    monkeypatch.delenv("SMI_DEVICE_MODES_FILE", raising=False)
    df.clear_overrides()
    yield
    df.clear_overrides()


def test_default_is_real():
    assert df.device_mode("pil2M") == df.REAL


def test_fake_all_env(monkeypatch):
    monkeypatch.setenv("SMI_FAKE_DEVICES", "all")
    assert df.device_mode("pil2M") == df.FAKE
    assert df.device_mode("anything") == df.FAKE


def test_fake_named_env(monkeypatch):
    monkeypatch.setenv("SMI_FAKE_DEVICES", "pil300KW, rayonix")
    assert df.device_mode("pil300KW") == df.FAKE
    assert df.device_mode("rayonix") == df.FAKE
    assert df.device_mode("pil2M") == df.REAL


def test_real_exempts_a_device_from_fake_all(monkeypatch):
    monkeypatch.setenv("SMI_FAKE_DEVICES", "all")
    monkeypatch.setenv("SMI_REAL_DEVICES", "energy")
    assert df.device_mode("energy") == df.REAL
    assert df.device_mode("pil2M") == df.FAKE


def test_force_argument_resolution():
    # device_mode itself doesn't take force; make_device does. Test override layer:
    df.configure_modes({"pil2M": "fake"})
    assert df.device_mode("pil2M") == df.FAKE
    df.clear_overrides()
    assert df.device_mode("pil2M") == df.REAL


def test_configure_modes_kwargs():
    df.configure_modes(linkam="fake")
    assert df.device_mode("linkam") == df.FAKE


def test_env_beats_in_process_override(monkeypatch):
    df.configure_modes({"pil2M": "fake"})
    monkeypatch.setenv("SMI_REAL_DEVICES", "pil2M")
    # explicit real env (priority 2) beats in-process override (priority 4)
    assert df.device_mode("pil2M") == df.REAL


def test_config_file(monkeypatch, tmp_path):
    f = tmp_path / "modes.csv"
    f.write_text("# name,mode\npil300KW,fake\nenergy,real\n")
    monkeypatch.setenv("SMI_DEVICE_MODES_FILE", str(f))
    assert df.device_mode("pil300KW") == df.FAKE
    assert df.device_mode("energy") == df.REAL
    assert df.device_mode("pil2M") == df.REAL  # not listed -> default


def test_parse_name_list():
    assert df._parse_name_list(None) == (set(), False)
    assert df._parse_name_list("") == (set(), False)
    assert df._parse_name_list("none") == (set(), False)
    assert df._parse_name_list("all") == (set(), True)
    names, is_all = df._parse_name_list("a, b ,c")
    assert names == {"a", "b", "c"} and is_all is False
