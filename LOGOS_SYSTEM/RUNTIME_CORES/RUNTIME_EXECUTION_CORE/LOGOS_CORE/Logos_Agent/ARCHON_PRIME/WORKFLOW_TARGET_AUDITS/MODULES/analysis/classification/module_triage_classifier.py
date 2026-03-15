#!/usr/bin/env python3
"""
ARCHON PRIME — Module Triage Classifier
=========================================
Classifies each Python module into a recovery triage category:

  EXTRACT_LOGIC   — Contains reusable logic worth extracting (high quality signals)
  KEEP_VERIFY     — Possibly useful; needs manual verification before inclusion
  DELETE          — Dead code, stubs, or trivially replaceable modules

Uses heuristics: symbol count, LOC, import depth, documentation presence,
naming conventions, and path-based signals.
Writes: module_triage.json
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

# Path segments that bias toward EXTRACT_LOGIC
EXTRACT_BIAS_PATHS = {"core", "engine", "reasoning", "logic", "agent", "math", "semantic"}

# Path segments that bias toward DELETE
DELETE_BIAS_PATHS = {"test", "tests", "stub", "stubs", "mock", "mocks", "scratch", "tmp", "temp", "old"}

# Minimum LOC threshold to be worth extracting
MIN_LOC_EXTRACT = 20

# Minimum symbol count to merit KEEP_VERIFY
MIN_SYMBOLS_KEEP = 3


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon module triage classifier")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def analyze_module(path: Path, target: Path) -> dict:
    rel = str(path.relative_to(target))
    module = rel.removesuffix(".py").replace(os.sep, ".")
    path_lower = rel.lower()

    result: dict = {
        "file": rel,
        "module": module,
        "loc": 0,
        "symbol_count": 0,
        "has_docstring": False,
        "has_type_hints": False,
        "import_count": 0,
        "is_empty": True,
        "path_bias": "neutral",
        "triage": "KEEP_VERIFY",
        "triage_reason": "",
    }

    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        result["triage"] = "DELETE"
        result["triage_reason"] = "unreadable"
        return result

    lines = [l for l in src.splitlines() if l.strip()]
    result["loc"] = len(lines)
    result["is_empty"] = result["loc"] == 0

    try:
        tree = ast.parse(src, filename=str(path))
    except SyntaxError:
        result["triage"] = "DELETE"
        result["triage_reason"] = "syntax_error"
        return result

    # Count symbols
    symbols = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    )
    result["symbol_count"] = symbols

    # Check for module docstring
    result["has_docstring"] = bool(ast.get_docstring(tree))

    # Check type hints
    result["has_type_hints"] = any(
        isinstance(n, ast.AnnAssign) or
        (isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.returns)
        for n in ast.walk(tree)
    )

    # Import count
    result["import_count"] = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, (ast.Import, ast.ImportFrom))
    )

    # Path bias
    parts = set(path_lower.replace("/", " ").replace("\\", " ").replace("_", " ").split())
    if EXTRACT_BIAS_PATHS & parts:
        result["path_bias"] = "extract"
    elif DELETE_BIAS_PATHS & parts:
        result["path_bias"] = "delete"

    # Triage decision
    if result["is_empty"] or result["loc"] < 5:
        result["triage"] = "DELETE"
        result["triage_reason"] = "empty_or_trivial"
    elif result["path_bias"] == "delete" and symbols < MIN_SYMBOLS_KEEP:
        result["triage"] = "DELETE"
        result["triage_reason"] = "test_or_stub_path_low_symbols"
    elif (
        result["loc"] >= MIN_LOC_EXTRACT
        and symbols >= MIN_SYMBOLS_KEEP
        and (result["has_docstring"] or result["has_type_hints"] or result["path_bias"] == "extract")
    ):
        result["triage"] = "EXTRACT_LOGIC"
        result["triage_reason"] = "high_quality_signals"
    elif symbols >= MIN_SYMBOLS_KEEP or result["loc"] >= MIN_LOC_EXTRACT:
        result["triage"] = "KEEP_VERIFY"
        result["triage_reason"] = "moderate_signal_needs_review"
    else:
        result["triage"] = "DELETE"
        result["triage_reason"] = "insufficient_signal"

    return result


def run(target: Path, out_dir: Path) -> None:
    print(f"[module_triage_classifier] Scanning: {target}")
    modules = []
    triage_counts: dict[str, int] = {"EXTRACT_LOGIC": 0, "KEEP_VERIFY": 0, "DELETE": 0}

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            info = analyze_module(Path(root) / fn, target)
            triage_counts[info["triage"]] = triage_counts.get(info["triage"], 0) + 1
            modules.append(info)

    extract = [m["file"] for m in modules if m["triage"] == "EXTRACT_LOGIC"]
    keep = [m["file"] for m in modules if m["triage"] == "KEEP_VERIFY"]
    delete = [m["file"] for m in modules if m["triage"] == "DELETE"]

    write_json(out_dir, "module_triage.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(modules),
        "triage_counts": triage_counts,
        "extract_logic": extract,
        "keep_verify": keep,
        "delete": delete,
        "modules": modules,
    })
    print(f"  Total: {len(modules)}  EXTRACT: {triage_counts['EXTRACT_LOGIC']}  "
          f"KEEP: {triage_counts['KEEP_VERIFY']}  DELETE: {triage_counts['DELETE']}")


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
