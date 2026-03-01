# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0
# FILE: Topology_Context_Provider.py
# PATH: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Topology_Context_Provider.py
# PROJECT: LOGOS_SYSTEM
# PHASE: M6B
# STATUS: GOVERNED

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Topology_Context_Provider
runtime_layer: orchestration
role: Topology context bridge
responsibility: Pure data holder bridging RGE topology selection to MSPC compilation context. Written by orchestration layer. Read by MSPC. No direct RGE or MSPC coupling.
runtime_classification: orchestration_support
boot_phase: Phase-A-Integration
expected_imports: []
provides: [TopologyContextProvider]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Returns None on unset or invalid input. MSPC handles None gracefully."
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from typing import Any, Dict, Optional


class TopologyContextProvider:
    """
    Pure data holder for RGE topology selection.
    """

    def __init__(self) -> None:
        self._current_context: Optional[Dict[str, Any]] = None

    def set_topology(self, rge_result: Optional[Dict[str, Any]]) -> None:
        if rge_result is None:
            self._current_context = None
            return

        if not rge_result.get("selected", False):
            self._current_context = None
            return

        self._current_context = rge_result.get("topology")

    def get_topology_context(self) -> Optional[Dict[str, Any]]:
        return self._current_context

    def clear(self) -> None:
        self._current_context = None
