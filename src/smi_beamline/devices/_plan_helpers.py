"""
smiclasses._plan_helpers
========================

Small, **importable, hardware-free** plan helpers (preprocessors/decorators) used by the
SMI plans in ``smibase`` (alignment, beam, ...).

These live here (rather than in ``smibase``) purely so they can be imported and unit-tested
off the beamline -- ``smibase`` modules grab ``RE``/``sd``/``bec`` from the IPython namespace at
import time and cannot be imported standalone.  When the logic modules are moved into a proper
``plans/`` package (restructure plan, Phase 3 structural sub-phase), this can move with them.

Nothing here touches EPICS, Redis, or IPython.
"""
from functools import wraps

try:
    import bluesky.preprocessors as bpp
except Exception:  # pragma: no cover - outside the beamline env
    bpp = None


__all__ = ["sanitize_name", "sample_name_decorator"]


#: Characters stripped from a human label to make a filename-safe token (matches the historical
#: ``sample_id`` behavior).
_UNSAFE = r"!@#$%^&*{}:/<>?\|`~+ =,"


def sanitize_name(name):
    """Return ``name`` with spaces / shell-unsafe characters replaced by ``_``."""
    return name.translate({ord(c): "_" for c in _UNSAFE})


def sample_name_decorator(name):
    """Tag every run opened by the wrapped plan with ``sample_name`` (run-scoped md).

    Replaces the old ``sample_id(...)`` pattern, which mutated the *global*
    ``RE.md['sample_name']`` before a plan -- a side effect that then leaked into unrelated
    subsequent runs.  This injects ``sample_name`` into each ``open_run`` *inside* the wrapped
    plan instead, so the name is scoped to that plan's runs and nothing global is mutated
    (Tenets 2/4).

    Semantics:
    * **set-default**: an inner scan that already passes its own ``md={'sample_name': ...}`` is
      left untouched (the explicit name wins).
    * ``name`` is sanitized via :func:`sanitize_name`, so a human-readable label such as
      ``"alignment height scan"`` is safe to pass.

    Example
    -------
    >>> @sample_name_decorator("alignment_gisaxs")
    ... def my_align():
    ...     yield from bp.rel_scan([pil2M], piezo.y, -1, 1, 11)   # -> sample_name on this run
    """
    safe = sanitize_name(name)

    def _dec(plan_func):
        @wraps(plan_func)
        def _wrapped(*args, **kwargs):
            def _mut(msg):
                if msg.command == "open_run" and "sample_name" not in msg.kwargs:
                    return msg._replace(kwargs={**msg.kwargs, "sample_name": safe})
                return msg
            return (yield from bpp.msg_mutator(plan_func(*args, **kwargs), _mut))
        return _wrapped
    return _dec
