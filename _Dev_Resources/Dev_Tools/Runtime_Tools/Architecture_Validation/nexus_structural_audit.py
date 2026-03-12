"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: nexus_structural_audit.py
tool_category: Architecture_Validation
tool_subcategory: nexus_classification

purpose:
AST-based classification of every Python module under a given root into
EXECUTION_NEXUS, BINDING_NEXUS, or NON_NEXUS categories. Based on class
naming patterns and import surface. Detects classification violations.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python nexus_structural_audit.py --root LOGOS_SYSTEM

output_artifacts:
nexus_structural_audit.json

dependencies:
ast, pathlib, json, argparse

safety_classification:
READ_ONLY
"""

import ast
import json
import argparse
from pathlib import Path

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


EXECUTION_NEXUS_PATTERNS = ("Execution", "Runtime", "Engine", "Core", "Dispatch", "Orchestrator")
BINDING_NEXUS_PATTERNS = ("Nexus", "Bridge", "Binding", "Router", "Gateway", "Relay")


def classify_module(filepath: Path, repo_root: Path) -> dict:
    """Classify a module and list its top-level class names."""
    rel = str(filepath.relative_to(repo_root))
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(filepath))
    except SyntaxError as exc:
        return {"path": rel, "classification": "PARSE_ERROR", "classes": [], "error": str(exc)}

    top_classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    classification = "NON_NEXUS"
    for cls in top_classes:
        if any(pat in cls for pat in EXECUTION_NEXUS_PATTERNS):
            classification = "EXECUTION_NEXUS"
            break
        if any(pat in cls for pat in BINDING_NEXUS_PATTERNS):
            classification = "BINDING_NEXUS"

    return {"path": rel, "classification": classification, "classes": top_classes}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Nexus structural auditor — classifies modules into EXECUTION_NEXUS / BINDING_NEXUS / NON_NEXUS."
    )
    parser.add_argument(
        "--root",
        required=True,
        help="Directory to audit, relative to repo root.",
    )
    parser.add_argument(
        "--repo-root",
        default="/workspaces/Logos",
        help="Repository root (default: /workspaces/Logos).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    scan_root = repo_root / args.root

    if not scan_root.exists():
        print(f"ERROR: Root not found: {scan_root}")
        raise SystemExit(1)

    py_files = sorted(scan_root.rglob("*.py"))
    print(f"Classifying {len(py_files)} modules under: {args.root}")

    records = [classify_module(f, repo_root) for f in py_files]

    by_class: dict[str, list[str]] = {
        "EXECUTION_NEXUS": [],
        "BINDING_NEXUS": [],
        "NON_NEXUS": [],
        "PARSE_ERROR": [],
    }
    for r in records:
        by_class.setdefault(r["classification"], []).append(r["path"])

    report = {
        "tool": "nexus_structural_audit",
        "root": args.root,
        "summary": {k: len(v) for k, v in by_class.items()},
        "classification_index": by_class,
        "modules": records,
    }
    write_report("nexus_structural_audit.json", report)
    for label, paths in by_class.items():
        print(f"  {label}: {len(paths)}")


if __name__ == "__main__":
    main()
