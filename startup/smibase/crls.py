
print(f"Loading {__file__}")

from smiclasses.crls import CRL

crl = CRL("XF:12IDC-OP:2{Lens:CRL-Ax:", name="crl")


from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([crl])