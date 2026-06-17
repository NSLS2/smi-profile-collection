"""
smi_beamline.plans.scan_naming
==============================

Beamline wiring for the **default scan-name template** -- the modern, recorded-field replacement
for the deprecated ``get_scan_md()`` / ``get_more_md()`` (which formatted *live* ``.position`` /
``.get()`` reads into the filename, so the value in the name was not guaranteed to be the value
actually recorded).

The generic, hardware-free engine (:func:`smi_beamline.devices._plan_helpers.scan_name_preprocessor`)
only needs two things: a filename **template** string with ``{recorded_field:spec}`` tokens, and a
``{data_key: device}`` map so it can read the referenced devices into every run.  This module
builds both from a small, declarative **registry of measurement sets** so that the common edits
are one-liners.

Turn-key editing -- the three things you'll change
--------------------------------------------------
Everything lives in :data:`MEASUREMENT_SETS` (named groups of :class:`Token`) and
:data:`DEFAULT_SETS` (which groups are on by default):

1. **Change formatting / layout of a value** -> edit that token's ``fragment`` (a plain
   ``str.format`` snippet, e.g. ``"{energy_energy:.2f}eV"`` -> ``"{energy_energy:.3f}eV"``).
2. **Add a signal** -> add one :class:`Token` to a set (the token carries its own fragment +
   the *device variable name* that produces it).
3. **Add / remove a whole set of measurements** -> add an entry to :data:`MEASUREMENT_SETS`,
   and/or change which set names are in :data:`DEFAULT_SETS`.

Nothing in ``startup.py`` needs to change for any of the above -- the installer resolves device
names against the namespace it is given (``globals()``), so a token referencing a device that is
not present is simply skipped (with a printed note) rather than erroring.

You can also toggle sets **live** in a session::

    from smi_beamline.plans import scan_naming as sn
    sn.enable_set("flux", RE=RE, ns=get_ipython().user_ns)      # turn xbpm flux on
    sn.disable_set("sdd", RE=RE, ns=get_ipython().user_ns)      # drop the SDD token
    sn.show_scan_naming()                                       # print what's active

Naming behaviour (what a run's ``sample_name`` becomes)
------------------------------------------------------
* A plain run name (the user/proposal prefix in ``RE.md['sample_name']``, or a per-run
  ``md={'sample_name': 'myfilm'}``) gets the active template **appended**:
  ``myfilm`` -> ``myfilm_{energy_energy:.2f}eV_wa{waxs_arc:04.1f}_sdd{pil2M_motor_z:.1f}mm``.
* A per-run name that **already contains ``{tokens}``** -- i.e. the user supplied their *own*
  recorded-field template such as ``md={'sample_name': 'test_{energy_energy}eV_{waxs_arc}wa'}``
  -- is taken **verbatim**; the default is *not* appended, and the field recording follows the
  user's tokens.  (This is the ``skip_if_tokens`` behaviour of the engine.)

In both cases the ``{token}`` placeholders are left unfilled for the downstream readout/symlink
worker to fill (via ``str.format``) from each run's recorded event fields.

Token / recorded-field reference (verified against the live device naming)
--------------------------------------------------------------------------
A token's ``key`` is the **flattened ophyd data key** the device publishes (NOT the variable
name).  Confirm one at the console with ``list(dev.describe())``.

========================  ===================  =====================================
key (token)               device var           meaning
========================  ===================  =====================================
``energy_energy``         ``energy``           photon energy, **eV** (PseudoSingle readback)
``waxs_arc``              ``waxs``             WAXS detector arc angle, deg
``pil2M_motor_z``         ``pil2m_pos``        SAXS (Pilatus 2M) detector Z, i.e. SDD, mm
``xbpm2_sumX``            ``xbpm2``            XBPM2 summed current
``ls_input_A_celsius``    ``ls``               LakeShore sample temperature, degC (example)
========================  ===================  =====================================

Units note: the recorded fields are in native EPICS units (energy **eV**, SDD **mm**), and the
``str.format`` worker does not do unit math, so fragments label them ``eV`` / ``mm`` to stay
truthful to what is recorded (``get_scan_md`` showed keV / m).  A derived unit would need either a
new device signal or a small change in the writer's ``single_doc_data``.
"""
from functools import partial

from dataclasses import dataclass

from smi_beamline.devices._plan_helpers import scan_name_preprocessor, template_field_names


__all__ = [
    "Token",
    "MEASUREMENT_SETS",
    "DEFAULT_SETS",
    "DEFAULT_SCAN_NAME_TEMPLATE",
    "active_tokens",
    "build_template",
    "build_token_devices",
    "make_scan_name_preprocessor",
    "install_default_scan_naming",
    "enable_set",
    "disable_set",
    "show_scan_naming",
]


