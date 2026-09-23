# CRL microfocusing — current understanding of the installed beamline

Branch: `feature/crl-microfocusing`.

This effort reconstructs the built reality at SMI because the original installed-system
documentation can no longer be found. The layout and labeled inventory below represent
our current best understanding; the focus calculations guide experimental checks.

## Results and report

- [Four-page PDF report](crl_report/crl_optics_report.pdf): installed layout/inventory,
  SSA–CRL–sample ray diagram, fewest-holder selection plot, and recommended energy bands.
- [Selection plot](crl_report/selection.png)
- [Focusing geometry diagram](crl_report/ray_geometry.png)
- [10 eV lookup table](crl_report/lookup.csv)
- [Analytic selection bands](crl_report/selection_bands.csv)

Using the accepted 3D-model geometry, the CRL center is **1600 mm upstream of the sample at
crl.z=0**. Positive `crl.z` moves the CRL closer to the sample, so the modeled image
distance is **q = 1600 mm − crl.z**; `crl.z=+300 mm` gives q≈1300 mm and
`crl.z=-300 mm` gives q≈1900 mm. With 3D-model travel **−300 to +300 mm**, the
image-distance range is **1300–1900 mm**. The default incident beam diverges from
the **SSA secondary source 10.5 m upstream of the CRL center at crl.z=0**.
With this source, the all-labeled-Be, two-sided model predicts coverage over
**2.1–2.3354 keV**, **2.3520–2.7633 keV**, and **3.5559–24 keV**. Gaps are
**2.3354–2.3520 keV** and **2.7633–3.5559 keV**. Boundaries are approximate
physical predictions, despite being calculated analytically within the model.

At **16.1 keV**, holder **3 alone** is now reachable: **crl.z≈+262.912 mm**, with
image distance **1337.088 mm** and focal length **1189.335 mm**. At the usual
**crl.z=+200 mm**, the source distance is 10.7 m and the sample distance is 1400 mm;
the calculated image is 1338.065 mm downstream of the lens, **61.935 mm upstream
of the sample**. This supersedes the collimated prediction of 210.665 mm defocus.

All 255 nonempty subsets of the eight populated holders are considered. Selection
minimizes **inserted holders**, then individual lens elements, then holder numbers
for a deterministic tie-break. This is not an optimization of transmission or spot
size. For example, a single holder containing eight lenses can outrank two holders
containing fewer lenses. No continuity/hysteresis penalty is applied, so some
switches require substantial Z jumps. Alternative solutions are available through
`focus_candidates()`.

## Inventory

| Holder | Contents | Material | Nominal IN (mm) | OUT (mm) |
|---|---|---|---:|---:|
| 1 | 1 × 50 µm | Be | 0 | +10 |
| 2 | 8 × 50 µm | Be | 0 | +10 |
| 3 | 16 × 50 µm | Be | 0 | +10 |
| 4 | 4 × 50 µm | Be | 0 | +10 |
| 5 | 2 × 50 µm | Be | 0 | +10 |
| 6 | Blank / uncharacterized | Unconfirmed | 0 | +10 |
| 7 | Blank / uncharacterized | Unconfirmed | 0 | −10 |
| 8 | Blank / uncharacterized | Unconfirmed | 0 | −10 |
| 9 | 1 × 200 µm | Be | 0 | −10 |
| 10 | 8 × 500 µm | Be | 0 | −10 |
| 11 | 1 × 500 µm | Be | 0 | −10 |
| 12 | 2 mm aperture | | 0 | −10 |

The lens sizes are assumed to be **per-surface radii**, each lens is assumed to have
two parabolic refracting surfaces, and every currently labeled CRL holder is assumed
to be Be. Blank positions may contain diamond CRLs. Twelve diamond lenses are known
to exist somewhere in the unlabeled/blanks, but they are excluded from this
calculation until commissioning experimentally confirms their holders, radii,
insertion positions, and material. Nominal IN=0 is not a measured alignment;
expected alignment search is about ±2 mm. Uncharacterized blanks and the aperture
are excluded from selection; this does not establish that the blanks have zero
physical lens power.

## Model

`src/smi_beamline/devices/crl_optics.py` uses only the standard library, and neither
imports device instances nor accesses EPICS. It computes the free-electron estimate

