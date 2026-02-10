# FILE: Triune_Sierpinski_Core.py
# PATH: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Agent_Resources/Cognition_Normalized/Triune_Sierpinski_Core.py
# PROJECT: LOGOS System
# PHASE: Phase-G
# STEP: TRI-CORE Shared Substrate
# STATUS: GOVERNED
# CLASSIFICATION: agent_shared_cognitive_substrate
# GOVERNANCE: ["Phase_G_Execution_Contract", "Runtime_Module_Header_Contract", "Agent_Activation_Gate_Contract"]
# ROLE: Bounded Sierpinski-triangle recursive analysis core shared by I1, I2, I3
# ORDERING GUARANTEE: ["LOGOS_AGENT_READY", "AGENT_ORCHESTRATION_AND_PROTOCOL_BINDING"]
# PROHIBITIONS: ["semantic_mutation", "state_mutation", "authority_escalation", "prediction", "language_generation", "protocol_execution"]
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
module_name: Triune_Sierpinski_Core
runtime_layer: agent_cognitive_substrate
role: Shared bounded recursive analysis engine
responsibility: Provides agent-local Sierpinski triangle fractal recursion for pre-execution analysis.
agent_binding: None (shared by I1, I2, I3)
protocol_binding: None
runtime_classification: cognitive_substrate
boot_phase: Phase-G
expected_imports: []
provides: [TriuneSierpinskiCore, FractalVertex, FractalTriangle, TriuneSummary]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Any recursion failure halts and returns terminal summary. No partial results propagate."
rewrite_provenance:
  source: TRI_CORE_Package/Triune_Recursive_Cognition_Core.py
  rewrite_phase: TRI-CORE_Build
  rewrite_timestamp: 2026-02-10T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass(frozen=True)
class FractalVertex:
    vertex_id: str
    depth: int
    payload: Any
    role: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FractalTriangle:
    apex: FractalVertex
    left: FractalVertex
    right: FractalVertex
    depth: int
    children: Tuple["FractalTriangle", ...] = ()


@dataclass(frozen=True)
class TriuneSummary:
    agent_id: str
    root_depth: int
    max_depth_reached: int
    total_triangles: int
    terminal_payloads: Tuple[Any, ...]
    apex_trace: Tuple[Any, ...]
    convergence_hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# TYPE ALIASES
# =============================================================================

TransformOperator = Callable[[Any, int, str], Tuple[Any, Any, Any]]
TerminationPredicate = Callable[[Any, int], bool]


# =============================================================================
# CORE ENGINE
# =============================================================================

