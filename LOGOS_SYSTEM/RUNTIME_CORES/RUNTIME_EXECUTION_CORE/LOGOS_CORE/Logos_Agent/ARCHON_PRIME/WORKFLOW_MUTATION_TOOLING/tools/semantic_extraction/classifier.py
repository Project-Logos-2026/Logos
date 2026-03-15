# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-073
# module_name:          classifier
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/semantic_extraction/classifier.py
# responsibility:       Analysis module: classifier
# runtime_stage:        analysis
# execution_entry:      None
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
classifier.py — Keyword-based function classification into DRAC AF categories.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: classifier.py
tool_category: Static_Analysis
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python classifier.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

from pathlib import Path
from typing import Optional

OUTPUT_ROOT = Path(
    "/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS"
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json

        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


# Category → keyword signals (checked against name + docstring + body_calls, lowercased)
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "AGENT_CONTROL": [
        "agent",
        "controller",
        "dispatch",
        "execute",
        "orchestrate",
        "lifecycle",
        "startup",
        "activate",
        "boot",
    ],
    "SEMANTIC_PROCESSING": [
        "parse",
        "interpret",
        "translate",
        "embed",
        "semantic",
        "token",
        "ontol",
        "meaning",
        "vector",
    ],
    "REASONING_ENGINE": [
        "infer",
        "deduce",
        "prove",
        "validate",
        "reason",
        "syllog",
        "logic",
        "bayes",
        "symbolic",
        "inference",
    ],
    "UTILITY_SUPPORT": [
        "load",
        "save",
        "convert",
        "serialize",
        "format",
        "read",
        "write",
        "util",
        "helper",
        "config",
    ],
    "SAFETY_GUARD": [
        "verify",
        "sanitize",
        "guard",
        "enforce",
        "secure",
        "attest",
        "audit",
        "constraint",
        "permit",
        "deny",
    ],
    "MATH_OPERATOR": [
        "compute",
        "matrix",
        "vector",
        "probability",
        "score",
        "numeric",
        "math",
        "calculate",
        "sum",
        "integral",
    ],
}

# Ordered for tie-breaking — first match wins if scores are tied
CATEGORY_ORDER = list(CATEGORY_KEYWORDS.keys())


def classify(name: str, docstring: str, body_calls: str) -> Optional[str]:
    """
    Return the best-matching DRAC AF category for a function.
    Returns None if no signal matches at all.
    """
    haystack = f"{name} {docstring} {body_calls}".lower()
    best_cat = None
    best_score = 0

    for cat in CATEGORY_ORDER:
        keywords = CATEGORY_KEYWORDS[cat]
        score = sum(1 for kw in keywords if kw in haystack)
        if score > best_score:
            best_score = score
            best_cat = cat

    return best_cat if best_score > 0 else None


def classify_record(record: dict) -> Optional[str]:
    """Convenience wrapper that accepts an ast_parser record dict."""
    return classify(
        name=record.get("name", ""),
        docstring=record.get("docstring", ""),
        body_calls=record.get("body_calls", ""),
    )
