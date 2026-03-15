#!/usr/bin/env python3
"""
ARCHON PRIME — Unused Symbol Detector
=======================================
Identifies functions and classes that are defined within a module but
never referenced by any other module in the repository. These "dark symbols"
are deletion candidates or candidates for consolidation.
Writes: unused_symbols.json
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
    p = argparse.ArgumentParser(description="Archon unused symbol detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def extract_definitions(path: Path) -> dict[str, list[str]]:
    """Extract top-level function and class definitions from a file."""
    funcs: list[str] = []
    classes: list[str] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return {"functions": funcs, "classes": classes}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
    return {"functions": funcs, "classes": classes}


def extract_all_usages(path: Path) -> set[str]:
    """Return all Name and Attribute identifiers used in a file."""
    names: set[str] = set()
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return names
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
    return names


def run(target: Path, out_dir: Path) -> None:
    print(f"[unused_symbol_detector] Scanning: {target}")

    py_files: list[Path] = []
    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in fnames:
            if fn.endswith(".py"):
                py_files.append(Path(root) / fn)

    # Collect all usages across the codebase
    all_used_names: set[str] = set()
    for fp in py_files:
        all_used_names.update(extract_all_usages(fp))

    # Check each module's definitions against cross-codebase usages
    results: list[dict] = []
    total_unused = 0

    for fp in sorted(py_files):
        rel = str(fp.relative_to(target))
        module = rel.removesuffix(".py").replace(os.sep, ".")
        defs = extract_definitions(fp)
        unused_funcs = [
            f for f in defs["functions"]
            if f not in all_used_names and not f.startswith("_") and f != "main"
        ]
        unused_classes = [
            c for c in defs["classes"]
            if c not in all_used_names and not c.startswith("_")
        ]
        if unused_funcs or unused_classes:
            total_unused += len(unused_funcs) + len(unused_classes)
            results.append({
                "module": module,
                "file": rel,
                "unused_functions": unused_funcs,
                "unused_classes": unused_classes,
                "unused_count": len(unused_funcs) + len(unused_classes),
                "total_defined": len(defs["functions"]) + len(defs["classes"]),
            })

    results.sort(key=lambda x: x["unused_count"], reverse=True)

    write_json(out_dir, "unused_symbols.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_scanned": len(py_files),
        "files_with_unused_symbols": len(results),
        "total_unused_symbols": total_unused,
        "modules": results,
    })
    print(f"  Files: {len(py_files)}  Unused symbols: {total_unused}  "
          f"Affected modules: {len(results)}")


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
