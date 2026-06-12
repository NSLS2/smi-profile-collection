"""Instantiate device classes against MOCK PVs (no hardware) via ``ophyd.sim.make_fake_device``.

This proves the ``smiclasses`` device classes are fully constructible off the beamline -- the
core Phase-1 capability.  ``make_fake_device`` swaps every ``EpicsSignal``/``EpicsMotor`` for an
in-memory fake, so no CA connection is attempted.  We assert each device builds, exposes the
expected components, and (where applicable) ``describe()``/``read()`` succeed.
"""
import pytest

from ophyd.sim import make_fake_device


def _fake(cls, **kwargs):
    return make_fake_device(cls)(prefix="FAKE:", name="dev", **kwargs)


def test_stg_pseudo_builds_and_has_backcompat_aliases():
    """STG_pseudo (the Huber stack) builds, and the legacy .th/.ph/.ch aliases resolve."""
    from smiclasses.manipulators import STG_pseudo

    stg = _fake(STG_pseudo)
    # pseudo axes
    for ax in ("x", "y", "z", "theta", "chi", "phi"):
        assert hasattr(stg, ax)
    # backwards-compatible aliases added in Phase 0 must point at the rotation pseudo-axes
    assert stg.th is stg.theta
    assert stg.ph is stg.phi
    assert stg.ch is stg.chi
    # aliases must NOT have leaked into the ophyd component model
    assert "th" not in stg.component_names
    assert "theta" in stg.component_names


def test_smaract_and_bdm_build():
    from smiclasses.manipulators import SMARACT, BDMStage

    piezo = _fake(SMARACT)
    for ax in ("x", "y", "z", "th", "ch"):
        assert hasattr(piezo, ax)

    bdm = _fake(BDMStage)
    for ax in ("x", "y", "th"):
        assert hasattr(bdm, ax)


def test_saxs_beamstops_build_and_describe():
    from smiclasses.beamstop import SAXSBeamStops

    bs = _fake(SAXSBeamStops)
    for ax in ("x_rod", "y_rod", "x_pin", "y_pin"):
        assert hasattr(bs, ax)
    # describe() should work against fake signals (no CA)
    assert isinstance(bs.describe(), dict)


def test_pilatus_saxs_detector_class_builds_fake_type():
    """The SAXS Pilatus class can be imported and a fake *type* built with mock PVs.

    NOTE: ``SAXS_Detector.__init__`` reads ``self.beamstop.x_pin.position`` (etc.) at
    construction time to infer the initial active-beamstop state.  On a freshly-made *fake*
    device those positions are ``None``, so full ``make_fake_device(...)()`` instantiation
    raises ``TypeError``.  That init-time hardware read is a separate device-cleanup item
    (tracked for a later phase, alongside the bdm/positioner fixes); it is NOT introduced by the
    Phase-1 decoupling.  Here we assert the class imports and the fake type is constructible, and
    that the Phase-1 deferrals hold (energyset no longer reads EPICS at class-definition).
    """
    from smiclasses.pilatus import SAXS_Detector
    from smiclasses.pilatus import PilatusDetectorCamV33

    FakeSAXS = make_fake_device(SAXS_Detector)
    assert FakeSAXS is not None
    # Phase-1 deferral: the cam's energyset default is a plain 0.0 (no class-definition EPICS
    # read).  Build the cam alone (it has no init-time .position read) to confirm.
    cam = make_fake_device(PilatusDetectorCamV33)(prefix="FAKE:cam1:", name="cam")
    assert cam.energyset.get() == 0.0


@pytest.mark.xfail(reason="SAXS_Detector.__init__ reads beamstop .position (None on a fresh "
                          "fake device); init-time hardware read is a later-phase device fix.",
                   raises=TypeError, strict=True)
def test_pilatus_saxs_detector_full_instantiation_xfail():
    """Documents the known init-time .position read; will pass once that is fixed (later phase)."""
    from smiclasses.pilatus import SAXS_Detector

    det = _fake(SAXS_Detector, asset_path="pilatus2m-test")
    assert hasattr(det, "beamstop")


def test_waxs_detector_builds_without_hardware():
    from smiclasses.pilatus import WAXS_Detector

    det = _fake(WAXS_Detector, asset_path="pilatus900kw-test")
    assert hasattr(det, "motors")
    assert hasattr(det.motors, "arc")  # the WAXS arc (arc-block readback)


def test_energy_pseudopositioner_builds_without_hardware():
    from smiclasses.energy import Energy

    en = _fake(Energy)
    assert hasattr(en, "energy")
    assert hasattr(en, "bragg")
    assert hasattr(en, "ivugap")


def test_lakeshore_and_linkam_build():
    from smiclasses.electrometers import new_LakeShore
    from smiclasses.linkam import LinkamThermal

    ls = _fake(new_LakeShore)
    assert hasattr(ls, "input_A_celsius")

    lk = _fake(LinkamThermal)
    # the readback Signal the Phase-2 Linkam-Heater fix will use
    assert hasattr(lk, "temperature_current")
