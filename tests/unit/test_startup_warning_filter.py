"""The compatibility filter suppresses one known notice, not other warnings."""

import ast
from pathlib import Path
from types import SimpleNamespace
import warnings


def test_tiled_compatibility_filter_is_narrow_and_scoped():
    path = Path(__file__).parents[2] / "startup" / "startup.py"
    tree = ast.parse(path.read_text())
    block = next(node for node in tree.body if isinstance(node, ast.With)
                 and "_warnings.catch_warnings" in ast.unparse(node.items[0].context_expr))

    def configure_base(*args, **kwargs):
        warnings.warn_explicit(
            "Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.",
            UserWarning, filename="context.py", lineno=255, module="tiled.client.context",
        )
        warnings.warn("another warning", UserWarning)

    ns = {"_warnings": warnings, "nslsii": SimpleNamespace(configure_base=configure_base),
          "_user_ns": {}, "IS_QS_WORKER": False}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        original = warnings.filters[:]
        exec(compile(ast.Module(body=[block], type_ignores=[]), str(path), "exec"), ns)
        assert warnings.filters == original
    assert [str(w.message) for w in caught] == ["another warning"]
