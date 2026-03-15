#!/usr/bin/env python3
"""
ARCHON PRIME — Code Complexity Analyzer
=========================================
Computes code complexity metrics for each Python module: cyclomatic
complexity (branch count), lines of code (LOC), logical lines, function
length distribution, and nesting depth. Writes: complexity_report.json
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

# Nodes that add a branch (each adds 1 to cyclomatic complexity)
BRANCH_NODES = (
    ast.If, ast.For, ast.While, ast.ExceptHandler,
    ast.With, ast.Assert, ast.comprehension,
    ast.BoolOp,  # or/and each represent branch
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon code complexity analyzer")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def cyclomatic_complexity(func_node: ast.AST) -> int:
    """Simplified cyclomatic complexity: 1 + number of branching nodes."""
    return 1 + sum(1 for _ in ast.walk(func_node) if isinstance(_, BRANCH_NODES))


def max_nesting_depth(func_node: ast.AST) -> int:
    """Compute maximum nesting depth within a function."""
    NESTING_NODES = (ast.If, ast.For, ast.While, ast.With, ast.Try)

    def depth(node: ast.AST, current: int) -> int:
        if isinstance(node, NESTING_NODES):
            current += 1
        return max(
            (depth(child, current) for child in ast.iter_child_nodes(node)),
            default=current,
        )

    return depth(func_node, 0)


def analyze_file(path: Path, target: Path) -> dict:
    rel = str(path.relative_to(target))
    module = rel.removesuffix(".py").replace(os.sep, ".")
    result: dict = {
        "file": rel,
        "module": module,
        "loc": 0,
        "logical_loc": 0,
        "blank_lines": 0,
        "comment_lines": 0,
        "function_count": 0,
        "class_count": 0,
        "avg_complexity": 0.0,
        "max_complexity": 0,
        "max_nesting": 0,
        "complexity_grade": "UNKNOWN",
        "functions": [],
        "error": None,
    }
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        result["error"] = str(exc)
        return result

    lines = src.splitlines()
    result["loc"] = len(lines)
    result["blank_lines"] = sum(1 for l in lines if not l.strip())
    result["comment_lines"] = sum(1 for l in lines if l.strip().startswith("#"))

    try:
        tree = ast.parse(src, filename=str(path))
    except Exception as exc:
        result["error"] = str(exc)
        return result

    # Logical LOC = statement nodes
    result["logical_loc"] = sum(
        1 for n in ast.walk(tree) if isinstance(n, ast.stmt)
    )

    fn_complexities: list[int] = []
    fn_depths: list[int] = []
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    result["class_count"] = len(classes)

    fn_details: list[dict] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            cc = cyclomatic_complexity(node)
            nd = max_nesting_depth(node)
            fn_len = (getattr(node, "end_lineno", node.lineno) - node.lineno + 1)
            fn_complexities.append(cc)
            fn_depths.append(nd)
            fn_details.append({
                "name": node.name,
                "lineno": node.lineno,
                "length_lines": fn_len,
                "cyclomatic_complexity": cc,
                "nesting_depth": nd,
            })

    result["function_count"] = len(fn_complexities)
    if fn_complexities:
        result["avg_complexity"] = round(sum(fn_complexities) / len(fn_complexities), 2)
        result["max_complexity"] = max(fn_complexities)
    if fn_depths:
        result["max_nesting"] = max(fn_depths)
    result["functions"] = sorted(fn_details, key=lambda x: x["cyclomatic_complexity"], reverse=True)[:10]

    mc = result["max_complexity"]
    result["complexity_grade"] = (
        "SIMPLE" if mc <= 5 else
        "MODERATE" if mc <= 10 else
        "COMPLEX" if mc <= 20 else
        "CRITICAL"
    )
    return result


def run(target: Path, out_dir: Path) -> None:
    print(f"[code_complexity_analyzer] Scanning: {target}")
    modules = []
    grade_counts: dict[str, int] = {}

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            info = analyze_file(Path(root) / fn, target)
            grade_counts[info["complexity_grade"]] = grade_counts.get(info["complexity_grade"], 0) + 1
            modules.append(info)

    modules.sort(key=lambda x: x["max_complexity"], reverse=True)
    total_loc = sum(m["loc"] for m in modules)
    avg_complexity = (
        round(sum(m["avg_complexity"] for m in modules) / len(modules), 2)
        if modules else 0.0
    )

    write_json(out_dir, "complexity_report.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(modules),
        "total_loc": total_loc,
        "average_cyclomatic_complexity": avg_complexity,
        "grade_distribution": grade_counts,
        "high_complexity_modules": [
            m["module"] for m in modules if m["complexity_grade"] in ("COMPLEX", "CRITICAL")
        ][:20],
        "modules": modules,
    })
    print(f"  Modules: {len(modules)}  Total LOC: {total_loc}  "
          f"Avg complexity: {avg_complexity}  CRITICAL: {grade_counts.get('CRITICAL', 0)}")


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
