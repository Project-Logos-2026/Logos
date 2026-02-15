from __future__ import annotations
'\nLOGOS_MODULE_METADATA\n---------------------\nmodule_name: result_packet\nruntime_layer: inferred\nrole: inferred\nagent_binding: None\nprotocol_binding: None\nboot_phase: inferred\nexpected_imports: []\nprovides: []\ndepends_on_runtime_state: False\nfailure_mode:\n  type: unknown\n  notes: ""\nrewrite_provenance:\n  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_runtime/result_packet.py\n  rewrite_phase: Phase_B\n  rewrite_timestamp: 2026-01-18T23:03:31.726474\nobservability:\n  log_channel: None\n  metrics: disabled\n---------------------\n'
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.config.hashing import safe_hash

@dataclass(frozen=True)
class SCPResultPacket:
    """
    Append-only output from SCP back to Logos.
    References SMP by smp_id; does not mutate SMP.
    """
    smp_id: str
    created_at: float
    status: str
    summary: str
    score_vector: Dict[str, float] = field(default_factory=dict)
    findings: Dict[str, Any] = field(default_factory=dict)
    recommended_next: Dict[str, Any] = field(default_factory=dict)
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {'smp_id': self.smp_id, 'created_at': self.created_at, 'status': self.status, 'summary': self.summary, 'score_vector': self.score_vector, 'findings': self.findings, 'recommended_next': self.recommended_next, 'provenance': self.provenance}

def emit_result_packet(*, smp_id: str, status: str, summary: str, score_vector: Optional[Dict[str, float]]=None, findings: Optional[Dict[str, Any]]=None, recommended_next: Optional[Dict[str, Any]]=None, reference_obj: Any=None) -> SCPResultPacket:
    """
    Create an SCPResultPacket. 'findings' should avoid raw unsafe content.
    Prefer hashes, labels, and high-level summaries.
    """
    prov = {}
    if reference_obj is not None:
        prov['reference_hash'] = safe_hash(reference_obj)
    return SCPResultPacket(smp_id=smp_id, created_at=time.time(), status=status, summary=summary, score_vector=score_vector or {}, findings=findings or {}, recommended_next=recommended_next or {}, provenance=prov)