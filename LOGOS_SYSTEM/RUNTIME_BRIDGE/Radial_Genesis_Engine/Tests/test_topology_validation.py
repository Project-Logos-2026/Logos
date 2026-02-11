"""
Internal deterministic validation tests for Radial Genesis Engine.
Supports direct execution.
"""

import sys
from pathlib import Path

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from LOGOS_SYSTEM.Runtime_Bridge.Radial_Genesis_Engine.Core.Topology_State import (
    TopologyState,
)


def run_tests() -> None:
    configs = TopologyState.enumerate_all_configurations()

    # Test 1: Configuration count
    assert len(configs) == 192, f"Expected 192 configs, got {len(configs)}"

    # Test 2: Uniqueness
    unique_snapshots = set()
    for config in configs:
        snapshot = str(config.snapshot())
        unique_snapshots.add(snapshot)

    assert len(unique_snapshots) == 192, "Duplicate configurations detected"

    print("Radial Genesis Engine validation passed.")


if __name__ == "__main__":
    run_tests()
