"""
LOGOS ARCHON RUNTIME ENTRYPOINT
Provides a controlled interface for invoking Archon Prime analysis.
"""

from ..archon_bridge import ArchonBridge

_archon = ArchonBridge()


def run_archon_scan(target_path: str):
    """
    Execute Archon analysis on a repository path.
    """
    return _archon.run_archon_analysis(target_path)
