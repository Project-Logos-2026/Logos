# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-079
# module_name:          semantic_extractor
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/semantic_extraction/semantic_extractor.py
# responsibility:       Analysis module: semantic extractor
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
semantic_extractor.py — Derive the minimal semantic modifier expression for a function.

Example:
    symbolic_deduction()  →  "deduce(symbolic)"
    agent_dispatch()      →  "dispatch(agent)"
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: semantic_extractor.py
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
python semantic_extractor.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import re
from pathlib import Path

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


# Ordered semantic verb vocabulary
SEMANTIC_VERBS = [
    "infer",
    "deduce",
    "prove",
    "validate",
    "reason",
    "compute",
    "execute",
    "dispatch",
    "orchestrate",
    "parse",
    "interpret",
    "translate",
    "embed",
    "sanitize",
    "verify",
    "guard",
    "enforce",
    "load",
    "save",
    "convert",
    "serialize",
    "format",
    "score",
    "activate",
    "boot",
    "register",
    "route",
    "schedule",
]

# Domain modifier vocabulary
DOMAIN_MODIFIERS = [
    "symbolic",
    "probabilistic",
    "semantic",
    "logical",
    "agent",
    "runtime",
    "temporal",
    "epistemic",
    "causal",
    "modal",
    "axiomatic",
    "numeric",
    "vector",
    "recursive",
    "bijective",
    "trinitarian",
    "governance",
    "safety",
    "memory",
    "planning",
]


def _tokenize(name: str) -> list[str]:
    """Split snake_case and camelCase name into lowercase tokens."""
    # camelCase split
    tokens = re.sub(r"([A-Z])", r"_\1", name).lower()
    return [t for t in re.split(r"[_\-\s]+", tokens) if t]


def extract(function_name: str, docstring: str = "") -> str:
    """
    Return the smallest semantic modifier expression for a function.
    Format: verb(modifier)  or  verb()  if no modifier found.
    """
    name_tokens = _tokenize(function_name)
    doc_tokens = _tokenize(docstring.split(".")[0]) if docstring else []
    all_tokens = name_tokens + doc_tokens

    # Find primary verb
    verb = None
    for tok in all_tokens:
        for sv in SEMANTIC_VERBS:
            if sv in tok or tok in sv:
                verb = sv
                break
        if verb:
            break
    if verb is None:
        verb = name_tokens[0] if name_tokens else "undefined"

    # Find domain modifier (first token that is NOT the verb)
    modifier = None
    for tok in all_tokens:
        for dm in DOMAIN_MODIFIERS:
            if dm in tok or tok in dm:
                modifier = dm
                break
        if modifier:
            break

    return f"{verb}({modifier})" if modifier else f"{verb}()"


def extract_record(record: dict) -> str:
    """Convenience wrapper that accepts an ast_parser record dict."""
    return extract(
        function_name=record.get("name", ""),
        docstring=record.get("docstring", ""),
    )
