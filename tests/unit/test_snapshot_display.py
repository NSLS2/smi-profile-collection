"""Pure console rendering tests; no device construction or hardware access."""

import pytest

from smi_beamline.plans.snapshot_display import snapshot_report


def _row(name="wbs.h", status="already there", current=1.0, target=1.0):
    return {
        "name": name,
        "status": status,
        "current": current,
        "target": target,
        "units": "mm",
        "delta": target - current
        if isinstance(current, float) and isinstance(target, float)
        else None,
    }


def test_changes_first_summary_hides_equal_values_without_mutating_rows():
    rows = [_row(f"unchanged.{i}") for i in range(250)]
    rows += [_row(f"change.{i}", "would move", 2.0, 1.0) for i in range(10)]
    before = [dict(row) for row in rows]
    text = snapshot_report(rows, title="DRY RUN", target_key="target", width=120)
    assert "260 selected values: 250 unchanged; 10 would change; 0 other" in text
    assert "unchanged.0" not in text
    assert all(f"change.{i}" in text for i in range(10))
    assert rows == before


def test_unavailable_and_read_only_differences_remain_visible():
    rows = [
        _row("unknown", "would move", None),
        _row(
            "failed", "unchanged", {"error": "read timeout"}, {"error": "read timeout"}
        ),
        _row("legacy", "missing saved", 1.0, None),
        _row("readonly", "skipped read-only", 2.0, 1.0),
        _row("readonly_equal", "skipped read-only"),
    ]
    text = snapshot_report(rows, title="DRY RUN", target_key="target", width=120)
    assert "5 selected values: 1 unchanged; 0 would change; 4 other" in text
    assert "current unavailable" in text
    assert "read timeout" in text
    assert "saved unavailable" in text
    assert "readonly_equal" not in text
    assert "readonly" in text


@pytest.mark.parametrize("width", [24, 40, 68, 80, 120])
def test_boxes_align_and_wrap_long_names_and_values(width):
    rows = [
        _row("OAV_config.plugins.very_long_plugin_name.enable", "changed", 2.0, 1.0)
    ]
    rows += [_row("error", "changed", {"error": "x" * 160 + "\n\x1b[31m|"})]
    text = snapshot_report(rows, title="DRY RUN", target_key="target", width=width)
    assert max(map(len, text.splitlines())) <= width
    assert "\x1b" not in text
    box_lines = [line for line in text.splitlines() if line.startswith(("|", "+"))]
    assert box_lines
    assert len(set(map(len, box_lines))) == 1
    assert all(line.endswith(line[0]) for line in box_lines)
    assert all(
        line.count("|") == box_lines[1].count("|")
        for line in box_lines
        if line.startswith("|")
    )


def test_show_unchanged_and_empty_selection():
    text = snapshot_report(
        [_row()], title="DRY RUN", target_key="target", show_unchanged=True
    )
    assert "wbs.h" in text
    assert "No value changes needed" in text
    text = snapshot_report([], title="DRY RUN", target_key="target")
    assert "0 selected values" in text
    assert "|" not in text


def test_comparison_uses_saved_column_and_shows_nonrestorable_differences():
    rows = [
        {
            "name": "diagnostic",
            "status": "read-only diff",
            "current": 3,
            "snapshot": 2,
            "delta": 1,
            "units": "mm",
        }
    ]
    text = snapshot_report(rows, title="COMPARE", target_key="snapshot")
    assert "Saved" in text
    assert "read-only diff" in text
    assert "0 unchanged; 0 would change; 1 other" in text


@pytest.mark.parametrize("operation", ["compare", "restore"])
def test_public_api_display_option_preserves_returned_rows(
    operation, monkeypatch, capsys
):
    from smi_beamline.plans import beam_snapshot

    saved_items = [
        {"name": "equal", "readback": 1.0, "kind": "motor", "restore": True},
        {"name": "different", "readback": 1.0, "kind": "motor", "restore": True},
    ]
    current = [dict(item) for item in saved_items]
    current[1]["readback"] = 2.0
    monkeypatch.setattr(beam_snapshot, "_collect_snapshot_items", lambda ns: current)
    function = (
        beam_snapshot.compare_beam_position_snapshot
        if operation == "compare"
        else beam_snapshot.restore_beam_position_snapshot
    )
    snapshot = {"items": saved_items}
    compact = function(snapshot, namespace={})
    text = capsys.readouterr().out
    assert "1 unchanged; 1 would change; 0 other" in text
    assert "| equal" not in text
    assert "different" in text
    complete = function(snapshot, namespace={}, show_unchanged=True)
    assert "| equal" in capsys.readouterr().out
    assert complete == compact
    assert function(snapshot, namespace={}, print_table=False) == compact
    assert capsys.readouterr().out == ""
