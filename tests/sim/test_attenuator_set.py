"""Tier-2 (sim) tests for the energy-aware :class:`AttenuatorSet` device.

Builds fake (non-broadcasting) attenuator banks and a fake energy source via the
``smi_beamline.devices._context`` seam, then checks that the device:

* reports an attenuation factor / transmission / text description for the inserted foils
  at the current energy,
* recomputes when the energy changes (so it works as a per-point primary reading), and
* ``set(target_factor)`` selects the fewest foils, drives the banks, and records the
  ACTUAL achieved factor (not the request).
"""
import pytest

from ophyd.sim import make_fake_device

from smi_beamline.devices import _context
from smi_beamline.devices.attenuators import AttenuatorSet, make_attenuator_bank


# ---------------------------------------------------------------------------
# fakes
# ---------------------------------------------------------------------------
class _FakeEnergy:
    """Minimal stand-in for the energy pseudo-positioner: ``.energy.readback.get()``."""

    class energy:
        class readback:
            _v = 10000.0

            @classmethod
            def get(cls):
                return cls._v

    @classmethod
    def set_eV(cls, v):
        cls.energy.readback._v = float(v)


def _fake_bank(pfx, name):
    Bank = make_attenuator_bank("Bank%s" % pfx, "XF:12IDC-OP:2{{Fltr:%s-{}}}" % pfx, range(1, 13))
    bank = make_fake_device(Bank)("", name=name)
    for n in bank.component_names:
        f = getattr(bank, n)
        f.settle_time = 0.05
        f.max_retries = 3
        f.timeout = 3.0
        f.retry_delay = 0.05
        f.cmd_timeout = 0.2
        # reliable open + close
        f.open_cmd.subscribe(lambda value, f=f, **k: f.status.sim_put("Open"), run=False)
        f.close_cmd.subscribe(lambda value, f=f, **k: f.status.sim_put("Not Open"), run=False)
        f.status.sim_put("Not Open")
    return bank


@pytest.fixture
def attset():
    _FakeEnergy.set_eV(10000.0)
    _context.configure(energy_source=_FakeEnergy())
    b1 = _fake_bank("1", "attenuators1")
    b2 = _fake_bank("2", "attenuators2")
    att = AttenuatorSet("", name="attenuation", banks=[b1, b2], bank_prefixes=["1", "2"])
    # speed up the selection-policy defaults for the test
    att.max_foils.put(4)
    att.tolerance.put(0.10)
    return att, b1, b2


# ---------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------
def test_no_foils_reports_unity(attset):
    att, b1, b2 = attset
    info = att.compute()
    assert info["attenuation_factor"] == 1.0
    assert info["transmission"] == 1.0
    assert info["inserted"] == []
    assert "none" in info["description"].lower()


def test_reports_factor_and_description_for_inserted_foils(attset):
    att, b1, b2 = attset
    # manually insert a known foil (att2_1 == Mo 20um) and one Cu (att1_1)
    b2.f1.status.sim_put("Open")
    b1.f1.status.sim_put("Open")
    info = att.compute()
    assert set(info["inserted"]) == {"1_1", "2_1"}
    assert info["attenuation_factor"] > 1.0
    # description names both foils + their materials
    assert "att1_1" in info["description"] and "Cu" in info["description"]
    assert "att2_1" in info["description"] and "Mo" in info["description"]
    # factor is the product of the two single-foil factors (transmissions multiply)
    from smi_beamline.devices import attenuator_data as ad
    expected = ad.attenuation_factor(["1_1", "2_1"], 10000.0)
    assert info["attenuation_factor"] == pytest.approx(expected, rel=1e-9)


def test_recomputes_when_energy_changes(attset):
    att, b1, b2 = attset
    b2.f1.status.sim_put("Open")            # Mo 20um
    att.trigger().wait(timeout=2)
    f_10kev = att.attenuation_factor.get()
    _FakeEnergy.set_eV(18000.0)
    att.trigger().wait(timeout=2)
    f_18kev = att.attenuation_factor.get()
    assert att.energy_eV.get() == 18000.0
    # Mo is much more transparent at 18 keV than 10 keV -> smaller factor
    assert f_18kev < f_10kev


# ---------------------------------------------------------------------------
# setting a target
# ---------------------------------------------------------------------------
def test_set_factor_selects_and_drives_foils(attset):
    att, b1, b2 = attset
    st = att.set(100)
    st.wait(timeout=10)
    assert st.success
    inserted = att.inserted.get()
    assert 1 <= len(inserted) <= 4
    # the foils the device says are in are actually Open on the banks
    for label in inserted:
        bank = b1 if label.startswith("1_") else b2
        child = getattr(bank, "f" + label.split("_", 1)[1])
        assert child.status.get() == "Open"
    # recorded factor is within tolerance of the request and matches the inserted foils
    assert att.within_tolerance.get() is True
    assert abs(att.attenuation_factor.get() / 100 - 1.0) <= 0.10


def test_set_records_actual_not_requested(attset):
    att, b1, b2 = attset
    att.set(100).wait(timeout=10)
    # requested is stored separately; the reported factor is the ACHIEVED one
    assert att.requested_factor.get() == 100
    assert att.attenuation_factor.get() != 100      # achieved value, not the request
    assert abs(att.attenuation_factor.get() - 100) / 100 <= 0.10


