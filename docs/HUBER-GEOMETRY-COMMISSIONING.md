# Huber geometry and GI CD-SAXS commissioning checklist

**Status: proposed commissioning checklist, not a validated motion procedure.**
The motor directions (especially Z), angular zeros, physical rotation centers,
beam direction, real travel, fixture fit and achievable accuracy remain to be
measured. Complete beamline safety review and staff authorization first. Do not
deploy or use the revised pseudo-positioner for sample motions until the
relevant checks below pass and the responsible staff accept the result.

## Objective and coordinate contract

- [ ] Record the profile revision, device configuration, date, staff, optics,
  energy, vacuum state, load, fixture and motor/encoder configuration.
- [ ] Confirm the physical stack: **theta is the bottom cradle joint**, chi is
  above theta, phi is above the cradle, and Y/X/Z translations carry the sample.
  Confirm axes, signs, coordinate conventions and any nonorthogonality by
  inspection and measurement. The nominal model is theta about X, chi about Z,
  phi about Y; X is inboard/outboard, Y vertical and Z along the beam.
- [ ] For GI CD-SAXS, align the **physical phi axis normal to the sample plane**.
  Then fly **`stage.phi_real` only**, with real theta and chi held fixed, so the
  sample rotates azimuthally at approximately constant incidence. For a fixed
  illuminated sample point, it must also lie on the physical phi axis. A raw
  phi fly does not command XYZ corrections. Verify both claims experimentally.
- [ ] Distinguish gravity vertical, beam direction, phi-axis direction and the
  sample normal. They need not be identical. A beam-parallel sample surface at
  zero incidence is not by itself a measurement of gravity vertical.
- [ ] Note the revised pseudo convention: `R_lab = Ry(phi) Rz(chi) Rx(theta)`;
  physical orientation is `Rx(-theta_real) Rz(chi_real) Ry(-phi_real)`. A pseudo
  angular move may move several real axes. Saved pseudo angles and plans from
  the old pass-through convention are **not automatically equivalent**.
  Euler angles are not independent fixed-lab rotations at finite angles. The
  negative theta and phi signs are provisional pending physical measurements;
  they do not establish the correct EPICS directions.
- [ ] Note provisional pseudo phi limits of -250 to +120 degrees. Confirm real
  EPICS limits, both ends of travel, all intermediate clearances, and the
  encoder's multi-turn convention. The pseudo angle is a lab Euler angle, not
  necessarily equal to physical phi; under the current model, at zero cradle
  angles it has the opposite sign. These pseudo limits are retained unchanged
  pending determination of the real motor direction; they do not certify real
  travel and must be reviewed against the physical motor limits.
- [ ] Record EPICS user/dial readbacks, direction, offset and offset-freeze/set
  configuration for each real motor. EPICS owns angular zeros; changing a motor
  zero or direction alters the model's zero frame and requires revalidation.
  `stage.theta_real`, `stage.chi_real` and `stage.phi_real` expose their
  Ophyd motor fields, including `user_offset`, to Bluesky. A write to an offset
  can change motor-coordinate interpretation: use the approved motor-record
  procedure and explicit authorization, not an ad hoc put.
- [ ] First measure each motor's physical direction against the agreed
  right-handed coordinate system, including the actual EPICS user and dial
  readbacks, `DIR`, offset, limits and angular zero. Use only independently
  approved small moves and a safe envelope. Record the measurements and their
  uncertainty; do not infer a direction from the current software signs.
- [ ] After measurement and staff review, decide whether any EPICS `DIR` and
  associated motor-record settings need correction so user coordinates follow
  the agreed right-hand-rule geometry. Changes belong to an authorized EPICS
  procedure with before/after records, limit and offset review, and a rollback
  plan; this checklist does not authorize or perform them.
- [ ] After any approved EPICS changes, independently remeasure directions,
  zeros, limits and rotation centers. Update the software transformations,
  pseudo limits, documentation and offline tests together to match the verified
  user-coordinate convention, removing provisional sign reversals only when
  the measurements justify it. Repeat the commissioning and safety review
  before using the revised transform for sample motion.
