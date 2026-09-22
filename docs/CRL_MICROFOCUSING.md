# CRL microfocusing — initial optics study

Branch: `feature/crl-microfocusing`.

## Results and report

- [PDF report](crl_report/crl_optics_report.pdf): inventory, assumptions, individual
  focal-length curves, recommended combinations/Z, energy bands, and curvature sensitivity.
- [Selection plot](crl_report/selection.png)
- [Focal-length plot](crl_report/focal_lengths.png)
- [Curvature sensitivity](crl_report/curvature_sensitivity.png)
- [10 eV lookup table](crl_report/lookup.csv)
- [Analytic selection bands](crl_report/selection_bands.csv)

With a **615 mm lens-to-sample distance at Z=0**, positive Z toward the sample,
and provisional travel **−50 to +250 mm**, the image-distance range is **365–665 mm**.
For collimated input the model predicts coverage from **2.1–2.6052 keV** and
**2.9180–24 keV**, with a gap between these intervals. Boundaries are approximate
physical predictions, despite being calculated analytically within the model.
The preferred configurations use at most four holders across this range.

All 255 nonempty subsets of the eight populated holders are considered. Selection
minimizes **inserted holders**, then individual lens elements, then holder numbers
for a deterministic tie-break. This is not an optimization of transmission or spot
size. For example, a single holder containing eight lenses can outrank two holders
containing fewer lenses. No continuity/hysteresis penalty is applied, so some
switches require substantial Z jumps. Alternative solutions are available through
`focus_candidates()`.

## Inventory

| Holder | Contents | Nominal IN (mm) | OUT (mm) |
|---|---|---:|---:|
| 1 | 1 × 50 µm | 0 | +10 |
| 2 | 8 × 50 µm | 0 | +10 |
| 3 | 16 × 50 µm | 0 | +10 |
| 4 | 4 × 50 µm | 0 | +10 |
| 5 | 2 × 50 µm | 0 | +10 |
| 6 | Empty | 0 | +10 |
| 7 | Empty | 0 | −10 |
| 8 | Empty | 0 | −10 |
| 9 | 1 × 200 µm | 0 | −10 |
| 10 | 8 × 500 µm | 0 | −10 |
| 11 | 1 × 500 µm | 0 | −10 |
| 12 | 2 mm aperture | 0 | −10 |

The lens sizes are assumed to be **per-surface radii**, each lens is assumed to have
two parabolic refracting surfaces, and all lenses are provisionally diamond.
Nominal IN=0 is not a measured alignment; expected alignment search is about ±2 mm.
Empty holders and the aperture contribute no refractive power and are excluded from
selection. Aperture-12 insertion policy is pending the optics review.

## Model

`src/smi_beamline/devices/crl_optics.py` uses only the standard library, and neither
imports device instances nor accesses EPICS. It computes the free-electron estimate

```text
delta(E) = r_e * lambda(E)^2 * n_e / (2*pi)
n_e = (rho / carbon atomic weight) * N_A * 6
P(E) = 1/f(E) = 2 * delta(E) * sum(N_i/R_i)
```

Density is 3.515 g/cm³ and carbon atomic weight is 12.011 g/mol. Constants and unit
conversions are explicit in `diamond_delta()`. At 10 keV, delta is approximately
7.29009×10⁻⁶, and one R=50 µm lens has f≈3.429 m. This is an **E⁻² approximation**
to delta using carbon scattering factor f1=6; it is not a Henke/CXRO optical-constant
table. Carbon's absorption edge lies below this energy range, but dispersion
corrections have not been quantified here. A future refinement can compare tabulated
carbon f1 and absorption data, then recalculate the band boundaries numerically.

The common-plane thin-lens approximation adds powers, ignoring individual holder
positions, element spacing, and stack thickness. Holder-dependent principal-plane
shifts could matter given the 300 mm available Z travel.

For a noncollimated beam define curvature `C0` at the **Z=0 reference plane**:

```text
C0 = ray slope / ray height                  [1/m]
C(Z) = C0 / (1 + C0 * Z_in_metres)
1/q = P - C(Z)
q = (sample_distance_mm - Z_mm) / 1000       [m]
```

