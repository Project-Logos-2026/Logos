# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MTP_Projection_Engine
runtime_layer: language_egress
role: Semantic Content Graph extraction from resolved SMPs
responsibility: Receives a resolved SMP post-TetraConscious compilation and
    extracts semantic primitives (SP-01 through SP-12) into a directed
    Semantic Content Graph suitable for downstream linearization.
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [hashlib, uuid, time, dataclasses, typing, enum]
provides: [ProjectionEngine, SemanticContentGraph, ContentNode, ContentEdge, ProjectionResult]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Returns empty graph with error flag on any extraction failure.
    Never fabricates content nodes. Never infers meaning beyond SMP payload.
rewrite_provenance:
  source: new_module
  rewrite_phase: MTP_Egress_Enhancement
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: MTP
  metrics: projection_count, node_count, edge_count, extraction_failures
---------------------
"""

import hashlib
import uuid
import time
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Tuple
from enum import Enum, IntEnum


# =============================================================================
# Semantic Primitive Types (SP-01 through SP-12, canonical closed set)
# =============================================================================

class SemanticPrimitive(Enum):
    ASSERTION = "SP-01"
    DISTINCTION = "SP-02"
    NEGATION = "SP-03"
    CONSTRAINT = "SP-04"
    DEPENDENCY = "SP-05"
    EVALUATION = "SP-06"
    UNCERTAINTY = "SP-07"
    UNKNOWN = "SP-08"
    COMMITMENT = "SP-09"
    RELATION = "SP-10"
    SCOPE = "SP-11"
    GROUNDING = "SP-12"


VALID_SP_CODES: FrozenSet[str] = frozenset(sp.value for sp in SemanticPrimitive)


class EdgeRelation(Enum):
    CAUSAL = "causal"
    TEMPORAL = "temporal"
    LOGICAL = "logical"
    SCOPE_CONTAINS = "scope_contains"
    DEPENDENCY = "dependency"
    NEGATES = "negates"
    CONSTRAINS = "constrains"
    GROUNDS = "grounds"
    EVALUATES = "evaluates"


class ProjectionStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


# =============================================================================
# Content Graph Structures
# =============================================================================

@dataclass(frozen=True)
class ContentNode:
    node_id: str
    primitive_type: SemanticPrimitive
    content: str
    modality: Optional[str] = None
    polarity: Optional[str] = None
    confidence: Optional[float] = None
    source_field: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "primitive_type": self.primitive_type.value,
            "content": self.content,
            "modality": self.modality,
            "polarity": self.polarity,
            "confidence": self.confidence,
            "source_field": self.source_field,
        }


@dataclass(frozen=True)
class ContentEdge:
    source_id: str
    target_id: str
    relation: EdgeRelation
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation": self.relation.value,
            "weight": self.weight,
        }


@dataclass
class SemanticContentGraph:
    graph_id: str
    source_smp_id: str
    source_smp_hash: str
    nodes: List[ContentNode] = field(default_factory=list)
    edges: List[ContentEdge] = field(default_factory=list)
    extraction_timestamp: float = 0.0
    status: ProjectionStatus = ProjectionStatus.FAILED

    def node_count(self) -> int:
        return len(self.nodes)

    def edge_count(self) -> int:
        return len(self.edges)

    def get_nodes_by_type(self, sp: SemanticPrimitive) -> List[ContentNode]:
        return [n for n in self.nodes if n.primitive_type == sp]

    def get_edges_from(self, node_id: str) -> List[ContentEdge]:
        return [e for e in self.edges if e.source_id == node_id]

    def get_edges_to(self, node_id: str) -> List[ContentEdge]:
        return [e for e in self.edges if e.target_id == node_id]

    def topological_order(self) -> List[str]:
        in_degree: Dict[str, int] = {n.node_id: 0 for n in self.nodes}
        adjacency: Dict[str, List[str]] = {n.node_id: [] for n in self.nodes}
        for edge in self.edges:
            if edge.target_id in in_degree:
                in_degree[edge.target_id] += 1
            if edge.source_id in adjacency:
                adjacency[edge.source_id].append(edge.target_id)

        queue = sorted([nid for nid, deg in in_degree.items() if deg == 0])
        order: List[str] = []
        while queue:
            current = queue.pop(0)
            order.append(current)
            for neighbor in sorted(adjacency.get(current, [])):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.nodes):
            return [n.node_id for n in self.nodes]

        return order

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "source_smp_id": self.source_smp_id,
            "source_smp_hash": self.source_smp_hash,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "node_count": self.node_count(),
            "edge_count": self.edge_count(),
            "extraction_timestamp": self.extraction_timestamp,
            "status": self.status.value,
        }


@dataclass
class ProjectionResult:
    graph: SemanticContentGraph
    warnings: List[str] = field(default_factory=list)
    unmapped_fields: List[str] = field(default_factory=list)
    extraction_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph": self.graph.to_dict(),
            "warnings": self.warnings,
            "unmapped_fields": self.unmapped_fields,
            "extraction_time_ms": self.extraction_time_ms,
        }


# =============================================================================
# SMP Field-to-Primitive Mapping
# =============================================================================

_FIELD_SP_MAP: Dict[str, SemanticPrimitive] = {
    "assertion": SemanticPrimitive.ASSERTION,
    "claim": SemanticPrimitive.ASSERTION,
    "statement": SemanticPrimitive.ASSERTION,
    "content": SemanticPrimitive.ASSERTION,
    "distinction": SemanticPrimitive.DISTINCTION,
    "category": SemanticPrimitive.DISTINCTION,
    "classification": SemanticPrimitive.DISTINCTION,
    "negation": SemanticPrimitive.NEGATION,
    "denial": SemanticPrimitive.NEGATION,
    "constraint": SemanticPrimitive.CONSTRAINT,
    "rule": SemanticPrimitive.CONSTRAINT,
    "limit": SemanticPrimitive.CONSTRAINT,
    "dependency": SemanticPrimitive.DEPENDENCY,
    "requires": SemanticPrimitive.DEPENDENCY,
    "depends_on": SemanticPrimitive.DEPENDENCY,
    "evaluation": SemanticPrimitive.EVALUATION,
    "assessment": SemanticPrimitive.EVALUATION,
    "judgment": SemanticPrimitive.EVALUATION,
    "score": SemanticPrimitive.EVALUATION,
    "uncertainty": SemanticPrimitive.UNCERTAINTY,
    "unknown": SemanticPrimitive.UNKNOWN,
    "commitment": SemanticPrimitive.COMMITMENT,
    "promise": SemanticPrimitive.COMMITMENT,
    "obligation": SemanticPrimitive.COMMITMENT,
    "relation": SemanticPrimitive.RELATION,
    "relationship": SemanticPrimitive.RELATION,
    "link": SemanticPrimitive.RELATION,
    "scope": SemanticPrimitive.SCOPE,
    "context": SemanticPrimitive.SCOPE,
    "domain": SemanticPrimitive.SCOPE,
    "grounding": SemanticPrimitive.GROUNDING,
    "evidence": SemanticPrimitive.GROUNDING,
    "source": SemanticPrimitive.GROUNDING,
    "reference": SemanticPrimitive.GROUNDING,
}

_RELATION_INFERENCE: Dict[Tuple[str, str], EdgeRelation] = {
    ("SP-05", "*"): EdgeRelation.DEPENDENCY,
    ("SP-03", "*"): EdgeRelation.NEGATES,
    ("SP-04", "*"): EdgeRelation.CONSTRAINS,
    ("SP-12", "*"): EdgeRelation.GROUNDS,
    ("SP-06", "*"): EdgeRelation.EVALUATES,
    ("SP-11", "*"): EdgeRelation.SCOPE_CONTAINS,
}


# =============================================================================
# Projection Engine
# =============================================================================

class ProjectionEngine:

    def __init__(self) -> None:
        self._node_counter: int = 0

    def project(self, smp_payload: Dict[str, Any]) -> ProjectionResult:
        start = time.monotonic()
        warnings: List[str] = []
        unmapped: List[str] = []

        smp_id = str(smp_payload.get("smp_id", "unknown"))
        smp_hash = self._hash_payload(smp_payload)

        graph = SemanticContentGraph(
            graph_id=f"SCG-{uuid.uuid4().hex[:12]}",
            source_smp_id=smp_id,
            source_smp_hash=smp_hash,
            extraction_timestamp=time.time(),
        )

        try:
            nodes, field_warnings, field_unmapped = self._extract_nodes(smp_payload)
            warnings.extend(field_warnings)
            unmapped.extend(field_unmapped)

            graph.nodes = nodes

            if len(nodes) > 1:
                edges = self._infer_edges(nodes)
                graph.edges = edges

            if len(nodes) == 0:
                graph.status = ProjectionStatus.FAILED
                warnings.append("No semantic content extracted from SMP")
            elif len(unmapped) > 0:
                graph.status = ProjectionStatus.PARTIAL
            else:
                graph.status = ProjectionStatus.SUCCESS

        except Exception as exc:
            graph.status = ProjectionStatus.FAILED
            warnings.append(f"Projection failed: {type(exc).__name__}")

        elapsed = (time.monotonic() - start) * 1000.0

        return ProjectionResult(
            graph=graph,
            warnings=warnings,
            unmapped_fields=unmapped,
            extraction_time_ms=elapsed,
        )

    def _extract_nodes(
        self, payload: Dict[str, Any]
    ) -> Tuple[List[ContentNode], List[str], List[str]]:
        nodes: List[ContentNode] = []
        warnings: List[str] = []
        unmapped: List[str] = []

        semantic_content = payload.get("semantic_content", payload)
        if not isinstance(semantic_content, dict):
            return nodes, ["semantic_content is not a dict"], unmapped

        for field_key, field_value in semantic_content.items():
            lower_key = field_key.lower()

            sp = _FIELD_SP_MAP.get(lower_key)
            if sp is None:
                sp = self._infer_primitive(lower_key, field_value)

            if sp is None:
                unmapped.append(field_key)
                continue

            content_str = self._extract_content_string(field_value)
            if not content_str:
                warnings.append(f"Empty content for field: {field_key}")
                continue

            modality = None
            polarity = None
            confidence = None

            if isinstance(field_value, dict):
                modality = field_value.get("modality")
                polarity = field_value.get("polarity")
                confidence = field_value.get("confidence")

            self._node_counter += 1
            node = ContentNode(
                node_id=f"N-{self._node_counter:04d}",
                primitive_type=sp,
                content=content_str,
                modality=str(modality) if modality else None,
                polarity=str(polarity) if polarity else None,
                confidence=float(confidence) if confidence is not None else None,
                source_field=field_key,
            )
            nodes.append(node)

        return nodes, warnings, unmapped

    def _infer_primitive(
        self, key: str, value: Any
    ) -> Optional[SemanticPrimitive]:
        for map_key, sp in _FIELD_SP_MAP.items():
            if map_key in key:
                return sp

        if isinstance(value, dict):
            if "polarity" in value and value.get("polarity") in ("negate", "deny"):
                return SemanticPrimitive.NEGATION
            if "confidence" in value:
                conf = value.get("confidence", 1.0)
                if isinstance(conf, (int, float)) and conf < 0.5:
                    return SemanticPrimitive.UNCERTAINTY

        return None

    def _infer_edges(self, nodes: List[ContentNode]) -> List[ContentEdge]:
        edges: List[ContentEdge] = []

        for i, src in enumerate(nodes):
            for j, tgt in enumerate(nodes):
                if i == j:
                    continue

                relation = self._edge_relation(src, tgt)
                if relation is not None:
                    edges.append(ContentEdge(
                        source_id=src.node_id,
                        target_id=tgt.node_id,
                        relation=relation,
                    ))

        return edges

    def _edge_relation(
        self, src: ContentNode, tgt: ContentNode
    ) -> Optional[EdgeRelation]:
        sp_code = src.primitive_type.value

        for (src_sp, tgt_sp), relation in _RELATION_INFERENCE.items():
            if src_sp == sp_code and tgt_sp == "*":
                return relation

        return None

    def _extract_content_string(self, value: Any) -> str:
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, dict):
            for key in ("text", "content", "value", "statement", "description"):
                if key in value and isinstance(value[key], str):
                    return value[key].strip()
            return str(value)
        if isinstance(value, (list, tuple)):
            parts = [self._extract_content_string(v) for v in value]
            return "; ".join(p for p in parts if p)
        if value is not None:
            return str(value)
        return ""

    def _hash_payload(self, payload: Dict[str, Any]) -> str:
        raw = str(sorted(payload.items())).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()
