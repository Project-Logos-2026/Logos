# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""
LOGOS_MODULE_METADATA
---------------------
module_name: Memory_Substrate
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Agent_Safety_Shims/Memory_Substrate.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Agent_Safety_Shims/Memory_Substrate.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Memory Substrate — Phase E Component
- Stores proposed state with provenance
- Enforces router-mediated authorization with bounded writes
- Logs all attempts
"""

import json
import time

from LOGOS_SYSTEM.Agent_Safety_Shims.Capability_Router import (
    CapabilityRouter,
    validate_authz_memory_bounded,
    router_allows_memory_write,
)


class MemorySubstrate:
    def __init__(self, router: CapabilityRouter):
        self.router = router
        self.storage = []
        self.log = []

    def write(self, entry, artifact=None):
        if artifact is None:
            self.log.append(
                {
                    "event": "write_refused",
                    "reason": "no_authorization_artifact",
                    "entry": entry,
                }
            )
            return False

        try:
            authorized = validate_authz_memory_bounded(artifact)
        except Exception as exc:
            self.log.append(
                {
                    "event": "write_refused",
                    "reason": "validation_exception",
                    "error": str(exc),
                    "entry": entry,
                }
            )
            return False

        if not authorized:
            self.log.append(
                {
                    "event": "write_refused",
                    "reason": "authorization_denied",
                    "entry": entry,
                }
            )
            return False

        # Router gate and expiry enforcement
        if not router_allows_memory_write(artifact):
            self.log.append(
                {
                    "event": "write_refused",
                    "reason": "router_denied",
                    "entry": entry,
                }
            )
            return False

        # Enforce bounds
        bounds = artifact.get("bounds", {})
        max_entries = bounds.get("max_entries")
        max_bytes_total = bounds.get("max_bytes_total")

        if isinstance(max_entries, int) and len(self.storage) >= max_entries:
            self.log.append(
                {
                    "event": "write_refused",
                    "reason": "bounds_exceeded_entries",
                    "entry": entry,
                }
            )
            return False

        # Approximate byte size using JSON serialization
        try:
            new_entry_bytes = len(json.dumps(entry))
            current_bytes = sum(len(json.dumps(e.get("entry", {}))) for e in self.storage)
        except Exception:
            new_entry_bytes = 0
            current_bytes = 0

        if isinstance(max_bytes_total, int) and (current_bytes + new_entry_bytes) > max_bytes_total:
            self.log.append(
                {
                    "event": "write_refused",
                    "reason": "bounds_exceeded_bytes",
                    "entry": entry,
                }
            )
            return False

        # Accept write
        record = {
            "entry": entry,
            "timestamp": time.time(),
            "artifact_id": artifact.get("artifact_id"),
        }
        self.storage.append(record)
        self.log.append(
            {
                "event": "write_accepted",
                "entry": entry,
            }
        )
        return True

    def read_all(self):
        return self.storage
