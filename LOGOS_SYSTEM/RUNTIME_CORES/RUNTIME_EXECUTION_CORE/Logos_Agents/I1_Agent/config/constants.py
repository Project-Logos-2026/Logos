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
module_name: constants
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
  source: System_Stack/Logos_Agents/I1_Agent/config/constants.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


# Stable constants used across agent cores (testing)
AGENT_I1 = "I1"
AGENT_I2 = "I2"
AGENT_I3 = "I3"
AGENT_LOGOS = "LOGOS"

PRIORITY_NORMAL = "normal"
PRIORITY_HIGH = "high"

DECISION_ALLOW = "allow"
DECISION_ANNOTATE = "annotate_only"
DECISION_DECOMPOSE = "decompose_only"
DECISION_QUARANTINE = "quarantine"
DECISION_ESCALATE = "escalate"
