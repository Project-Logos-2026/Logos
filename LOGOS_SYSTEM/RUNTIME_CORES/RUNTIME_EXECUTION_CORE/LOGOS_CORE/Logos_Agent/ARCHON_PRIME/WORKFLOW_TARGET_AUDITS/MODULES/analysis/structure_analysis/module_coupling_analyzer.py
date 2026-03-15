#!/usr/bin/env python3
"""
ARCHON PRIME — Module Coupling Analyzer
=========================================
Computes afferent coupling (Ca: incoming dependencies) and efferent coupling
(Ce: outgoing dependencies) for each Python module. Derives instability metric
I = Ce / (Ca + Ce). High instability = likely utility leaf; low = stable core.
Writes: coupling_report.json
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
    p = argparse.ArgumentParser(description="Archon module coupling analyzer")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def collect_imports(path: Path) -> list[str]:
    """Return list of imported module stems (non-stdlib, non-relative)."""
    imports: list[str] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                if node.module:
                    imports.append(f".<rel>.{node.module}")
            elif node.module:
                top = node.module.split(".")[0]
                if top not in STDLIB_TOPS:
                    imports.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top not in STDLIB_TOPS:
                    imports.append(alias.name)
    return list(set(imports))


def run(target: Path, out_dir: Path) -> None:
    print(f"[module_coupling_analyzer] Scanning: {target}")

    # First pass: collect all module stems and their imports (efferent)
    module_imports: dict[str, list[str]] = {}
    module_files: dict[str, str] = {}  # stem → rel path

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            fp = Path(root) / fn
            rel = str(fp.relative_to(target))
            stem = rel.removesuffix(".py").replace(os.sep, ".")
            module_imports[stem] = collect_imports(fp)
            module_files[stem] = rel

    # Second pass: compute Ca (afferent) — how many modules import THIS one
    afferent: dict[str, int] = {m: 0 for m in module_imports}
    for stem, imports in module_imports.items():
        for imp in imports:
            # Match against known module stems
            for known in module_imports:
                if imp == known or imp.startswith(known + ".") or known.endswith(imp.split(".")[-1]):
                    if known != stem:
                        afferent[known] = afferent.get(known, 0) + 1
                        break

    # Build final report
    modules = []
    for stem, imports in sorted(module_imports.items()):
        ce = len(imports)  # efferent = outgoing internal imports
        ca = afferent.get(stem, 0)
        total = ca + ce
        instability = round(ce / total, 3) if total else 0.0
        modules.append({
            "module": stem,
            "file": module_files[stem],
            "afferent_coupling": ca,
            "efferent_coupling": ce,
            "instability": instability,
            "coupling_category": (
                "STABLE_CORE" if instability < 0.25 else
                "BALANCED" if instability < 0.75 else
                "VOLATILE_LEAF"
            ),
            "outgoing_imports": imports[:15],
        })

    # Sort by instability descending
    modules.sort(key=lambda x: x["instability"], reverse=True)

    avg_instability = (
        round(sum(m["instability"] for m in modules) / len(modules), 3) if modules else 0.0
    )

    write_json(out_dir, "coupling_report.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(modules),
        "average_instability": avg_instability,
        "category_counts": {
            "STABLE_CORE": sum(1 for m in modules if m["coupling_category"] == "STABLE_CORE"),
            "BALANCED": sum(1 for m in modules if m["coupling_category"] == "BALANCED"),
            "VOLATILE_LEAF": sum(1 for m in modules if m["coupling_category"] == "VOLATILE_LEAF"),
        },
        "modules": modules,
    })
    print(f"  Modules: {len(modules)}  Avg instability: {avg_instability}")


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
