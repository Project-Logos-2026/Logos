from __future__ import annotations
'\nLOGOS_MODULE_METADATA\n---------------------\nmodule_name: Omni_Property_Integration\nruntime_layer: inferred\nrole: inferred\nagent_binding: None\nprotocol_binding: None\nboot_phase: inferred\nexpected_imports: []\nprovides: []\ndepends_on_runtime_state: False\nfailure_mode:\n  type: unknown\n  notes: ""\nrewrite_provenance:\n  source: System_Stack/Logos_Agents/I3_Agent/_core/Omni_Property_Integration.py\n  rewrite_phase: Phase_B\n  rewrite_timestamp: 2026-01-18T23:03:31.726474\nobservability:\n  log_channel: None\n  metrics: disabled\n---------------------\n'
'OmniProperty integration for I3 (Omnipresence).\n\nRole: force multiplier for I3\'s domain (ARP / planning & advanced reasoning).\nConstraints:\n- Deterministic\n- No inference / no belief formation\n- Adds context-coverage, locality/span, and traceability metadata only\n\nInterpretation of Omnipresence in-system:\n- Not metaphysical claims; operational: "context span" coverage across available inputs.\n'
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I3_Agent.config.hashing import safe_hash
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I3_Agent.diagnostics.errors import IntegrationError

@dataclass(frozen=True)
class OmnipresenceMetrics:
    identity_hash: str
    context_span_score: float
    missing_context_refs: List[str]
    notes: List[str]

class OmnipresenceIntegration:
    """Force multiplier for I3: attaches deterministic context-span metadata."""

    def __init__(self, ontology_blob: Dict[str, Any]):
        self.ontology_blob = ontology_blob or {}
        self._validate_minimal_shape()

    def _validate_minimal_shape(self) -> None:
        if not isinstance(self.ontology_blob, dict):
            raise IntegrationError('ontology_blob must be a dict')

    def compute_metrics(self, *, context_refs: Optional[List[str]]=None, available_context: Optional[Dict[str, Any]]=None) -> OmnipresenceMetrics:
        context_refs = context_refs or []
        available_context = available_context or {}
        identity_hash = safe_hash(self.ontology_blob)
        missing: List[str] = []
        for rid in context_refs:
            if rid not in available_context:
                missing.append(rid)
        total = max(1, len(context_refs))
        span = 1.0 - len(missing) / total
        notes: List[str] = []
        if missing:
            notes.append('Some context refs unavailable (span reduced).')
        return OmnipresenceMetrics(identity_hash=identity_hash, context_span_score=round(max(0.0, min(1.0, span)), 4), missing_context_refs=missing, notes=notes)

    def enrich_packet(self, *, packet: Dict[str, Any], context_refs: Optional[List[str]]=None, available_context: Optional[Dict[str, Any]]=None, field: str='omnipresence') -> Dict[str, Any]:
        if not isinstance(packet, dict):
            raise IntegrationError('packet must be a dict')
        metrics = self.compute_metrics(context_refs=context_refs, available_context=available_context)
        out = dict(packet)
        out[field] = {'identity_hash': metrics.identity_hash, 'context_span_score': metrics.context_span_score, 'missing_context_refs': list(metrics.missing_context_refs), 'notes': list(metrics.notes)}
        return out