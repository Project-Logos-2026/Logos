"""
Dependency Resolver Tool
Validates declared dependency order without execution.
"""

from typing import Dict, List


def validate_dependency_order(
    phases: List[str],
    dependencies: Dict[str, List[str]]
) -> bool:
    seen = set()

    for phase in phases:
        required = dependencies.get(phase, [])
        if any(req not in seen for req in required):
            return False
        seen.add(phase)

    return True
