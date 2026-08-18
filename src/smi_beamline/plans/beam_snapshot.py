"""Beam-positioning snapshot helpers for commissioning.

This module intentionally starts with save + dry-run compare.  Restore should
remain conservative until the saved scope and ordering are validated live.
"""

from datetime import datetime, timezone
import getpass
import math

from smi_beamline.devices.bimorph import N_BIMORPH_CH


SNAPSHOT_KEY_PREFIX = "beam_position_snapshots"
SNAPSHOT_INDEX_KEY = "beam_position_snapshots:index"
SCHEMA_VERSION = 1


__all__ = [
    "beam_snapshot_devices",
    "save_beam_position_snapshot",
    "compare_beam_position_snapshot",
    "restore_beam_position_snapshot",
    "format_snapshot_diff",
    "list_beam_position_snapshots",
]


def _now():
    return datetime.now(timezone.utc).isoformat()


def _safe_get(obj):
    try:
        return obj.get()
    except Exception as exc:  # noqa: BLE001 - live read diagnostics should be explicit, not fatal
        return {"error": "{}: {}".format(type(exc).__name__, exc)}


def _as_jsonable(value):
    if isinstance(value, dict):
        return {str(k): _as_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_as_jsonable(v) for v in value]
    try:
        import numpy as np

        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, np.ndarray):
            return value.tolist()
    except Exception:
        pass
    return value


def _num(value):
    if isinstance(value, dict) and "error" in value:
        return None
    try:
        return float(value)
    except Exception:
        return None


def _signal_value(signal):
    return _as_jsonable(_safe_get(signal))


def _optional_signal_value(device, *attrs):
    for attr in attrs:
        if hasattr(device, attr):
            return _signal_value(getattr(device, attr))
    return None


def _motor_item(name, group, motor, *, restore=True):
    return {
        "name": name,
        "group": group,
        "kind": "motor",
        "device": getattr(motor, "name", name),
        "pv": getattr(motor, "prefix", None),
        "restore": bool(restore),
        "readback": _signal_value(motor.user_readback),
        "setpoint": _signal_value(motor.user_setpoint),
        "offset": _signal_value(motor.user_offset),
        "low_limit": _signal_value(motor.low_limit),
        "high_limit": _signal_value(motor.high_limit),
        "speed": _optional_signal_value(motor, "velocity", "speed"),
        "units": _signal_value(getattr(motor, "motor_egu", None)) if hasattr(motor, "motor_egu") else None,
        "timestamp": _now(),
    }


def _bimorph_voltage_items(name, group, dev):
    items = []
    for i in range(N_BIMORPH_CH):
        output = getattr(dev, "ch{}".format(i))
        target = getattr(dev, "ch{}_trg_rb".format(i))
        status = getattr(dev, "ch{}_status".format(i))
        items.append({
            "name": "{}.ch{}".format(name, i),
            "group": group,
            "kind": "bimorph_voltage",
            "device": getattr(dev, "name", name),
            "channel": i,
            "pv": getattr(output, "pvname", None),
            "restore": True,
            "readback": _signal_value(output),
            "target_readback": _signal_value(target),
            "status": _signal_value(status),
            "units": "V",
            "timestamp": _now(),
        })
    return items


def _registry_from_namespace(ns):
    entries = []
    for dev_name in ("wbs", "ssa", "eslit", "cslit"):
        dev = ns[dev_name]
        for axis in ("h", "hg", "v", "vg"):
            entries.append(("{}.{}".format(dev_name, axis), "slits", getattr(dev, axis), True))

    entries.extend([
        ("energy.bragg", "dcm", ns["energy"].bragg, False),
        ("energy.dcmgap", "dcm", ns["energy"].dcmgap, False),
        ("dcm_config.pitch", "dcm", ns["dcm_config"].pitch, False),
        ("dcm_config.roll", "dcm", ns["dcm_config"].roll, False),
        ("xbpm2_pos.x", "diagnostics", ns["xbpm2_pos"].x, False),
        ("xbpm2_pos.y", "diagnostics", ns["xbpm2_pos"].y, False),
        ("xbpm3_pos.x", "diagnostics", ns["xbpm3_pos"].x, False),
        ("xbpm3_pos.y", "diagnostics", ns["xbpm3_pos"].y, False),
        ("energy.ivugap", "undulator", ns["energy"].ivugap, False),
    ])

    for dev_name in ("hfm", "vfm", "vdm"):
        dev = ns[dev_name]
        for axis in ("x", "y", "th"):
            entries.append(("{}.{}".format(dev_name, axis), "mirrors", getattr(dev, axis), True))

    return entries