# --------------------------------------------------------------------------- the Token primitive
@dataclass(frozen=True)
class Token:
    """One value in a scan-name template: a ``str.format`` ``fragment`` + the device that feeds it.

    Parameters
    ----------
    fragment : str
        The piece of filename this token contributes, as a ``str.format`` snippet referencing the
        recorded data key, e.g. ``"{energy_energy:.2f}eV"`` or ``"sdd{pil2M_motor_z:.1f}mm"``.
        **This is where both the value's formatting and its surrounding label live** -- change
        the spec (``:.2f``) or the text (``eV``) here.
    device : str
        The **variable name** of the ophyd device that records the key referenced by ``fragment``
        (e.g. ``"energy"``, ``"waxs"``, ``"pil2m_pos"``).  Resolved against the namespace at
        install time; if absent, the token is skipped.  Use ``""``/``None`` for a token whose key
        is always recorded by the plan itself (then nothing extra is read).
    """
    fragment: str
    device: str = ""

    @property
    def keys(self):
        """The recorded data key(s) referenced by ``fragment`` (usually exactly one)."""
        return template_field_names(self.fragment)


# --------------------------------------------------------------------------- the registry
#: Named groups of tokens.  **Edit this** to add/remove signals or whole measurement sets.
#: Each value is a list of :class:`Token`.  A set is included in the default template iff its name
#: is in :data:`DEFAULT_SETS`.
MEASUREMENT_SETS = {
    # The classic get_scan_md trio (energy / WAXS arc / SDD).
    "energy": [Token("{energy_energy:.2f}eV", "energy")],
    "waxs":   [Token("wa{waxs_arc:04.1f}", "waxs")],
    "sdd":    [Token("sdd{pil2M_motor_z:.1f}mm", "pil2m_pos")],

    # Optional sets -- not on by default; enable with enable_set("flux") etc.
    "flux":   [Token("xbpm{xbpm2_sumX:.3f}", "xbpm2")],
    # Example you can copy: sample temperature from the LakeShore.
    # "temperature": [Token("{ls_input_A_celsius:.1f}C", "ls")],
}

#: Which sets are appended to every scan name by default (order = order in the filename).
DEFAULT_SETS = ["energy", "waxs", "sdd"]

#: Token separator within the appended template (also the join to the user/proposal prefix).
SEPARATOR = "_"


def active_tokens(sets=None):
    """Return the flat, ordered list of :class:`Token` for the given set names.

    ``sets`` defaults to :data:`DEFAULT_SETS`.  Unknown set names raise ``KeyError`` so a typo is
    caught immediately.
    """
    names = list(DEFAULT_SETS if sets is None else sets)
    tokens = []
    for name in names:
        if name not in MEASUREMENT_SETS:
            raise KeyError(
                f"unknown measurement set {name!r}; known sets: {sorted(MEASUREMENT_SETS)}"
            )
        tokens.extend(MEASUREMENT_SETS[name])
    return tokens


def build_template(sets=None, *, separator=SEPARATOR):
    """Join the active tokens' fragments into the filename template string."""
    return separator.join(t.fragment for t in active_tokens(sets))


def build_token_devices(ns, sets=None):
    """Build the ``{recorded_data_key: device_object}`` map for the active tokens.

    Parameters
    ----------
    ns : mapping
        The namespace to resolve device *variable names* against (the live ``globals()`` /
        ``user_ns``).  A token whose device is missing/``None`` in ``ns`` is skipped.
    sets : list[str], optional
        Set names (default :data:`DEFAULT_SETS`).

    Returns
    -------
    dict
        ``{data_key: device}`` for every active token whose device resolved.
    """
    mapping = {}
    for tok in active_tokens(sets):
        if not tok.device:
            continue
        dev = ns.get(tok.device) if hasattr(ns, "get") else getattr(ns, tok.device, None)
        if dev is None:
            continue
        for key in tok.keys:
            mapping[key] = dev
    return mapping


#: The default template string, derived from :data:`DEFAULT_SETS` (kept for back-compat / display;
#: the installer recomputes from the live ``MEASUREMENT_SETS``/``DEFAULT_SETS`` each call).
DEFAULT_SCAN_NAME_TEMPLATE = build_template()


# --------------------------------------------------------------------------- preprocessor factory
def make_scan_name_preprocessor(*, template=None, token_devices=None, base_name=None, **kwargs):
    """Return a ready-to-install ``plan -> plan`` preprocessor bound to ``template`` / devices.

    Thin ``functools.partial`` over
    :func:`smi_beamline.devices._plan_helpers.scan_name_preprocessor`.  ``template`` defaults to
    the current :func:`build_template` result.
    """
    if template is None:
        template = build_template()
    return partial(
        scan_name_preprocessor,
        template=template,
        token_devices=token_devices or {},
        base_name=base_name,
        **kwargs,
    )


