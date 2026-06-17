"""Unit tests for the scan-name templating engine + registry-based wiring.

Pure code: these construct **no** devices and do **not** run a RunEngine.  The message-level
behaviour (read injection, append-on-open_run, collision-safety) is covered in
``tests/sim/test_scan_naming_preprocessor.py``.
"""
import pytest

from smi_beamline.devices import _plan_helpers as ph
from smi_beamline.plans import scan_naming as sn


# --------------------------------------------------------------------------- template parsing
def test_template_field_names_basic():
    assert ph.template_field_names("t_{energy_energy:.1f}eV_{waxs_arc:04.1f}wa") == [
        "energy_energy", "waxs_arc"
    ]


def test_template_field_names_dedup_and_order():
    # repeated token -> listed once, first-seen order preserved
    assert ph.template_field_names("{b}_{a}_{b:.1f}") == ["b", "a"]


def test_template_field_names_strips_attr_and_index():
    assert ph.template_field_names("{dev.sub}_{arr[0]}") == ["dev", "arr"]


def test_template_field_names_ignores_positional_and_empty():
    assert ph.template_field_names("plain text, no tokens") == []
    assert ph.template_field_names("{}_{x}") == ["x"]
    assert ph.template_field_names("") == []
    assert ph.template_field_names(None) == []


# --------------------------------------------------------------------------- Token primitive
def test_token_keys_parses_its_fragment():
    assert sn.Token("{energy_energy:.2f}eV", "energy").keys == ["energy_energy"]
    assert sn.Token("plain", "").keys == []


# --------------------------------------------------------------------------- registry / sets
def test_default_sets_are_known():
    assert all(name in sn.MEASUREMENT_SETS for name in sn.DEFAULT_SETS)


def test_active_tokens_default_is_energy_waxs_sdd():
    toks = sn.active_tokens()  # defaults to DEFAULT_SETS
    keys = [k for t in toks for k in t.keys]
    assert keys == ["energy_energy", "waxs_arc", "pil2M_motor_z"]


def test_active_tokens_unknown_set_raises():
    with pytest.raises(KeyError):
        sn.active_tokens(["energy", "not_a_set"])


def test_build_template_default_matches_constant():
    assert sn.build_template() == sn.DEFAULT_SCAN_NAME_TEMPLATE
    assert sn.build_template() == "{energy_energy:.2f}eV_wa{waxs_arc:04.1f}_sdd{pil2M_motor_z:.1f}mm"


def test_build_template_subset_and_order():
    # selecting/ordering sets controls the filename layout
    assert sn.build_template(["sdd", "energy"]) == "sdd{pil2M_motor_z:.1f}mm_{energy_energy:.2f}eV"


def test_build_template_with_flux_set():
    assert sn.build_template(["energy", "flux"]) == "{energy_energy:.2f}eV_xbpm{xbpm2_sumX:.3f}"


# --------------------------------------------------------------------------- default template
def test_default_template_tokens_match_known_record_keys():
    # The default template must only reference the keys the active sets know how to record.
    keys = set(ph.template_field_names(sn.DEFAULT_SCAN_NAME_TEMPLATE))
    assert keys == {"energy_energy", "waxs_arc", "pil2M_motor_z"}


def test_default_template_is_str_format_renderable():
    # It must render with str.format given the recorded values (this is what the worker does).
    vals = {"energy_energy": 16100.0, "waxs_arc": 20.0, "pil2M_motor_z": 8300.0}
    out = sn.DEFAULT_SCAN_NAME_TEMPLATE.format(**vals)
    assert out == "16100.00eV_wa20.0_sdd8300.0mm"


def test_arc_token_is_zero_padded_width4():
    # mirrors get_scan_md's zfill(4) on the arc value
    assert sn.DEFAULT_SCAN_NAME_TEMPLATE.format(
        energy_energy=1, waxs_arc=2.5, pil2M_motor_z=1
    ).count("wa02.5") == 1


# --------------------------------------------------------------------------- build_token_devices
class _Dev:
    def __init__(self, name):
        self.name = name


def test_build_token_devices_resolves_from_namespace():
    ns = {"energy": _Dev("e"), "waxs": _Dev("w"), "pil2m_pos": _Dev("p")}
    td = sn.build_token_devices(ns)  # default sets
    assert set(td) == {"energy_energy", "waxs_arc", "pil2M_motor_z"}
    assert td["energy_energy"] is ns["energy"]
    assert td["pil2M_motor_z"] is ns["pil2m_pos"]


def test_build_token_devices_skips_missing_devices():
    ns = {"energy": _Dev("e")}  # waxs / pil2m_pos absent
    td = sn.build_token_devices(ns)
    assert td == {"energy_energy": ns["energy"]}


def test_build_token_devices_honors_set_selection():
    ns = {"energy": _Dev("e"), "xbpm2": _Dev("x")}
    td = sn.build_token_devices(ns, ["energy", "flux"])
    assert set(td) == {"energy_energy", "xbpm2_sumX"}


# --------------------------------------------------------------------------- preprocessor factory
def test_make_scan_name_preprocessor_returns_callable():
    pp = sn.make_scan_name_preprocessor(token_devices={}, base_name="x")
    assert callable(pp)


def test_make_scan_name_preprocessor_defaults_template():
    pp = sn.make_scan_name_preprocessor(token_devices={})
    # the partial carries the default template
    assert pp.keywords["template"] == sn.DEFAULT_SCAN_NAME_TEMPLATE
