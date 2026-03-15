#!/usr/bin/env python3
"""
ARCHON PRIME — Docstring Indexer
==================================
Extracts and indexes all docstrings from Python modules, classes, and
functions across the target repository. Produces a searchable docstring
corpus. Writes: docstring_index.json
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
    p = argparse.ArgumentParser(description="Archon docstring indexer")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def get_docstring(node: ast.AST) -> str | None:
    """Return the docstring of a node if it has one."""
    return ast.get_docstring(node, clean=True)


def extract_docstrings(path: Path, target: Path) -> list[dict]:
    rel = str(path.relative_to(target))
    module_stem = rel.removesuffix(".py").replace(os.sep, ".")
    entries: list[dict] = []

    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception as exc:
        return [{"file": rel, "symbol": "<parse_error>", "kind": "error", "docstring": str(exc), "lineno": 0}]

    # Module docstring
    module_doc = get_docstring(tree)
    if module_doc:
        entries.append({
            "file": rel,
            "module": module_stem,
            "symbol": module_stem,
            "kind": "module",
            "docstring": module_doc,
            "lineno": 1,
        })

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            doc = get_docstring(node)
            if doc:
                entries.append({
                    "file": rel,
                    "module": module_stem,
                    "symbol": f"{module_stem}.{node.name}",
                    "kind": "class",
                    "docstring": doc,
                    "lineno": node.lineno,
                })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = get_docstring(node)
            if doc:
                entries.append({
                    "file": rel,
                    "module": module_stem,
                    "symbol": f"{module_stem}.{node.name}",
                    "kind": "async_function" if isinstance(node, ast.AsyncFunctionDef) else "function",
                    "docstring": doc,
                    "lineno": node.lineno,
                })

    return entries


def run(target: Path, out_dir: Path) -> None:
    print(f"[docstring_indexer] Scanning: {target}")
    all_entries: list[dict] = []
    files_with_docs = 0
    files_total = 0

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            files_total += 1
            entries = extract_docstrings(Path(root) / fn, target)
            if entries:
                files_with_docs += 1
            all_entries.extend(entries)

    # Build quick-access index by kind
    by_kind: dict[str, list[str]] = {}
    for e in all_entries:
        kind = e.get("kind", "unknown")
        by_kind.setdefault(kind, []).append(e.get("symbol", ""))

    write_json(out_dir, "docstring_index.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_scanned": files_total,
        "files_with_docstrings": files_with_docs,
        "total_docstrings": len(all_entries),
        "by_kind_counts": {k: len(v) for k, v in by_kind.items()},
        "coverage_ratio": round(files_with_docs / files_total, 3) if files_total else 0.0,
        "entries": all_entries,
    })
    print(f"  Files: {files_total}  Docstrings: {len(all_entries)}  "
          f"Coverage: {files_with_docs}/{files_total}")


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
