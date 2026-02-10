# FILE: I3_Triune_Fractal_Binding.py
# PATH: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/I3_Agent/_core/I3_Triune_Fractal_Binding.py
# PROJECT: LOGOS System
# PHASE: Phase-G
# STEP: TRI-CORE Agent Binding (I3)
# STATUS: GOVERNED
# CLASSIFICATION: agent_cognitive_binding
# GOVERNANCE: ["Phase_G_Execution_Contract", "Runtime_Module_Header_Contract", "Global_Bijective_Recursion_Core_Contract"]
# ROLE: I3 inferential recursive analysis binding — ARP-aligned, pre-execution
# ORDERING GUARANTEE: ["LOGOS_AGENT_READY", "AGENT_ORCHESTRATION_AND_PROTOCOL_BINDING"]
# PROHIBITIONS: ["semantic_mutation", "state_mutation", "authoritative_conclusion", "autonomous_goal_selection", "prediction", "protocol_execution"]
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
module_name: I3_Triune_Fractal_Binding
runtime_layer: agent_cognitive_binding
role: I3 inferential recursion binding for TRI-CORE
responsibility: Configures TriuneSierpinskiCore with I3-specific inferential expansion operators targeting dependency unfolding, consequence space, and constraint propagation.
agent_binding: I3
protocol_binding: ARP (read-only alignment)
runtime_classification: cognitive_binding
boot_phase: Phase-G
expected_imports: [Common.Recursive_Cognition.Triune_Sierpinski_Core]
provides: [i3_analyze]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Transform failures produce terminal vertices. No partial inferential claims propagate."
rewrite_provenance:
  source: TRI_CORE_Package/I3_TRICORE_Binding.py
  rewrite_phase: TRI-CORE_Build
  rewrite_timestamp: 2026-02-10T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from typing import Any, Dict, List, Tuple

from Common.Recursive_Cognition.Triune_Sierpinski_Core import (
    TriuneSierpinskiCore,
    TriuneSummary,
)


# =============================================================================
# INFERENTIAL EXPANSION AXES
# =============================================================================

_EXPANSION_AXES: Tuple[Tuple[str, ...], ...] = (
    ("dependency_unfolding", "prerequisite_chain", "dependency_depth"),
    ("consequence_space", "entailment_reach", "implication_fan"),
    ("constraint_propagation", "scope_boundary_effects", "exclusion_cascade"),
)

# =============================================================================
# SEMANTIC RELATION SUBSET (inference-relevant)
# =============================================================================

_INFERENCE_RELATIONS: Tuple[str, ...] = (
    "SR-02_entails",
    "SR-03_constrains",
    "SR-04_depends_on",
    "SR-05_excludes",
    "SR-07_refines",
    "SR-08_abstracts",
)


# =============================================================================
# I3 TRANSFORM OPERATOR
# =============================================================================

def _i3_inferential_transform(payload: Any, depth: int, agent_id: str) -> Tuple[Any, Any, Any]:
    """Decompose payload along inferential expansion axes.

    Depth 0: Partition into dependency analysis, consequence analysis, constraint analysis.
    Depth 1+: Each sub-partition expands within its axis, unfolding
    further dependency chains, broader consequence spaces, and deeper constraint propagation.

    The transform never mutates the original payload. It produces three read-only
    inferential projections representing different reasoning-space lenses.
    """
    axis_index = depth % len(_EXPANSION_AXES)
    current_axis = _EXPANSION_AXES[axis_index]

    if isinstance(payload, dict):
        raw = payload
    else:
        raw = {"_opaque_payload": payload}

    triadic = raw.get("triadic_scores", {})
    violations = raw.get("violations", [])
    analysis = raw.get("analysis", {})
    classification = raw.get("classification", {})

    dependency_signals = _extract_dependency_signals(raw)
    consequence_signals = _extract_consequence_signals(raw)
    constraint_signals = _extract_constraint_signals(raw)

    apex_projection = {
        "source_agent": agent_id,
        "depth": depth,
        "axis": current_axis[0] if current_axis else "dependency_unfolding",
        "inference_mode": "dependency",
        "dependency_chain": dependency_signals,
        "chain_depth": len(dependency_signals),
        "unfolding_complete": len(dependency_signals) == 0,
        "triadic_context": {k: v for k, v in triadic.items() if k in ("coherence", "truth")},
        "active_relations": [r for r in _INFERENCE_RELATIONS if "depends" in r or "entails" in r],
        "inferential_marker": f"apex_d{depth}",
    }

    left_projection = {
        "source_agent": agent_id,
        "depth": depth,
        "axis": current_axis[1] if len(current_axis) > 1 else "consequence_space",
        "inference_mode": "consequence",
        "consequence_signals": consequence_signals,
        "entailment_reach": len(consequence_signals),
        "implication_bounded": depth >= 3,
        "triadic_context": {k: v for k, v in triadic.items() if k in ("existence", "goodness")},
        "active_relations": [r for r in _INFERENCE_RELATIONS if "entails" in r or "refines" in r or "abstracts" in r],
        "inferential_marker": f"left_d{depth}",
    }

    right_projection = {
        "source_agent": agent_id,
        "depth": depth,
        "axis": current_axis[2] if len(current_axis) > 2 else "constraint_propagation",
        "inference_mode": "constraint",
        "constraint_signals": constraint_signals,
        "propagation_depth": depth,
        "exclusion_detected": any("exclusion" in str(v).lower() or "violation" in str(v).lower() for v in violations),
        "triadic_context": {k: v for k, v in triadic.items() if k in ("conservation", "feasibility")},
        "active_relations": [r for r in _INFERENCE_RELATIONS if "constrains" in r or "excludes" in r],
        "inferential_marker": f"right_d{depth}",
    }

    return apex_projection, left_projection, right_projection


