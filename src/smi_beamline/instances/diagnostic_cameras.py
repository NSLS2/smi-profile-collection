"""Diagnostic module overlays, using operator-supplied IOC prefixes."""

from smi_beamline.devices.device_factory import make_device
from smi_beamline.devices.diagnostic_cameras import DiagnosticCamera, OAVConfiguration

__all__ = ["OAV_config", "cam9", "cam10"]

cam9 = make_device(DiagnosticCamera, "XF:12ID2-OP{GigE-Cam:9}", name="cam9")
cam10 = make_device(DiagnosticCamera, "XF:12ID2-OP{GigE-Cam:10}", name="cam10")
OAV_config = make_device(OAVConfiguration, "XF:12IDC-BI{Cam:SAM}", name="OAV_config")
