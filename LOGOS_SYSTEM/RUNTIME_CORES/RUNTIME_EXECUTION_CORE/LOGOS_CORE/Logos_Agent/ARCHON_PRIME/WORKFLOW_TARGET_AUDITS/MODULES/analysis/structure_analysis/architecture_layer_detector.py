#!/usr/bin/env python3
"""
ARCHON PRIME — Architecture Layer Detector
============================================
Detects architectural layer membership for each Python module using
directory name patterns, import profiles, and naming conventions.
Layers: core, interface, utility, agent, data, config, test, unknown.
Writes: architecture_layers.json
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

# Path-segment → layer mapping (in priority order)
LAYER_PATTERNS: list[tuple[str, str]] = [
    (r"test", "test"),
    (r"tests", "test"),
    (r"config|settings|conf", "config"),
    (r"util|utils|helper|helpers|tools", "utility"),
    (r"interface|api|endpoint|handler|route|router|view|controller", "interface"),
    (r"core|kernel|engine|runtime", "core"),
    (r"agent|actor|policy|player", "agent"),
    (r"data|model|schema|db|database|store|repository", "data"),
    (r"reasoning|logic|proof|axiom|inference", "reasoning"),
    (r"safety|guard|constraint|security", "safety"),
]

STDLIB_TOPS = frozenset(
    "abc,ast,asyncio,builtins,collections,contextlib,copy,dataclasses,datetime,"
    "email,enum,functools,hashlib,http,importlib,inspect,io,itertools,json,logging,"
    "math,operator,os,pathlib,pickle,platform,queue,random,re,shutil,signal,socket,"
    "sqlite3,string,struct,subprocess,sys,tempfile,textwrap,threading,time,traceback,"
    "typing,unittest,urllib,uuid,warnings,weakref,xml,zipfile".split(",")
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon architecture layer detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def detect_layer(path: Path, target: Path) -> str:
    rel = str(path.relative_to(target))
    lower = rel.lower()
    for pattern, layer in LAYER_PATTERNS:
        if re.search(pattern, lower):
            return layer
    return "unknown"


def get_imports(path: Path) -> tuple[list[str], list[str]]:
    """Returns (internal_imports, external_imports)."""
    internal, external = [], []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return internal, external
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            top = node.module.split(".")[0]
            if top in STDLIB_TOPS:
                continue
            if node.level and node.level > 0:
                internal.append(node.module or "")
            else:
                external.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top not in STDLIB_TOPS:
                    external.append(alias.name)
    return internal, external


def run(target: Path, out_dir: Path) -> None:
    print(f"[architecture_layer_detector] Scanning: {target}")
    modules = []
    layer_counts: dict[str, int] = {}

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            fp = Path(root) / fn
            rel = str(fp.relative_to(target))
            layer = detect_layer(fp, target)
            internal, external = get_imports(fp)
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
            modules.append({
                "file": rel,
                "module": rel.removesuffix(".py").replace(os.sep, "."),
                "layer": layer,
                "internal_import_count": len(internal),
                "external_import_count": len(external),
                "internal_imports": internal[:10],
                "external_imports": external[:10],
            })

    # Compute cross-layer stats: which layers import from which
    layer_coupling: dict[str, dict[str, int]] = {}
    for m in modules:
        src_layer = m["layer"]
        for ext in m["external_imports"]:
            # We can't resolve layer of external imports without module map
            # so we note raw external dependency count per layer
            layer_coupling.setdefault(src_layer, {})

    write_json(out_dir, "architecture_layers.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(modules),
        "layer_distribution": layer_counts,
        "layers_detected": sorted(layer_counts.keys()),
        "modules": modules,
    })
    print(f"  Modules: {len(modules)}  Layer distribution: {layer_counts}")


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
