# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: logos_protocol_nexus
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
  source: System_Stack/Logos_Protocol/Logos_Protocol_Nexus/logos_protocol_nexus.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

# === Canonical Logos Protocol Nexus Façade ===
# This file aggregates protocol-level Nexus façades into a single governed surface.
# No execution logic lives here.

from Logos_System.System_Stack.Synthetic_Cognition_Protocol.SCP_Nexus.scp_nexus_orchestrator import FractalNexus
from Logos_System.System_Stack.Advanced_Reasoning_Protocol.ARP_Nexus.arp_nexus_orchestrator import BayesianNexus
from Logos_System.System_Stack.Cognitive_State_Protocol.CSP_Nexus.csp_nexus_orchestrator import (
    MemoryConsolidationStage,
    MemoryRecallType,
    MemoryTrace,
    MemoryConsolidator,
    MemoryRecallSystem,
    AbstractionEngine,
    MemoryApplicationSystem,
    LivingMemorySystem,
)
from Logos_System.System_Stack.Meaning_Translation_Protocol.MTP_Nexus.mtp_nexus_orchestrator import *
from Logos_System.System_Stack.System_Operations_Protocol.SOP_Nexus.sop_nexus_orchestrator import (
    AgentType,
    ProtocolType,
    NexusLifecycle,
    AgentRequest,
    NexusResponse,
    BaseNexus,
    create_agent_request,
    PlanningType,
    GapType,
    LinguisticOperation,
    PlanningRequest,
    GapDetectionRequest,
    LinguisticRequest,
    LOGOSAgentNexus,
)

__all__ = [
    # SCP
    "FractalNexus",

    # ARP
    "BayesianNexus",

    # CSP
    "MemoryConsolidationStage",
    "MemoryRecallType",
    "MemoryTrace",
    "MemoryConsolidator",
    "MemoryRecallSystem",
    "AbstractionEngine",
    "MemoryApplicationSystem",
    "LivingMemorySystem",

    # SOP
    "AgentType",
    "ProtocolType",
    "NexusLifecycle",
    "AgentRequest",
    "NexusResponse",
    "BaseNexus",
    "create_agent_request",
    "PlanningType",
    "GapType",
    "LinguisticOperation",
    "PlanningRequest",
    "GapDetectionRequest",
    "LinguisticRequest",
    "LOGOSAgentNexus",
]
