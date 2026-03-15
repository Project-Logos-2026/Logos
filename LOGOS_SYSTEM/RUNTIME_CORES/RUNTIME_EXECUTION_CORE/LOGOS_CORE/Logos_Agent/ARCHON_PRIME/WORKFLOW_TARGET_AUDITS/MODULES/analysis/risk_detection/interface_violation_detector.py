#!/usr/bin/env python3
"""
ARCHON PRIME — Interface Violation Detector
=============================================
Identifies imports from internal (privacy-by-convention) submodules:
  - importing via `_`-prefixed modules or names
  - importing from known private implementation packages
  - cross-layer imports that violate the architectural layering contract

Writes: interface_violations.json
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

# Patterns for private/internal module imports
PRIVATE_MODULE_PATTERN = re.compile(r"(?:^|\.)_[a-zA-Z]")

# Names that, when imported, suggest reaching into implementation details
IMPL_DETAIL_NAMES = {"_impl", "_internal", "_private", "_base", "_core", "_compat"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon interface violation detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def find_violations(path: Path, target: Path) -> list[dict]:
    violations: list[dict] = []
    rel = str(path.relative_to(target))
    module = rel.removesuffix(".py").replace(os.sep, ".")

    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception:
        return violations

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            # Check for private module imports
            if PRIVATE_MODULE_PATTERN.search(mod):
                violations.append({
                    "importer": module,
                    "imported": mod,
                    "violation_type": "private_module_import",
                    "lineno": node.lineno,
                    "severity": "MEDIUM",
                })
            # Check for impl-detail names
            for part in mod.split("."):
                if part in IMPL_DETAIL_NAMES:
                    violations.append({
                        "importer": module,
                        "imported": mod,
                        "violation_type": "implementation_detail_import",
                        "lineno": node.lineno,
                        "severity": "HIGH",
                    })
                    break
            # Check imported names themselves (from x import _y)
            for alias in node.names:
                if alias.name.startswith("_") and not alias.name.startswith("__"):
                    violations.append({
                        "importer": module,
                        "imported": f"{mod}.{alias.name}",
                        "violation_type": "private_name_import",
                        "lineno": node.lineno,
                        "severity": "LOW",
                    })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if PRIVATE_MODULE_PATTERN.search(alias.name):
                    violations.append({
                        "importer": module,
                        "imported": alias.name,
                        "violation_type": "private_module_import",
                        "lineno": node.lineno,
                        "severity": "MEDIUM",
                    })

    return violations


def run(target: Path, out_dir: Path) -> None:
    print(f"[interface_violation_detector] Scanning: {target}")
    all_violations: list[dict] = []
    severity_counts: dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    type_counts: dict[str, int] = {}
    files_scanned = 0

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            files_scanned += 1
            violations = find_violations(Path(root) / fn, target)
            for v in violations:
                severity_counts[v["severity"]] = severity_counts.get(v["severity"], 0) + 1
                vtype = v["violation_type"]
                type_counts[vtype] = type_counts.get(vtype, 0) + 1
            all_violations.extend(violations)

    # Group by importer module
    by_module: dict[str, list[dict]] = {}
    for v in all_violations:
        by_module.setdefault(v["importer"], []).append(v)

    write_json(out_dir, "interface_violations.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_scanned": files_scanned,
        "total_violations": len(all_violations),
        "severity_counts": severity_counts,
        "type_counts": type_counts,
        "affected_modules": len(by_module),
        "risk_level": (
            "HIGH" if severity_counts["HIGH"] > 0 else
            "MEDIUM" if severity_counts["MEDIUM"] > 0 else
            "LOW" if severity_counts["LOW"] > 0 else "NONE"
        ),
        "violations": all_violations,
    })
    print(f"  Files: {files_scanned}  Violations: {len(all_violations)}  "
          f"Severity: {severity_counts}")


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
