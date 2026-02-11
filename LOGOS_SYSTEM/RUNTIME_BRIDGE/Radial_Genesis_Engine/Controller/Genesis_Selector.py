"""
Radial_Genesis_Engine - Genesis_Selector
Deterministic configuration evaluation and selection.
References: GENESIS_SELECTOR_STATE_MACHINE.md, RGE_SOVEREIGNTY_CONTRACT.md
"""

from typing import Any, Dict

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.Mode_Controller import (
    ModeController,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.RGE_Override_Channel import (
    RGEOverrideChannel,
)

from ..Core.Topology_State import TopologyState


class GenesisSelector:
    """
    Deterministic selector with Runtime_Bridge governance hooks.
    References: GENESIS_SELECTOR_STATE_MACHINE.md
    """

    def __init__(
        self,
        scoring_module=None,
        mode_controller: ModeController | None = None,
        override_channel: RGEOverrideChannel | None = None,
    ) -> None:
        self.scoring_module = scoring_module
        self.mode_controller = mode_controller
        self.override_channel = override_channel
        self._retained_state: Dict[str, Any] = {}
        self._infeasible_config_ids: set[str] = set()

    def evaluate_configuration(self, state_snapshot: Dict[str, Any]) -> float:
        if self.scoring_module:
            return self.scoring_module.compute_score(state_snapshot)
        return 0.0

    def reset_retained_state(self) -> None:
        self._retained_state.clear()
        self._infeasible_config_ids.clear()

    def mark_configuration_infeasible(self, config: TopologyState) -> None:
        self._infeasible_config_ids.add(self._config_id(config))

    def _config_id(self, config: TopologyState) -> str:
        """
        Canonical deterministic ID for tie-breaking.
        """
        ordered_agents = sorted(config.agent_assignments.items())
        assignment_str = "|".join(f"{key}:{value}" for key, value in ordered_agents)
        return f"R{config.rotation_index}|{assignment_str}"

    def select_best(self) -> TopologyState | None:
        if self.mode_controller and not self.mode_controller.is_activation_allowed():
            return None

        all_configs = TopologyState.enumerate_all_configurations()

        best_score = float("inf")
        best_config = None
        best_id = None

        for config in all_configs:
            if self.override_channel and self.override_channel.should_yield():
                if self.override_channel.is_hard_override():
                    self.reset_retained_state()
                return None

            if self._config_id(config) in self._infeasible_config_ids:
                continue

            score = self.evaluate_configuration(config.snapshot())
            config_id = self._config_id(config)

            if (score < best_score) or (score == best_score and config_id < best_id):
                best_score = score
                best_config = config
                best_id = config_id

        return best_config
