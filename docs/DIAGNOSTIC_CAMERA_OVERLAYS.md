# Diagnostic camera overlays

The profile exports `cam9` and `cam10` for the diagnostic module cameras:

- `cam9`: `XF:12ID2-OP{GigE-Cam:9}`
- `cam10`: `XF:12ID2-OP{GigE-Cam:10}`

These are overlay-only interfaces, not acquisition detectors. They do not trigger
images, write files, or automatically enable overlays when constructed or staged.
The overlay component is lazy so profile loading does not wait for camera PVs.

Each exposes `over1.overlay_1` through `over1.overlay_8`. For example:

```python
# Read existing settings; no acquisition or writes. Bound each live read.
cam10.over1.overlay_3.use.get(timeout=2)
cam10.over1.overlay_3.position_x.get(timeout=2)
cam10.over1.overlay_3.position_y.get(timeout=2)
cam10.over1.overlay_3.size_x.get(timeout=2)
cam10.over1.overlay_3.size_y.get(timeout=2)
cam10.over1.overlay_3.width_x.get(timeout=2)
```

Other fields are `blue`, `green`, `red`, `center_x`, `center_y`, `draw_mode`,
`overlay_portname` (the `Name` PV), `shape`, and `width_y`. Geometry is in image
pixels. `use` is the individual overlay enable, not camera acquisition or the
plugin-wide callback enable. Signals read the `_RBV` PV; explicit signal writes
target the corresponding setting PV. No writes are performed during startup.

The existing on-axis camera remains `OAV.over1`. These additions do not yet add
camera overlays to beam-position snapshots or change the OAV device definition.
Load the additions at a staff-approved profile reload/restart, not by importing
the entire startup during an active acquisition.

## OAV-only transform and plugin routing

`OAV_config` is a separate configuration device at `XF:12IDC-BI{Cam:SAM}`.
It does not replace `OAV`, add new staging behavior to it, or acquire images.
Only this sidecar has the requested plugin ports/enables; cam9/cam10 do not.

```python
OAV_config.plugins.over1.enable.get(timeout=2)          # EnableCallbacks_RBV
OAV_config.plugins.over1.nd_array_port.get(timeout=2)   # NDArrayPort
OAV_config.plugins.over1.port_name.get(timeout=2)       # PortName_RBV (read-only)
OAV_config.trans1.type_.get(timeout=2)                   # Trans1:Type
```

Plugin attributes are lowercase (`attr1`, `bar1`, `cb1`, `cc1`, `cc2`, `cv1`,
`codec1`, `codec2`, `edge1`, `fft1`, `gather1`, `hdf1`, `jpeg1`, `magick1`,
`nexus1`, `over1`, `proc1`, `pva1`, `roi1`--`roi4`, `roistat1`, `scatter1`,
`stats1`--`stats5`, `tiff1`, `trans1`, `image1`, `netcdf1`). PV prefix case is
preserved. No rates, queue statistics, blocking settings, or file-writing
controls from the supplied list are added. `PortName_RBV` is identity information,
not a restorable port setting; `NDArrayPort` is the selectable input port.

The transform `Type` mapping follows modern ophyd/ADCore (rotation/reflection).
It was not included in the supplied PV list and still needs IOC verification.
The existing `OAV.trans1` uses ophyd's unversioned legacy TransformPlugin, whose
four-transform mapping differs; that existing device is intentionally unchanged.
Do not assume the modern `Type` record exists based on fake tests. If the IOC
uses a legacy transform, obtain its actual transform PV list before changing
this binding. The sidecar and its plugin containers are lazy and have empty
stage settings; construction and staging do not change routing or enables.

Offline tests cover all eight slots, field suffixes, fake readbacks, unchanged
enable settings on stage/unstage, and factory exports. Live IOC connectivity and
enum definitions still require operator verification; fake tests establish neither.

```bash
pixi run -e test python -m pytest tests/sim/test_diagnostic_cameras.py
```
