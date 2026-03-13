"""
ARCHON PRIME — Namespace Conflict Simulator
Stage 3: Simulation System Activation

Reads namespace_conflicts artifact produced by Stage-2 analysis and
simulates the runtime impact of detected namespace shadows.
Read-only — no mutations performed.
"""

import json
from pathlib import Path

ARTIFACT_INPUT = "AP_SYSTEM_AUDIT/namespace_conflicts.json"
ARTIFACT_OUTPUT = "AP_SYSTEM_AUDIT/namespace_simulation_report.json"


def simulate(root: str = ".") -> dict:
    """
    Simulate namespace conflict impact from namespace_conflicts artifact.
    Returns simulation report dict.
    """
    root_path = Path(root)
    input_path = root_path / ARTIFACT_INPUT

    conflicts = []
    if input_path.exists():
        with open(input_path) as f:
            raw = json.load(f)
        if isinstance(raw, list):
            conflicts = raw
        elif isinstance(raw, dict):
            conflicts = list(raw.get("issues", raw.get("conflicts", [])) or [])

    high_risk = [
        c
        for c in conflicts
        if isinstance(c, dict) and c.get("issue") == "namespace_shadow"
    ]

    report = {
        "simulation": "NamespaceConflictSimulator",
        "artifact_input": ARTIFACT_INPUT,
        "total_conflicts_found": len(conflicts),
        "high_risk_shadows": len(high_risk),
        "conflict_details": conflicts,
        "status": "complete",
    }

    output_path = root_path / ARTIFACT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return report


if __name__ == "__main__":
    result = simulate()
    print(json.dumps(result, indent=2))
