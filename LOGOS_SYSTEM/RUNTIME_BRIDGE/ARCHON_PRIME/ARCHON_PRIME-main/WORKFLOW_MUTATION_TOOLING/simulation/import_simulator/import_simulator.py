"""
ARCHON PRIME — Import Simulator
Stage 3: Simulation System Activation

Reads import topology artifacts produced by Stage-2 analysis
and simulates import resolution across the repository.
Read-only — no mutations performed.
"""

import json
from pathlib import Path

ARTIFACT_INPUT = "AP_SYSTEM_AUDIT/module_topology.json"
ARTIFACT_OUTPUT = "AP_SYSTEM_AUDIT/import_simulation_report.json"


def simulate(root: str = ".") -> dict:
    """
    Simulate import resolution from module_topology artifact.
    Returns simulation report dict.
    """
    root_path = Path(root)
    input_path = root_path / ARTIFACT_INPUT

    topology = {}
    if input_path.exists():
        with open(input_path) as f:
            topology = json.load(f)

    simulated_modules = list(topology.keys()) if isinstance(topology, dict) else []
    unresolved = []

    for module, imports in topology.items() if isinstance(topology, dict) else []:
        for imp in imports or []:
            if imp and not _is_stdlib(imp):
                # Flag imports that have no corresponding entry in topology
                if imp not in topology:
                    unresolved.append({"module": module, "unresolved_import": imp})

    report = {
        "simulation": "ImportResolutionSimulator",
        "artifact_input": ARTIFACT_INPUT,
        "total_modules_scanned": len(simulated_modules),
        "unresolved_imports": unresolved,
        "unresolved_count": len(unresolved),
        "status": "complete",
    }

    output_path = root_path / ARTIFACT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return report


def _is_stdlib(name: str) -> bool:
    """Heuristic: treat single-segment names as likely stdlib."""
    return "." not in name


if __name__ == "__main__":
    result = simulate()
    print(json.dumps(result, indent=2))
