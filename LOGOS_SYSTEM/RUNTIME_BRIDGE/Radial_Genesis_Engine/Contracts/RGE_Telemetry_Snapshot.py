"""
Radial_Genesis_Engine - RGE_Telemetry_Snapshot Contract
Immutable telemetry snapshot for RGE integration.
Conforms to Phase_5_Hysteresis_Formalization.md and contract spec.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass(frozen=True)
class RGE_Telemetry_Snapshot:
    task_id: str
    tick_id: int
    triad: Tuple[float, float, float]
    raw_counts: Tuple[int, int, int]
    commutation_residuals: Dict[str, float]
    stability_scalars: Dict[str, float]

    def __post_init__(self):
        # Validate floats in [0,1]
        for idx, v in enumerate(self.triad):
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"triad[{idx}] out of bounds: {v}")
        for k, v in self.commutation_residuals.items():
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"commutation_residuals[{k}] out of bounds: {v}")
        for k, v in self.stability_scalars.items():
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"stability_scalars[{k}] out of bounds: {v}")
        # Validate required fields
        if not self.task_id or self.tick_id is None:
            raise ValueError("Missing required fields in RGE_Telemetry_Snapshot")
        if len(self.triad) != 3 or len(self.raw_counts) != 3:
            raise ValueError("Triad and raw_counts must be length 3")
        if not self.commutation_residuals or not self.stability_scalars:
            raise ValueError("Missing commutation_residuals or stability_scalars")
