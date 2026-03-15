#!/usr/bin/env python3
"""
ARCHON PRIME — AST Dependency Analyzer
==========================================
For each Python module, builds an AST-level dependency profile:
  - which symbols it uses from each imported module
  - which of its symbols are referenced by other modules
  - internal vs external dependency classification
Writes: ast_dependency_analysis.json
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
STDLIB_TOPS = frozenset({
    "os", "sys", "re", "ast", "json", "math", "time", "datetime", "pathlib",
    "typing", "collections", "itertools", "functools", "abc", "io", "contextlib",
    "dataclasses", "enum", "copy", "hashlib", "logging", "warnings", "threading",
    "subprocess", "shutil", "tempfile", "argparse", "unittest", "types",
    "inspect", "importlib", "string", "struct", "socket", "http", "urllib",
    "base64", "uuid", "random", "statistics", "decimal", "fractions", "heapq",
    "bisect", "array", "queue", "weakref", "gc", "platform", "signal",
})


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon AST dependency analyzer")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def classify_import(module: str, known_modules: set[str]) -> str:
    if not module:
        return "unknown"
    top = module.split(".")[0]
    if top in STDLIB_TOPS:
        return "stdlib"
    if module in known_modules or top in known_modules:
        return "internal"
    return "third_party"


def analyze_file(path: Path, known_stems: set[str]) -> dict:
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception as e:
        return {"error": str(e), "imports": [], "name_usages": []}

    imports: list[dict] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "module": alias.name,
                    "names": [],
                    "classification": classify_import(alias.name, known_stems),
                    "lineno": node.lineno,
                })
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            names = [a.name for a in node.names]
            imports.append({
                "module": mod,
                "names": names,
                "classification": classify_import(mod, known_stems),
                "lineno": node.lineno,
            })

    # Collect Name usages (post-import references)
    imported_names: set[str] = set()
    for imp in imports:
        for n in imp["names"]:
            imported_names.add(n)

    usages: list[dict] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in imported_names:
            usages.append({"name": node.id, "lineno": node.lineno,
                           "ctx": type(node.ctx).__name__})

    by_class: dict[str, list] = {"stdlib": [], "internal": [], "third_party": [], "unknown": []}
    for imp in imports:
        by_class.setdefault(imp["classification"], []).append(imp["module"])

    return {
        "imports": imports,
        "import_summary": {cls: sorted(set(mods)) for cls, mods in by_class.items()},
        "name_usages": usages[:50],
    }


def run(target: Path, out_dir: Path) -> None:
    print(f"[ast_dependency_analyzer] Scanning: {target}")
    py_files = []
    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if fn.endswith(".py"):
                py_files.append(Path(root) / fn)

    known_stems = {fp.stem for fp in py_files}
    results: list[dict] = []
    stdlib_count = third_party_count = internal_count = 0

    for fp in py_files:
        rel = str(fp.relative_to(target))
        analysis = analyze_file(fp, known_stems)
        for imp in analysis.get("imports", []):
            c = imp.get("classification", "")
            if c == "stdlib":
                stdlib_count += 1
            elif c == "third_party":
                third_party_count += 1
            elif c == "internal":
                internal_count += 1
        results.append({
            "file": rel,
            "module": rel.removesuffix(".py").replace(os.sep, "."),
            **analysis,
        })

    write_json(out_dir, "ast_dependency_analysis.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_analyzed": len(results),
        "totals": {
            "stdlib_imports": stdlib_count,
            "internal_imports": internal_count,
            "third_party_imports": third_party_count,
        },
        "modules": results,
    })
    print(f"  Files: {len(results)}  Internal: {internal_count}  "
          f"ThirdParty: {third_party_count}  Stdlib: {stdlib_count}")


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
