# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: pxl_symbol_key
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Tools/formal_logic_enrichment/pxl_symbol_key.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Tools/formal_logic_enrichment/pxl_symbol_key.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
PXL symbol key.

Provides minimal primitives and operators for enrichment-only emission.
No proof, no validation, no admissibility checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PXLPrimitive:
    symbol: str
    name: str
    description: str


@dataclass(frozen=True)
class PXLOperator:
    symbol: str
    name: str
    description: str


PXL_SYMBOL_KEY: Dict[str, Dict[str, str]] = {
    "primitives": {
        "E": "existence",
        "G": "goodness",
        "T": "truth",
        "U": "unity",
    },
    "operators": {
        "~": "negation",
        "&": "conjunction",
        "|": "disjunction",
        "->": "implication",
        "<->": "biconditional",
        "forall": "universal_quantifier",
        "exists": "existential_quantifier",
    },
}


def get_primitive(symbol: str) -> PXLPrimitive:
    name = PXL_SYMBOL_KEY["primitives"].get(symbol, "unknown")
    return PXLPrimitive(symbol=symbol, name=name, description=f"PXL primitive {name}")


def get_operator(symbol: str) -> PXLOperator:
    name = PXL_SYMBOL_KEY["operators"].get(symbol, "unknown")
    return PXLOperator(symbol=symbol, name=name, description=f"PXL operator {name}")