# --------------------------------------------------------------------------- install / toggle
def install_default_scan_naming(RE, ns=None, *, sets=None, template=None, replace=True,
                                verbose=False, **devices):
    """Append the default scan-name preprocessor to ``RE.preprocessors`` (the beamline default).

    After this, **every** plan run through ``RE`` gets its run-scoped ``sample_name`` extended
    with the active template (filled later by the readout worker from recorded fields), and the
    devices those tokens reference are read into each data-taking run's primary stream.  The
    existing ``sample_name`` is **appended to, never overwritten** -- the per-run name resolves as
    ``<user/proposal prefix or per-run name>_<template>`` (the prefix is read live from
    ``RE.md['sample_name']`` each run).

    Parameters
    ----------
    RE : RunEngine
        The live RunEngine.
    ns : mapping, optional
        Namespace to resolve token device *variable names* against (the live ``globals()`` /
        ``user_ns``).  If omitted, ``devices`` (below) must supply the objects directly.
    sets : list[str], optional
        Which measurement sets to activate (default :data:`DEFAULT_SETS`).
    template : str, optional
        Override the template string outright (default: built from ``sets``).
    replace : bool
        If True (default), first remove any previously-installed scan-name preprocessor (tagged
        ``_smi_scan_naming``) so re-running this in a live session does not stack duplicates.
    verbose : bool
        Print the resolved template and which token devices were/weren't found.
    **devices
        Optional ``var_name=device`` overrides merged over ``ns`` (handy for tests, or to inject a
        device not in the namespace).

    Returns
    -------
    callable
        The installed preprocessor (also appended to ``RE.preprocessors``).
    """
    # Resolve namespace = ns (if any) overlaid with explicit device kwargs.
    resolved = {}
    if ns is not None:
        resolved.update(ns if isinstance(ns, dict) else dict(ns))
    resolved.update({k: v for k, v in devices.items() if v is not None})

    if template is None:
        template = build_template(sets)
    token_devices = build_token_devices(resolved, sets)

    if verbose:
        # Report which token devices resolved vs. were skipped (a token is skipped when its
        # device variable is absent from the namespace).
        found_names = sorted({
            tok.device
            for tok in active_tokens(sets)
            if tok.device and any(k in token_devices for k in tok.keys)
        })
        missing = sorted({
            tok.device
            for tok in active_tokens(sets)
            if tok.device and not any(k in token_devices for k in tok.keys)
        })
        print(f"scan-naming template: {template}")
        print(f"  token devices found: {found_names}")
        if missing:
            print(f"  NOT FOUND (token skipped): {missing}")

    if replace:
        RE.preprocessors[:] = [
            pp for pp in RE.preprocessors if not getattr(pp, "_smi_scan_naming", False)
        ]

    pp = make_scan_name_preprocessor(
        template=template,
        token_devices=token_devices,
        base_name=lambda: RE.md.get("sample_name"),
    )
    # Tag it (and remember its config) so toggles / re-installs can find and rebuild it.
    try:
        pp._smi_scan_naming = True
        pp._smi_ns = resolved
        pp._smi_sets = list(DEFAULT_SETS if sets is None else sets)
    except (AttributeError, TypeError):
        pass

    RE.preprocessors.append(pp)
    return pp


def _current_pp(RE):
    """Return the installed scan-naming preprocessor on ``RE`` (or ``None``)."""
    for pp in getattr(RE, "preprocessors", []):
        if getattr(pp, "_smi_scan_naming", False):
            return pp
    return None


def enable_set(name, *, RE, ns=None):
    """Turn measurement set ``name`` ON and re-install the preprocessor on ``RE``.

    Resolves devices against ``ns`` if given, else against the namespace captured at the last
    install.  Idempotent.
    """
    if name not in MEASUREMENT_SETS:
        raise KeyError(f"unknown set {name!r}; known: {sorted(MEASUREMENT_SETS)}")
    pp = _current_pp(RE)
    sets = list(getattr(pp, "_smi_sets", DEFAULT_SETS)) if pp else list(DEFAULT_SETS)
    if name not in sets:
        sets.append(name)
    use_ns = ns if ns is not None else (getattr(pp, "_smi_ns", {}) if pp else {})
    return install_default_scan_naming(RE, use_ns, sets=sets, verbose=True)


def disable_set(name, *, RE, ns=None):
    """Turn measurement set ``name`` OFF and re-install the preprocessor on ``RE``."""
    pp = _current_pp(RE)
    sets = list(getattr(pp, "_smi_sets", DEFAULT_SETS)) if pp else list(DEFAULT_SETS)
    sets = [s for s in sets if s != name]
    use_ns = ns if ns is not None else (getattr(pp, "_smi_ns", {}) if pp else {})
    return install_default_scan_naming(RE, use_ns, sets=sets, verbose=True)


def show_scan_naming(RE=None):
    """Print the available sets, which are active, and the current template."""
    pp = _current_pp(RE) if RE is not None else None
    active = list(getattr(pp, "_smi_sets", DEFAULT_SETS)) if pp else list(DEFAULT_SETS)
    print("Measurement sets (■ = active by default install):")
    for name, toks in MEASUREMENT_SETS.items():
        mark = "■" if name in active else "□"
        frags = " ".join(t.fragment for t in toks)
        print(f"  {mark} {name:12s} {frags}")
    print(f"\nActive sets : {active}")
    print(f"Template    : {build_template(active)}")
    if pp is not None:
        print("(installed on the given RE)")
