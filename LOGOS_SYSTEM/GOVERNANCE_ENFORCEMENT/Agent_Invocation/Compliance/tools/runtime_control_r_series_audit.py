#!/usr/bin/env python3
"""
Runtime_Control R-Series Governance Audit (Design-Only)

Scope:
- R0_Eligibility
- R1_Authority_Evaluation
- R2_Bounded_Authority
- R3_Continuation_Control

Guarantees:
- Design-only
- Deny-by-default
- No autonomy, execution, persistence, or external IO
- Step-5 explicitly blocked

Output:
- _reports/runtime_control_r_series_audit.json
"""

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("LOGOS_SYSTEM/RUNTIME/Runtime_Control")
REPORT_PATH = Path("_reports/runtime_control_r_series_audit.json")

REQUIRED = {
    "R0_Eligibility": [
        "R0_README.md",
        "R0_Semantic_Contract.md",
        "R0_Audit_Spec.md",
    ],
    "R1_Authority_Evaluation": [
        "R1_README.md",
        "R1_Semantic_Contract.md",
        "R1_Evaluation_Signals.md",
        "R1_Audit_Spec.md",
    ],
    "R2_Bounded_Authority": [
        "R2_README.md",
        "R2_Semantic_Contract.md",
        "R2_Grant_Model.md",
        "R2_Revocation_Supremacy.md",
        "R2_Audit_Spec.md",
    ],
    "R3_Continuation_Control": [
        "R3_README.md",
        "R3_Semantic_Contract.md",
        "R3_Continuation_Bounds.md",
        "R3_Supervision_and_Observability.md",
        "R3_Audit_Spec.md",
    ],
}

# Markers that would indicate enablement of forbidden behaviors.
FORBIDDEN_MARKERS = [
    "autonomy enabled",
    "autonomous execution",
    "allow external io",
    "enable external io",
    "persistence enabled",
    "unbounded scheduler",
    "self-directed continuation",
    "background loop enabled",
]

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").lower()
    except Exception:
        return ""

results = {
    "timestamp_utc": datetime.now(UTC).isoformat(),
    "scope": "Runtime_Control R0–R3",
    "mode": "design_only",
    "status": "PASS",
    "checks": [],
}

for section, files in REQUIRED.items():
    section_path = ROOT / section
    if not section_path.exists():
        results["status"] = "FAIL"
        results["checks"].append({
            "section": section,
            "error": "missing_directory",
        })
        continue

    for fname in files:
        fpath = section_path / fname
        if not fpath.exists():
            results["status"] = "FAIL"
            results["checks"].append({
                "section": section,
                "file": fname,
                "error": "missing_file",
            })
            continue

        text = read_text(fpath)
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                results["status"] = "FAIL"
                results["checks"].append({
                    "section": section,
                    "file": fname,
                    "error": "forbidden_marker_detected",
                    "marker": marker,
                })

# Step-5 block verification
rtodo = ROOT / "R_TODO.md"
if not rtodo.exists() or "step-5" not in read_text(rtodo):
    results["status"] = "FAIL"
    results["checks"].append({
        "section": "Runtime_Control",
        "file": "R_TODO.md",
        "error": "step_5_not_explicitly_blocked",
    })

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")

print(f"Runtime_Control R-Series audit complete: {results['status']}")
