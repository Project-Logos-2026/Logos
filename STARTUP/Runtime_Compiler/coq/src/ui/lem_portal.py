# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: lem_portal
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for STARTUP/Runtime_Compiler/coq/src/ui/lem_portal.py.
agent_binding: None
protocol_binding: None
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: STARTUP/Runtime_Compiler/coq/src/ui/lem_portal.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""UI hook that only unlocks after the Law of Excluded Middle is discharged."""


import json
from pathlib import Path

PORTAL_STATE = (
    Path(__file__).resolve().parents[1] / "state" / "lem_discharge_state.json"
)


def open_identity_portal() -> dict:
    """Return portal metadata if and only if the LEM discharge completed."""

    if not PORTAL_STATE.exists():
        raise PermissionError("LEM discharge incomplete – portal access denied.")
    return json.loads(PORTAL_STATE.read_text(encoding="utf-8"))
