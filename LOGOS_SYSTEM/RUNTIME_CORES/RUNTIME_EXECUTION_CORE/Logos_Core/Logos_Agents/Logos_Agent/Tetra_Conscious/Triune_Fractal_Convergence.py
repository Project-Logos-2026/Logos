# FILE: Triune_Fractal_Convergence.py
# PATH: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Logos_Agent/Tetra_Conscious/Triune_Fractal_Convergence.py
# PROJECT: LOGOS System
# PHASE: Phase-G
# STEP: TRI-CORE Nexus Convergence
# STATUS: GOVERNED
# CLASSIFICATION: logos_agent_cognitive_synthesis
# GOVERNANCE: ["Phase_G_Execution_Contract", "Runtime_Module_Header_Contract", "Trinitarian_Logic_Core_Contract", "Global_Bijective_Recursion_Core_Contract"]
# ROLE: Tetrahedral convergence of I1/I2/I3 triune fractal summaries at Logos Agent
# ORDERING GUARANTEE: ["LOGOS_AGENT_READY", "AGENT_ORCHESTRATION_AND_PROTOCOL_BINDING"]
# PROHIBITIONS: ["semantic_mutation", "state_mutation", "authority_escalation", "protocol_execution", "agent_impersonation", "truth_generation"]
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
module_name: Triune_Fractal_Convergence
runtime_layer: logos_agent_synthesis
role: Tetrahedral convergence of agent-local TRI-CORE outputs
responsibility: Collects I1/I2/I3 TriuneSummaries, validates structural completeness, aligns to tetrahedral faces, and produces a single synthesized cognition artifact for Logos Agent.
agent_binding: Logos_Agent
protocol_binding: None (synthesis only)
runtime_classification: cognitive_synthesis
boot_phase: Phase-G
expected_imports: [Common.Recursive_Cognition.Triune_Sierpinski_Core]
provides: [converge_triune_fractals, TriuneConvergenceResult]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Missing or structurally invalid summaries halt convergence. No partial synthesis propagates."
rewrite_provenance:
  source: TRI_CORE_Package/Nexus_Triune_Fractal_Convergence.py
  rewrite_phase: TRI-CORE_Build
  rewrite_timestamp: 2026-02-10T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from Cognition_Normalized.Triune_Sierpinski_Core import TriuneSummary


# =============================================================================
# CONVERGENCE RESULT
# =============================================================================

@dataclass(frozen=True)
class TriuneConvergenceResult:
    status: str
    tetrahedral_faces: Dict[str, TriuneSummary]
    synthesis: Dict[str, Any]
    convergence_hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# VALIDATION
# =============================================================================

_REQUIRED_AGENTS: Tuple[str, ...] = ("I1", "I2", "I3")


class ConvergenceValidationError(Exception):
    pass


def _validate_summary(summary: Any, expected_agent: str) -> TriuneSummary:
    """Validate that a summary is structurally sound and belongs to the expected agent."""
    if not isinstance(summary, TriuneSummary):
        raise ConvergenceValidationError(
            f"Expected TriuneSummary for {expected_agent}, got {type(summary).__name__}"
        )

    if summary.agent_id != expected_agent:
        raise ConvergenceValidationError(
            f"Agent ID mismatch: expected {expected_agent}, got {summary.agent_id}"
        )

    if summary.total_triangles < 1:
        raise ConvergenceValidationError(
            f"Summary for {expected_agent} contains no triangles"
        )

    if not summary.convergence_hash:
        raise ConvergenceValidationError(
            f"Summary for {expected_agent} has no convergence hash"
        )

    return summary


# =============================================================================
# TETRAHEDRAL ALIGNMENT
# =============================================================================

