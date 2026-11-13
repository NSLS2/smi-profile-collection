"""Exercise the detector restart cleanup without importing devices or connecting to hardware."""

import ast
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest


pytestmark = pytest.mark.unit


@pytest.fixture
def restart():
    path = Path(__file__).parents[2] / "src/smi_beamline/instances/pilatus.py"
    tree = ast.parse(path.read_text())
    function = next(node for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == "restartWAXS")
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))

    calls = Mock()
    client = Mock()
    shell = Mock()
    telnet = Mock()
    telnet.eof = False
    telnet.read_very_eager.return_value = b"Set detector gap-fill to: -1"
    client.invoke_shell.return_value = shell
    client.exec_command.return_value = (Mock(), Mock(), Mock())
    calls.attach_mock(telnet, "telnet")
    calls.attach_mock(shell, "shell")
    calls.attach_mock(client, "client")

    def sleep(seconds):
        yield seconds

    namespace = {
        "client": client,
        "hostname": "fake-host",
        "username": "fake-user",
        "password": "fake-password",
        "telnet_command": "telnet localhost 20002",
        "telnetlib": SimpleNamespace(Telnet=Mock(return_value=telnet)),
        "time": SimpleNamespace(time=Mock(return_value=0)),
        "bps": SimpleNamespace(sleep=sleep),
    }
    exec(compile(module, str(path), "exec"), namespace)
    return SimpleNamespace(plan=namespace["restartWAXS"], calls=calls, client=client,
                           shell=shell, telnet=telnet, namespace=namespace)


def assert_cleanup_order(restart):
    close_calls = [c for c in restart.calls.mock_calls if c in (
        call.telnet.close(), call.shell.close(), call.client.close())]
    assert close_calls == [call.telnet.close(), call.shell.close(), call.client.close()]


def test_restart_closes_telnet_before_ssh(restart):
    assert list(restart.plan()) == [3]
    assert restart.telnet.sock is restart.shell
    assert_cleanup_order(restart)


def test_restart_closes_resources_on_read_error(restart):
    restart.telnet.read_very_eager.side_effect = OSError("read failed")
    with pytest.raises(OSError, match="read failed"):
        list(restart.plan())
    assert_cleanup_order(restart)


def test_restart_closes_resources_on_timeout(restart):
    restart.namespace["time"].time.side_effect = [0, 0, 121]
    restart.telnet.read_very_eager.return_value = b""
    assert list(restart.plan()) == []
    assert_cleanup_order(restart)


def test_restart_closes_resources_on_eof(restart):
    restart.telnet.eof = True
    restart.telnet.read_very_eager.return_value = b""
    assert list(restart.plan()) == []
    assert_cleanup_order(restart)


def test_restart_closes_resources_when_plan_is_closed(restart):
    plan = restart.plan()
    assert next(plan) == 3
    plan.close()
    assert_cleanup_order(restart)


def test_restart_closes_ssh_if_telnet_close_fails(restart):
    restart.telnet.close.side_effect = OSError("close failed")
    with pytest.raises(OSError, match="close failed"):
        list(restart.plan())
    assert_cleanup_order(restart)


def test_restart_closes_shell_if_telnet_creation_fails(restart):
    restart.namespace["telnetlib"].Telnet.side_effect = OSError("creation failed")
    with pytest.raises(OSError, match="creation failed"):
        list(restart.plan())
    restart.telnet.close.assert_not_called()
    restart.shell.close.assert_called_once()
    restart.client.close.assert_called_once()


def test_restart_closes_ssh_if_connect_fails(restart):
    restart.client.connect.side_effect = OSError("connect failed")
    with pytest.raises(OSError, match="connect failed"):
        list(restart.plan())
    restart.telnet.close.assert_not_called()
    restart.shell.close.assert_not_called()
    restart.client.close.assert_called_once()
