"""Unit tests for the ``smi_beamline.devices._context`` dependency seam.

The seam lets device classes reach ``RE.md`` / ``mdsave`` / current-energy without importing
``smibase``.  It must degrade gracefully when unconfigured (so tests / off-beamline import work)
and read injected objects by reference when configured (so live ``RE.md`` mutations are seen).
"""
from smi_beamline.devices import _context


def test_unconfigured_defaults_are_safe():
    # autouse fixture leaves the seam unconfigured
    assert _context.is_configured() is False
    assert _context.get_md() == {}
    assert _context.get_config() == {}
    assert _context.current_energy_eV() is None


def test_configure_md_and_config_by_reference():
    class _FakeRE:
        def __init__(self):
            self.md = {"data_session": "pass-1", "cycle": "2026-1"}

    re = _FakeRE()
    cfg = {"saxs_beam_offset_x_mm": 100.0}
    _context.configure(run_engine=re, config_dict=cfg)

    assert _context.is_configured() is True
    assert _context.get_md()["data_session"] == "pass-1"
    assert _context.get_config()["saxs_beam_offset_x_mm"] == 100.0

    # stored by reference: later RE.md mutation is visible
    re.md["data_session"] = "pass-2"
    assert _context.get_md()["data_session"] == "pass-2"


def test_current_energy_from_callable():
    _context.configure(energy_source=lambda: 2450.0)
    assert _context.current_energy_eV() == 2450.0


def test_current_energy_from_object_with_readback():
    class _RB:
        def get(self):
            return 8980.0

    class _E:
        class energy:
            readback = _RB()

    _context.configure(energy_source=_E())
    assert _context.current_energy_eV() == 8980.0


def test_current_energy_never_raises_on_bad_source():
    _context.configure(energy_source=lambda: (_ for _ in ()).throw(RuntimeError("no PV")))
    # should swallow the error and return None, not raise
    assert _context.current_energy_eV() is None


def test_sd_bec_db_injection_and_accessors():
    assert _context.get_sd() is None and _context.get_bec() is None and _context.get_db() is None
    sd, bec, db = object(), object(), object()
    _context.configure(sd=sd, bec=bec, db=db)
    assert _context.get_sd() is sd
    assert _context.get_bec() is bec
    assert _context.get_db() is db


def test_baseline_register_noop_when_unconfigured():
    # no sd injected -> returns False, never raises (keeps modules importable headless)
    assert _context.baseline_register("anything") is False


def test_baseline_register_accepts_args_and_iterable():
    class _FakeSD:
        def __init__(self):
            self.baseline = []

    sd = _FakeSD()
    _context.configure(sd=sd)
    # individual args
    assert _context.baseline_register("a", "b") is True
    # a single iterable (the form the instance modules use)
    _context.baseline_register(["c", "d"])
    assert sd.baseline == ["a", "b", "c", "d"]
