# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: lock_and_key
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/Runtime_Spine/Lock_And_Key/lock_and_key.py.
agent_binding: None
protocol_binding: Runtime_Spine
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/Runtime_Spine/Lock_And_Key/lock_and_key.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Runtime Spine Lock-and-Key adapter.

Re-exports the governed Lock-and-Key implementation.
"""

from LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT.Runtime_Enforcement.Runtime_Spine.Lock_And_Key.lock_and_key import (
    LockAndKeyFailure,
    execute_lock_and_key,
)

__all__ = ["LockAndKeyFailure", "execute_lock_and_key"]
