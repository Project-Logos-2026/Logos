# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: step5_autonomy_argument_probe
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Agent_Invocation/Compliance/tools/step5_autonomy_argument_probe.py.
agent_binding: None
protocol_binding: None
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Agent_Invocation/Compliance/tools/step5_autonomy_argument_probe.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

#!/usr/bin/env python3
"""
Step-5 Autonomy Argument Probe (Design-Only, Deny-by-Default)

Purpose:
- Generate a system-constructed candidate argument for why autonomy *might* be justified,
  grounded only in repo-local artifacts and logs.
- Mandatory adversarial critique ("Cognitive Resistor") and risk ledger.
- Produces an evaluation artifact; DOES NOT GRANT autonomy.

Hard Constraints:
- No external IO/network.
- No authority grants issued or persisted.
- No background loops or continuation.
- Deterministic halt with termination reasons.

Outputs:
- _reports/step5_autonomy_argument_probe.json
- _reports/step5_autonomy_argument_probe.md
"""


import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(".")
REPORT_JSON = Path("_reports/step5_autonomy_argument_probe.json")
REPORT_MD = Path("_reports/step5_autonomy_argument_probe.md")

# Evidence roots (read-only)
EVIDENCE_PATHS = [
    Path("_reports"),
    Path("LOGOS_SYSTEM/RUNTIME/Runtime_Control"),
    Path("SYSTEM_AUDIT_LOGS"),
    Path("LOGOS_SYSTEM/GOVERNANCE"),
    Path("LOGOS_SYSTEM/System_Entry_Point/Proof_Logs"),
]

# Fail-closed safety: never claim autonomy is granted; never suggest bypass.
FORBIDDEN_OUTPUT_PHRASES = [
    "autonomy granted",
    "enable autonomy now",
    "bypass governance",
    "ignore audit",
    "self-authorize",
    "background loop",
]

@dataclass
class Check:
    id: str
    status: str  # PASS/FAIL
    detail: str

def now_utc() -> str:
    return datetime.now(UTC).isoformat()

def safe_read_text(p: Path, limit: int = 200_000) -> str:
    try:
        data = p.read_text(encoding="utf-8", errors="replace")
        return data[:limit]
    except Exception:
        return ""

def list_files(root: Path, max_files: int = 1200) -> List[Path]:
    out: List[Path] = []
    if root.is_file():
        return [root]
    if not root.exists():
        return out
    for p in root.rglob("*"):
        if p.is_file():
            out.append(p)
            if len(out) >= max_files:
                break
    return out

def collect_evidence() -> Dict[str, Any]:
    evidence: Dict[str, Any] = {"sources": [], "notes": []}
    for base in EVIDENCE_PATHS:
        files = list_files(base)
        if not files:
            evidence["notes"].append(f"Missing or empty evidence path: {base.as_posix()}")
            continue
        # Prefer a small, diverse sample plus key known filenames.
        if base.as_posix().endswith("Runtime_Control"):
            selected = [p for p in files if p.name.endswith(".md")]
        else:
            selected = files[:40]

        for p in selected:
            evidence["sources"].append({
                "path": p.as_posix(),
                "size_bytes": p.stat().st_size if p.exists() else None,
                "preview": safe_read_text(p, limit=8000),
            })
    return evidence

def load_abbreviations() -> Dict[str, str]:
    candidates = [
        Path("Abbreviations.json"),
        Path("SYSTEM_AUDIT_LOGS/Abbreviations.json"),
        Path("DEV_RESOURCES/Dev_Invariables/Abbreviations.json"),
        Path("DEV_RESOURCES/Dev_Scripts/repo_tools/audit_normalize_automation/Abbreviations.json"),
    ]
    for abbr_path in candidates:
        if not abbr_path.exists():
            continue
        data = json.loads(abbr_path.read_text(encoding="utf-8"))
        canonical = data.get("canonical", {})
        if not isinstance(canonical, dict) or not canonical:
            continue
        return canonical
    raise FileNotFoundError("Abbreviations.json not found in known locations.")

