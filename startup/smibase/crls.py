
print(f"Loading {__file__}")

from ..smiclasses import CRL

crl = CRL("XF:12IDC-OP:2{Lens:CRL-Ax:", name="crl")


from .base import sd

sd.baseline.extend([crl])