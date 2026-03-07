"""
Radial_Genesis_Engine - RGE_Telemetry_Snapshot_V2 Contract
Immutable telemetry snapshot produced during RGE evaluation cycles.

Passive data structure only. No runtime logic, no mutation, no reasoning.
JSON-serializable. Compatible with CIF import standards.

Replaces: Contracts/RGE_Telemetry_Snapshot.py (V1, removed in Stage-0.5)
Reference: RGE_Design_Spec.md Section 2.1, Section 3.1
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class RGETelemetrySnapshotV2:
    """
    Immutable telemetry snapshot produced during RGE evaluation cycles.

    Captures scoring diagnostics and configuration metadata
    without performing reasoning or mutation.
    """

    configuration_id: str
    composite_score: float

    module_scores: Dict[str, float]

    completion_score: float
    completion_potential: float

    participant_count: int
    participant_diversity: float

    resonance_score: float
    novelty_score: float

    telemetry_tags: List[str]

    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "configuration_id": self.configuration_id,
            "composite_score": self.composite_score,
            "module_scores": self.module_scores,
            "completion_score": self.completion_score,
            "completion_potential": self.completion_potential,
            "participant_count": self.participant_count,
            "participant_diversity": self.participant_diversity,
            "resonance_score": self.resonance_score,
            "novelty_score": self.novelty_score,
            "telemetry_tags": self.telemetry_tags,
            "metadata": self.metadata,
        }
