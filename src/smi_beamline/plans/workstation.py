"""Single-device QueueServer controls for the first smi-acquire commissioning slice."""

import math

from bluesky import plan_stubs as bps
from bluesky_queueserver import parameter_annotation_decorator


def _target(alias):
    # Let QueueServer validate the device against its allowed list and translate
    # the wire name to the worker's existing object before calling the plan.
    return parameter_annotation_decorator({'parameters': {'device': {
        'annotation': 'Target', 'devices': {'Target': [alias]},
    }}})


def workstation_surface(namespace):
    """Expose only bindings the device factory actually loaded; create no PVs."""
    surface = {}
    if namespace.get('OAV') is not None:
        exposure = namespace['OAV'].cam.acquire_time

        @_target('oav_acquire_time')
        def mv(device, value: float):
            """Set on-axis microscope exposure in seconds (one target only)."""
            if device is not exposure or not math.isfinite(value) or not .0001 <= value <= 2:
                raise ValueError('Expected on-axis camera exposure in [0.0001, 2] seconds')
            yield from bps.mv(device, value)

        surface.update(oav_acquire_time=exposure, mv=mv)

    if namespace.get('piezo') is not None:
        x = namespace['piezo'].x

        @_target('sample_piezo_x')
        def mvr(device, delta: float):
            """Jog sample piezo X by a relative displacement in native motor units."""
            if device is not x or not math.isfinite(delta):
                raise ValueError('Expected sample piezo X and a finite displacement')
            yield from bps.mvr(device, delta)

        surface.update(sample_piezo_x=x, mvr=mvr)
    return surface
