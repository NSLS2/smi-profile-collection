"""Optional OAV snapshot wrappers for user scans."""

import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp


__all__ = ["oav_snapshot", "with_oav_snapshots"]


def _namespace():
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None:
            return ip.user_ns
    except Exception:
        pass
    return {}


def _default_cameras():
    ns = _namespace()
    cameras = []
    for name in ("OAV_writing", "OAV2_writing"):
        cam = ns.get(name)
        if cam is not None:
            cameras.append(cam)
    if cameras:
        return cameras
    raise ValueError("No cameras supplied and OAV_writing/OAV2_writing are not available")


def _camera_format(camera):
    if hasattr(camera, "jpg"):
        return "jpeg"
    if hasattr(camera, "jpeg"):
        return "jpeg"
    if hasattr(camera, "tiff"):
        return "tiff"
    return "detector"


def oav_snapshot(cameras=None, *, label="snapshot", md=None):
    """Take one OAV snapshot run.

    The existing SMI OAV writing devices currently expose TIFF filestore plugins,
    not JPEG plugins.  This helper will use JPEG-capable devices if supplied in
    the future, but defaults to the already-configured TIFF-writing OAV devices.
    """
    cameras = list(_default_cameras() if cameras is None else cameras)
    run_md = {
        "plan_name": "oav_snapshot",
        "snapshot_label": str(label),
        "snapshot_type": "oav",
        "detectors": [getattr(cam, "name", repr(cam)) for cam in cameras],
        "formats": {getattr(cam, "name", repr(cam)): _camera_format(cam) for cam in cameras},
    }
    if md:
        run_md.update(md)

    def _body():
        print("OAV snapshot: {} using {}".format(
            label, ", ".join(getattr(cam, "name", repr(cam)) for cam in cameras)))
        yield from bps.open_run(md=run_md)
        try:
            yield from bps.trigger_and_read(cameras, name="oav_snapshot")
        finally:
            yield from bps.close_run()

    return (yield from bpp.stage_wrapper(_body(), cameras))


def with_oav_snapshots(plan, cameras=None, *, before=True, after=True, md=None):
    """Wrap any plan with optional before/after OAV snapshot runs.

    Examples
    --------
    ``RE(with_oav_snapshots(bp.scan([pil2M], motor, -1, 1, 11)))``

    ``RE(with_oav_snapshots(my_plan(), before=False))``
    """
    cameras = list(_default_cameras() if cameras is None else cameras)
    if before:
        yield from oav_snapshot(cameras, label="before", md=md)
    result = yield from plan
    if after:
        yield from oav_snapshot(cameras, label="after", md=md)
    return result