- [ ] Record all nine center signals. Their existing defaults are not measured
  calibrations and are in-memory signals; retain the measured calibration
  externally and restore it deliberately when needed. Each center is expressed
  in its joint parent frame at the shared zero pose; its coordinate along its
  own rotation axis is a gauge choice, not an independently measured point.
- [ ] Record the 0.001 translation and 0.0001 angular software deadbands in
  their respective motor units. Neither value establishes encoder accuracy,
  reproducibility, trajectory smoothness, or angular stability.

## Safety and measurement preparation

- [ ] Obtain staff approval for the fixture and every motion envelope; check
  clearance through the entire path, not just endpoint motor limits. Check
  vacuum compatibility, load, cable routing, beamstop/detector protection,
  thermal monitoring and applicable beamline safety procedures.
- [ ] Agree in advance on safe approach directions, scan limits and stop
  criteria. Start with small, reviewed ranges; do not assume the nominal cradle
  +/-4-degree or phi -250/+120-degree ranges are currently safe or reachable.
- [ ] Verify motor readbacks, step directions, translations and scale with
  small, approved independent checks. The Z EPICS direction was changed; the
  model uses the resulting user coordinate without an additional reversal.
  Confirm its physical sign and the centers in that coordinate before use.
- [ ] Use **Huber real motors only** for the baseline Huber calibration and
  keep the SmarAct motors fixed and documented. Move between fixture features
  using Huber translations only after checking reach and clearance. SmarAct may
  be used later as an independent cross-check or if fixture reach requires it,
  but record its moves and model its axes separately; do not silently mix them
  into a Huber fit. Huber-only calibration does not calibrate SmarAct.
- [ ] Choose rigid, distinguishable fiducials with known relative geometry.
  At least two separated features, including separation approximately along phi
  and a useful radial lever arm, improve observability. A long uniform pin is
  not a point along its length: define and validate a reproducible tip, crossing
  or other 3D feature. Record feature IDs, lever arms and uncertainty.
- [ ] Confirm detector response, beam stability, scan fitting method and
  reproducibility; preserve raw scans and fit uncertainties. A failed or
  ambiguous fit is not a calibration point. Record positions, readbacks,
  timestamps, approach direction, temperature and intensity with every scan.

## Beam and translation reference

- [ ] Measure beam X and Y at two or preferably three **known longitudinal
  positions**, with a calibrated/surveyed baseline and transverse directions.
  Repeat a station to check drift; fit a beam line and uncertainty. A single
  knife edge at one Z measures position, not direction.
- [ ] Confirm how the same physical feature is located at each station. If the
  translating axes tilt with the cradle, include their known transformations;
  do not assume a nominal Z readback is a surveyed beam-direction baseline.
  If required observables are unavailable, add independent metrology.
- [ ] Check X/Y repeatability and scale; the scientist reports these are
  consistent, but record the present measured results and conditions. Establish
  Z sign and scale independently. For vertical-axis experiments, obtain an
  independent gravity/level reference; beam measurements alone cannot supply it.
- [ ] Set a beam-direction uncertainty budget. As an example, a 1 µm relative
  transverse error across 100 mm is about 0.00057 degrees, already over half
  of a 0.001-degree total tolerance. Include systematics and temporal drift.

## Nested-axis measurement and model fitting

- [ ] At a safe cradle reference pose, measure both fiducials across a broad,
  approved set of physical phi angles. Include enough widely separated angles
  to distinguish a circle/axis from a local slope; repeat reference poses.
- [ ] At several of those phi angles, repeat measurements at safely accessible
  positive and negative theta offsets, then chi offsets. Use raw joint
  readbacks, not the pseudo transform under test. Select actual values after
  travel/clearance review; reserve several mixed-angle poses for validation.
- [ ] As a starting *measurement design*, not a motion recipe: consider seven
  phi poses near -180, -135, -90, -45, 0, 45 and 90 degrees at the cradle
  reference, plus theta +/-2 degrees and chi +/-2 degrees at three separated
  phi poses. This is 19 poses; with two fiducials it is 38 feature-location
  measurements, plus repeats and held-out poses. Each location may require two
  transverse scans. Replace or omit any pose outside verified limits, approach,
  clearance or thermal constraints; offsets are relative to the measured
  reference and must fit the actual real limits. An accepted fit may require
  more points, different fiducials or independent metrology.