def test_set_one_retracts_all(attset):
    att, b1, b2 = attset
    att.set(100).wait(timeout=10)
    assert att.inserted.get()                      # something is in
    att.set(1).wait(timeout=10)
    assert att.inserted.get() == []                # all retracted
    assert att.attenuation_factor.get() == 1.0
    for bank in (b1, b2):
        assert bank.inserted_foils() == []


def test_set_for_planned_energy(attset):
    att, b1, b2 = attset
    # current energy is 10 keV but we stage attenuation for a PLANNED 18 keV
    labels, factor, ok, energy = att.describe_factor(50, energy_eV=18000.0)
    assert energy == 18000.0
    st = att.set_for_energy(50, 18000.0)
    st.wait(timeout=10)
    assert att.energy_eV.get() == 18000.0
    assert set(att.inserted.get()) == set(labels)


def test_set_out_of_tolerance_warns_but_applies(attset, caplog):
    att, b1, b2 = attset
    att.tolerance.put(0.001)        # absurdly tight (0.1%) -> 3.3x cannot be matched
    att.set(3.3).wait(timeout=10)
    # it still applied a combination and flagged out-of-tolerance
    assert att.within_tolerance.get() is False
    assert att.inserted.get() != []                 # the best-effort combo was applied
    # and the reported factor is the ACTUAL achieved one (used the closest combo)
    assert att.attenuation_factor.get() != 1.0


# ---------------------------------------------------------------------------
# start-document metadata: setting/changing attenuation must update RE.md so the
# value lands in the START document of the next run (bluesky snapshots RE.md at open_run).
# ---------------------------------------------------------------------------
def test_state_md_shape():
    """state_md() returns the per-foil + overall dict written to RE.md."""
    _FakeEnergy.set_eV(10000.0)
    _context.configure(energy_source=_FakeEnergy())
    b1 = _fake_bank("1", "attenuators1")
    b2 = _fake_bank("2", "attenuators2")
    att = AttenuatorSet("", name="attenuation", banks=[b1, b2], bank_prefixes=["1", "2"])
    b2.f1.status.sim_put("Open")     # Mo 20um
    md = att.state_md()
    assert set(md) == {"foils", "attenuation_factor", "transmission", "energy_eV", "description"}
    assert "att2_1" in md["foils"]
    assert md["foils"]["att2_1"] == {"material": "Mo_20um", "thickness": "1x"}
    assert md["attenuation_factor"] > 1.0


def test_set_updates_RE_md():
    """A set() writes RE.md[md_key] immediately (via the context seam)."""
    from bluesky import RunEngine
    import bluesky.plan_stubs as bps

    _FakeEnergy.set_eV(10000.0)
    RE = RunEngine({})
    _context.configure(run_engine=RE, energy_source=_FakeEnergy())
    b1 = _fake_bank("1", "attenuators1")
    b2 = _fake_bank("2", "attenuators2")
    att = AttenuatorSet("", name="attenuation", banks=[b1, b2], bank_prefixes=["1", "2"])

    assert att.md_key not in RE.md
    RE(bps.mv(att, 100))
    entry = RE.md[att.md_key]
    assert abs(entry["attenuation_factor"] / 100 - 1.0) <= 0.10
    assert entry["foils"]                       # named foils present
    assert "att" in entry["description"]


def test_change_lands_in_next_start_document():
    """After changing attenuation, the NEXT run's start document carries the new value."""
    from bluesky import RunEngine
    from bluesky.plans import count
    from ophyd.sim import det
    import bluesky.plan_stubs as bps

    _FakeEnergy.set_eV(10000.0)
    RE = RunEngine({})
    _context.configure(run_engine=RE, energy_source=_FakeEnergy())
    b1 = _fake_bank("1", "attenuators1")
    b2 = _fake_bank("2", "attenuators2")
    att = AttenuatorSet("", name="attenuation", banks=[b1, b2], bank_prefixes=["1", "2"])

    docs = []
    RE(bps.mv(att, 100))
    RE(count([det], num=1), lambda n, d: docs.append((n, d)))
    start = next(d for n, d in docs if n == "start")
    assert att.md_key in start
    assert abs(start[att.md_key]["attenuation_factor"] / 100 - 1.0) <= 0.10

    # change attenuation -> next run reflects it
    docs.clear()
    RE(bps.mv(att, 1))                          # retract all
    RE(count([det], num=1), lambda n, d: docs.append((n, d)))
    start2 = next(d for n, d in docs if n == "start")
    assert start2[att.md_key]["attenuation_factor"] == 1.0
    assert start2[att.md_key]["foils"] == {}


def test_md_write_is_noop_without_run_engine(attset):
    """Off-beamline (no RE wired) compute() must not raise even though it mirrors to RE.md."""
    att, b1, b2 = attset           # this fixture wires only the energy source, not an RE
    # get_md() returns a throwaway {}; compute() should still succeed
    info = att.compute()
    assert info["attenuation_factor"] == 1.0

