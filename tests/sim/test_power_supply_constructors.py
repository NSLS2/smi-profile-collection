"""Exercise real EPICS signal constructors without opening Channel Access PVs.

make_fake_device replaces the constructors and can hide incompatible Cpt kwargs.
"""
from unittest.mock import MagicMock

import pytest

from smi_beamline.devices.power_supply import PowerSupply


@pytest.mark.parametrize("attr", PowerSupply.component_names)
def test_real_signal_constructor_accepts_component_kwargs(attr):
    component = getattr(PowerSupply, attr)
    cl = MagicMock()
    pv = cl.get_pv.return_value
    pv._reference_count = 0
    signal = component.cls(
        "SIM:PS:" + component.suffix,
        name="ps_" + attr,
        cl=cl,
        **component.kwargs,
    )
    assert signal.name == "ps_" + attr
    assert cl.get_pv.called
    signal.destroy()
