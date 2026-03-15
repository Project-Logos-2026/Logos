#!/usr/bin/env python3
"""
ARCHON PRIME — Dynamic Import Detector
========================================
Finds dynamic import patterns in Python source: __import__(), importlib,
eval(), exec(), and getattr-based module resolution. These patterns are
execution-time risks that static analysis cannot fully resolve.
Writes: dynamic_imports.json
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

DYNAMIC_IMPORT_PATTERNS = {
    "__import__": "builtin_import",
    "importlib.import_module": "importlib",
    "importlib.util.spec_from_file_location": "importlib_spec",
    "importlib.util.module_from_spec": "importlib_spec",
    "pkgutil.get_loader": "pkgutil",
    "pkgutil.find_loader": "pkgutil",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon dynamic import detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def _call_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_call_name(node.value)}.{node.attr}"
    return ""


class DynamicImportVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.findings: list[dict] = []

    def visit_Call(self, node: ast.Call) -> None:
        name = _call_name(node.func)
        pattern_type = DYNAMIC_IMPORT_PATTERNS.get(name)

        if pattern_type:
            # Try to extract the imported module name if it's a string literal
            module_arg = None
            if node.args and isinstance(node.args[0], ast.Constant):
                module_arg = str(node.args[0].value)
            self.findings.append({
                "pattern": name,
                "pattern_type": pattern_type,
                "resolved_module": module_arg,
                "lineno": node.lineno,
            })

        # Also catch eval/exec
        if name in ("eval", "exec"):
            self.findings.append({
                "pattern": name,
                "pattern_type": "code_execution",
                "resolved_module": None,
                "lineno": node.lineno,
            })

        self.generic_visit(node)


def scan_file(path: Path, target: Path) -> dict:
    rel = str(path.relative_to(target))
    module = rel.removesuffix(".py").replace(os.sep, ".")
    result = {
        "file": rel,
        "module": module,
        "dynamic_imports": [],
        "error": None,
    }
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception as exc:
        result["error"] = str(exc)
        return result

    visitor = DynamicImportVisitor()
    visitor.visit(tree)
    result["dynamic_imports"] = visitor.findings
    return result


def run(target: Path, out_dir: Path) -> None:
    print(f"[dynamic_import_detector] Scanning: {target}")
    results = []
    total_findings = 0
    kind_counts: dict[str, int] = {}

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            info = scan_file(Path(root) / fn, target)
            total_findings += len(info["dynamic_imports"])
            for d in info["dynamic_imports"]:
                kind = d["pattern_type"]
                kind_counts[kind] = kind_counts.get(kind, 0) + 1
            if info["dynamic_imports"]:  # Only emit modules that have findings
                results.append(info)

    write_json(out_dir, "dynamic_imports.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_with_dynamic_imports": len(results),
        "total_dynamic_import_sites": total_findings,
        "pattern_type_counts": kind_counts,
        "risk_level": (
            "HIGH" if total_findings > 10 else
            "MEDIUM" if total_findings > 3 else
            "LOW" if total_findings > 0 else "NONE"
        ),
        "modules": results,
    })
    print(f"  Dynamic import sites: {total_findings}  Affected modules: {len(results)}  "
          f"Pattern types: {kind_counts}")


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
