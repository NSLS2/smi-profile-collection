"""Single-device QueueServer controls for the first smi-acquire commissioning slice."""

import math

from bluesky import plan_stubs as bps
from bluesky_queueserver import parameter_annotation_decorator


def _target(*aliases):
    # Let QueueServer validate the device against its allowed list and translate
    # the wire name to the worker's existing object before calling the plan.
    return parameter_annotation_decorator({'parameters': {'device': {
        'annotation': 'Target', 'devices': {'Target': list(aliases)},
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

        axes = {'sample_piezo_x': x}
        if getattr(namespace['piezo'], 'y', None) is not None:
            axes['sample_piezo_y'] = namespace['piezo'].y

        @_target(*axes)
        def mvr(device, delta: float):
            """Jog one sample piezo axis by a relative displacement in native motor units."""
            if not any(device is axis for axis in axes.values()) or not math.isfinite(delta):
                raise ValueError('Expected a configured sample piezo axis and finite displacement')
            yield from bps.mvr(device, delta)

        surface.update(axes, mvr=mvr)
    return surface


def sample_loading_surface(namespace, sample_mapping):
    """Worker adapter for smi_plans: IDs in queue items, resolved Sample in the plan."""
    def load_sample(holder_id: str, sample_id: str, updated: float, max_step_um: float):
        """Position piezo XYZ on an already-mounted holder; no exchange or metadata edits."""
        from smi_plans import SampleStore
        from smi_plans._core import goto_sample
        if sample_mapping.get('schema_version') != 1:
            raise ValueError('Uninitialized or unsupported shared sample store')
        store = SampleStore(sample_mapping)
        mag = store.magazine()
        if mag.measurement_holder_id != holder_id or holder_id not in mag.holder_ids:
            raise ValueError('Selected holder is not the recorded measurement holder')
        s = store.get_sample(sample_id)
        if (s.id != sample_id or s.holder_id != holder_id or s.id not in store.get_holder(holder_id).sample_ids
                or s.updated != updated):
            raise ValueError('Sample changed; refresh before loading')
        pos = s.runnable_position()  # refined first, otherwise nominal, just as in goto_sample
        if pos.frame != 'lab' or not math.isfinite(max_step_um) or max_step_um <= 0:
            raise ValueError('Need an absolute lab position and positive piezo travel cap')
        p, h = namespace['piezo'], namespace['stage']
        for a in ('x', 'y', 'z'):
            target = getattr(pos, 'piezo_' + a)
            current = float((yield from bps.rd(getattr(p, a))))
            if (target is None or not math.isfinite(target) or not math.isfinite(current)
                    or abs(target-current) > max_step_um):
                raise ValueError('Missing or out-of-range piezo target; no move issued')
        skip = [p.th, h.x, h.y, h.z, h.theta, h.chi, h.phi]
        yield from goto_sample(s, piezo_dev=p, hexa_dev=h, skip=skip)

    return {'load_sample': load_sample} if {'piezo', 'stage'} <= namespace.keys() else {}
