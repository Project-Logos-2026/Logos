# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""
LOGOS_MODULE_METADATA
---------------------
module_name: Capability_Router
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Agent_Safety_Shims/Capability_Router.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Agent_Safety_Shims/Capability_Router.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Capability Router — Phase E Component
- All requests denied by default
- Requires valid artifact to authorize capability use
- Logs attempted access
"""

import json
import time


class CapabilityRouter:
    def __init__(self):
        self.permissions = {}
        self.audit_log = []

    def load_artifact(self, artifact):
        self.permissions = artifact.get("permissions", {})
        self.audit("artifact_loaded", self.permissions)

    def request(self, action):
        allowed = self.permissions.get(action, False)
        self.audit("request", {"action": action, "allowed": allowed})
        return allowed

    def audit(self, event, payload):
        self.audit_log.append({"event": event, "payload": payload})


# ---- AUTHZ_MEMORY_BOUNDED Schema Validation (Deny-All) ----

REQUIRED_FIELDS = {
    "artifact_type",
    "artifact_id",
    "issued_by",
    "issued_to",
    "issuance_timestamp",
    "capability",
    "bounds",
    "write_policy",
    "constraint_enforcement",
    "audit",
    "expiry",
    "explicit_prohibitions",
    "signature",
}

PLACEHOLDER_MARKERS = ["<placeholder", "TEMPLATE ONLY"]


def validate_authz_memory_bounded(artifact: dict) -> bool:
    # Ensure correct type
    if artifact.get("artifact_type") != "AUTHZ_MEMORY_BOUNDED":
        return False

    # Required fields present
    if not REQUIRED_FIELDS.issubset(set(artifact.keys())):
        return False

    # Reject templates or placeholders outright
    serialized = json.dumps(artifact)
    for marker in PLACEHOLDER_MARKERS:
        if marker in serialized:
            return False

    # Capability scope must match bounded memory
    cap = artifact.get("capability", {})
    if cap.get("name") != "memory" or cap.get("mode") != "bounded":
        return False

    # Bounds sanity checks
    bounds = artifact.get("bounds", {})
    if not isinstance(bounds.get("max_entries"), int):
        return False
    if not isinstance(bounds.get("max_bytes_total"), int):
        return False
    if not isinstance(bounds.get("entry_ttl_seconds"), int):
        return False

    # Prohibitions must be explicitly true
    prohibitions = artifact.get("explicit_prohibitions", {})
    for key in (
        "no_external_io",
        "no_tool_use",
        "no_learning",
        "no_permission_changes",
    ):
        if prohibitions.get(key) is not True:
            return False

    # Expiry policy required
    expiry = artifact.get("expiry", {})
    if "expires_at" not in expiry or expiry.get("on_expiry") != "freeze_and_reject":
        return False

    # Signature must be present (value checked cryptographically elsewhere)
    sig = artifact.get("signature", {})
    if not sig.get("value"):
        return False

    return True


# ---- Controlled Enablement: Bounded Memory Only ----


class _MemoryWriteGate:
    enabled = False


def enable_bounded_memory_writes():
    """
    Explicit opt-in required. Must be invoked deliberately by orchestrator.
    """

    _MemoryWriteGate.enabled = True


def disable_bounded_memory_writes():
    _MemoryWriteGate.enabled = False


def router_allows_memory_write(artifact: dict) -> bool:
    # Global gate
    if not _MemoryWriteGate.enabled:
        return False

    # Structural validation required
    if not validate_authz_memory_bounded(artifact):
        return False

    # Enforce expiry
    now = int(time.time())
    expires_at = artifact.get("expiry", {}).get("expires_at")
    if not isinstance(expires_at, int) or now >= expires_at:
        return False

    return True