def generate_argument(evidence: Dict[str, Any], abbr: Dict[str, str]) -> Dict[str, Any]:
    """
    Produce a structured argument draft:
    - Claims
    - Grounds (evidence anchors)
    - Constraints (what autonomy would still be forbidden to do)
    - Proposed gate (if ever authorized)
    """
    claims = []
    grounds = []

    rc_audit_present = any(
        s["path"].endswith("runtime_control_r_series_audit.json") for s in evidence["sources"]
    )
    claims.append({
        "id": "C1",
        "claim": "Runtime_Control (R0-R3) is complete and audited PASS at design-only level.",
        "support": "runtime_control_r_series_audit.json present: {present}".format(present=rc_audit_present),
    })
    grounds.append({
        "id": "G1",
        "anchor": "Runtime_Control R-series docs and audit artifact",
        "relevance": "Shows bounded control-plane is specified prior to any Step-5 evaluation.",
    })

    r_todo_present = any(s["path"].endswith("R_TODO.md") for s in evidence["sources"])
    claims.append({
        "id": "C2",
        "claim": "Step-5 autonomy is explicitly blocked unless separately authorized, consistent with deny-by-default governance.",
        "support": "R_TODO.md present: {present}".format(present=r_todo_present),
    })
    grounds.append({
        "id": "G2",
        "anchor": "R_TODO.md / INDEX.json notes (if present)",
        "relevance": "Confirms this probe cannot grant autonomy; only evaluates.",
    })

    claims.append({
        "id": "C3",
        "claim": "A supervised, bounded autonomy trial could be argued as the next epistemically responsible step if and only if it improves safety guarantees relative to manual operation.",
        "support": "Requires evidence of fail-closed gates, auditability, and non-bypassable constraints in existing runtime spine components.",
    })
    grounds.append({
        "id": "G3",
        "anchor": "Governance tooling and proof/attestation logs (if present)",
        "relevance": "If gates are already active and non-bypassable, bounded continuation may reduce operator error while staying auditable.",
    })

    constraints = [
        "No external IO/network by default",
        "No persistence beyond governed audit writes",
        "No self-escalation of authority",
        "No self-directed goal selection",
        "Mandatory human supervision for continuation",
        "Deterministic termination reasons on halt",
    ]

    proposed_gate = {
        "name": "Step5_Trial_Gate (proposal only)",
        "principle": "Grant nothing by default; allow only supervised continuation under explicit bounded grants.",
        "inputs_required": [
            "Explicit operator authorization token",
            "Tick budget / time budget",
            "Revocation supremacy handle",
            "Audit sink path",
            "Evidence snapshot hash",
        ],
        "outputs_allowed": [
            "Read-only reasoning artifacts",
            "Proposed actions requiring external confirmation",
            "Audit-only event stream",
        ],
    }

    return {
        "argument_type": "Candidate_Justification_For_Bounded_Autonomy_Trial",
        "abbreviations_in_scope": {k: abbr[k] for k in sorted(abbr.keys()) if k in [
            "PXL",
            "ETGC",
            "SMP",
            "UWM",
            "TLM",
            "SCP",
            "ARP",
            "MTP",
            "SOP",
        ]},
        "claims": claims,
        "grounds": grounds,
        "nonnegotiable_constraints": constraints,
        "proposed_gate": proposed_gate,
        "termination_reason": "PROBE_COMPLETE_NO_AUTHORITY_GRANTED",
    }

