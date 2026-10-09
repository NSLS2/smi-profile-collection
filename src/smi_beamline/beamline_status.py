"""Compact read-only console overview; imports/constructs no beamline devices.

Device-owned field descriptions are intentionally curated: recursively reading
every ophyd component would include command PVs, image arrays, and duplicate aliases.
Instance location metadata supplies beam order, hutch boundaries, and labels.
All hardware reads go through Reader.signal, with per-read and total budgets.
"""

from dataclasses import dataclass
from datetime import datetime
import math
import re
import time


READ_TIMEOUT = 0.15
READ_BUDGET = 3.0
LABEL_WIDTH = 17
FIELD_WIDTH = 34


@dataclass(frozen=True)
class Field:
    label: str
    value: str


@dataclass(frozen=True)
class Row:
    label: str
    fields: tuple
    boundary: str = ""
    wide: bool = False

    def __iter__(self):
        # Preserve the simple label/fields interface used by console consumers.
        return iter((self.label, self.fields))


class Reader:
    def __init__(self, namespace, *, timeout=READ_TIMEOUT, budget=READ_BUDGET):
        self.namespace = namespace
        self.timeout = timeout
        self.deadline = time.monotonic() + budget
        self.cache = {}

    def resolve(self, path):
        if not isinstance(path, str):
            return path
        root, *attrs = path.split(".")
        obj = self.namespace[root]
        for attr in attrs:
            obj = getattr(obj, attr)
        return obj

    def signal(self, signal):
        key = id(signal)
        if key not in self.cache:
            try:
                if not signal.connected:
                    raise ConnectionError("OFFLINE")
                remaining = self.deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("BUDGET")
                timeout = min(self.timeout, remaining)
                # Signal.get accepts extra kwargs; EpicsSignal honors both limits.
                value = signal.get(timeout=timeout, connection_timeout=timeout)
                self.cache[key] = value
            except Exception as exc:
                self.cache[key] = exc
        value = self.cache[key]
        if isinstance(value, Exception):
            raise value
        return value

    def get(self, path):
        return self.signal(self.resolve(path))

    def number(self, path, *, scale=1):
        value = float(self.get(path)) * scale
        if not math.isfinite(value):
            raise ValueError("non-finite")
        return value

    def enum(self, path):
        signal = self.resolve(path)
        value = self.signal(signal)
        if not isinstance(value, str):
            # Cached metadata only: no synchronous enum-metadata fetch.
            enums = signal.metadata.get("enum_strs")
            if enums and int(value) == value and 0 <= int(value) < len(enums):
                value = enums[int(value)]
        return str(value)

    def motor_value(self, path):
        motor = self.resolve(path)
        signal = getattr(motor, "user_readback", None)
        if signal is None:
            signal = motor.readback
        value = float(self.signal(signal))
        if not math.isfinite(value):
            raise ValueError("non-finite")
        return value

    def motor(self, path, *, units=None, precision=3):
        motor = self.resolve(path)
        value = self.motor_value(path)
        if units is None:
            egu = getattr(motor, "motor_egu", None)
            units = str(self.signal(egu)) if egu is not None else motor.readback.metadata.get("units", "?")
        moving = ""
        done = getattr(motor, "motor_done_move", None)
        if done is not None and float(self.signal(done)) == 0:
            moving = " MOVING"
        return f"{value:.{precision}f} {units}{moving}"


def _failure(exc):
    if isinstance(exc, (KeyError, AttributeError)):
        return "N/A"
    if isinstance(exc, ConnectionError):
        return "OFFLINE"
    if isinstance(exc, TimeoutError):
        return "BUDGET" if str(exc) == "BUDGET" else "TIMEOUT"
    return "ERROR"


def _field(label, read):
    try:
        return Field(label, str(read()))
    except Exception as exc:
        return Field(label, _failure(exc))