```text
delta_m(E) = r_e * lambda(E)^2 * n_e,m / (2*pi)
n_e,m = (rho_m / atomic_weight_m) * N_A * Z_m
P(E) = 1/f(E) = sum_i 2 * delta_material_i(E) * N_i/R_i
```

Be density is 1.848 g/cm³ and Be atomic weight is 9.0121831 g/mol. Diamond density
is 3.515 g/cm³ and carbon atomic weight is 12.011 g/mol. Constants and unit
conversions are explicit in `beryllium_delta()` and `diamond_delta()`. At 10 keV,
delta(Be) is approximately 3.40539×10⁻⁶ and delta(diamond) is approximately
7.29009×10⁻⁶. One Be R=50 µm lens has f≈7.341 m. This is an **E⁻² approximation**
to delta using neutral-atom scattering factors Be f1=4 and C f1=6; it is not a
Henke/CXRO optical-constant table. The Be and carbon absorption edges lie below
this energy range, but dispersion and absorption corrections have not been quantified
here. A future refinement can compare tabulated f1 and absorption data, then
recalculate the band boundaries numerically.

The common-plane thin-lens approximation adds powers, ignoring individual holder
positions, element spacing, and stack thickness. Holder-dependent principal-plane
shifts could matter given the 600 mm available Z travel.

The SSA is modeled as the effective geometrical secondary source, with no
intervening focusing optics in this propagation model. Its 10.5 m upstream distance
is measured from the **CRL Z=0 center**, not from the sample. Thus:

```text
p(Z) = 10.5 + Z_mm / 1000                   [m, SSA to lens]
q(Z) = 1.6 - Z_mm / 1000                    [m, lens to sample]
p(Z) + q(Z) = 12.1                         [m, fixed SSA to sample]
1/f = 1/p(Z) + 1/q(Z)
C0 = 1/10.5 = +0.095238095238...            [1/m at CRL Z=0]
```

Positive Z increases source-to-lens distance while decreasing lens-to-sample
distance. The implementation propagates the curvature as the CRL moves, rather
than holding it fixed at 1/10.5 everywhere. At Z=−300, 0, +300 mm, source distances
are 10.2, 10.5, 10.8 m respectively. More generally, curvature `C0` at the
**Z=0 reference plane** obeys:

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
Those need more beam and lens dimensions. The SSA aperture alone does not prove
that the actual wavefront has this curvature: the model assumes it is the effective
source, to be checked against focus measurements. Finite SSA size and illumination
also affect the image.

The report's ray diagram shows the CRLs at −300, 0 and +300 mm with fixed SSA
and sample positions. Each panel uses the required thin-lens power at that position
and quotes the equivalent energy for holder 3. Rays are propagated from the SSA,
refracted by `slope_out = slope_in - height/f`, then propagated to the sample.
Longitudinal distances are to scale; transverse ray heights are arbitrary. These
are three different focusing settings, not a fixed-energy beam that remains focused
as the CRLs move.

## Usage with the existing CRL object

Existing components remain `EpicsMotor`s with their original PV suffixes:
`crl.lens1` … `crl.lens12`, `crl.x`, `crl.y`, `crl.z`, `crl.ph`, `crl.th`.
The added methods are **calculations only**, using explicit **keV** inputs:

```python
crl.lens_inventory                       # immutable inventory and nominal positions
solution = crl.recommend_focus(10.0)      # no motor read or movement
solution.holders                        # (1, 4)
solution.z_mm                           # approximately -109.89 mm
solution.focal_length_mm                 # approximately 1468.26 mm
solution.image_distance_mm               # approximately 1709.89 mm (not equal to f)
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
    sample_distance_mm=1600,
    z_min_mm=-295,                      # example 5 mm margin
    z_max_mm=295,
    incident_curvature_per_m=1 / 10.5,  # SSA 10.5 m upstream of CRL Z=0
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
`--incident-curvature-per-m`. Default curvature is `1/10.5` per metre; explicitly
pass `--incident-curvature-per-m 0` for a collimated comparison (or construct
`CRLGeometry(incident_curvature_per_m=0)`). Generated artifacts record the active
geometry and curvature. No startup profile or hardware instance is loaded by
report generation or these tests.

## Follow-up

1. Plan focus measurements at a few energies and holder combinations.
2. Experimentally confirm and measure blank-holder contents: are they diamond CRLs?
3. Develop advanced alignment routines using the measured results.
