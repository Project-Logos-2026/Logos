#!/usr/bin/env python3
"""
ARCHON PRIME — AST Semantic Analyzer
======================================
Infers high-level semantic roles for each Python module using AST-derived
signals: keyword patterns, import profiles, function naming, class presence,
and decorator usage. Writes: semantic_analysis_report.json
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

# Role → signal keyword sets (matched against names and string literals)
ROLE_SIGNALS: dict[str, list[str]] = {
    "reasoning":  ["infer", "reason", "derive", "conclude", "hypothesis", "logic", "proof", "axiom", "belief"],
    "agent":      ["agent", "actor", "run_loop", "step", "policy", "action", "observation", "reward"],
    "utility":    ["util", "helper", "convert", "format", "parse", "serialize", "sanitize", "clamp"],
    "safety":     ["validate", "guard", "constraint", "forbidden", "deny", "allow", "check", "restrict"],
    "math":       ["matrix", "vector", "norm", "gradient", "optimize", "loss", "probability", "sample"],
    "semantic":   ["embed", "token", "similarity", "cluster", "classify", "nlp", "corpus", "vocab"],
    "interface":  ["router", "endpoint", "handler", "request", "response", "server", "api", "route"],
    "data":       ["load", "save", "read", "write", "cache", "store", "fetch", "query", "schema"],
    "test":       ["test_", "assert_", "fixture", "mock", "stub", "patch", "parametrize"],
    "config":     ["config", "settings", "env", "environment", "init", "setup", "configure"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon AST semantic analyzer")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def score_roles(names: list[str]) -> dict[str, int]:
    lower = [n.lower() for n in names]
    scores = {}
    for role, signals in ROLE_SIGNALS.items():
        score = sum(1 for n in lower for s in signals if s in n)
        if score:
            scores[role] = score
    return scores


def analyze_file(path: Path, target: Path) -> dict:
    rel = str(path.relative_to(target))
    result: dict = {
        "file": rel,
        "module": rel.removesuffix(".py").replace(os.sep, "."),
        "primary_role": "unknown",
        "role_scores": {},
        "all_names": [],
        "imports": [],
        "classes": [],
        "functions": [],
        "has_main_block": False,
        "error": None,
    }
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception as exc:
        result["error"] = str(exc)
        return result

    names: list[str] = []
    imports: list[str] = []
    classes: list[str] = []
    functions: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
            else:
                for alias in node.names:
                    imports.append(alias.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
            names.append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
            names.append(node.name)

    # Check for if __name__ == "__main__"
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.If):
            cond = ast.unparse(node.test)
            if "__name__" in cond and "__main__" in cond:
                result["has_main_block"] = True

    # Use path parts as additional signal sources
    path_words = re.sub(r"[^a-z0-9]", " ", rel.lower()).split()
    all_names = names + imports + path_words
    scores = score_roles(all_names)

    result["role_scores"] = scores
    result["primary_role"] = max(scores, key=scores.__getitem__) if scores else "utility"
    result["all_names"] = names[:50]  # cap
    result["imports"] = imports[:30]
    result["classes"] = classes
    result["functions"] = functions[:40]
    return result


def run(target: Path, out_dir: Path) -> None:
    print(f"[ast_semantic_analyzer] Scanning: {target}")
    modules = []
    role_counts: dict[str, int] = {}

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            info = analyze_file(Path(root) / fn, target)
            modules.append(info)
            role = info["primary_role"]
            role_counts[role] = role_counts.get(role, 0) + 1

    write_json(out_dir, "semantic_analysis_report.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(modules),
        "role_distribution": role_counts,
        "modules": modules,
    })
    print(f"  Modules: {len(modules)}  Roles: {role_counts}")


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
