"""Hardware-free, changes-first console rendering for snapshot reports."""

import math
import shutil
import textwrap
from numbers import Real


def _unavailable(value):
    return (
        value is None
        or (isinstance(value, dict) and "error" in value)
        or (isinstance(value, Real) and not math.isfinite(value))
    )


def _cell(value):
    if value is None:
        return "N/A"
    if isinstance(value, Real) and not isinstance(value, (int, bool)):
        return f"{value:.9g}"
    # ASCII escapes keep control sequences/newlines and wide Unicode from
    # breaking the table or injecting terminal commands. Nothing is truncated.
    return str(value).encode("unicode_escape").decode("ascii").replace("|", r"\x7c")


def _box(headers, records, width):
    cells = [[_cell(value) for value in record] for record in records]
    minimums = [10, 8, 8, 8, 4, 12]
    if width < sum(minimums) + 3 * len(headers) + 1:
        # Narrow consoles get vertically arranged records, not overflowing columns.
        lines = []
        for record in cells:
            lines.extend(_box_pairs(list(zip(headers, record, strict=True)), width))
        return lines
    widths = [
        max(len(header), *(len(row[i]) for row in cells))
        for i, header in enumerate(headers)
    ]
    budget = width - 3 * len(headers) - 1
    while sum(widths) > budget:
        candidates = [i for i, size in enumerate(widths) if size > minimums[i]]
        if not candidates:
            break
        index = max(candidates, key=lambda i: widths[i])
        widths[index] -= 1
    return _draw_box(headers, cells, widths)


def _box_pairs(pairs, width):
    widths = [min(8, max(4, width // 3)), 0]
    widths[1] = max(1, width - widths[0] - 7)
    return _draw_box(["Field", "Value"], pairs, widths)


def _draw_box(headers, records, widths):
    border = "+" + "+".join("-" * (size + 2) for size in widths) + "+"

    def render(record):
        wrapped = [
            textwrap.wrap(text, size, drop_whitespace=False, replace_whitespace=False)
            or [""]
            for text, size in zip(record, widths, strict=True)
        ]
        for index in range(max(map(len, wrapped))):
            yield (
                "| "
                + " | ".join(
                    (parts[index] if index < len(parts) else "").ljust(size)
                    for parts, size in zip(wrapped, widths, strict=True)
                )
                + " |"
            )

    lines = [border, *render(headers), border]
    for record in records:
        lines.extend(render(record))
        lines.append(border)
    return lines


def snapshot_report(rows, *, title, target_key, show_unchanged=False, width=None):
    """Render all changes/issues, hiding verified equal rows by default.

    The returned row data and restore policy are not altered. Unknown current
    values are displayed for review even if the restore policy schedules a move.
    """
    width = max(
        24, width if width is not None else shutil.get_terminal_size((120, 24)).columns
    )
    unchanged, changes, attention = [], [], []
    for row in rows:
        current, target = row.get("current"), row.get(target_key)
        status = row.get("status", "unknown")
        unavailable = _unavailable(current) or _unavailable(target)
        if unavailable:
            attention.append(row)
        elif status in ("unchanged", "already there") or (
            status == "skipped read-only" and current == target
        ):
            unchanged.append(row)
        elif status == "would move":
            changes.append(row)
        else:
            attention.append(row)

    lines = [
        title,
        (
            f"{len(rows)} selected values: {len(unchanged)} unchanged; "
            f"{len(changes)} would change; {len(attention)} other differences / need review."
        ),
    ]
    headers = [
        "Setting",
        "Current",
        "Target" if target_key == "target" else "Saved",
        "Delta",
        "Units",
        "Status",
    ]
    for heading, selected in (
        ("Would change", changes),
        ("Other differences / needs review (not necessarily restorable)", attention),
        ("Unchanged", unchanged if show_unchanged else []),
    ):
        if not selected:
            continue
        lines.extend(["", heading])
        records = []
        for row in selected:
            status = row.get("status", "unknown")
            if _unavailable(row.get("current")):
                status += "; current unavailable"
            if _unavailable(row.get(target_key)):
                status += "; saved unavailable"
            records.append(
                [
                    row.get("name"),
                    row.get("current"),
                    row.get(target_key),
                    "" if row.get("delta") is None else row["delta"],
                    row.get("units") or "",
                    status,
                ]
            )
        lines.extend(_box(headers, records, width))
    if not changes and not attention:
        lines.append("No value changes needed in the selected settings.")
    if unchanged and not show_unchanged:
        lines.append(
            "Unchanged rows hidden; use show_unchanged=True for the full table."
        )
    # Keep summaries, titles, and hints within the same terminal width as boxes.
    return "\n".join(
        part
        for line in lines
        for part in (
            textwrap.wrap(line, width) if not line.startswith(("+", "|")) else [line]
        )
        or [""]
    )
