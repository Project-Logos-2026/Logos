"""
Phase Tracker Tool
Pure utility for external systems to query DRAC state.
"""

from typing import List
from DRAC.CORE.DRAC_Core import DRACPhaseState


def summarize_phases(phases: List[DRACPhaseState]) -> dict:
    return {
        "completed": [p.phase_id for p in phases if p.status == "COMPLETED"],
        "incomplete": [p.phase_id for p in phases if p.status != "COMPLETED"],
        "total": len(phases),
    }