def _motor_registry(ns):
    return {name: motor for name, group, motor, restore in _registry_from_namespace(ns)}


def _bimorph_registry(ns):
    return {"hfm_voltage": ns["hfm_voltage"], "vfm_voltage": ns["vfm_voltage"]}


def beam_snapshot_devices(namespace=None):
    """Return the explicit commissioning registry used by snapshots."""
    ns = namespace if namespace is not None else globals()
    registry = []
    for name, group, motor, restore in _registry_from_namespace(ns):
        registry.append({
            "name": name,
            "group": group,
            "kind": "motor",
            "device": getattr(motor, "name", name),
            "restore": restore,
        })
    for dev_name in ("hfm_voltage", "vfm_voltage"):
        for i in range(N_BIMORPH_CH):
            registry.append({
                "name": "{}.ch{}".format(dev_name, i),
                "group": "mirror_voltages",
                "kind": "bimorph_voltage",
                "device": dev_name,
                "channel": i,
                "restore": True,
            })
    return registry


def _collect_snapshot_items(ns):
    items = []
    for name, group, motor, restore in _registry_from_namespace(ns):
        items.append(_motor_item(name, group, motor, restore=restore))
    items.extend(_bimorph_voltage_items("hfm_voltage", "mirror_voltages", ns["hfm_voltage"]))
    items.extend(_bimorph_voltage_items("vfm_voltage", "mirror_voltages", ns["vfm_voltage"]))
    return items


def _snapshot_payload(name, ns, note=None):
    return {
        "schema_version": SCHEMA_VERSION,
        "snapshot_name": name,
        "created": _now(),
        "beamline": "smi",
        "operator": getpass.getuser(),
        "note": note,
        "items": _collect_snapshot_items(ns),
    }


def _snapshot_key(name):
    return "{}:{}".format(SNAPSHOT_KEY_PREFIX, name)


def _store_snapshot(mdsave, snapshot):
    name = snapshot["snapshot_name"]
    mdsave[_snapshot_key(name)] = snapshot
    index = dict(mdsave.get(SNAPSHOT_INDEX_KEY, {}))
    index[name] = {
        "created": snapshot["created"],
        "note": snapshot.get("note"),
        "count": len(snapshot.get("items", [])),
    }
    mdsave[SNAPSHOT_INDEX_KEY] = index


def save_beam_position_snapshot(name=None, *, note=None, namespace=None, store=None):
    """Save the current beam-positioning state into Redis-backed ``mdsave``."""
    ns = namespace if namespace is not None else globals()
    if name is None:
        name = "beam_position_{}".format(datetime.now().strftime("%Y_%m_%d_%H%M%S"))
    mds = store if store is not None else ns["mdsave"]
    snapshot = _snapshot_payload(str(name), ns, note=note)
    _store_snapshot(mds, snapshot)
    print("saved beam position snapshot {!r}: {} items".format(str(name), len(snapshot["items"])))
    return snapshot


def _load_snapshot(snapshot_or_name, ns, store):
    if isinstance(snapshot_or_name, dict):
        return snapshot_or_name
    mds = store if store is not None else ns["mdsave"]
    return mds[_snapshot_key(str(snapshot_or_name))]


def _current_by_name(ns):
    return {item["name"]: item for item in _collect_snapshot_items(ns)}


def _diff_status(current, saved):
    cur = _num(current.get("readback")) if current else None
    old = _num(saved.get("readback")) if saved else None
    if current is None:
        return "missing current", None
    if saved is None:
        return "missing saved", None
    if cur is None or old is None:
        if current.get("readback") == saved.get("readback"):
            return "unchanged", None
        return "changed", None
    delta = cur - old
    if math.isclose(delta, 0.0, abs_tol=1e-9):
        return "unchanged", delta
    if not saved.get("restore"):
        return "read-only diff", delta
    return "would move", delta