# =============================================================================
# SIGNAL EXTRACTION HELPERS
# =============================================================================

def _extract_dependency_signals(raw: Dict[str, Any]) -> List[str]:
    """Extract dependency-relevant signals from the payload."""
    signals: List[str] = []

    analysis = raw.get("analysis", {})
    if isinstance(analysis, dict):
        domains = analysis.get("selected_iel_domains", analysis.get("selected_domains", []))
        if isinstance(domains, list):
            for d in domains:
                signals.append(f"domain_dep:{d}")

    if raw.get("bridge_passed") is False:
        signals.append("bridge_dependency_unmet")

    violations = raw.get("violations", [])
    for v in violations:
        if "dependency" in str(v).lower() or "prerequisite" in str(v).lower():
            signals.append(f"violation_dep:{v}")

    chain = raw.get("dependency_chain", [])
    if isinstance(chain, list):
        signals.extend(chain)

    return signals


def _extract_consequence_signals(raw: Dict[str, Any]) -> List[str]:
    """Extract consequence-space signals from the payload."""
    signals: List[str] = []

    final = raw.get("final_decision", "")
    if final:
        signals.append(f"decision_consequence:{final}")

    route = raw.get("route_to", "")
    if route:
        signals.append(f"routing_consequence:{route}")

    triadic = raw.get("triadic_scores", {})
    for k, v in triadic.items():
        if isinstance(v, (int, float)) and v < 0.5:
            signals.append(f"low_triadic:{k}={v}")

    consequence_signals = raw.get("consequence_signals", [])
    if isinstance(consequence_signals, list):
        signals.extend(consequence_signals)

    return signals


def _extract_constraint_signals(raw: Dict[str, Any]) -> List[str]:
    """Extract constraint-propagation signals from the payload."""
    signals: List[str] = []

    classification = raw.get("classification", {})
    if isinstance(classification, dict):
        constraints = classification.get("constraints", [])
        if isinstance(constraints, list):
            for c in constraints:
                signals.append(f"constraint:{c}")

    violations = raw.get("violations", [])
    for v in violations:
        if "constraint" in str(v).lower() or "scope" in str(v).lower() or "bridge" in str(v).lower():
            signals.append(f"constraint_violation:{v}")

    triage = raw.get("triage_vector", {})
    if isinstance(triage, dict) and triage.get("overlay_type") == "hard":
        signals.append("hard_triage_constraint")

    constraint_signals = raw.get("constraint_signals", [])
    if isinstance(constraint_signals, list):
        signals.extend(constraint_signals)

    return signals


# =============================================================================
# I3 TERMINATION PREDICATE
# =============================================================================

def _i3_termination_predicate(payload: Any, depth: int) -> bool:
    """Terminate when inferential expansion exhausts productive unfolding.

    I3 allows deeper recursion (5) for consequence exploration.
    Terminates early if all dependency chains are fully unfolded and
    constraint propagation has stabilized.
    """
    if depth >= 5:
        return True

    if isinstance(payload, dict):
        unfolding_complete = payload.get("unfolding_complete", False)
        implication_bounded = payload.get("implication_bounded", False)
        if unfolding_complete and implication_bounded:
            return True

        chain_depth = payload.get("chain_depth", -1)
        if isinstance(chain_depth, int) and chain_depth == 0:
            entailment_reach = payload.get("entailment_reach", -1)
            if isinstance(entailment_reach, int) and entailment_reach == 0:
                return True

    return False


# =============================================================================
# I3 TRI-CORE INSTANCE
# =============================================================================

_I3_TRICORE = TriuneSierpinskiCore(
    agent_id="I3",
    max_depth=6,
    transform_operator=_i3_inferential_transform,
    termination_predicate=_i3_termination_predicate,
)


# =============================================================================
# PUBLIC INTERFACE
# =============================================================================

def i3_analyze(payload: Any) -> TriuneSummary:
    """Execute I3 inferential recursive analysis over an ARP inference seed.

    Expected input: ARP inference seed fields as dict (read-only).
    Output: TriuneSummary for attachment to payload metadata.
    """
    return _I3_TRICORE.analyze(payload)
