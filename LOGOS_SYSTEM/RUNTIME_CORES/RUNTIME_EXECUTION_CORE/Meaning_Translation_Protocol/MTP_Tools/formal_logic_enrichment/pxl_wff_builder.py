# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: pxl_wff_builder
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Tools/formal_logic_enrichment/pxl_wff_builder.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Tools/formal_logic_enrichment/pxl_wff_builder.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
PXL well-formed formula (WFF) builder.

Enrichment-only builder that preserves ambiguity. It constructs a minimal
syntax tree without validation or admissibility checks.
"""


from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .pxl_symbol_key import PXL_SYMBOL_KEY


@dataclass
class WFFNode:
    token: str
    children: List["WFFNode"]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "token": self.token,
            "children": [child.to_dict() for child in self.children],
            "metadata": self.metadata,
        }


class PXLWFFBuilder:
    """
    Build a shallow WFF tree from tokens.

    The builder does not enforce formation rules; it annotates unknown tokens
    and records ambiguity for downstream handling.
    """

    def __init__(self) -> None:
        self.symbol_key = PXL_SYMBOL_KEY

    def build(self, tokens: List[str]) -> WFFNode:
        root = WFFNode(token="ROOT", children=[], metadata={"role": "root"})
        for token in tokens:
            node = WFFNode(
                token=token,
                children=[],
                metadata=self._classify_token(token),
            )
            root.children.append(node)
        return root

    def _classify_token(self, token: str) -> Dict[str, Any]:
        if token in self.symbol_key["primitives"]:
            return {"type": "primitive", "label": self.symbol_key["primitives"][token]}
        if token in self.symbol_key["operators"]:
            return {"type": "operator", "label": self.symbol_key["operators"][token]}
        return {"type": "ambiguous", "label": "unknown"}