Positive curvature means divergence; negative means convergence. A signed radius
of +10 m corresponds to C0=+0.1/m. A fixed upstream point source a distance p from
the Z=0 plane corresponds to C0=1/p; a downstream focus a distance d away to C0=−1/d.
This parameter describes wavefront curvature, not incoherent angular divergence.
The code propagates curvature as Z changes and solves the conjugate equation,
including both real roots when applicable. Multiple in-range roots for the same
combination are ranked by travel margin, then Z. Curvatures that place an incident
beam focus in the lens travel are rejected.

Distinct horizontal and vertical curvatures can be evaluated with separate models;
in general they will not share a common best-focus Z. Gaussian-beam diffraction,
source emittance, aberrations, transmission, and spot sizes are not predicted.
Those need more beam and lens dimensions. A curvature of ±0.1/m shifts the calculated
Z by tens of millimetres, so even a weak departure from collimation matters.

## Usage with the existing CRL object

Existing components remain `EpicsMotor`s with their original PV suffixes:
`crl.lens1` … `crl.lens12`, `crl.x`, `crl.y`, `crl.z`, `crl.ph`, `crl.th`.
The added methods are **calculations only**, using explicit **keV** inputs:

```python
crl.lens_inventory                       # immutable inventory and nominal positions
solution = crl.recommend_focus(10.0)      # no motor read or movement
solution.holders                        # (2,)
solution.z_mm                           # approximately +186.34 mm
solution.focal_length_mm                 # approximately 428.66 mm
crl.focus_candidates(10.0)               # ranked alternatives
crl.focal_length(10.0, holders=[1, 9])    # effective focal length in mm
```

Do not pass the beamline energy motor's eV value without converting it to keV.
Out-of-range and nonfinite energies are rejected. Within the supported energy
range, `recommend_focus()` raises `NoFocusSolution` for an unreachable energy;
`focus_candidates()` returns an empty tuple. There is no clamping to a travel limit.

For geometry/curvature changes or a chosen end-of-travel margin:

```python
from smi_beamline.devices.crl_optics import CRLGeometry, CRLModel, NoFocusSolution

geometry = CRLGeometry(
    sample_distance_mm=615,
    z_min_mm=-45,                       # example 5 mm margin
    z_max_mm=245,
    incident_curvature_per_m=0.02,      # example +50 m radius at Z=0
)
solution = crl.recommend_focus(10, geometry=geometry)
model = CRLModel(geometry)              # also usable without any CRL device
bands = model.selection_bands()
```

Lookup CSV sampling is 10 eV; exact boundaries for this analytic model are in the
selection-band CSV. **Never interpolate Z across a holder change or coverage gap.**
Evaluate `recommend()` at the desired energy. At shared band endpoints multiple
combinations may be feasible; the recommendation uses the stated ranking.

## Reproduce and validate

From the repository root, with the existing pixi test environment:

```bash
PYTHONPATH=src .pixi/envs/test/bin/python scripts/crl_optics_report.py --output docs/crl_report
.pixi/envs/test/bin/python -m pytest tests/unit/test_crl_optics.py tests/sim/test_crl.py
```

The report script accepts `--sample-distance-mm`, `--z-min-mm`, `--z-max-mm`, and
`--incident-curvature-per-m`. Generated artifacts record the geometry. No startup
profile or hardware instance is loaded by report generation or these tests.

## Next phase after optics review

1. Confirm diamond, radii, holder spacings, the 615 mm reference plane, and actual Z
   limits. Measure at least one energy/combination/best-focus Z calibration point.
2. Choose the detector and alignment metric (transmission or measured spot size),
   scan resolution, and handling of a weak or boundary optimum.
3. Decide aperture-12 behavior and persistence for per-holder calibrated IN values.
   The repository has an existing Redis-backed configuration facility that can be
   used once the storage policy is settled.
4. Add Bluesky insertion/retraction, IN-position scans, and the microfocusing plan
   that applies a chosen combination followed by its calculated Z. These motion
   plans are deferred by agreement until the optics report has been reviewed.
