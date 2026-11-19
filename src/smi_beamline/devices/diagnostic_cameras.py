"""Overlay-only diagnostic camera interfaces, without acquisition or file writing.

Plain Devices avoid the automatic enable-on-stage behavior of detector plugins.
SignalWithRBV reads *_RBV and writes the matching setting only on explicit put/set.
"""

from collections import OrderedDict

from ophyd import Component as Cpt
from ophyd import Device, EpicsSignal, EpicsSignalRO
from ophyd.areadetector.base import EpicsSignalWithRBV as SignalWithRBV
from ophyd.device import create_device_from_components


class CameraOverlay(Device):
    """One overlay's geometry, appearance, and individual enable setting."""

    blue = Cpt(SignalWithRBV, "Blue")
    center_x = Cpt(SignalWithRBV, "CenterX")
    center_y = Cpt(SignalWithRBV, "CenterY")
    draw_mode = Cpt(SignalWithRBV, "DrawMode")
    green = Cpt(SignalWithRBV, "Green")
    overlay_portname = Cpt(SignalWithRBV, "Name", string=True)
    position_x = Cpt(SignalWithRBV, "PositionX")
    position_y = Cpt(SignalWithRBV, "PositionY")
    red = Cpt(SignalWithRBV, "Red")
    shape = Cpt(SignalWithRBV, "Shape")
    size_x = Cpt(SignalWithRBV, "SizeX")
    size_y = Cpt(SignalWithRBV, "SizeY")
    use = Cpt(SignalWithRBV, "Use")
    width_x = Cpt(SignalWithRBV, "WidthX")
    width_y = Cpt(SignalWithRBV, "WidthY")


class CameraOverlays(Device):
    """Eight overlay slots; no automatic enable-on-stage behavior."""

    overlay_1 = Cpt(CameraOverlay, "1:", kind="config")
    overlay_2 = Cpt(CameraOverlay, "2:", kind="config")
    overlay_3 = Cpt(CameraOverlay, "3:", kind="config")
    overlay_4 = Cpt(CameraOverlay, "4:", kind="config")
    overlay_5 = Cpt(CameraOverlay, "5:", kind="config")
    overlay_6 = Cpt(CameraOverlay, "6:", kind="config")
    overlay_7 = Cpt(CameraOverlay, "7:", kind="config")
    overlay_8 = Cpt(CameraOverlay, "8:", kind="config")


class DiagnosticCamera(Device):
    """Camera overlay configuration, without an assumed acquisition driver."""

    over1 = Cpt(CameraOverlays, "Over1:", kind="config", lazy=True)


class CameraPluginRouting(Device):
    """Only plugin ports and callback enable; no acquisition/statistics controls."""

    enable = Cpt(SignalWithRBV, "EnableCallbacks")
    nd_array_port = Cpt(EpicsSignal, "NDArrayPort", string=True)
    port_name = Cpt(EpicsSignalRO, "PortName_RBV", string=True)


# Exact case-sensitive plugin prefixes supplied for the OAV IOC only.
OAV_PLUGIN_PREFIXES = (
    "Attr1",
    "Bar1",
    "CB1",
    "CC1",
    "CC2",
    "CV1",
    "Codec1",
    "Codec2",
    "Edge1",
    "FFT1",
    "Gather1",
    "HDF1",
    "JPEG1",
    "Magick1",
    "Nexus1",
    "Over1",
    "Proc1",
    "Pva1",
    "ROI1",
    "ROI2",
    "ROI3",
    "ROI4",
    "ROIStat1",
    "Scatter1",
    "Stats1",
    "Stats2",
    "Stats3",
    "Stats4",
    "Stats5",
    "TIFF1",
    "Trans1",
    "image1",
    "netCDF1",
)


OAVPluginRouting = create_device_from_components(
    "OAVPluginRouting",
    **OrderedDict(
        (
            prefix.lower(),
            Cpt(CameraPluginRouting, prefix + ":", kind="config", lazy=True),
        )
        for prefix in OAV_PLUGIN_PREFIXES
    ),
)


class CameraTransform(Device):
    """ADCore >=2.1 rotation/reflection setting; IOC presence needs verification.

    The modern transform plugin uses Type, not the legacy Type1--Type4 chain.
    This follows ophyd's TransformPlugin_V21 mapping; no Type_RBV is assumed.
    """

    type_ = Cpt(EpicsSignal, "Type", string=True, lazy=True)


class OAVConfiguration(Device):
    """OAV-only transform and routing sidecar, independent of image acquisition."""

    plugins = Cpt(OAVPluginRouting, "", kind="config", lazy=True)
    trans1 = Cpt(CameraTransform, "Trans1:", kind="config", lazy=True)