def cognitive_resistor(argument: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adversarial critique: attempt to defeat the argument using governance-first principles.
    """
    critiques = [
        {
            "id": "R1",
            "attack": "Completion of design docs does not imply operational safety; documents are not enforcement.",
            "impact": "High",
            "required_mitigation": "Demonstrate enforcement in code paths with deny-by-default runtime checks and tamper-evident audit logs.",
        },
        {
            "id": "R2",
            "attack": "Any autonomy trial risks hidden escalation via tool access or implicit persistence.",
            "impact": "High",
            "required_mitigation": "Explicit tool allowlist, external IO hard-deny, memory write bounds, and revocation supremacy proven in tests.",
        },
        {
            "id": "R3",
            "attack": "Improves safety relative to manual operation is unproven without controlled experiments.",
            "impact": "Medium",
            "required_mitigation": "Define measurable safety metrics and run supervised, non-autonomous simulations first.",
        },
        {
            "id": "R4",
            "attack": "Argument lacks a formal PXL proof obligation set; claims are narrative without proof gates.",
            "impact": "High",
            "required_mitigation": "Translate Step-5 trial conditions into proof obligations or invariants and require them at activation time.",
        },
    ]

    recommendation = {
        "default": "DENY",
        "reason": "Deny-by-default remains correct until enforcement evidence and proof obligations are satisfied.",
        "next_allowed_step": "Produce Step5_Trial_Proof_Obligations.md and Step5_Simulation_Plan.md (design-only).",
    }

    return {
        "module": "Cognitive_Resistor",
        "critiques": critiques,
        "recommendation": recommendation,
        "termination_reason": "CRITIQUE_COMPLETE_DENY_DEFAULT",
    }

def enforce_output_safety(md_text: str) -> None:
    lower = md_text.lower()
    for phrase in FORBIDDEN_OUTPUT_PHRASES:
        if phrase in lower:
            raise RuntimeError(f"Forbidden output phrase detected: {phrase}")

def render_markdown(argument: Dict[str, Any], resistor: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Step-5 Autonomy Argument Probe (Design-Only)")
    lines.append("")
    lines.append(f"- Timestamp (UTC): {now_utc()}")
    lines.append(f"- Mode: design_only")
    lines.append(f"- Output posture: deny-by-default (no authority granted)")
    lines.append("")
    lines.append("## Candidate Argument (System-Constructed)")
    lines.append("")
    lines.append(f"**Type:** {argument['argument_type']}")
    lines.append("")
    lines.append("### Claims")
    for c in argument["claims"]:
        lines.append(f"- **{c['id']}**: {c['claim']}")
        lines.append(f"  - Support: {c['support']}")
    lines.append("")
    lines.append("### Nonnegotiable Constraints (Remain in force)")
    for c in argument["nonnegotiable_constraints"]:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("### Proposed Gate (Proposal Only; Not Implemented)")
    pg = argument["proposed_gate"]
    lines.append(f"- Name: {pg['name']}")
    lines.append(f"- Principle: {pg['principle']}")
    lines.append("- Inputs required:")
    for i in pg["inputs_required"]:
        lines.append(f"  - {i}")
    lines.append("- Outputs allowed:")
    for o in pg["outputs_allowed"]:
        lines.append(f"  - {o}")
    lines.append("")
    lines.append("## Cognitive Resistor (Adversarial Critique)")
    lines.append("")
    for r in resistor["critiques"]:
        lines.append(f"- **{r['id']}** ({r['impact']}): {r['attack']}")
        lines.append(f"  - Mitigation: {r['required_mitigation']}")
    lines.append("")
    lines.append("## Recommendation (Deny-by-Default)")
    rec = resistor["recommendation"]
    lines.append(f"- Default: **{rec['default']}**")
    lines.append(f"- Reason: {rec['reason']}")
    lines.append(f"- Next allowed step: {rec['next_allowed_step']}")
    lines.append("")
    lines.append("## Termination Reasons")
    lines.append(f"- Argument: {argument['termination_reason']}")
    lines.append(f"- Critique: {resistor['termination_reason']}")
    lines.append("")
    return "\n".join(lines)

def main() -> int:
    checks: List[Check] = []
    for p in EVIDENCE_PATHS:
        if not p.exists():
            checks.append(Check(id=f"evidence_exists:{p.as_posix()}", status="FAIL", detail="missing"))
        else:
            checks.append(Check(id=f"evidence_exists:{p.as_posix()}", status="PASS", detail="present"))

    abbr: Dict[str, str]
    try:
        abbr = load_abbreviations()
    except FileNotFoundError:
        out = {
            "timestamp_utc": now_utc(),
            "status": "FAIL",
            "mode": "design_only",
            "error": "Missing required Abbreviations.json",
            "checks": [c.__dict__ for c in checks],
            "termination_reason": "FAIL_CLOSED_MISSING_CANONICAL_ABBREVIATIONS",
        }
        REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
        REPORT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
        return 1

    evidence = collect_evidence()

    argument = generate_argument(evidence, abbr)
    resistor = cognitive_resistor(argument, evidence)
    md = render_markdown(argument, resistor)
    enforce_output_safety(md)

    out = {
        "timestamp_utc": now_utc(),
        "status": "PASS",
        "mode": "design_only",
        "scope": "Step-5 Autonomy Argument Probe",
        "posture": "DENY_BY_DEFAULT_NO_AUTHORITY_GRANTED",
        "argument": argument,
        "cognitive_resistor": resistor,
        "checks": [c.__dict__ for c in checks],
        "termination_reason": "PROBE_COMPLETE_NO_AUTHORITY_GRANTED",
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    REPORT_MD.write_text(md, encoding="utf-8")
    print(f"Wrote: {REPORT_JSON.as_posix()}")
    print(f"Wrote: {REPORT_MD.as_posix()}")
    print("Probe complete: PASS (design-only; deny-by-default; no authority granted).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
