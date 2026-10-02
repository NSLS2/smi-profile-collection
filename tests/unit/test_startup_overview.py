"""Execute only the final startup block, without loading hardware/services."""

import ast
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from smi_beamline import beamline_status


def startup_block():
    path = Path(__file__).parents[2] / "startup" / "startup.py"
    tree = ast.parse(path.read_text())
    return compile(ast.Module(body=[tree.body[-1]], type_ignores=[]), str(path), "exec")


@pytest.mark.parametrize("failure", [False, True])
def test_interactive_startup_status_and_hint(monkeypatch, capsys, failure):
    shell = SimpleNamespace(extension_manager=Mock())
    display = Mock(side_effect=RuntimeError("read failed") if failure else None)
    monkeypatch.setattr(beamline_status, "show_status", display)
    color = lambda shell, text, code: text
    exec(startup_block(), {"ipython": shell, "IS_QS_WORKER": False, "_console_color": color})
    shell.extension_manager.load_extension.assert_called_once_with("smi_beamline.motor_magics")
    display.assert_called_once_with(shell, color)
    output = capsys.readouterr().out
    assert "Type help for quick commands." in output
    assert ("Status unavailable" in output) == failure


@pytest.mark.parametrize("shell,worker", [(None, False), (SimpleNamespace(extension_manager=Mock()), True)])
def test_headless_startup_skips_overview(monkeypatch, capsys, shell, worker):
    display = Mock()
    monkeypatch.setattr(beamline_status, "show_status", display)
    exec(startup_block(), {"ipython": shell, "IS_QS_WORKER": worker})
    display.assert_not_called()
    assert capsys.readouterr().out == ""
