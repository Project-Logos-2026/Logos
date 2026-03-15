"""
ARCHON PRIME — Dependency Resolution Simulator
Stage 3: Simulation System Activation

Reads dependency graph artifact produced by Stage-2 analysis and
simulates dependency resolution to detect missing or conflicting deps.
Read-only — no mutations performed.
"""

import json
from pathlib import Path

ARTIFACT_INPUT = "AP_SYSTEM_AUDIT/dependency_graph.json"
ARTIFACT_OUTPUT = "AP_SYSTEM_AUDIT/dependency_simulation_report.json"


def simulate(root: str = ".") -> dict:
    """
    Simulate dependency resolution from dependency_graph artifact.
    Returns simulation report dict.
    """
    root_path = Path(root)
    input_path = root_path / ARTIFACT_INPUT

    graph = {}
    if input_path.exists():
        with open(input_path) as f:
            graph = json.load(f)

    missing_deps = []
    cycles_detected = []

    if isinstance(graph, dict):
        known = set(graph.keys())
        for module, deps in graph.items():
            for dep in deps or []:
                if dep and dep not in known:
                    missing_deps.append({"module": module, "missing_dependency": dep})

        # Simple cycle detection via DFS
        visited = set()
        rec_stack = set()

        def _has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            for dep in graph.get(node) or []:
                if dep not in graph:
                    continue
                if dep not in visited:
                    if _has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    cycles_detected.append({"cycle_at": node, "back_edge": dep})
                    return True
            rec_stack.discard(node)
            return False

        for mod in list(graph.keys()):
            if mod not in visited:
                _has_cycle(mod)

    report = {
        "simulation": "DependencyResolutionSimulator",
        "artifact_input": ARTIFACT_INPUT,
        "total_modules": len(graph) if isinstance(graph, dict) else 0,
        "missing_dependencies": missing_deps,
        "missing_dependency_count": len(missing_deps),
        "cycles_detected": cycles_detected,
        "cycle_count": len(cycles_detected),
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
