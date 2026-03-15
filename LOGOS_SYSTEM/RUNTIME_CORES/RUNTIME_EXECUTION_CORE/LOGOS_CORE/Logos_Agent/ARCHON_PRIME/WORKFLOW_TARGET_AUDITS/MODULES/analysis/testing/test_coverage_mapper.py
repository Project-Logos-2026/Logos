#!/usr/bin/env python3
"""
ARCHON PRIME — Test Coverage Mapper
=====================================
Maps test files to their corresponding source modules using filename
conventions (test_foo.py → foo.py, foo_test.py → foo.py), pytest marker
analysis, and docstring references. Produces a coverage map showing which
source modules have corresponding test files and which do not.
Writes: test_coverage_map.json
"""
import argparse
import ast
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"
OUTPUT_ROOT = Path(os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT))
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
RUN_TS = datetime.now(timezone.utc).isoformat()

SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", ".mypy_cache"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon test coverage mapper")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def is_test_file(path: Path) -> bool:
    name = path.stem.lower()
    return name.startswith("test_") or name.endswith("_test")


def get_tested_module_name(test_path: Path) -> str | None:
    """Derive the probable source module name from a test file name."""
    name = test_path.stem.lower()
    if name.startswith("test_"):
        return name[5:]  # test_foo → foo
    if name.endswith("_test"):
        return name[:-5]  # foo_test → foo
    return None


def extract_test_markers(path: Path) -> list[str]:
    """Extract pytest markers from a test file."""
    markers: list[str] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return markers
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in node.decorator_list:
                dec_str = ast.unparse(dec)
                if "mark." in dec_str or "pytest." in dec_str:
                    markers.append(dec_str)
    return list(set(markers))


def extract_imported_modules(path: Path) -> list[str]:
    """Return all modules imported by a test file (potential sources under test)."""
    modules: list[str] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return modules
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name)
    return modules


def run(target: Path, out_dir: Path) -> None:
    print(f"[test_coverage_mapper] Scanning: {target}")

    # Collect all Python files
    all_py: list[Path] = []
    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in fnames:
            if fn.endswith(".py"):
                all_py.append(Path(root) / fn)

    source_files = {p for p in all_py if not is_test_file(p)}
    test_files = {p for p in all_py if is_test_file(p)}

    # Build stem → source file map
    stem_to_source: dict[str, str] = {
        p.stem.lower(): str(p.relative_to(target)) for p in source_files
    }

    # Map each test file to its source
    test_maps: list[dict] = []
    covered_source_stems: set[str] = set()

    for tf in sorted(test_files):
        rel = str(tf.relative_to(target))
        tested = get_tested_module_name(tf)
        imported = extract_imported_modules(tf)
        markers = extract_test_markers(tf)

        # Match by naming convention
        source_file = stem_to_source.get(tested) if tested else None

        # Fallback: check imports
        if source_file is None and imported:
            for imp in imported:
                leaf = imp.split(".")[-1].lower()
                if leaf in stem_to_source:
                    source_file = stem_to_source[leaf]
                    break

        if source_file:
            covered_source_stems.add(Path(source_file).stem.lower())

        test_maps.append({
            "test_file": rel,
            "derived_source_name": tested,
            "mapped_source": source_file,
            "mapping_status": "mapped" if source_file else "unmapped",
            "imports": imported[:10],
            "markers": markers[:10],
        })

    # Identify uncovered source files
    uncovered = [
        str(p.relative_to(target))
        for p in sorted(source_files)
        if p.stem.lower() not in covered_source_stems
    ]

    coverage_ratio = round(
        (len(source_files) - len(uncovered)) / len(source_files), 3
    ) if source_files else 0.0

    write_json(out_dir, "test_coverage_map.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_python_files": len(all_py),
        "source_files": len(source_files),
        "test_files": len(test_files),
        "source_files_covered": len(source_files) - len(uncovered),
        "coverage_ratio": coverage_ratio,
        "uncovered_source_count": len(uncovered),
        "uncovered_sources": uncovered[:50],
        "test_mappings": test_maps,
    })
    print(f"  Source: {len(source_files)}  Tests: {len(test_files)}  "
          f"Coverage ratio: {coverage_ratio}  Uncovered: {len(uncovered)}")


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
