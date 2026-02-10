# FILE: I2_Triune_Fractal_Binding.py
# PATH: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/I2_Agent/I2_Agent_Core/I2_Triune_Fractal_Binding.py
# PROJECT: LOGOS System
# PHASE: Phase-G
# STEP: TRI-CORE Agent Binding (I2)
# STATUS: GOVERNED
# CLASSIFICATION: agent_cognitive_binding
# GOVERNANCE: ["Phase_G_Execution_Contract", "Runtime_Module_Header_Contract", "Modifier_Binding_Contract"]
# ROLE: I2 semantic recursive analysis binding — MTP-aligned, pre-execution
# ORDERING GUARANTEE: ["LOGOS_AGENT_READY", "AGENT_ORCHESTRATION_AND_PROTOCOL_BINDING"]
# PROHIBITIONS: ["semantic_mutation", "state_mutation", "language_generation", "prediction", "protocol_execution", "truth_generation"]
# FAILURE SEMANTICS: FAIL_CLOSED
from __future__ import annotations

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: I2_Triune_Fractal_Binding
runtime_layer: agent_cognitive_binding
role: I2 semantic recursion binding for TRI-CORE
responsibility: Configures TriuneSierpinskiCore with I2-specific semantic projection operators targeting abstraction, explanation stability, and primitive coverage.
agent_binding: I2
protocol_binding: MTP (read-only alignment)
runtime_classification: cognitive_binding
boot_phase: Phase-G
expected_imports: [Common.Recursive_Cognition.Triune_Sierpinski_Core]
provides: [i2_analyze]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Transform failures produce terminal vertices. No partial semantic claims propagate."
rewrite_provenance:
  source: TRI_CORE_Package/I2_TRICORE_Binding.py
  rewrite_phase: TRI-CORE_Build
  rewrite_timestamp: 2026-02-10T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from typing import Any, Dict, List, Tuple

from Cognition_Normalized.Triune_Sierpinski_Core import (
    TriuneSierpinskiCore,
    TriuneSummary,
)


# =============================================================================
# SEMANTIC PRIMITIVE CATEGORIES (SP-01 through SP-12)
# =============================================================================

_SEMANTIC_PRIMITIVES: Tuple[str, ...] = (
    "SP-01_assertion",
    "SP-02_distinction",
    "SP-03_negation",
    "SP-04_constraint",
    "SP-05_dependency",
    "SP-06_evaluation",
    "SP-07_uncertainty",
    "SP-08_unknown",
    "SP-09_commitment",
    "SP-10_relation",
    "SP-11_scope",
    "SP-12_grounding",
)

# =============================================================================
# SEMANTIC STATE CONDITIONS (SSC-01 through SSC-04)
# =============================================================================

_STATE_CONDITIONS: Tuple[str, ...] = (
    "SSC-01_complete",
    "SSC-02_partial",
    "SSC-03_unresolved",
    "SSC-04_inadmissible",
)

# =============================================================================
# SEMANTIC ANALYSIS DIMENSIONS
# =============================================================================

_ANALYSIS_DIMENSIONS: Tuple[Tuple[str, ...], ...] = (
    ("abstraction_depth", "specificity_gradient", "refinement_chain_length"),
    ("explanation_stability", "meaning_preservation", "drift_detection"),
    ("primitive_coverage", "relation_coherence", "state_classification"),
)


# =============================================================================
# I2 TRANSFORM OPERATOR
# =============================================================================

