"""Interactive helpers for cleaning persistent RunEngine metadata."""

from pprint import pformat

from smi_beamline.devices import _context


RE_MD_WHITELIST = frozenset({
    "SAF_number",
    "beamline_attenuators",
    "beamline_name",
    "beamline_sample_environment",
    "cycle",
    "data_session",
    "facility",
    "project_name",
    "proposal",
    "sample_name",
    "scan_id",
    "start_datetime",
    "tiled_access_tags",
    "username",
    "versions"
    #"SAXS_setup", # not sure we want this persistant
})


def _live_re_md():
    md = _context.get_md()
    if md == {} and _context.get_re() is None:
        raise RuntimeError("No RunEngine is configured; pass a dict-like md explicitly.")
    return md


def _format_value(value):
    text = pformat(value, width=88, compact=True)
    if len(text) > 1000:
        return text[:997] + "..."
    return text


def clean_re_md(md=None, *, whitelist=RE_MD_WHITELIST):
    """Interactively remove non-whitelisted keys from ``RE.md``.

    This is a startup-console convenience for the persistent Redis-backed
    metadata dict.  It treats ``md`` as a normal mutable mapping: it lists every
    key not in ``whitelist``, asks once whether to continue, then asks before
    deleting each key.

    Parameters
    ----------
    md : mutable mapping, optional
        Dict-like metadata object to clean.  Defaults to the live ``RE.md``.
    whitelist : collection of str, optional
        Keys that should remain in ``RE.md``.

    Returns
    -------
    list[str]
        Keys deleted during this call.
    """
    if md is None:
        md = _live_re_md()

    keep = set(whitelist)
    extra_keys = sorted(k for k in md.keys() if k not in keep)

    if not extra_keys:
        print("RE.md has no extraneous keys.")
        return []

    print("Extraneous RE.md keys:")
    for key in extra_keys:
        print(f"- {key}: {_format_value(md[key])}")

    answer = input("Review these keys for removal? [y/N] ").strip().lower()
    if answer not in {"y", "yes"}:
        print("No changes made.")
        return []

    deleted = []
    for key in extra_keys:
        if key not in md:
            continue

        print(f"\n{key}: {_format_value(md[key])}")
        while True:
            action = input("Delete this key? [d]elete/[s]kip/[e]nd: ").strip().lower()
            if action in {"d", "delete", "y", "yes"}:
                del md[key]
                deleted.append(key)
                print(f"Deleted {key!r}.")
                break
            if action in {"s", "skip", "n", "no", ""}:
                print(f"Skipped {key!r}.")
                break
            if action in {"e", "end", "q", "quit"}:
                print("Stopped cleanup.")
                return deleted
            print("Please enter d/delete, s/skip, or e/end.")

    print(f"Deleted {len(deleted)} key(s).")
    return deleted
