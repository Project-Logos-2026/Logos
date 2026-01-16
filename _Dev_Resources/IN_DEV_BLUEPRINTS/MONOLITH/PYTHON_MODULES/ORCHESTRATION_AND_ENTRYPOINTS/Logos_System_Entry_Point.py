"""
LOGOS System Entry Point

NOTE:
- This is the sole public entrypoint for system startup.
- All legacy entrypoints are deprecated.
"""

from PYTHON_MODULES.ORCHESTRATION_AND_ENTRYPOINTS.BOOTSTRAP_PIPELINES.Canonical_System_Bootstrap_Pipeline import system_bootstrap


def main(initial_context: dict) -> dict:
    return system_bootstrap(initial_context)
