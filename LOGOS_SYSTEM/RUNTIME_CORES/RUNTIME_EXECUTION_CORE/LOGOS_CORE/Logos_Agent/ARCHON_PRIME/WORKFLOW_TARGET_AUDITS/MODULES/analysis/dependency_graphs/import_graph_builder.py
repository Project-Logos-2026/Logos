#!/usr/bin/env python3
"""
ARCHON PRIME — Import Graph Builder
======================================
Parses all Python files in the target directory and builds a complete
import dependency graph (nodes = modules, edges = import relationships).
Writes: import_graph.json, import_graph_edges.json
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
    p = argparse.ArgumentParser(description="Archon import graph builder")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def collect_python_files(target: Path) -> list[Path]:
    files = []
    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if fn.endswith(".py"):
                files.append(Path(root) / fn)
    return files


def parse_imports(path: Path) -> list[dict]:
    imports = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({"type": "import", "module": alias.name,
                                 "alias": alias.asname, "lineno": node.lineno})
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            names = [alias.name for alias in node.names]
            imports.append({"type": "from_import", "module": mod,
                             "names": names, "level": node.level, "lineno": node.lineno})
    return imports


def run(target: Path, out_dir: Path) -> None:
    print(f"[import_graph_builder] Scanning: {target}")
    py_files = collect_python_files(target)

    # Build module registry: stem → relative path
    module_registry: dict[str, str] = {}
    nodes: list[dict] = []
    for fp in py_files:
        rel = str(fp.relative_to(target))
        mod_key = rel.removesuffix(".py").replace(os.sep, ".")
        module_registry[fp.stem.lower()] = mod_key
        nodes.append({"id": mod_key, "file": rel})

    edges: list[dict] = []
    module_imports: dict[str, list[dict]] = {}
    for fp in py_files:
        rel = str(fp.relative_to(target))
        src_mod = rel.removesuffix(".py").replace(os.sep, ".")
        raw_imports = parse_imports(fp)
        module_imports[src_mod] = raw_imports

        for imp in raw_imports:
            tgt_mod = imp["module"]
            if not tgt_mod:
                continue
            # Attempt to resolve to a known module
            stem = tgt_mod.split(".")[-1].lower()
            resolved = module_registry.get(stem)
            edges.append({
                "from": src_mod,
                "to": tgt_mod,
                "resolved_to": resolved,
                "type": imp["type"],
                "lineno": imp["lineno"],
            })

    internal_edges = [e for e in edges if e["resolved_to"] is not None]
    external_edges = [e for e in edges if e["resolved_to"] is None]

    write_json(out_dir, "import_graph.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "internal_edge_count": len(internal_edges),
        "external_edge_count": len(external_edges),
        "nodes": nodes,
        "edges": edges,
    })
    write_json(out_dir, "import_graph_edges.json", {
        "generated_at": RUN_TS,
        "internal_edges": internal_edges,
        "external_edges": external_edges,
    })

    print(f"  Modules: {len(nodes)}  Total imports: {len(edges)}")
    print(f"  Internal: {len(internal_edges)}  External: {len(external_edges)}")


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
