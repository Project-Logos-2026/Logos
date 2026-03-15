#!/usr/bin/env python3
"""
ARCHON PRIME — Circular Dependency Detector
=============================================
Detects circular import dependencies using Tarjan's Strongly Connected
Components algorithm on the module import graph. Circular dependencies
are a common source of import errors and architectural decay.
Writes: circular_dependencies.json
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

STDLIB_TOPS = frozenset(
    "abc,ast,asyncio,builtins,collections,contextlib,copy,dataclasses,datetime,"
    "email,enum,functools,hashlib,http,importlib,inspect,io,itertools,json,logging,"
    "math,operator,os,pathlib,pickle,platform,queue,random,re,shutil,signal,socket,"
    "sqlite3,string,struct,subprocess,sys,tempfile,textwrap,threading,time,traceback,"
    "typing,unittest,urllib,uuid,warnings,weakref,xml,zipfile".split(",")
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon circular dependency detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def get_internal_imports(path: Path, known_stems: set[str]) -> list[str]:
    """Return list of internal module stems imported by this file."""
    result: list[str] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return result
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                top = node.module.split(".")[0]
                if top in STDLIB_TOPS:
                    continue
                # Check if this import refers to a known internal module
                for stem in known_stems:
                    if node.module == stem or node.module.startswith(stem + ".") or stem.endswith(node.module):
                        result.append(stem)
                        break
        elif isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top in STDLIB_TOPS:
                    continue
                for stem in known_stems:
                    if alias.name == stem or alias.name.startswith(stem + "."):
                        result.append(stem)
                        break
    return list(set(result))


def tarjan_scc(graph: dict[str, list[str]]) -> list[list[str]]:
    """Tarjan's SCC algorithm. Returns list of SCCs (as sorted lists)."""
    index_counter = [0]
    stack: list[str] = []
    on_stack: dict[str, bool] = {}
    index: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    sccs: list[list[str]] = []

    def strongconnect(v: str) -> None:
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True

        for w in graph.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif on_stack.get(w, False):
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            scc: list[str] = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            sccs.append(sorted(scc))

    for v in graph:
        if v not in index:
            strongconnect(v)
    return sccs


def run(target: Path, out_dir: Path) -> None:
    print(f"[circular_dependency_detector] Scanning: {target}")

    # Collect all module stems
    stem_to_file: dict[str, str] = {}
    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in fnames:
            if fn.endswith(".py"):
                fp = Path(root) / fn
                rel = str(fp.relative_to(target))
                stem = rel.removesuffix(".py").replace(os.sep, ".")
                stem_to_file[stem] = rel

    known_stems = set(stem_to_file.keys())

    # Build adjacency list (edges = internal imports)
    graph: dict[str, list[str]] = {}
    for stem, rel in stem_to_file.items():
        imports = get_internal_imports(target / rel, known_stems - {stem})
        graph[stem] = imports

    # Find SCCs
    sccs = tarjan_scc(graph)
    cycles = [scc for scc in sccs if len(scc) > 1]
    trivial = [scc for scc in sccs if len(scc) == 1]

    write_json(out_dir, "circular_dependencies.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(stem_to_file),
        "total_sccs": len(sccs),
        "circular_cycles": len(cycles),
        "risk_level": (
            "HIGH" if cycles else "NONE"
        ),
        "cycles": [
            {
                "size": len(c),
                "modules": c,
            }
            for c in sorted(cycles, key=len, reverse=True)
        ],
        "acyclic_modules_count": sum(len(s) for s in trivial),
    })
    print(f"  Modules: {len(stem_to_file)}  Circular cycles: {len(cycles)}")


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
