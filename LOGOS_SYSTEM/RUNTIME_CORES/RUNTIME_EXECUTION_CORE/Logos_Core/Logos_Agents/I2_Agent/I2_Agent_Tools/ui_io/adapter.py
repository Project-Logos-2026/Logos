# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
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
module_name: adapter
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
  source: System_Stack/Logos_Agents/I2_Agent/protocol_operations/ui_io/adapter.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


import json
from dataclasses import dataclass
from typing import Any, Dict

from I2_Agent.config.constants import AGENT_I2
from I2_Agent.config.hashing import safe_hash
from I2_Agent.connections.id_handler import generate_packet_identity
from I2_Agent.connections.router import decide_route
from I2_Agent.protocol_operations.smp import build_smp
try:
    from I2_Agent.protocol_operations.semantic_projection_monitor import (
        I2SemanticClusterMonitor,
    )
except ImportError:  # pragma: no cover - fail-closed
    I2SemanticClusterMonitor = None

try:
    from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Tools.core_processing.MTP_aggregator import (
        build_mtp_smp_packet,
    )
except ImportError:  # pragma: no cover - fail-closed to I2 fallback
    build_mtp_smp_packet = None


SEMANTIC_MONITOR = I2SemanticClusterMonitor() if I2SemanticClusterMonitor else None


@dataclass(frozen=True)
class InboundResponse:
    route: str
    priority: str
    reason: str
    payload: Dict[str, Any]


def _normalize_inbound(inbound: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(inbound)
    except Exception:
        parsed = None

    if isinstance(parsed, dict):
        return parsed

    # Fallback: wrap raw text into a dict for downstream stability.
    return {"input": inbound}


def route_input(*, inbound: str, default_route: str) -> InboundResponse:
    raw_payload = _normalize_inbound(inbound)
    identity = generate_packet_identity(origin=AGENT_I2, reference_obj=raw_payload)

    input_reference = {
        "input_hash": safe_hash(raw_payload),
        "original_input": raw_payload,
    }

    classification = {
        "tags": [],
        "domain": "unknown",
        "confidence": 0.0,
    }

    analysis = {
        "recommended_action": "allow",
        "summary": "UI ingress baseline",
    }

    transform_report: Dict[str, Any] = {
        "attempted": [],
        "succeeded": [],
        "failed": [],
        "status": "not_transformed",
    }

    benevolence = {"status": "unchecked"}

    triadic_scores: Dict[str, float] = {
        "existence": 0.0,
        "goodness": 0.0,
        "truth": 0.0,
    }

    provenance = {
        "ingress": "ui_io",
        "packet_identity": identity.to_dict(),
    }

    smp_dict: Dict[str, Any]

    if build_mtp_smp_packet is not None:
        mtp_packet = build_mtp_smp_packet(
            raw_input=raw_payload,
            context={"ingress": "ui_io", "packet_identity": identity.to_dict()},
            header_overrides={
                "source": "I2_UI_IO",
                "epistemic_status": "PROVISIONAL",
                "privation_gate_result": "pre_gated",
                "language": raw_payload.get("language", "und"),
            },
        )
        smp_dict = {
            "mtp_status": mtp_packet.get("status"),
            "mtp_reason": mtp_packet.get("reason"),
            "mtp_smp": mtp_packet.get("smp"),
            "route_to": default_route,
            "final_decision": "allow",
        }
    else:
        smp_obj = build_smp(
            origin_agent=AGENT_I2,
            input_reference=input_reference,
            classification=classification,
            analysis=analysis,
            transform_report=transform_report,
            bridge_passed=True,
            benevolence=benevolence,
            triadic_scores=triadic_scores,
            final_decision="allow",
            violations=[],
            route_to=default_route,
            triage_vector=None,
            delta_profile={},
            parent_id=identity.parent_id,
            provenance=provenance,
        )

        smp_dict = smp_obj.to_dict()

    if SEMANTIC_MONITOR is not None:
        recomposed = SEMANTIC_MONITOR.register_payload(smp_dict, actor=AGENT_I2)
        if recomposed:
            smp_dict["i2_recomposition"] = [
                {
                    "family": item.family,
                    "smp_t": item.smp_t,
                    "aa_f": item.aa_f,
                    "retired_segment_ids": item.retired_segment_ids,
                    "timestamp": item.timestamp,
                }
                for item in recomposed
            ]
    decision = decide_route(smp=smp_dict, default_route=default_route)

    return InboundResponse(
        route=decision.route_to,
        priority=decision.priority,
        reason=decision.reason,
        payload=smp_dict,
    )


def handle_inbound(*, inbound: str, default_route: str) -> InboundResponse:
    return route_input(inbound=inbound, default_route=default_route)
