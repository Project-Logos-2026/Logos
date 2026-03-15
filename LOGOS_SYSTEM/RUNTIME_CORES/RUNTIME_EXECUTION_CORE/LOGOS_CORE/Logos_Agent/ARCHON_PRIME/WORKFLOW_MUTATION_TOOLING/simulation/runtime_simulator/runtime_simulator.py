"""
ARCHON PRIME — Runtime Boot Simulator
Stage 3: Simulation System Activation

Reads dependency graph and structure map artifacts produced by Stage-2
and simulates repository runtime boot sequence.
Read-only — no mutations performed.
"""

import json
from pathlib import Path

ARTIFACT_INPUT_GRAPH = "AP_SYSTEM_AUDIT/dependency_graph.json"
ARTIFACT_INPUT_STRUCTURE = "AP_SYSTEM_AUDIT/structure_map.json"
ARTIFACT_OUTPUT = "AP_SYSTEM_AUDIT/runtime_boot_simulation.json"


def simulate(root: str = ".") -> dict:
    """
    Simulate runtime boot order from dependency graph and structure map.
    Returns simulation report dict.
    """
    root_path = Path(root)

    graph = _load_json(root_path / ARTIFACT_INPUT_GRAPH)
    structure = _load_json(root_path / ARTIFACT_INPUT_STRUCTURE)

    entry_points = []
    boot_order = []
    unresolvable = []

    if isinstance(graph, dict):
        for module, deps in graph.items():
            if not deps:
                entry_points.append(module)
        try:
            boot_order = _topological_sort(graph)
        except Exception as exc:
            unresolvable.append(str(exc))

    file_count = len(structure) if isinstance(structure, list) else 0

    report = {
        "simulation": "RuntimeBootSimulator",
        "artifact_inputs": [ARTIFACT_INPUT_GRAPH, ARTIFACT_INPUT_STRUCTURE],
        "entry_points_detected": entry_points,
        "boot_order_length": len(boot_order),
        "repository_file_count": file_count,
        "unresolvable": unresolvable,
        "status": "complete",
    }

    output_path = root_path / ARTIFACT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return report


def _load_json(path: Path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def _topological_sort(graph: dict) -> list:
    """Kahn's algorithm — returns modules in dependency resolution order."""
    in_degree = {n: 0 for n in graph}
    for _node, deps in graph.items():
        for d in deps or []:
            if d in in_degree:
                in_degree[d] = in_degree.get(d, 0) + 1

    queue = [n for n, deg in in_degree.items() if deg == 0]
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for dep in graph.get(node) or []:
            if dep in in_degree:
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)
    return order


if __name__ == "__main__":
    result = simulate()
    print(json.dumps(result, indent=2))
