# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: arp_compiler_core
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/compiler/arp_compiler_core.py.
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/compiler/arp_compiler_core.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..reasoning.pxl_reasoner import PXLReasoner
from ..reasoning.iel_reasoner import IELReasoner
from ..reasoning.mathematical_reasoner import MathematicalReasoner
from ..reasoning.unified_reasoner import UnifiedReasoner


class ARPCompilerCore:
    def __init__(
        self,
        pxl: Optional[PXLReasoner] = None,
        iel: Optional[IELReasoner] = None,
        mathematical: Optional[MathematicalReasoner] = None,
        unified: Optional[UnifiedReasoner] = None,
    ) -> None:
        self.pxl = pxl or PXLReasoner()
        self.iel = iel or IELReasoner()
        self.mathematical = mathematical or MathematicalReasoner()
        self.unified = unified or UnifiedReasoner()

    def compile(self, aaced_packet: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        pxl_out = self.pxl.analyze(aaced_packet, context)
        iel_out = self.iel.analyze(aaced_packet, context, pxl_out=pxl_out)
        math_out = self.mathematical.analyze(aaced_packet, context)
        unified_out = self.unified.analyze(
            aaced_packet,
            context,
            pxl_out=pxl_out,
            iel_out=iel_out,
            math_out=math_out,
        )

        return {
            "protocol": "ARP",
            "type": "AA_PRE_STRUCTURED",
            "analysis_stack": {
                "pxl": pxl_out,
                "iel": iel_out,
                "mathematical": math_out,
                "unified": unified_out,
            },
            "status": "compiled",
        }