def _selected(item, *, names=None, groups=None, exclude=None):
    name = item.get("name")
    group = item.get("group")
    if names is not None and name not in names:
        return False
    if groups is not None and group not in groups:
        return False
    if exclude is not None and name in exclude:
        return False
    return True


def _restore_rows(saved, current, *, names=None, groups=None, exclude=None, tolerance=0.0):
    current_by_name = {item["name"]: item for item in current}
    rows = []
    for item in saved.get("items", []):
        if not _selected(item, names=names, groups=groups, exclude=exclude):
            continue
        row = {
            "name": item.get("name"),
            "group": item.get("group"),
            "target": item.get("readback"),
            "current": current_by_name.get(item.get("name"), {}).get("readback"),
            "units": item.get("units"),
            "status": "pending",
        }
        if not item.get("restore"):
            row["status"] = "skipped read-only"
        elif item.get("kind") not in ("motor", "bimorph_voltage"):
            row["status"] = "skipped non-motor"
        elif _num(item.get("readback")) is None:
            row["status"] = "skipped non-numeric target"
        else:
            cur = _num(row["current"])
            target = _num(row["target"])
            row["delta"] = None if cur is None else target - cur
            if cur is not None and math.isclose(cur, target, abs_tol=float(tolerance)):
                row["status"] = "already there"
            else:
                row["status"] = "would move"
        rows.append(row)
    return rows


def _print_restore_rows(rows, *, dry_run):
    print("beam position snapshot restore {}".format("dry run" if dry_run else "plan"))
    print("{:<24s} {:<16s} {:>14s} {:>14s} {:>12s} {:<8s} {}".format(
        "name", "group", "current", "target", "delta", "units", "status"))
    for row in rows:
        delta = "" if row.get("delta") is None else "{:.6g}".format(row["delta"])
        print("{:<24s} {:<16s} {:>14s} {:>14s} {:>12s} {:<8s} {}".format(
            str(row.get("name")),
            str(row.get("group") or ""),
            str(row.get("current")),
            str(row.get("target")),
            delta,
            str(row.get("units") or ""),
            str(row.get("status")),
        ))


def format_snapshot_diff(current, saved):
    """Return printable diff rows comparing current collected state to a snapshot."""
    current_by_name = {item["name"]: item for item in current}
    saved_by_name = {item["name"]: item for item in saved.get("items", [])}
    rows = []
    for name in sorted(set(current_by_name) | set(saved_by_name)):
        cur = current_by_name.get(name)
        old = saved_by_name.get(name)
        status, delta = _diff_status(cur, old)
        rows.append({
            "name": name,
            "group": (cur or old or {}).get("group"),
            "current": (cur or {}).get("readback"),
            "snapshot": (old or {}).get("readback"),
            "delta": delta,
            "units": (cur or old or {}).get("units"),
            "status": status,
            "action": "none" if status in ("unchanged", "read-only diff") else status,
        })
    return rows


def _print_diff(rows):
    print("{:<24s} {:<16s} {:>14s} {:>14s} {:>12s} {:<8s} {}".format(
        "name", "group", "current", "snapshot", "delta", "units", "status"))
    for row in rows:
        delta = "" if row["delta"] is None else "{:.6g}".format(row["delta"])
        print("{:<24s} {:<16s} {:>14s} {:>14s} {:>12s} {:<8s} {}".format(
            str(row["name"]),
            str(row.get("group") or ""),
            str(row.get("current")),
            str(row.get("snapshot")),
            delta,
            str(row.get("units") or ""),
            str(row.get("status")),
        ))


def compare_beam_position_snapshot(snapshot_or_name, *, namespace=None, store=None, print_table=True):
    """Dry-run comparison between current state and a saved snapshot.  Never moves hardware."""
    ns = namespace if namespace is not None else globals()
    saved = _load_snapshot(snapshot_or_name, ns, store)
    current = _collect_snapshot_items(ns)
    rows = format_snapshot_diff(current, saved)
    if print_table:
        _print_diff(rows)
    return rows


