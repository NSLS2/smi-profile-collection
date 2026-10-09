# Alignment fit recovery

The height and angular scan helpers in `smi_beamline.plans.alignment` share
bounded scan/fit/move recovery. This includes the helpers used by
`alignement_gisaxs_hex`, the other GISAXS variants, XRR, and BDM alignment.

Before moving to a result, they require a successful fit with a finite center
inside the measured interval and a measured feature away from the scan's end.
For derivative scans, the strongest **absolute** intensity change locates the
feature, so falling edges are handled as well as rising edges.

If the result fails these checks, the next scan is centered at the scan endpoint
nearest the measured feature. It retains the original width and number of points.
The direction comes from the data, not an extrapolated fitted center. For example,
a scan from 1.5 to 2.5 whose strongest change is at the low end is repeated from
1.0 to 2.0, centered at 1.5.

Each helper permits three additional scans by default. Override this when calling
a helper directly, for example:

```python
RE(align_gisaxs_height_hex(0.5, 21, der=True, max_retries=2))
```

`max_retries=0` retains validation but disables rescans. Existing top-level
alignment calls use the default automatically.

The plan stops with a descriptive `RuntimeError` if it exhausts its retries,
would revisit a previous scan center, has flat/non-finite data with no usable
feature, or cannot fit the next full scan within motor limits. Endpoint checks
use the motor's `check_value`, including transformed real-axis limits for the
hexapod pseudo motors, and happen **before** the recenter move. Scans return to
their current scan center before analysis; a rejected fit is never sent to the
motor. Each recovery attempt prints the rejected result and the next center.

`ps()` continues to expose `cen`, `peak`, `com`, and `fwhm`, with additional
`x_data`, `y_data`, `fit_kind`, and `fit_success` attributes for validation. Its
step-fit initial slope scales with the scan width, and previous results are
cleared before analyzing each run.
