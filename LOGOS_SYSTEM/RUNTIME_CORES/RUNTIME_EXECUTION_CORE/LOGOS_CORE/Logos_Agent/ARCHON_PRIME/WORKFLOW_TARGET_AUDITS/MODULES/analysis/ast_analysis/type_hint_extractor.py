#!/usr/bin/env python3
"""
ARCHON PRIME — Type Hint Extractor
=====================================
Extracts all type annotations from function signatures, class attributes,
and module-level annotated assignments across the target repository.
Writes: type_hint_report.json
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
    p = argparse.ArgumentParser(description="Archon type hint extractor")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def unparse_safe(node: ast.expr | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def extract_type_hints(path: Path) -> list[dict]:
    hints: list[dict] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception:
        return hints

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Parameter annotations
            for arg in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
                if arg.annotation:
                    hints.append({
                        "context": "parameter",
                        "function": node.name,
                        "name": arg.arg,
                        "annotation": unparse_safe(arg.annotation),
                        "lineno": arg.lineno if hasattr(arg, "lineno") else node.lineno,
                    })
            # Return annotation
            if node.returns:
                hints.append({
                    "context": "return",
                    "function": node.name,
                    "name": "return",
                    "annotation": unparse_safe(node.returns),
                    "lineno": node.lineno,
                })
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            hints.append({
                "context": "variable",
                "function": None,
                "name": node.target.id,
                "annotation": unparse_safe(node.annotation),
                "lineno": node.lineno,
            })
    return hints


def run(target: Path, out_dir: Path) -> None:
    print(f"[type_hint_extractor] Scanning: {target}")
    results: list[dict] = []
    total_hints = 0
    total_annotated = 0
    total_unannotated = 0

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            fp = Path(root) / fn
            rel = str(fp.relative_to(target))
            hints = extract_type_hints(fp)

            # Count annotated vs unannotated functions in this file
            annotated = len({h["function"] for h in hints if h["context"] == "return"})
            try:
                src = fp.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(src)
                all_fns = sum(1 for n in ast.walk(tree)
                              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
            except Exception:
                all_fns = 0
            unannotated = max(0, all_fns - annotated)

            total_hints += len(hints)
            total_annotated += annotated
            total_unannotated += unannotated
            results.append({
                "file": rel,
                "module": rel.removesuffix(".py").replace(os.sep, "."),
                "hint_count": len(hints),
                "annotated_functions": annotated,
                "unannotated_functions": unannotated,
                "coverage_ratio": round(annotated / all_fns, 3) if all_fns else 1.0,
                "type_hints": hints,
            })

    write_json(out_dir, "type_hint_report.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_processed": len(results),
        "total_type_hints": total_hints,
        "total_annotated_functions": total_annotated,
        "total_unannotated_functions": total_unannotated,
        "overall_coverage": (
            round(total_annotated / (total_annotated + total_unannotated), 3)
            if (total_annotated + total_unannotated) else 1.0
        ),
        "modules": results,
    })
    print(f"  Files: {len(results)}  Type hints: {total_hints}  "
          f"Annotation coverage: {total_annotated}/{total_annotated + total_unannotated} functions")


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