- [ ] Repeat selected poses from opposite directions and at different times or
  thermal states. Record any load-dependent or time-dependent deviations.
- [ ] Fit all observations jointly with a nested rigid-body model, comparing
  alternate signs and the old versus confirmed nesting. Include the beam line,
  fixture geometry and measurement uncertainties. Fit axis **lines**, not
  fictitious uniquely observable 3D center points.
- [ ] Check fit rank, parameter correlations and confidence intervals. A
  single pin or a single beam station cannot independently identify all
  axis centers, beam direction, joint zeros and fixture orientation. Fix gauge
  freedoms using documented datums or add metrology instead of assigning false
  precision. Resolve nonorthogonality, runout or flexure only if the dataset
  supports them. Record unresolved correlations explicitly.
- [ ] Compare predictions with held-out mixed theta/chi/phi observations and
  with each fiducial separately. Inspect residual versus angle, approach,
  temperature and time. Reject the model when the residuals exceed the agreed
  measurement or experiment budget; do not keep retuning centers per pose.
- [ ] Independently verify the proposed software transform and its actual
  motor directions at small reviewed moves. The offline unit tests establish
  algebra only, not hardware identity, signs, fixture clearance or deployment.
- [ ] Review measured EPICS angular zeros and fitted centers together. Record
  who approved any changes, their before/after values and a rollback plan.
  Do not use a sample-specific tilt or beam drift as an unexplained mechanical
  center change. Recheck after remounting, motor-record changes or large load/
  thermal changes.

## GI CD-SAXS acceptance

- [ ] Install and identify a flat reference/sample with a known or measured
  surface normal. Distinguish this sample-specific calibration from the Huber
  instrument geometry. Account for holder repeatability and sample flatness.
- [ ] Using suitable direct and reflected beam measurements, determine the
  beam-relative sample orientation and the cradle setting that makes the
  **physical phi axis parallel to the sample normal** at the chosen incidence.
  Check that the selected setting is mechanically reachable with margin.
- [ ] At several static physical phi positions over the intended scan range,
  with theta and chi fixed, independently measure incidence and the beam
  footprint/selected point. Include held-out angles and repeat positions.
  A single GI alignment or a successful software round-trip is insufficient.
- [ ] Before declaring a 0.001-degree result, specify whether the tolerance is
  maximum absolute error, peak-to-peak drift or another metric, plus confidence
  and the time/phi interval. Allocate uncertainty to beam direction/drift,
  sample normal, axis alignment, fit, readback, thermal/mechanical drift and
  measurement timing. Show that the full budget meets the selected criterion.
- [ ] After static acceptance and separate safety review, validate a
  representative **phi-real-only continuous trajectory**. Record physical phi,
  theta/chi and appropriate independent angle/position observables with
  timestamps; check detector exposure timing and q/azimuth reconstruction.
  Verify no theta, chi or XYZ motor is commanded during the fly. Check motion
  speed, runout, heating, drift and repeatability at the intended duty cycle.
- [ ] Stop and investigate if alpha or the illuminated point fails its budget.
  Angle-independent sample position is not guaranteed by the angular condition,
  and constant incidence is not guaranteed merely by accurate phi readback.
  Document limitations and the approved working range; do not silently change
  center signals to force agreement.

## Record of outcome

- [ ] Store raw scans, fit code/results, uncertainties, model version, motor
  offsets/limits, centers, fixture details, signs, operating conditions,
  validation plots and staff acceptance in the agreed beamline record.
- [ ] Record a separate sample-specific reference, beam configuration and
  expiration/recheck triggers. Do not equate this with a permanent instrument
  calibration. Note whether `phi_real` single-axis GI flying has been accepted.

For each fiducial observation, retain at minimum: feature ID; real X/Y/Z,
theta/chi/phi user and dial readbacks; fitted crossing coordinates and their
uncertainties; scan UID; beam monitor/intensity; timestamp; approach direction;
temperature and any SmarAct coordinates. Separately retain detector/ROI,
optics and calibration version. Distinguish a missing reading from zero.
