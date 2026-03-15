#!/usr/bin/env python3
"""
ARCHON PRIME — Cohesion Analyzer
==================================
Measures intra-module cohesion by comparing the proportion of functions
that share common names, imports, or call patterns. Low cohesion indicates
a module is doing too many unrelated things and may need to be split.
Writes: cohesion_report.json
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
    p = argparse.ArgumentParser(description="Archon cohesion analyzer")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


class FunctionInfo:
    def __init__(self, name: str):
        self.name = name
        self.used_names: set[str] = set()
        self.called_names: set[str] = set()

    def shared_names_with(self, other: "FunctionInfo") -> int:
        return len(self.used_names & other.used_names)


def extract_functions(tree: ast.Module) -> list[FunctionInfo]:
    fns: list[FunctionInfo] = []
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        fi = FunctionInfo(node.name)
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                fi.used_names.add(child.id)
            elif isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    fi.called_names.add(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    fi.called_names.add(child.func.attr)
        fns.append(fi)
    return fns


def compute_cohesion(fns: list[FunctionInfo]) -> float:
    """
    Lack of Cohesion of Methods (LCOM) simplified:
    ratio of function pairs that share NO used names.
    Returns cohesion = 1 - lcom (1.0 = perfectly cohesive).
    """
    n = len(fns)
    if n < 2:
        return 1.0
    pairs = n * (n - 1) // 2
    shared = 0
    for i in range(n):
        for j in range(i + 1, n):
            if fns[i].shared_names_with(fns[j]) > 0:
                shared += 1
    lcom = 1.0 - (shared / pairs)
    cohesion = 1.0 - lcom
    return round(cohesion, 4)


def analyze_file(path: Path, target: Path) -> dict:
    rel = str(path.relative_to(target))
    module = rel.removesuffix(".py").replace(os.sep, ".")
    result: dict = {
        "file": rel,
        "module": module,
        "function_count": 0,
        "class_count": 0,
        "cohesion_score": 1.0,
        "cohesion_grade": "UNKNOWN",
        "function_names": [],
        "error": None,
    }
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception as exc:
        result["error"] = str(exc)
        return result

    fns = extract_functions(tree)
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    cohesion = compute_cohesion(fns)

    result["function_count"] = len(fns)
    result["class_count"] = len(classes)
    result["cohesion_score"] = cohesion
    result["cohesion_grade"] = (
        "HIGH" if cohesion >= 0.7 else
        "MEDIUM" if cohesion >= 0.4 else
        "LOW"
    )
    result["function_names"] = [f.name for f in fns[:20]]
    return result


def run(target: Path, out_dir: Path) -> None:
    print(f"[cohesion_analyzer] Scanning: {target}")
    modules = []
    grade_counts: dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            info = analyze_file(Path(root) / fn, target)
            grade_counts[info["cohesion_grade"]] = grade_counts.get(info["cohesion_grade"], 0) + 1
            modules.append(info)

    # Sort by cohesion ascending (worst first)
    modules.sort(key=lambda x: x["cohesion_score"])

    avg_cohesion = (
        round(sum(m["cohesion_score"] for m in modules) / len(modules), 4)
        if modules else 0.0
    )

    write_json(out_dir, "cohesion_report.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(modules),
        "average_cohesion_score": avg_cohesion,
        "grade_distribution": grade_counts,
        "low_cohesion_candidates": [m["module"] for m in modules if m["cohesion_grade"] == "LOW"][:20],
        "modules": modules,
    })
    print(f"  Modules: {len(modules)}  Avg cohesion: {avg_cohesion}  "
          f"LOW: {grade_counts['LOW']}  HIGH: {grade_counts['HIGH']}")


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
