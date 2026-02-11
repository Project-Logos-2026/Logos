# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MTP_Semantic_Linearizer
runtime_layer: language_egress
role: AF-LANG-001 Semantic Linearizer
responsibility: Transforms a Semantic Content Graph into a canonical linear
    sequence suitable for downstream rendering. Performs structural
    normalization, canonical ordering, and symbol disambiguation.
    Operates read-only over meaning. Does not introduce new semantics.
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [dataclasses, typing, enum]
provides: [SemanticLinearizer, LinearizationPlan, LinearUnit, DiscourseMode]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Returns empty plan with error status on ordering failure.
    Falls back to insertion-order if topological sort fails.
rewrite_provenance:
  source: new_module
  rewrite_phase: MTP_Egress_Enhancement
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: MTP
  metrics: linearization_count, unit_count, reorder_events
---------------------
"""

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


# =============================================================================
# Discourse Modes (from Language Backend Audit Attestation)
# =============================================================================

class DiscourseMode(Enum):
    TECHNICAL = "technical"
    DECLARATIVE = "declarative"
    EXPLANATORY = "explanatory"


class LinearizationStatus(Enum):
    SUCCESS = "success"
    FALLBACK = "fallback"
    FAILED = "failed"


# =============================================================================
# Canonical Ordering Rules
# =============================================================================

_SP_CANONICAL_ORDER: Dict[str, int] = {
    "SP-11": 0,   # Scope first (establishes context)
    "SP-12": 1,   # Grounding (establishes evidence base)
    "SP-01": 2,   # Assertion (primary claims)
    "SP-02": 3,   # Distinction (differentiations)
    "SP-10": 4,   # Relation (connections)
    "SP-05": 5,   # Dependency (prerequisites)
    "SP-04": 6,   # Constraint (limits)
    "SP-06": 7,   # Evaluation (assessments)
    "SP-09": 8,   # Commitment (obligations)
    "SP-03": 9,   # Negation (denials)
    "SP-07": 10,  # Uncertainty (caveats)
    "SP-08": 11,  # Unknown (gaps)
}


# =============================================================================
# Linear Unit
# =============================================================================

@dataclass(frozen=True)
class LinearUnit:
    unit_id: str
    source_node_id: str
    primitive_code: str
    content: str
    sequence_position: int
    discourse_role: str
    modality: Optional[str] = None
    polarity: Optional[str] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "source_node_id": self.source_node_id,
            "primitive_code": self.primitive_code,
            "content": self.content,
            "sequence_position": self.sequence_position,
            "discourse_role": self.discourse_role,
            "modality": self.modality,
            "polarity": self.polarity,
            "confidence": self.confidence,
        }


# =============================================================================
# Linearization Plan
# =============================================================================

@dataclass
class LinearizationPlan:
    plan_id: str
    source_graph_id: str
    source_graph_hash: str
    discourse_mode: DiscourseMode
    units: List[LinearUnit] = field(default_factory=list)
    status: LinearizationStatus = LinearizationStatus.FAILED
    linearization_timestamp: float = 0.0

    def unit_count(self) -> int:
        return len(self.units)

    def get_unit_by_node(self, node_id: str) -> Optional[LinearUnit]:
        for u in self.units:
            if u.source_node_id == node_id:
                return u
        return None

    def coverage_check(self, graph_node_ids: List[str]) -> Dict[str, Any]:
        covered = {u.source_node_id for u in self.units}
        missing = [nid for nid in graph_node_ids if nid not in covered]
        extra = [u.source_node_id for u in self.units if u.source_node_id not in graph_node_ids]
        return {
            "total_nodes": len(graph_node_ids),
            "covered": len(covered),
            "missing": missing,
            "extra": extra,
            "bijective": len(missing) == 0 and len(extra) == 0,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "source_graph_id": self.source_graph_id,
            "source_graph_hash": self.source_graph_hash,
            "discourse_mode": self.discourse_mode.value,
            "units": [u.to_dict() for u in self.units],
            "unit_count": self.unit_count(),
            "status": self.status.value,
            "linearization_timestamp": self.linearization_timestamp,
        }


# =============================================================================
# Discourse Role Assignment
# =============================================================================

_SP_DISCOURSE_ROLES: Dict[str, Dict[str, str]] = {
    "technical": {
        "SP-01": "declaration",
        "SP-02": "specification",
        "SP-03": "exclusion",
        "SP-04": "constraint",
        "SP-05": "prerequisite",
        "SP-06": "metric",
        "SP-07": "caveat",
        "SP-08": "gap",
        "SP-09": "requirement",
        "SP-10": "association",
        "SP-11": "scope_boundary",
        "SP-12": "citation",
    },
    "declarative": {
        "SP-01": "statement",
        "SP-02": "clarification",
        "SP-03": "denial",
        "SP-04": "condition",
        "SP-05": "dependency",
        "SP-06": "judgment",
        "SP-07": "qualification",
        "SP-08": "acknowledgment",
        "SP-09": "pledge",
        "SP-10": "connection",
        "SP-11": "framing",
        "SP-12": "basis",
    },
    "explanatory": {
        "SP-01": "claim",
        "SP-02": "distinction",
        "SP-03": "counterpoint",
        "SP-04": "limitation",
        "SP-05": "foundation",
        "SP-06": "assessment",
        "SP-07": "hedge",
        "SP-08": "open_question",
        "SP-09": "commitment",
        "SP-10": "link",
        "SP-11": "context",
        "SP-12": "evidence",
    },
}


# =============================================================================
# Semantic Linearizer (AF-LANG-001)
# =============================================================================

class SemanticLinearizer:

    def linearize(
        self,
        graph: Any,
        discourse_mode: DiscourseMode = DiscourseMode.DECLARATIVE,
    ) -> LinearizationPlan:

        graph_hash = hashlib.sha256(
            str(graph.to_dict()).encode("utf-8")
        ).hexdigest()

        plan = LinearizationPlan(
            plan_id=f"LP-{graph.graph_id}",
            source_graph_id=graph.graph_id,
            source_graph_hash=graph_hash,
            discourse_mode=discourse_mode,
            linearization_timestamp=time.time(),
        )

        if not graph.nodes:
            plan.status = LinearizationStatus.FAILED
            return plan

        try:
            ordered_ids = self._compute_order(graph)
            plan.status = LinearizationStatus.SUCCESS
        except Exception:
            ordered_ids = [n.node_id for n in graph.nodes]
            plan.status = LinearizationStatus.FALLBACK

        node_map = {n.node_id: n for n in graph.nodes}
        role_table = _SP_DISCOURSE_ROLES.get(
            discourse_mode.value, _SP_DISCOURSE_ROLES["declarative"]
        )

        units: List[LinearUnit] = []
        for pos, nid in enumerate(ordered_ids):
            node = node_map.get(nid)
            if node is None:
                continue

            sp_code = node.primitive_type.value
            role = role_table.get(sp_code, "content")

            unit = LinearUnit(
                unit_id=f"LU-{pos:04d}",
                source_node_id=nid,
                primitive_code=sp_code,
                content=node.content,
                sequence_position=pos,
                discourse_role=role,
                modality=node.modality,
                polarity=node.polarity,
                confidence=node.confidence,
            )
            units.append(unit)

        plan.units = units
        return plan

    def _compute_order(self, graph: Any) -> List[str]:
        topo = graph.topological_order()

        node_map = {n.node_id: n for n in graph.nodes}

        def sort_key(nid: str) -> tuple:
            node = node_map.get(nid)
            if node is None:
                return (999, nid)
            sp_rank = _SP_CANONICAL_ORDER.get(node.primitive_type.value, 50)
            topo_rank = topo.index(nid) if nid in topo else 999
            return (sp_rank, topo_rank, nid)

        ordered = sorted(node_map.keys(), key=sort_key)
        return ordered