def _i2_semantic_transform(payload: Any, depth: int, agent_id: str) -> Tuple[Any, Any, Any]:
    """Decompose payload along semantic analysis dimensions.

    Depth 0: Partition into abstraction analysis, explanation stability, coverage analysis.
    Depth 1+: Each sub-partition refines within its dimension.

    The transform never mutates the original payload. It produces three read-only
    semantic projections representing different meaning-layer lenses.
    """
    dim_index = depth % len(_ANALYSIS_DIMENSIONS)
    current_dim = _ANALYSIS_DIMENSIONS[dim_index]

    if isinstance(payload, dict):
        raw = payload
    else:
        raw = {"_opaque_payload": payload}

    classification = raw.get("classification", {})
    triadic = raw.get("triadic_scores", {})
    metadata_header = raw.get("metadata_header", {})
    epistemic_status = metadata_header.get("epistemic_status", "PROVISIONAL")
    classification_state = raw.get("classification_state", None)

    present_primitives = _detect_primitive_coverage(raw)
    state_condition = _assess_state_condition(raw, present_primitives)

    apex_projection = {
        "source_agent": agent_id,
        "depth": depth,
        "dimension": current_dim[0] if len(current_dim) > 0 else "abstraction",
        "abstraction_level": depth,
        "epistemic_status": epistemic_status,
        "primitive_subset": present_primitives[:4],
        "triadic_context": {k: v for k, v in triadic.items() if k in ("existence", "truth")},
        "state_condition": state_condition,
        "semantic_marker": f"apex_d{depth}",
    }

    left_projection = {
        "source_agent": agent_id,
        "depth": depth,
        "dimension": current_dim[1] if len(current_dim) > 1 else "stability",
        "abstraction_level": depth,
        "classification_domain": classification.get("domain", "unknown"),
        "bridge_passed": raw.get("bridge_passed", None),
        "primitive_subset": present_primitives[4:8],
        "triadic_context": {k: v for k, v in triadic.items() if k in ("goodness", "conservation")},
        "semantic_marker": f"left_d{depth}",
    }

    right_projection = {
        "source_agent": agent_id,
        "depth": depth,
        "dimension": current_dim[2] if len(current_dim) > 2 else "coverage",
        "abstraction_level": depth,
        "primitive_coverage_ratio": len(present_primitives) / len(_SEMANTIC_PRIMITIVES),
        "primitive_subset": present_primitives[8:],
        "missing_primitives": [p for p in _SEMANTIC_PRIMITIVES if p not in present_primitives],
        "triadic_context": {k: v for k, v in triadic.items() if k in ("feasibility", "coherence")},
        "semantic_marker": f"right_d{depth}",
    }

    return apex_projection, left_projection, right_projection


# =============================================================================
# SEMANTIC DETECTION HELPERS
# =============================================================================

def _detect_primitive_coverage(raw: Dict[str, Any]) -> List[str]:
    """Determine which semantic primitives are evidenced in the payload."""
    present: List[str] = []

    if raw.get("classification") or raw.get("analysis"):
        present.append("SP-01_assertion")
    if raw.get("violations"):
        present.append("SP-02_distinction")
        present.append("SP-03_negation")
    if raw.get("classification", {}).get("constraints") or raw.get("bridge_passed") is not None:
        present.append("SP-04_constraint")
    if raw.get("triadic_scores"):
        present.append("SP-06_evaluation")
    if raw.get("classification_state") in (None, "PROVISIONAL"):
        present.append("SP-07_uncertainty")
    if raw.get("metadata_header", {}).get("epistemic_status") == "PROVISIONAL":
        present.append("SP-08_unknown")
    if raw.get("final_decision"):
        present.append("SP-09_commitment")
    if raw.get("route_to"):
        present.append("SP-10_relation")
    if raw.get("triage_vector"):
        present.append("SP-12_grounding")

    return present


def _assess_state_condition(raw: Dict[str, Any], present: List[str]) -> str:
    """Classify the semantic state condition of the payload."""
    violations = raw.get("violations", [])
    bridge = raw.get("bridge_passed", None)

    if bridge is False or violations:
        if any("invariant" in str(v).lower() for v in violations):
            return "SSC-04_inadmissible"

    coverage = len(present) / len(_SEMANTIC_PRIMITIVES)
    if coverage >= 0.75 and not violations:
        return "SSC-01_complete"

    unknowns = [p for p in present if "unknown" in p.lower() or "uncertainty" in p.lower()]
    if unknowns:
        return "SSC-03_unresolved"

    return "SSC-02_partial"


# =============================================================================
# I2 TERMINATION PREDICATE
# =============================================================================

def _i2_termination_predicate(payload: Any, depth: int) -> bool:
    """Terminate when semantic analysis reaches stable abstraction.

    I2 allows moderate depth (4) for explanation shaping.
    Terminates early if coverage is high and no meaning drift is detected.
    """
    if depth >= 4:
        return True

    if isinstance(payload, dict):
        coverage = payload.get("primitive_coverage_ratio", 0.0)
        if isinstance(coverage, (int, float)) and coverage >= 0.8:
            return True

        state = payload.get("state_condition", "")
        if state == "SSC-01_complete":
            return True

    return False


# =============================================================================
# I2 TRI-CORE INSTANCE
# =============================================================================

_I2_TRICORE = TriuneSierpinskiCore(
    agent_id="I2",
    max_depth=5,
    transform_operator=_i2_semantic_transform,
    termination_predicate=_i2_termination_predicate,
)


# =============================================================================
# PUBLIC INTERFACE
# =============================================================================

def i2_analyze(payload: Any) -> TriuneSummary:
    """Execute I2 semantic recursive analysis over a meaning-normalized payload.

    Expected input: MTP intake-normalized packet fields as dict (read-only).
    Output: TriuneSummary for attachment to payload metadata.
    """
    return _I2_TRICORE.analyze(payload)
