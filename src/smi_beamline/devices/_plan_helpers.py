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
import string
from functools import wraps

try:
    import bluesky.preprocessors as bpp
    import bluesky.plan_stubs as bps
    from bluesky.utils import Msg
except Exception:  # pragma: no cover - outside the beamline env
    bpp = None
    bps = None
    Msg = None


__all__ = [
    "sanitize_name",
    "sample_name_decorator",
    "template_field_names",
    "scan_name_preprocessor",
]


#: Characters stripped from a human label to make a filename-safe token (matches the historical
#: ``sample_id`` behavior).
#:
#: NOTE: this intentionally includes ``{``, ``}`` and ``:`` -- so it must only be applied to the
#: *human label* part of a name, NEVER to a filename **template** (whose ``{energy_energy:.1f}``
#: tokens depend on those characters).  :func:`scan_name_preprocessor` keeps the two apart.
_UNSAFE = r"!@#$%^&*{}:/<>?\|`~+ =,"


def sanitize_name(name):
    """Return ``name`` with spaces / shell-unsafe characters replaced by ``_``."""
    return name.translate({ord(c): "_" for c in _UNSAFE})


def template_field_names(template):
    """Return the list of recorded-field keys referenced by a ``str.format`` ``template``.

    The filename ``template`` carries ``{data_key}`` / ``{data_key:spec}`` tokens that the
    readout worker fills (via ``str.format``) from the **recorded event fields** of the run.
    This returns the base data keys (``energy_energy``, ``waxs_arc``, ...), stripped of any
    format spec, attribute (``.foo``) or index (``[0]``) access, and de-duplicated in order.

    Tokens with an empty field name (``{}`` positional) are ignored, as are the structural
    tokens the worker itself supplies (``det_name`` / ``det_type`` / ``N``).

    >>> template_field_names("t_{energy_energy:.1f}eV_{waxs_arc:04.1f}wa")
    ['energy_energy', 'waxs_arc']
    """
    if not template:
        return []
    seen = []
    for _literal, field_name, _spec, _conv in string.Formatter().parse(template):
        if not field_name:
            continue
        base = field_name.split(".")[0].split("[")[0]
        if base and base not in seen:
            seen.append(base)
    return seen


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


