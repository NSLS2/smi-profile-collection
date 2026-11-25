"""Run the Finch wire payload through real QS discovery, permissions and preparation."""

from pathlib import Path
from types import SimpleNamespace

from bluesky import RunEngine
from bluesky_queueserver.manager.profile_ops import (
    existing_plans_and_devices_from_nspace, load_allowed_plans_and_devices, prepare_plan,
)
from ophyd import Signal
import pytest

from smi_beamline.plans.workstation import workstation_surface


@pytest.fixture
def worker():
    exposure = Signal(name='OAV_cam_acquire_time', value=1.)
    x = Signal(name='piezo_x', value=3.)
    ns = workstation_surface({'OAV': SimpleNamespace(cam=SimpleNamespace(acquire_time=exposure)),
                              'piezo': SimpleNamespace(x=x)})
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


def test_missing_targets_not_advertised():
    assert not workstation_surface({})
    assert set(workstation_surface({'piezo': SimpleNamespace(x=Signal(name='x'))})) == {
        'sample_piezo_x', 'mvr'}
