from __future__ import annotations

from typing import Any, Dict, Optional


class ARPToNexusRouter:
    def __init__(self, nexus_client: Optional[Any] = None) -> None:
        self.nexus_client = nexus_client

    def handoff(self, compiled_packet: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        if self.nexus_client and hasattr(self.nexus_client, "receive_from_arp"):
            return self.nexus_client.receive_from_arp(compiled_packet=compiled_packet, context=context)

        return {
            "status": "no_nexus",
            "reason": "nexus_client not configured",
            "compiled_packet": compiled_packet,
            "context": context,
        }
