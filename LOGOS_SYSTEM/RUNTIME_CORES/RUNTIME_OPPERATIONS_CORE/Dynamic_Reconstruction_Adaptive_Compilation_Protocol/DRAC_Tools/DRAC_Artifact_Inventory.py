"""
Artifact Inventory Tool
Tracks assembly artifacts without semantic inspection.
"""

from typing import Dict


class ArtifactInventory:
    def __init__(self):
        self._artifacts: Dict[str, str] = {}

    def register(self, artifact_id: str, artifact_type: str) -> None:
        self._artifacts[artifact_id] = artifact_type

    def list_all(self) -> Dict[str, str]:
        return dict(self._artifacts)

    def count(self) -> int:
        return len(self._artifacts)
