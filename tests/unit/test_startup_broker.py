"""Exercise startup subscriptions without external services or device imports."""

import ast
from pathlib import Path
from types import SimpleNamespace

import bluesky.plan_stubs as bps
from databroker import Broker
import nslsii
import pytest


@pytest.mark.parametrize("worker", [False, True])
def test_startup_uses_remote_broker_and_preserves_callbacks(monkeypatch, worker):
    path = Path(__file__).parents[2] / "startup" / "startup.py"
    tree = ast.parse(path.read_text())
    start = next(i for i, node in enumerate(tree.body)
                 if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                 and ast.unparse(node.value.func) == "nslsii.configure_base")
    end = next(i for i, node in enumerate(tree.body[start:], start)
               if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
               and ast.unparse(node.value.func) == "RE.subscribe")
    documents = []
    kafka = []
    bec_documents = []

    def forbidden_broker(*args, **kwargs):
        pytest.fail("startup must not construct a local Mongo broker")

    def configure_kafka(engine, beamline_name):
        assert beamline_name == "smi"
        engine.subscribe(lambda name, doc: kafka.append(name))

    def configure_base(namespace, **kwargs):
        # Replace only services/UI; exercise real nslsii subscription ordering.
        kwargs.update(redis_url=None, configure_logging=False, ipython_logging=False,
                      magics=False, mpl=False, pbar=False, tb_minimize=False)
        nslsii.configure_base(namespace, **kwargs)

    from bluesky.callbacks.best_effort import BestEffortCallback
    monkeypatch.setattr(Broker, "named", forbidden_broker)
    monkeypatch.setattr(nslsii, "configure_kafka_publisher", configure_kafka)
    monkeypatch.setattr(BestEffortCallback, "__call__",
                        lambda self, name, doc: bec_documents.append(name))
    
    class CallableNamespace(SimpleNamespace):
        def __hash__(self):
            return id(self)  # Uses the object's unique memory address

        def __call__(self, name, doc):
            documents.append(name)

    ns = {"nslsii": SimpleNamespace(configure_base=configure_base), "_user_ns": {},
          "IS_QS_WORKER": worker,
          "tiled_inserter": CallableNamespace()}
    exec(compile(ast.Module(body=tree.body[start:end + 1], type_ignores=[]), str(path), "exec"), ns)

    def plan():
        yield from bps.open_run()
        yield from bps.close_run()

    ns["RE"](plan())
    assert documents == ["start", "stop"]
    assert kafka == documents
    assert bec_documents == documents
