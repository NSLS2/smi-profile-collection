"""Run the Finch wire payload through real QS discovery, permissions and preparation."""

from pathlib import Path
from types import SimpleNamespace

from bluesky import RunEngine
from bluesky_queueserver.manager.profile_ops import (
    existing_plans_and_devices_from_nspace, load_allowed_plans_and_devices, prepare_plan,
)
from ophyd import Signal
import pytest

from smi_beamline.plans.workstation import sample_loading_surface, workstation_surface


@pytest.fixture
def worker():
    exposure = Signal(name='OAV_cam_acquire_time', value=1.)
    x = Signal(name='piezo_x', value=3.)
    ns = workstation_surface({'OAV': SimpleNamespace(cam=SimpleNamespace(acquire_time=exposure)),
                              'piezo': SimpleNamespace(x=x, y=Signal(name='y', value=2.))})
    plans, devices, ps, ds = existing_plans_and_devices_from_nspace(nspace=ns, max_depth=1)
    ap, ad = load_allowed_plans_and_devices(existing_plans=plans, existing_devices=devices,
        path_user_group_permissions=str(Path(__file__).resolve().parents[2] / 'startup' /
                                        'user_group_permissions.yaml'))

    def prepare(group, name, alias, value):
        item = dict(item_type='plan', name=name, args=[alias, value], user_group=group,
                    meta={'smi_acquire_command': 'trial'})
        return prepare_plan(item, plans_in_nspace=ps, devices_in_nspace=ds, allowed_plans=ap,
                            allowed_devices=ad, nspace=ns)
    return exposure, x, ad, prepare


@pytest.mark.parametrize('group', ['primary', 'gui'])
def test_workstation_items(worker, group):
    exposure, x, devices, prepare = worker
    re = RunEngine({})
    for name, alias, value, target, expected in [
        ('mv', 'oav_acquire_time', .2, exposure, .2), ('mv', 'oav_acquire_time', 1., exposure, 1.),
        ('mvr', 'sample_piezo_x', -.1, x, 2.9),
    ]:
        assert devices[group][alias]['is_movable']
        p = prepare(group, name, alias, value)
        assert p['args'][0] is target
        re(p['callable'](*p['args'], **p['kwargs']))
        assert target.get() == pytest.approx(expected)
    with pytest.raises(RuntimeError):
        prepare(group, 'mv', 'sample_piezo_x', .2)
    y = prepare(group, 'mvr', 'sample_piezo_y', .05)
    re(y['callable'](*y['args'], **y['kwargs']))
    assert y['args'][0].get() == pytest.approx(2.05)
    assert x.get() == pytest.approx(2.9)


def test_missing_targets_not_advertised():
    assert not workstation_surface({})
    assert set(workstation_surface({'piezo': SimpleNamespace(x=Signal(name='x'))})) == {
        'sample_piezo_x', 'mvr'}


def test_load_sample_resolves_shared_refined_version_at_execution():
    from smi_plans import Holder, Position, Sample, SampleStore
    def axes(names):
        return SimpleNamespace(**{a: Signal(name=a, value=0.) for a in names.split()})
    p, h = axes('x y z th'), axes('x y z theta chi phi')
    mapping = {}
    store = SampleStore(mapping)
    holder = Holder(name='bar')
    sample = Sample(name='film', holder_id=holder.id, nominal=Position(frame='holder', piezo_x=200),
                    refined=Position(frame='lab', piezo_x=1, piezo_y=2, piezo_z=3, stage_x=90))
    store.put_sample(sample)
    holder.sample_ids.append(sample.id)
    store.put_holder(holder)
    mag = store.magazine()
    mag.holder_ids.append(holder.id)
    store._put_magazine(mag)
    store.set_measurement_holder(holder.id)
    store.set_active_sample(None)
    ns = sample_loading_surface({'piezo':p, 'stage':h}, mapping)
    plans, devices, ps, ds = existing_plans_and_devices_from_nspace(nspace=ns)
    ap, ad = load_allowed_plans_and_devices(existing_plans=plans, existing_devices=devices,
        path_user_group_permissions=str(Path(__file__).resolve().parents[2] / 'startup/user_group_permissions.yaml'))
    args = [holder.id, sample.id, sample.updated, 4.]
    prepared = prepare_plan({'name':'load_sample','item_type':'plan','args':args,'user_group':'gui'},
                            plans_in_nspace=ps, devices_in_nspace=ds, allowed_plans=ap, allowed_devices=ad)
    engine = RunEngine({})
    engine(prepared['callable'](*prepared['args']))
    assert (p.x.get(),p.y.get(),p.z.get(),h.x.get()) == (1,2,3,0)
    assert store.magazine().active_sample_id is None
    p.x.set(10).wait()
    with pytest.raises(ValueError, match='no move issued'):
        engine(ns['load_sample'](*args))
    assert p.x.get() == 10
    sample.md['notes'] = 'changed after review'
    store.put_sample(sample)
    with pytest.raises(ValueError, match='changed'):
        engine(ns['load_sample'](*args))
    store.set_measurement_holder(None)
    with pytest.raises(ValueError, match='measurement holder'):
        engine(ns['load_sample'](*args))
