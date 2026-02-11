"""
Radial_Genesis_Engine - Genesis_Selector
Deterministic configuration evaluation and selection.
"""

from typing import Any, Dict

from ..Core.Topology_State import TopologyState


class GenesisSelector:
    def __init__(self, scoring_module=None) -> None:
        self.scoring_module = scoring_module

    def evaluate_configuration(self, state_snapshot: Dict[str, Any]) -> float:
        if self.scoring_module:
            return self.scoring_module.compute_score(state_snapshot)
        return 0.0

    def _config_id(self, config: TopologyState) -> str:
        """
        Canonical deterministic ID for tie-breaking.
        """
        ordered_agents = sorted(config.agent_assignments.items())
        assignment_str = "|".join(f"{key}:{value}" for key, value in ordered_agents)
        return f"R{config.rotation_index}|{assignment_str}"

    def select_best(self) -> TopologyState | None:
        all_configs = TopologyState.enumerate_all_configurations()

        best_score = float("inf")
        best_config = None
        best_id = None

        for config in all_configs:
            score = self.evaluate_configuration(config.snapshot())
            config_id = self._config_id(config)

            if (score < best_score) or (score == best_score and config_id < best_id):
                best_score = score
                best_config = config
                best_id = config_id

        return best_config
