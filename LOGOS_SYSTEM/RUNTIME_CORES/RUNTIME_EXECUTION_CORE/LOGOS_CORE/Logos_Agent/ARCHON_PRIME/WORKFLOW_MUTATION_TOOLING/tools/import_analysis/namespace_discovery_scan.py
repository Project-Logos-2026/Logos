# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-058
# module_name:          namespace_discovery_scan
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/import_analysis/namespace_discovery_scan.py
# responsibility:       Analysis module: namespace discovery scan
# runtime_stage:        analysis
# execution_entry:      main
# allowed_targets:      []
# forbidden_targets:    ["SYSTEM", "WORKFLOW_NEXUS"]
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       [SPEC-AP-V2.1]
# implementation_phase: PHASE_2
# authoring_authority:  ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================
from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate

enforce_runtime_gate()

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: namespace_discovery_scan.py
tool_category: Architecture_Validation
tool_subcategory: namespace_mapping

purpose:
Discovers the physical on-disk locations of namespace roots in the repo.
For each target namespace name, locates all matching directories and reports
their full paths, depth, and whether an __init__.py is present.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python namespace_discovery_scan.py --targets LOGOS_SYSTEM STARTUP logos

output_artifacts:
namespace_discovery.json

dependencies:
pathlib, json, argparse

safety_classification:
READ_ONLY
"""

import argparse
import json
from pathlib import Path

OUTPUT_ROOT = Path(
    "/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS"
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


def discover_namespaces(
    targets: list[str], repo_root: Path, exclude: list[str]
) -> dict:
    """Find all directories matching each target name under repo_root."""
    results: dict[str, list[dict]] = {t: [] for t in targets}

    for dirpath in sorted(repo_root.rglob("*")):
        if not dirpath.is_dir():
            continue
        if any(exc in dirpath.parts for exc in exclude):
            continue
        if dirpath.name in targets:
            rel = dirpath.relative_to(repo_root)
            depth = len(rel.parts)
            has_init = (dirpath / "__init__.py").exists()
            results[dirpath.name].append(
                {
                    "path": str(rel),
                    "depth": depth,
                    "has_init": has_init,
                }
            )

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Discover physical locations of named namespaces in the repository."
    )
    parser.add_argument(
        "--targets",
        nargs="+",
        required=True,
        help="Namespace (directory) names to locate.",
    )
    parser.add_argument(
        "--root",
        default="/workspaces/ARCHON_PRIME",
        help="Repository root to scan (default: /workspaces/ARCHON_PRIME).",
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=["__pycache__", ".git", ".venv", "node_modules"],
        help="Directory names to exclude from search.",
    )
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    print(f"Discovering namespaces: {args.targets}")
    print(f"Scanning: {repo_root}")

    findings = discover_namespaces(args.targets, repo_root, args.exclude)

    summary = {name: len(locs) for name, locs in findings.items()}
    report = {
        "tool": "namespace_discovery_scan",
        "root": str(repo_root),
        "targets": args.targets,
        "summary": summary,
        "findings": findings,
    }
    write_report("namespace_discovery.json", report)
    for name, locs in findings.items():
        print(f"  {name}: {len(locs)} location(s)")
        for loc in locs[:3]:
            print(f"    {loc['path']}")


if __name__ == "__main__":
    main()
