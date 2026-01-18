# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: OmniProperty_Integration
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/Logos_Agents/I1_Agent/_core/OmniProperty_Integration.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
OmniProperty integration for I1 (Omniscience).

Role: force multiplier for I1's domain (SCP / epistemic handling).
Constraints:
- Deterministic
- No inference / no belief formation
- Adds traceability, coverage, and consistency metadata only
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from I1_Agent.config.hashing import safe_hash
from I1_Agent.diagnostics.errors import IntegrationError


@dataclass(frozen=True)
class OmniscienceMetrics:
    identity_hash: str
    coverage_score: float
    missing_refs: List[str]
    notes: List[str]


class OmniscienceIntegration:
    """
    Force multiplier for I1: attaches deterministic epistemic-strength metadata.
    Does not alter semantic content; only adds trace/coverage signals.
    """

    def __init__(self, ontology_blob: Dict[str, Any]):
        self.ontology_blob = ontology_blob or {}
        self._validate_minimal_shape()

    def _validate_minimal_shape(self) -> None:
        # Keep this intentionally light: core may be JSON-only today.
        # We only require that the ontology is a dict and serializable.
        if not isinstance(self.ontology_blob, dict):
            raise IntegrationError("ontology_blob must be a dict")

    def compute_metrics(
        self,
        *,
        referenced_ids: Optional[List[str]] = None,
        known_registry: Optional[Dict[str, Any]] = None,
    ) -> OmniscienceMetrics:
        """
        Deterministically computes identity/coverage signals.
        - referenced_ids: ids referenced by the current pipeline step (entities/props/relations)
        - known_registry: optional map of ids -> definition/record (epistemic registry)
        """
        referenced_ids = referenced_ids or []
        known_registry = known_registry or {}

        identity_hash = safe_hash(self.ontology_blob)

        missing: List[str] = []
        for rid in referenced_ids:
            if rid not in known_registry:
                missing.append(rid)

        total = max(1, len(referenced_ids))
        coverage = 1.0 - (len(missing) / total)

        notes: List[str] = []
        if missing:
            notes.append("Some referenced ids are not present in registry (coverage reduced).")

        return OmniscienceMetrics(
            identity_hash=identity_hash,
            coverage_score=round(max(0.0, min(1.0, coverage)), 4),
            missing_refs=missing,
            notes=notes,
        )

    def enrich_packet(
        self,
        *,
        packet: Dict[str, Any],
        referenced_ids: Optional[List[str]] = None,
        known_registry: Optional[Dict[str, Any]] = None,
        field: str = "omniscience",
    ) -> Dict[str, Any]:
        """
        Returns a new dict with omniscience metadata added under `field`.
        Does not modify existing meaning content (payload).
        """
        if not isinstance(packet, dict):
            raise IntegrationError("packet must be a dict")

        metrics = self.compute_metrics(
            referenced_ids=referenced_ids,
            known_registry=known_registry,
        )

        out = dict(packet)
        out[field] = {
            "identity_hash": metrics.identity_hash,
            "coverage_score": metrics.coverage_score,
            "missing_refs": list(metrics.missing_refs),
            "notes": list(metrics.notes),
        }
        return out
