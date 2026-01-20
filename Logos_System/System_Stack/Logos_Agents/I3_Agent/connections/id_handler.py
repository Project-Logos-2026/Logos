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
module_name: id_handler
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
  source: System_Stack/Logos_Agents/I3_Agent/connections/id_handler.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .hashing import safe_hash


@dataclass(frozen=True)
class PacketIdentity:
    """Stateless, structured identity block for packets and SMP handoffs."""
    packet_id: str
    origin: str
    created_at: float
    parent_id: Optional[str] = None
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "origin": self.origin,
            "created_at": self.created_at,
            "parent_id": self.parent_id,
            "session_id": self.session_id,
        }


def generate_packet_identity(
    *,
    origin: str,
    parent_id: Optional[str] = None,
    session_id: Optional[str] = None,
    reference_obj: Any = None,
) -> PacketIdentity:
    """Create a unique packet identity.

    - origin: e.g., "I1", "I2", "I3", "LOGOS"
    - parent_id: upstream packet id if chaining
    - session_id: optional run/session marker
    - reference_obj: optional object to derive an additional stable reference hash
    """
    now = time.time()
    rand = uuid.uuid4().hex[:8]
    ref = safe_hash(reference_obj)[:8] if reference_obj is not None else ""
    suffix = f"{rand}{('-' + ref) if ref else ''}"
    packet_id = f"{origin}-{int(now)}-{suffix}"
    return PacketIdentity(
        packet_id=packet_id,
        origin=origin,
        created_at=now,
        parent_id=parent_id,
        session_id=session_id,
    )
