# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: pxl_ambiguity_profile
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Tools/formal_logic_enrichment/pxl_ambiguity_profile.py.
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Tools/formal_logic_enrichment/pxl_ambiguity_profile.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
PXL ambiguity profile.

Records unresolved ambiguities without attempting resolution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AmbiguityProfile:
    sources: List[str] = field(default_factory=list)
    notes: Dict[str, Any] = field(default_factory=dict)

    def add(self, source: str, note: Any) -> None:
        self.sources.append(source)
        self.notes[source] = note

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sources": list(self.sources),
            "notes": dict(self.notes),
        }
