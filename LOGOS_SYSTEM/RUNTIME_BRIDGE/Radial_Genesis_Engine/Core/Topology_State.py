"""
Radial_Genesis_Engine - Topology_State
Deterministic radial topology model (D8 symmetry).
Includes configuration enumeration and invariant enforcement.
"""

from dataclasses import dataclass
import itertools
from typing import Dict, List

PROTOCOL_COUNT = 8
AXIS_COUNT = 4
AGENTS = ["I1", "I2", "I3", "LOGOS"]
AXES = ["AXIS_0", "AXIS_1", "AXIS_2", "AXIS_3"]


@dataclass
class TopologyState:
    rotation_index: int  # 0-7
    agent_assignments: Dict[str, str]  # agent_id -> axis_id

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not (0 <= self.rotation_index < PROTOCOL_COUNT):
            raise ValueError("Invalid rotation_index")

        if set(self.agent_assignments.keys()) != set(AGENTS):
            raise ValueError("All agents must be assigned")

        if len(set(self.agent_assignments.values())) != AXIS_COUNT:
            raise ValueError("Each axis must have exactly one agent")

    def rotate_left(self) -> None:
        self.rotation_index = (self.rotation_index - 1) % PROTOCOL_COUNT

    def rotate_right(self) -> None:
        self.rotation_index = (self.rotation_index + 1) % PROTOCOL_COUNT

    def snapshot(self) -> Dict[str, Dict[str, str] | int]:
        return {
            "rotation_index": self.rotation_index,
            "agent_assignments": self.agent_assignments.copy(),
        }

    @staticmethod
    def enumerate_all_configurations() -> List["TopologyState"]:
        configs: List[TopologyState] = []
        for rotation in range(PROTOCOL_COUNT):
            for perm in itertools.permutations(AXES):
                assignments = dict(zip(AGENTS, perm))
                configs.append(TopologyState(rotation, assignments))
        return configs