class TriuneSierpinskiCore:
    """Bounded Sierpinski-triangle recursive analysis engine.

    Properties:
    - Two-dimensional Sierpinski triangle fractal
    - Bounded recursion depth (structurally enforced)
    - Deterministic traversal order: apex -> left -> right
    - No global topology awareness
    - No orbit prediction
    - No semantic mutation
    - No authority over truth or state
    - Produces read-only summaries only
    """

    __slots__ = (
        "_agent_id",
        "_max_depth",
        "_transform",
        "_terminate",
    )

    def __init__(
        self,
        *,
        agent_id: str,
        max_depth: int,
        transform_operator: TransformOperator,
        termination_predicate: TerminationPredicate,
    ) -> None:
        if not agent_id or not isinstance(agent_id, str):
            raise ValueError("agent_id must be a non-empty string")
        if not isinstance(max_depth, int) or max_depth < 1:
            raise ValueError("max_depth must be a positive integer")
        if max_depth > 12:
            raise ValueError("max_depth exceeds structural safety bound (12)")
        if not callable(transform_operator):
            raise TypeError("transform_operator must be callable")
        if not callable(termination_predicate):
            raise TypeError("termination_predicate must be callable")

        self._agent_id = agent_id
        self._max_depth = max_depth
        self._transform = transform_operator
        self._terminate = termination_predicate

    @property
    def agent_id(self) -> str:
        return self._agent_id

    @property
    def max_depth(self) -> int:
        return self._max_depth

    def analyze(self, payload: Any) -> TriuneSummary:
        """Execute bounded recursive analysis over the payload.

        This is the single public entry point. It produces a TriuneSummary
        that can be attached to payload metadata without mutation.
        """
        root = self._recurse(payload, depth=0)
        terminal_payloads: List[Any] = []
        apex_trace: List[Any] = []
        total_triangles = self._collect(root, terminal_payloads, apex_trace)
        max_depth_reached = max(
            (v.depth for v in _all_vertices(root)),
            default=0,
        )

        return TriuneSummary(
            agent_id=self._agent_id,
            root_depth=0,
            max_depth_reached=max_depth_reached,
            total_triangles=total_triangles,
            terminal_payloads=tuple(terminal_payloads),
            apex_trace=tuple(apex_trace),
            convergence_hash=_deterministic_hash(self._agent_id, total_triangles, max_depth_reached),
            metadata={
                "fractal_type": "sierpinski_triangle",
                "bounded": True,
                "max_depth_configured": self._max_depth,
                "deterministic": True,
                "mutative": False,
            },
        )

    def _recurse(self, payload: Any, depth: int) -> FractalTriangle:
        """Recursive Sierpinski subdivision.

        At each depth, the transform operator decomposes the payload into
        three sub-payloads (apex, left, right). Each sub-payload is then
        recursively analyzed unless termination is reached.
        """
        vid_prefix = f"{self._agent_id}_D{depth}"

        if depth >= self._max_depth or self._terminate(payload, depth):
            terminal = FractalVertex(
                vertex_id=f"{vid_prefix}_TERMINAL",
                depth=depth,
                payload=payload,
                role="terminal",
                metadata={"terminal": True, "reason": "depth" if depth >= self._max_depth else "predicate"},
            )
            return FractalTriangle(
                apex=terminal,
                left=terminal,
                right=terminal,
                depth=depth,
                children=(),
            )

        try:
            apex_payload, left_payload, right_payload = self._transform(payload, depth, self._agent_id)
        except Exception:
            fallback = FractalVertex(
                vertex_id=f"{vid_prefix}_FAILCLOSED",
                depth=depth,
                payload=payload,
                role="fail_closed",
                metadata={"terminal": True, "reason": "transform_failure"},
            )
            return FractalTriangle(
                apex=fallback,
                left=fallback,
                right=fallback,
                depth=depth,
                children=(),
            )

        apex_v = FractalVertex(
            vertex_id=f"{vid_prefix}_APEX",
            depth=depth,
            payload=apex_payload,
            role="apex",
        )
        left_v = FractalVertex(
            vertex_id=f"{vid_prefix}_LEFT",
            depth=depth,
            payload=left_payload,
            role="left",
        )
        right_v = FractalVertex(
            vertex_id=f"{vid_prefix}_RIGHT",
            depth=depth,
            payload=right_payload,
            role="right",
        )

        child_apex = self._recurse(apex_payload, depth + 1)
        child_left = self._recurse(left_payload, depth + 1)
        child_right = self._recurse(right_payload, depth + 1)

        return FractalTriangle(
            apex=apex_v,
            left=left_v,
            right=right_v,
            depth=depth,
            children=(child_apex, child_left, child_right),
        )

    def _collect(
        self,
        triangle: FractalTriangle,
        terminal_payloads: List[Any],
        apex_trace: List[Any],
    ) -> int:
        """Walk the fractal tree, collecting terminal payloads and apex trace."""
        count = 1
        apex_trace.append(triangle.apex.payload)

        if not triangle.children:
            if triangle.apex.metadata.get("terminal"):
                terminal_payloads.append(triangle.apex.payload)
            return count

        for child in triangle.children:
            count += self._collect(child, terminal_payloads, apex_trace)

        return count


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _all_vertices(triangle: FractalTriangle) -> List[FractalVertex]:
    """Flatten all vertices from a fractal tree."""
    result = [triangle.apex, triangle.left, triangle.right]
    for child in triangle.children:
        result.extend(_all_vertices(child))
    return result


def _deterministic_hash(agent_id: str, total: int, max_depth: int) -> str:
    """Produce a stable convergence identifier without cryptographic imports."""
    raw = f"{agent_id}:{total}:{max_depth}"
    h = 0
    for ch in raw:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return f"{agent_id}_TRICORE_{h:08x}"
