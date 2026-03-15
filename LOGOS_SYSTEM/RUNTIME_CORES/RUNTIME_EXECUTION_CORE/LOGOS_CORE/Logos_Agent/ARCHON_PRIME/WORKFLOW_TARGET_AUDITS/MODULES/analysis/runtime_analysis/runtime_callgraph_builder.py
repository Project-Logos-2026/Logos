#!/usr/bin/env python3
"""
ARCHON PRIME — Runtime Call Graph Builder
==========================================
Builds a static call graph from Python AST: which functions call which
others, within and across modules. Useful for tracing execution paths
and identifying hot-path dependencies. Writes: callgraph.json
"""
import argparse
import ast
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"
OUTPUT_ROOT = Path(os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT))
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
RUN_TS = datetime.now(timezone.utc).isoformat()

SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", ".mypy_cache"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon runtime call graph builder")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def _name_from_call(node: ast.expr) -> str:
    """Extract called function name from a Call node's func attribute."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_name_from_call(node.value)}.{node.attr}"
    return "<dynamic>"


class CallVisitor(ast.NodeVisitor):
    def __init__(self, module: str):
        self.module = module
        self.current_fn: str | None = None
        self.edges: list[dict] = []
        self._fn_stack: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        qualified = f"{self.module}.{node.name}"
        self._fn_stack.append(qualified)
        self.generic_visit(node)
        self._fn_stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef  # type: ignore[assignment]

    def visit_Call(self, node: ast.Call) -> None:
        caller = self._fn_stack[-1] if self._fn_stack else f"{self.module}.<module>"
        callee = _name_from_call(node.func)
        self.edges.append({"caller": caller, "callee": callee, "lineno": node.lineno})
        self.generic_visit(node)


def build_callgraph_for_file(path: Path, target: Path) -> list[dict]:
    rel = str(path.relative_to(target))
    module = rel.removesuffix(".py").replace(os.sep, ".")
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception:
        return []
    visitor = CallVisitor(module)
    visitor.visit(tree)
    return visitor.edges


def run(target: Path, out_dir: Path) -> None:
    print(f"[runtime_callgraph_builder] Scanning: {target}")
    all_edges: list[dict] = []
    nodes: set[str] = set()
    files_processed = 0

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            edges = build_callgraph_for_file(Path(root) / fn, target)
            for e in edges:
                nodes.add(e["caller"])
            all_edges.extend(edges)
            files_processed += 1

    # Compute call frequency
    callee_freq: dict[str, int] = {}
    for e in all_edges:
        callee_freq[e["callee"]] = callee_freq.get(e["callee"], 0) + 1

    top_callees = sorted(callee_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    write_json(out_dir, "callgraph.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_processed": files_processed,
        "total_edges": len(all_edges),
        "unique_callers": len(nodes),
        "top_callees": [{"callee": c, "call_count": n} for c, n in top_callees],
        "edges": all_edges,
    })
    print(f"  Files: {files_processed}  Edges: {len(all_edges)}  Callers: {len(nodes)}")


def main() -> None:
    args = parse_args()
    target = Path(args.target).resolve()
    out_dir = Path(args.output)
    if not target.exists():
        print(f"[FATAL] Target not found: {target}", file=sys.stderr)
        sys.exit(1)
    run(target, out_dir)


if __name__ == "__main__":
    main()
