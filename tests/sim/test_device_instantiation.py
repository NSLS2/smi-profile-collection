"""Build the device classes as FAKE devices through :mod:`smiclasses.device_factory`.

This proves the ``smiclasses`` device classes are fully constructible off the
beamline via the same factory the live profile uses (``force="fake"`` here;
``SMI_FAKE_DEVICES=all`` in production).  ``make_fake_device`` swaps every
``EpicsSignal``/``EpicsMotor`` for an in-memory fake, so no CA connection is
attempted.  We assert each device builds, exposes the expected components, and
(where applicable) ``describe()``/``read()`` succeed.
"""
from smiclasses import device_factory as df
import pytest


def test_factory_records_mode_and_registry(make_fake):
    from smiclasses.manipulators import SMARACT

    piezo = make_fake(SMARACT, name="piezo")
    assert ("piezo") in df.registered()
    mode, inst = df.registry()["piezo"]
    assert mode == df.FAKE
    assert inst is piezo


def test_stg_pseudo_builds_and_has_backcompat_aliases(make_fake):
    """STG_pseudo (the Huber stack) builds, and the legacy .th/.ph/.ch aliases resolve."""
    from smiclasses.manipulators import STG_pseudo

    stg = make_fake(STG_pseudo, name="stage")
    for ax in ("x", "y", "z", "theta", "chi", "phi"):
        assert hasattr(stg, ax)
    # backwards-compatible aliases added in Phase 0 must point at the rotation pseudo-axes
    assert stg.th is stg.theta
    assert stg.ph is stg.phi
    assert stg.ch is stg.chi
    # aliases must NOT have leaked into the ophyd component model
    assert "th" not in stg.component_names
    assert "theta" in stg.component_names


def test_smaract_and_bdm_build(make_fake):
    from smiclasses.manipulators import SMARACT, BDMStage

    piezo = make_fake(SMARACT, name="piezo")
    for ax in ("x", "y", "z", "th", "ch"):
        assert hasattr(piezo, ax)

    bdm = make_fake(BDMStage, name="bdm")
    for ax in ("x", "y", "th"):
        assert hasattr(bdm, ax)


def test_saxs_beamstops_build_and_describe(make_fake):
    from smiclasses.beamstop import SAXSBeamStops

    bs = make_fake(SAXSBeamStops, name="bs")
    for ax in ("x_rod", "y_rod", "x_pin", "y_pin"):
        assert hasattr(bs, ax)
    # describe() should work against fake signals (no CA)
    assert isinstance(bs.describe(), dict)


def test_pilatus_cam_builds_without_class_definition_epics_read(make_fake):
    """Phase-1 deferral: the cam's energyset default is a plain 0.0 (no class-definition EPICS read)."""
    from smiclasses.pilatus import PilatusDetectorCamV33

    cam = make_fake(PilatusDetectorCamV33, name="cam", prefix="FAKE:cam1:")
    assert cam.energyset.get() == 0.0


def test_saxs_detector_full_instantiation(make_fake):
    """SAXS_Detector now builds fully as a fake.

    Its ``__init__`` and the immediate ``update_beam_center`` subscription read
    ``.position`` on the beamstop/detector motors.  Those reads are now guarded
    against unconnected (``None``) positioners, so a fresh fake builds cleanly
    and leaves ``active_beamstop`` at its 'none' default.  (Previously xfail.)
    """
    from smiclasses.pilatus import SAXS_Detector

    det = make_fake(SAXS_Detector, name="pil2M", asset_path="pilatus2m-test")
    assert hasattr(det, "beamstop")
    assert det.active_beamstop.get() == "none"


def test_factory_seed_sets_fake_signal_values(make_fake):
    """The factory ``seed=`` applies values *after* construction (e.g. to put a
    device in a known state before a plan).  Verify a seeded readback reads back.

    (Note: seed runs post-__init__, so it cannot influence init-time inference
    such as SAXS_Detector.active_beamstop; use ``force``/component defaults for that.)
    """
    from smiclasses.beamstop import SAXSBeamStops

    bs = make_fake(SAXSBeamStops, name="bs", seed={"x_rod.user_readback": 6.8})
    assert bs.x_rod.position == pytest.approx(6.8)


def test_waxs_detector_builds_without_hardware(make_fake):
    from smiclasses.pilatus import WAXS_Detector

    det = make_fake(WAXS_Detector, name="pil900KW", asset_path="pilatus900kw-test")
    assert hasattr(det, "motors")
    assert hasattr(det.motors, "arc")  # the WAXS arc (arc-block readback)


def test_energy_pseudopositioner_builds_without_hardware(make_fake):
    from smiclasses.energy import Energy

    en = make_fake(Energy, name="energy")
    assert hasattr(en, "energy")
    assert hasattr(en, "bragg")
    assert hasattr(en, "ivugap")


def test_lakeshore_and_linkam_build(make_fake):
    from smiclasses.electrometers import new_LakeShore
    from smiclasses.linkam import LinkamThermal

    ls = make_fake(new_LakeShore, name="lakeshore")
    assert hasattr(ls, "input_A_celsius")

    # output1..4 are now PROPER Components (M6): they appear in the device tree and were faked
    # (not left holding real EpicsSignals).
    for n in ("output1", "output2", "output3", "output4"):
        assert n in ls.component_names
        out = getattr(ls, n)
        for sig in ("P", "I", "D", "temp_set_point", "status"):
            assert hasattr(out, sig)
        # the fake makes signals settable in memory; if they were real EpicsSignals this would
        # try to hit CA.
        out.P.set(1.0).wait(timeout=1)

    lk = make_fake(LinkamThermal, name="linkam")
    # the readback Signal the Phase-2 Linkam-Heater fix will use
    assert hasattr(lk, "temperature_current")


def test_lakeshore_d_gain_points_at_d_pv():
    """The D (derivative) gain must address Gain:D-SP, not Gain:I-SP (a 2022 copy-paste bug)."""
    from smiclasses.electrometers import output_lakeshore

    # Inspect the Component suffixes directly -- no instantiation, so no CA contact.
    assert output_lakeshore.I.suffix == "Gain:I-SP"
    assert output_lakeshore.D.suffix == "Gain:D-SP"
    assert output_lakeshore.D.suffix != output_lakeshore.I.suffix
