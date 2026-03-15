#!/usr/bin/env python3
"""
ARCHON PRIME — Dead Module Detector
=====================================
Identifies Python modules that are never imported by any other module in
the repository (unreferenced/orphaned modules). These are candidates for
removal or consolidation. Writes: dead_modules.json
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

# Modules matching these patterns are usually intended to be standalone
EXEMPT_PATTERNS = {"__main__", "main", "setup", "conftest", "test_", "_test"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon dead module detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def collect_imported_names(path: Path) -> set[str]:
    """Return all module names imported in the given file."""
    imported: set[str] = set()
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return imported
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
            # Also add the top-level package
            imported.add(node.module.split(".")[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
                imported.add(alias.name.split(".")[0])
    return imported


def is_exempt(stem: str) -> bool:
    name = stem.split(".")[-1].lower()
    return any(p in name for p in EXEMPT_PATTERNS) or name.startswith("__")


def run(target: Path, out_dir: Path) -> None:
    print(f"[dead_module_detector] Scanning: {target}")

    # First pass: collect all module stems
    all_py_files: dict[str, Path] = {}
    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in fnames:
            if fn.endswith(".py"):
                fp = Path(root) / fn
                rel = str(fp.relative_to(target))
                stem = rel.removesuffix(".py").replace(os.sep, ".")
                all_py_files[stem] = fp

    # Second pass: collect all imported names from all files
    all_imported: set[str] = set()
    for stem, fp in all_py_files.items():
        all_imported.update(collect_imported_names(fp))

    # Determine dead modules
    dead: list[dict] = []
    for stem, fp in sorted(all_py_files.items()):
        if is_exempt(stem):
            continue
        # Check if this module is referenced by any import
        leaf = stem.split(".")[-1]
        is_referenced = (
            stem in all_imported or
            leaf in all_imported or
            any(stem in name or name in stem for name in all_imported)
        )
        if not is_referenced:
            rel = str(fp.relative_to(target))
            try:
                loc = len(fp.read_text(encoding="utf-8", errors="replace").splitlines())
            except Exception:
                loc = 0
            dead.append({
                "module": stem,
                "file": rel,
                "loc": loc,
            })

    # Sort by LOC descending (biggest dead modules first)
    dead.sort(key=lambda x: x["loc"], reverse=True)

    write_json(out_dir, "dead_modules.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(all_py_files),
        "dead_module_count": len(dead),
        "dead_ratio": round(len(dead) / len(all_py_files), 3) if all_py_files else 0.0,
        "total_dead_loc": sum(m["loc"] for m in dead),
        "dead_modules": dead,
    })
    print(f"  Total modules: {len(all_py_files)}  Dead: {len(dead)}  "
          f"Dead LOC: {sum(m['loc'] for m in dead)}")


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