def restore_beam_position_snapshot(snapshot_or_name, *, namespace=None, store=None,
                                   names=None, groups=None, exclude=None, dry_run=True,
                                   tolerance=0.0, print_table=True):
    """Restore restorable motors from a beam-position snapshot.

    This is intentionally conservative: diagnostic/DCM axes saved as ``restore=False`` are never
    moved.  Bimorph voltages are restored by staging all 16 channel targets on a mirror, then
    applying that mirror once; unselected channels are staged from current outputs to avoid
    applying stale targets.  The default ``dry_run=True`` prints the planned actions without
    yielding any move messages; pass ``dry_run=False`` to emit the restore plan.

    Parameters
    ----------
    snapshot_or_name : dict or str
        Snapshot payload or saved snapshot name.
    names, groups, exclude : iterable, optional
        Limit restore to explicit item names, groups, or exclude names.
    dry_run : bool
        If True, only report.  If False, move selected restorable motors to saved readbacks.
    tolerance : float
        Skip moves whose current readback is already within this absolute tolerance.
    """
    ns = namespace if namespace is not None else globals()
    saved = _load_snapshot(snapshot_or_name, ns, store)
    current = _collect_snapshot_items(ns)
    names = None if names is None else set(names)
    groups = None if groups is None else set(groups)
    exclude = None if exclude is None else set(exclude)
    rows = _restore_rows(saved, current, names=names, groups=groups, exclude=exclude,
                         tolerance=tolerance)
    if print_table:
        _print_restore_rows(rows, dry_run=dry_run)

    if dry_run:
        return rows

    def _plan():
        import bluesky.plan_stubs as bps

        motors = _motor_registry(ns)
        bimorphs = _bimorph_registry(ns)
        for row in rows:
            if row["status"] != "would move" or str(row["name"]).split(".", 1)[0] in bimorphs:
                continue
            motor = motors.get(row["name"])
            if motor is None:
                print("skipping missing motor {!r}".format(row["name"]))
                continue
            yield from bps.mv(motor, float(row["target"]))
            row["status"] = "moved"
        for dev_name, dev in bimorphs.items():
            dev_rows = [row for row in rows
                        if row["status"] == "would move"
                        and str(row["name"]).startswith(dev_name + ".")]
            if not dev_rows:
                continue
            targets = list(dev.read_outputs())
            for row in dev_rows:
                ch = int(str(row["name"]).rsplit("ch", 1)[1])
                targets[ch] = float(row["target"])
            yield from dev.set_targets(targets)
            yield from dev.apply_and_wait()
            for row in dev_rows:
                row["status"] = "moved"
        return rows

    return _plan()


def list_beam_position_snapshots(*, namespace=None, store=None):
    ns = namespace if namespace is not None else globals()
    mds = store if store is not None else ns["mdsave"]
    index = dict(mds.get(SNAPSHOT_INDEX_KEY, {}))
    for name, info in sorted(index.items(), key=lambda kv: kv[1].get("created", "")):
        print("{:<28s} {:<32s} {:>3}  {}".format(
            name, info.get("created", ""), info.get("count", ""), info.get("note") or ""))
    return index


# The factory imports this module before startup.py updates the IPython namespace.  Pulling the
# live objects from package instance modules here makes the public functions usable directly at the prompt.
try:
    from smi_beamline.devices._context import get_config as _get_config
    mdsave = _get_config()
    from smi_beamline.instances.slits import wbs, ssa, eslit, cslit  # noqa: F401
    from smi_beamline.instances.energy import energy, dcm_config  # noqa: F401
    from smi_beamline.instances.xbpms import xbpm2_pos, xbpm3_pos  # noqa: F401
    from smi_beamline.instances.mirrors import hfm, vfm, vdm, hfm_voltage, vfm_voltage  # noqa: F401
except Exception:
    # Keep import-clean for tests/offline use; callers can pass namespace/store explicitly.
    pass
