"""Fixtures for the ``sim`` tier: build fake, non-broadcasting devices.

Every device here is built through :func:`smiclasses.device_factory.make_device`
with ``force="fake"``, so the construction path is identical to what the live
profile would use with ``SMI_FAKE_DEVICES=all`` -- but no Channel Access
connection is ever opened.
"""
import pytest

from smiclasses import device_factory as df


@pytest.fixture
def make_fake():
    """Return a builder: ``make_fake(cls, name=..., prefix=..., seed=..., **kw)``."""

    def _build(cls, *, name, prefix="FAKE:", seed=None, **kwargs):
        return df.make_device(cls, prefix, name=name, force=df.FAKE, seed=seed, **kwargs)

    return _build