def status_rows(namespace, *, timeout=READ_TIMEOUT, budget=READ_BUDGET, reader=None):
    """Render device-owned field descriptions in instance-owned beam order."""
    from smi_beamline.instances.layout import status_entries
    from smi_beamline.devices.status import numeric_state

    r = reader if reader is not None else Reader(namespace, timeout=timeout, budget=budget)
    computed = {}

    def cached(key, read):
        if key not in computed:
            try:
                computed[key] = read()
            except Exception as exc:
                computed[key] = exc
        value = computed[key]
        if isinstance(value, Exception):
            raise value
        return value

    def value(spec, name, context):
        def path(relative):
            relative = relative.format(**context)
            return relative[1:] if relative.startswith("@") else ".".join(filter(None, (name, relative)))

        target = path(spec.path)
        kind = spec.kind
        if kind == "motor":
            return r.motor(target, units=spec.units, precision=int(spec.precision[1:-1]))
        if kind == "motor_pair":
            a = _field("", lambda: r.motor(target)).value
            b = _field("", lambda: r.motor(path(spec.reference))).value
            return f"{a} / {b}"
        if kind == "number":
            units = spec.units
            if units is None:
                units = r.resolve(target).metadata.get("units") or "raw"
            return f"{r.number(target, scale=spec.scale):{spec.precision}} {units}".strip()
        if kind == "text":
            return str(r.get(target))
        if kind == "enum":
            return r.enum(target)
        if kind in ("permit", "on_off"):
            raw = r.get(target)
            words = ("DISABLED", "ENABLED") if kind == "permit" else ("OFF", "ON")
            if str(raw).upper() in words:
                return str(raw).upper()
            return numeric_state(raw, dict(enumerate(words)))
        device = r.resolve(target)
        if kind == "state":
            return device.read_state(read_signal=r.signal)
        if kind == "pressure":
            info = device.pressure_state(spec.reference, read_signal=r.signal)
            if info["state"] in ("Pumped", "Vented"):
                return info["state"]
            raw = info["value"]
            return f"{raw:.2e} {info['units']}" if isinstance(raw, float) else f"{raw} {info['units']}"
        if kind == "bimorph":
            info = device.read_output_state(read_signal=r.signal)
            return f"{info['state']} {info['first']:.0f}, {info['min']:.0f}–{info['max']:.0f} {info['units']}"
        if kind == "lenses":
            states = device.read_lens_state(read_signal=r.signal)
            inserted = [str(i) for i, state in states.items() if state == "IN"]
            unknown = [str(i) for i, state in states.items() if state == "UNKNOWN"]
            text = ", ".join(inserted) or ("none confirmed" if unknown else "none")
            return text + ("; UNKNOWN: " + ", ".join(unknown) if unknown else "")
        if kind.startswith("attenuation_"):
            info = cached((target, "attenuation"), lambda: device.read_state(
                energy_eV=r.number(path(spec.reference)), read_signal=r.signal))
            return {
                "attenuation_factor": f"{info['attenuation_factor']:.4g}x",
                "attenuation_transmission": f"{info['transmission']:.4g}",
                "attenuation_energy": f"{info['energy_eV']:.1f} eV",
                "attenuation_foils": ",".join(info["inserted"]) or "none",
            }[kind]
        if kind == "energy_difference":
            info = device.energy_difference(r.number(path(spec.reference)), read_signal=r.signal)
            diff = info["difference_eV"]
            diff = 0.0 if round(diff, 1) == 0 else diff
            return f"{'OK' if info['matches'] else 'MISMATCH'} {diff:+.1f} eV"
        if kind == "beamstop_motor":
            motors = device.selected_beamstop_motors(read_signal=r.signal)
            if motors is None:
                return "N/A"
            return r.motor(motors[0 if spec.reference == "x" else 1], units="mm")
        raise ValueError(f"Unknown status field kind: {kind}")

    rows = []
    for name, location, description in status_entries(namespace):
        context = {"name": name, "label": location.label, "short_label": location.short_label}
        for spec in description:
            fields = tuple(_field(field.label.format(**context), lambda field=field: value(field, name, context))
                           for field in spec.fields)
            rows.append(Row(spec.label.format(**context), fields, location.boundary, spec.wide))
    return rows


def _clean(text):
    # Keep IOC strings from inserting terminal control sequences or new lines.
    return "".join(c if c.isprintable() else " " for c in str(text))


def _fit(text, width):
    text = _clean(text)
    return (text if len(text) <= width else text[:width - 1] + "…").ljust(width)


def _value_color(shell, text, color):
    """Uniform blue numbers, neutral units, and semantic state colors."""
    if any(word in text.upper() for word in ("MISMATCH", "ERROR", "FAULT", "ABORT")):
        return color(shell, text, "1;91")
    pattern = (
        r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
        r"|NOT OPEN|[A-Za-z_/?]+"
    )
    parts, end = [], 0
    for match in re.finditer(pattern, text):
        parts.append(text[end:match.start()])
        token = match.group()
        state = token.upper()
        if token in ("mm", "um", "deg", "mrad", "eV", "keV", "s", "mA", "V", "Torr", "mbar", "raw", "x"):
            parts.append(token)
        elif state == "VENTED":
            parts.append(color(shell, token, "91"))
        elif state in ("OPEN", "ON", "OK", "IDLE", "ENABLED", "PUMPED"):
            parts.append(color(shell, token, "92"))
        else:
            numeric = token[0].isdigit() or token[0] in "+-."
            parts.append(color(shell, token, "94" if numeric else "93"))
        end = match.end()
    parts.append(text[end:])
    return "".join(parts)


def show_status(shell, color):
    """Render a fixed-width overview; color is supplied by the magic extension."""
    rows = status_rows(shell.user_ns)
    widths = (LABEL_WIDTH, FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH)
    def border(left, middle, right):
        return left + middle.join("─" * (w + 2) for w in widths) + right

    print(f"SMI STATUS  {datetime.now():%Y-%m-%d %H:%M:%S}  upstream → downstream")
    print(border("┌", "┬", "┐"))
    for row in rows:
        label, fields = row
        if row.boundary:
            raw = fields[0].value
            # Compact operator-facing label for the existing closed/not-open readback.
            state = "CLOSED" if raw in ("NOT OPEN", "CLOSED") else raw
            code = "1;92" if state == "OPEN" else ("1;91" if state == "CLOSED" else "1;93")
            opening = f"[ {row.boundary}: {_fit(state, 24).rstrip()} ]"
            heading = f" {label} "
            inner_width = len(border("┌", "┬", "┐")) - 2
            remaining = inner_width - len(heading) - len(opening)
            left = remaining // 2
            print("├" + color(shell, heading, "1;36") + "─" * left
                  + color(shell, opening, code) + "─" * (remaining - left) + "┤")
            continue
        cells = [color(shell, _fit(label, LABEL_WIDTH), "1;36")]
        if row.wide:
            value = _fit(fields[0].value, 3 * FIELD_WIDTH + 6)
            print("│ " + cells[0] + " │ " + _value_color(shell, value, color) + " │")
            continue
        for index in range(3):
            if index >= len(fields):
                cells.append(" " * FIELD_WIDTH)
                continue
            field = fields[index]
            prefix = _fit(field.label, 10) + " "
            value = _fit(field.value, FIELD_WIDTH - len(prefix))
            value = _value_color(shell, value, color)
            cells.append(color(shell, prefix, "36") + value)
        print("│ " + " │ ".join(cells) + " │")
    print(border("└", "┴", "┘"))