def scan_name_preprocessor(
    plan,
    *,
    template,
    token_devices=None,
    base_name=None,
    separator="_",
    primary_stream="primary",
    skip_if_tokens=True,
):
    """Extend every run's ``sample_name`` with a recorded-field **filename template** and make
    sure the fields the resulting name references are actually recorded.

    This is the generic, hardware-free engine behind the beamline default (see the wiring helper
    :mod:`smi_beamline.plans.scan_naming` that supplies ``template`` and ``token_devices``).  It is
    meant to be installed on ``RE.preprocessors`` so it applies to **every** plan, but it is a
    plain plan-preprocessor (``plan -> plan``) and can also be used ad hoc.

    What it does, per run
    ---------------------
    1. **Names the run (append, never clobber).**  At ``open_run`` it determines the run's
       *existing* name -- in priority order: the run's own ``md={'sample_name': ...}`` (what the
       plan / :func:`sample_name_decorator` passed) or, failing that, ``base_name`` (the wiring
       passes ``RE.md['sample_name']``, i.e. the user/proposal prefix) -- and produces the final
       name as follows:

       * **Existing name already contains a ``{token}``** (only when ``skip_if_tokens``, the
         default): the user supplied their *own* recorded-field template, so it is taken as the
         complete name and the default ``template`` is **not** appended.  (The name is used
         verbatim -- not sanitized -- since it intentionally carries ``{...}`` tokens.)
       * **Plain string existing name** (no tokens): the default ``template`` is appended as
         ``sanitize_name(existing) + separator + template``.  Only the human label is sanitized;
         the template's braces/colons are preserved.
       * **No existing name**: the name is just ``template``.

       Append is idempotent: a name that already ends with ``separator + template`` is not
       appended again (this also makes the rewrite safe under ``plan_mutator`` re-entry).

       In all cases the tokens are left **unfilled** for the downstream readout/symlink worker to
       fill from each run's recorded fields (``str.format``).

    2. **Records the referenced fields.**  It parses the run's *final* name for ``{data_key}``
       tokens and, for each that maps to a device in ``token_devices``, injects a ``read`` of that
       device into every ``primary`` Event of the run -- so the value lands in the documents and
       the worker can fill the token.  This is what makes
       ``RE(bp.count([pil2M], md={'sample_name': '..{waxs_arc}..'}))`` work without the user
       adding ``waxs`` to the detector list.  Only devices whose key appears in the final name are
       read (an energy-only name does not force a WAXS read).  A token device the plan **already**
       reads itself is excluded from injection so no object is read twice in one Event (which
       raises) -- this covers the device named in the ``detectors``/``motors`` of the ``open_run``
       (e.g. ``bp.count([pil2M, energy], md=...{energy_energy}...)`` or a scan *over* ``energy``)
       **and** the parent/child case (reading a parent device records its children's keys, so a
       token that is an ancestor or descendant of a read device is excluded too -- e.g. plan reads
       ``pil900KW`` and the token device is its ``.motors`` sub-device, whose ``waxs_arc`` key the
       parent already records).

    How the reads are inserted (robustness)
    ---------------------------------------
    The token reads are inserted as a **tail right after** each ``create('primary')`` (the same
    pattern :func:`bluesky.preprocessors.baseline_wrapper` uses).  This preprocessor therefore
    **never** intercepts ``save``/``drop`` and cannot disturb the bundle accounting of the run, or
    of any other ``plan_mutator``-based preprocessor whose bundles interleave with it -- in
    particular the ``baseline`` stream opened by ``SupplementalData`` (``sd.baseline``) at run
    open/close.

    Detectors-only by construction
    ------------------------------
    The field reads are injected only inside ``primary`` Event bundles, which a data-taking plan
    (count/scan/...) emits and a bare ``mv``/baseline-only run does not.  So a run that records no
    ``primary`` data gets no injected reads (and writes no file); the name on its start document
    is inert.

    Parameters
    ----------
    plan : generator
        The plan to wrap (the RunEngine passes this when installed on ``RE.preprocessors``).
    template : str
        The default filename template, with recorded-field tokens, e.g.
        ``"{energy_energy:.1f}eV_wa{waxs_arc:04.1f}"``.  If falsy, the plan is returned unchanged.
    token_devices : mapping[str, Readable], optional
        Map of recorded **data key** -> ophyd device that produces it (``{"energy_energy":
        energy, "waxs_arc": waxs, ...}``).  A device is read into the primary stream iff one of
        its keys appears in the run's final name.  Keys with no device are left for the user to
        record (e.g. by including that detector themselves).
    base_name : str or callable, optional
        Fallback existing name to prepend when a run does not carry its own ``sample_name``.  May
        be a plain string, or a **zero-arg callable** evaluated fresh at each ``open_run`` -- the
        wiring passes ``lambda: RE.md.get('sample_name')`` so the live user/proposal prefix is
        picked up per run (and not frozen at install time).  May be ``None``/empty.
    separator : str
        Joiner between the existing name and the template (default ``"_"``).
    primary_stream : str
        Event-stream name to inject reads into (default ``"primary"``).
    skip_if_tokens : bool
        If True (default), do not append ``template`` when the existing name already contains a
        ``{token}`` (the user supplied their own recorded-field template); the user name is then
        used as-is and *its* tokens drive the field recording.  If False, ``template`` is always
        appended.

    Returns
    -------
    generator
        The wrapped plan.
    """
    if not template:
        return (yield from plan)

    token_devices = token_devices or {}

    def _devices_for(name):
        # The (de-duplicated, order-preserving) token devices to read so ``name``'s tokens are
        # fillable -- only those whose recorded key actually appears in ``name``.
        out = []
        for key in template_field_names(name):
            dev = token_devices.get(key)
            if dev is not None and dev not in out:
                out.append(dev)
        return out

    suffix = f"{separator}{template}"
    default_inject = _devices_for(template)

    def _resolve_base():
        # ``base_name`` may be a callable (e.g. ``lambda: RE.md.get('sample_name')``) so the live
        # user/proposal prefix is read fresh per run rather than frozen when the PP was installed.
        b = base_name() if callable(base_name) else base_name
        return "" if b is None else str(b)

    # Per-run state.
    #   ``inject`` : the token devices to read into each primary bundle of THIS run -- decided at
    #                ``open_run`` from the run's *final* name (so a user-supplied ``{token}`` name
    #                records its own tokens), MINUS any device the plan already reads itself (the
    #                ``detectors``/``motors`` named on the open_run), so we never read one object
    #                twice in an Event (which raises in the RunEngine).
    # The reads are inserted as a **tail after** ``create('primary')`` (the same proven pattern as
    # ``bluesky.preprocessors.baseline_wrapper``), so this preprocessor NEVER intercepts ``save``
    # and cannot disturb the bundle accounting of the run or of any other interleaved preprocessor
    # (e.g. the ``baseline`` stream from SupplementalData).
    state = {"inject": list(default_inject)}

    def _related_names(dev):
        """All device names in ``dev``'s tree that could share recorded keys with it:
        ``dev`` itself, every ancestor (walking ``.parent`` to the root), and every descendant
        sub-component.  Used to decide whether ``dev`` would COLLIDE with a device the plan reads
        (reading a parent reads its children's keys, and vice-versa, so either direction is a
        duplicate-key collision in one Event)."""
        names = set()
        # self + ancestors
        node = dev
        seen = set()
        while node is not None and id(node) not in seen:
            seen.add(id(node))
            nm = getattr(node, "name", None)
            if nm:
                names.add(nm)
            node = getattr(node, "parent", None)
        # descendants (sub-components), if this is a Device with a component tree
        walker = getattr(dev, "walk_subdevices", None)
        if callable(walker):
            try:
                for _attr, sub in walker(include_lazy=True):
                    nm = getattr(sub, "name", None)
                    if nm:
                        names.add(nm)
            except Exception:
                pass
        return names

    def _inject_set(name, msg):
        """Token devices to inject for a run named ``name`` whose open_run is ``msg`` -- excluding
        any device the plan reads itself (so no duplicate read in a bundle).

        A token device is excluded when it, an ancestor, or a descendant of it is named in the
        plan's ``detectors``/``motors`` -- because reading a parent device also records its
        children's keys (and vice-versa), so injecting the token too would collide on those keys
        (e.g. plan reads ``pil900KW`` and the token device is its ``.motors`` sub-device, whose
        ``waxs_arc`` key ``pil900KW`` already records)."""
        devs = _devices_for(name)
        if not devs:
            return []
        already = set(msg.kwargs.get("detectors", []) or [])
        already |= set(msg.kwargs.get("motors", []) or [])
        if not already:
            return list(devs)
        return [d for d in devs if not (_related_names(d) & already)]

    def _mutate(msg):
        cmd = msg.command

        if cmd == "open_run":
            existing = msg.kwargs.get("sample_name")
            if existing is None:
                existing = _resolve_base()
            existing = "" if existing is None else str(existing)

            existing_has_tokens = bool(template_field_names(existing))

            if skip_if_tokens and existing_has_tokens:
                # The user supplied their OWN recorded-field template -> use it verbatim (do not
                # append the default, do not sanitize away its braces).  Record from ITS tokens.
                state["inject"] = _inject_set(existing, msg)
                return None, None

            if existing and (existing == template or existing.endswith(suffix)):
                # Already ends with the default template (idempotent / re-entry-safe): leave as-is.
                # Returning ``(None, None)`` also breaks the potential ``plan_mutator`` re-entry
                # loop -- the renamed ``open_run`` we emit below carries the final name, so when
                # ``plan_mutator`` feeds that (new) msg object back through here it lands in this
                # branch (or the token branch above) and passes straight through.
                state["inject"] = _inject_set(existing, msg)
                return None, None

            if existing:
                new_name = f"{sanitize_name(existing)}{suffix}"
            else:
                new_name = template
            state["inject"] = _inject_set(new_name, msg)

            def _renamed_open_run():
                # The response (run uid) to THIS message is what the host plan receives back from
                # ``open_run`` -- so it must be the last (only) message of the head generator.  The
                # detectors/motors kwargs are preserved, so the re-fed msg recomputes the same
                # inject set.
                yield msg._replace(kwargs={**msg.kwargs, "sample_name": new_name})

            return _renamed_open_run(), None

        if cmd == "create" and msg.kwargs.get("name", primary_stream) == primary_stream:
            # Inject the token reads right AFTER the create (as a tail), so they land inside the
            # just-opened primary bundle.  ``inject`` already excludes anything the plan reads
            # itself, so there is no duplicate-read collision and we never touch ``save``.
            if not state["inject"]:
                return None, None

            def _inject_after_create():
                for dev in state["inject"]:
                    yield Msg("read", dev)

            return None, _inject_after_create()

        return None, None

    return (yield from bpp.plan_mutator(plan, _mutate))
