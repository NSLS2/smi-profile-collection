from smi_beamline.devices import _context
from smi_beamline.devices.crls import CRL


crl = CRL("XF:12IDC-OP:2{Lens:CRL-Ax:", name="crl")

_context.baseline_register([crl])