def _align_to_tetrahedron(
    i1: TriuneSummary,
    i2: TriuneSummary,
    i3: TriuneSummary,
) -> Dict[str, Any]:
    """Align three triangular summaries as faces of a tetrahedron.

    The Sierpinski tetrahedron is composed of:
    - Face I1 (structural): epistemic grounding, invariant integrity
    - Face I2 (semantic): meaning stability, abstraction coherence
    - Face I3 (inferential): dependency completeness, consequence boundedness
    - Base: Logos Agent synthesis plane

    This function computes alignment metrics without mutating any summary.
    """
    depth_spread = (
        i1.max_depth_reached,
        i2.max_depth_reached,
        i3.max_depth_reached,
    )
    depth_mean = sum(depth_spread) / 3.0
    depth_variance = sum((d - depth_mean) ** 2 for d in depth_spread) / 3.0

    triangle_counts = (
        i1.total_triangles,
        i2.total_triangles,
        i3.total_triangles,
    )
    total_triangles = sum(triangle_counts)

    terminal_counts = (
        len(i1.terminal_payloads),
        len(i2.terminal_payloads),
        len(i3.terminal_payloads),
    )

    raw_balance = min(triangle_counts) / max(triangle_counts) if max(triangle_counts) > 0 else 0.0

    depth_normalized = tuple(
        tc / (3 ** d) if d > 0 else tc
        for tc, d in zip(triangle_counts, depth_spread)
    )
    dn_max = max(depth_normalized) if depth_normalized else 1.0
    normalized_balance = min(depth_normalized) / dn_max if dn_max > 0 else 0.0

    return {
        "depth_spread": depth_spread,
        "depth_mean": round(depth_mean, 4),
        "depth_variance": round(depth_variance, 4),
        "triangle_counts": triangle_counts,
        "total_triangles": total_triangles,
        "terminal_counts": terminal_counts,
        "raw_balance_ratio": round(raw_balance, 4),
        "normalized_balance_ratio": round(normalized_balance, 4),
        "tetrahedral_coherent": depth_variance < 6.0 and normalized_balance > 0.25,
    }


# =============================================================================
# SYNTHESIS
# =============================================================================

def _synthesize(
    i1: TriuneSummary,
    i2: TriuneSummary,
    i3: TriuneSummary,
    alignment: Dict[str, Any],
) -> Dict[str, Any]:
    """Produce a synthesis artifact from aligned summaries.

    This does not generate new truth. It collects and structures the
    analytical outputs from all three agents into a single artifact
    suitable for Logos Agent downstream processing.
    """
    structural_findings = {
        "apex_trace_length": len(i1.apex_trace),
        "terminal_count": len(i1.terminal_payloads),
        "depth_reached": i1.max_depth_reached,
        "convergence_hash": i1.convergence_hash,
    }

    semantic_findings = {
        "apex_trace_length": len(i2.apex_trace),
        "terminal_count": len(i2.terminal_payloads),
        "depth_reached": i2.max_depth_reached,
        "convergence_hash": i2.convergence_hash,
    }

    inferential_findings = {
        "apex_trace_length": len(i3.apex_trace),
        "terminal_count": len(i3.terminal_payloads),
        "depth_reached": i3.max_depth_reached,
        "convergence_hash": i3.convergence_hash,
    }

    return {
        "structural": structural_findings,
        "semantic": semantic_findings,
        "inferential": inferential_findings,
        "alignment": alignment,
        "synthesis_type": "triune_tetrahedral_convergence",
        "mutative": False,
        "authoritative": False,
    }


def _convergence_hash(i1: TriuneSummary, i2: TriuneSummary, i3: TriuneSummary) -> str:
    """Produce a deterministic convergence identifier for the triune result."""
    raw = f"{i1.convergence_hash}:{i2.convergence_hash}:{i3.convergence_hash}"
    h = 0
    for ch in raw:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return f"LOGOS_TRICONV_{h:08x}"


# =============================================================================
# PUBLIC INTERFACE
# =============================================================================

def converge_triune_fractals(
    *,
    i1_summary: TriuneSummary,
    i2_summary: TriuneSummary,
    i3_summary: TriuneSummary,
) -> TriuneConvergenceResult:
    """Converge three agent TRI-CORE summaries into a tetrahedral synthesis.

    This is the single entry point for Logos Agent cognitive convergence
    of fractal analysis results. It validates all inputs, aligns to
    tetrahedral geometry, and produces a non-authoritative synthesis artifact.

    On any validation failure, raises ConvergenceValidationError (fail-closed).
    """
    v_i1 = _validate_summary(i1_summary, "I1")
    v_i2 = _validate_summary(i2_summary, "I2")
    v_i3 = _validate_summary(i3_summary, "I3")

    alignment = _align_to_tetrahedron(v_i1, v_i2, v_i3)
    synthesis = _synthesize(v_i1, v_i2, v_i3, alignment)
    conv_hash = _convergence_hash(v_i1, v_i2, v_i3)

    return TriuneConvergenceResult(
        status="converged" if alignment["tetrahedral_coherent"] else "degraded",
        tetrahedral_faces={
            "I1_structural": v_i1,
            "I2_semantic": v_i2,
            "I3_inferential": v_i3,
        },
        synthesis=synthesis,
        convergence_hash=conv_hash,
        metadata={
            "geometry": "sierpinski_tetrahedron",
            "faces": 3,
            "base": "LOGOS_AGENT",
            "governance_authority": "LOGOS_PROTOCOL",
            "mutation": False,
            "predictive": False,
        },
    )
