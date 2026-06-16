

from smiclasses.crls import CRL

crl = CRL("XF:12IDC-OP:2{Lens:CRL-Ax:", name="crl")


from smiclasses import _context

_context.baseline_register([crl])

