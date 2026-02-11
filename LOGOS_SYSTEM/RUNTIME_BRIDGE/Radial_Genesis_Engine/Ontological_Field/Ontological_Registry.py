"""
Ontological Field Registry.
Loads canonical 29-property complex anchors for evaluation.
"""

import json


class OntologicalRegistry:
    def __init__(self, json_path: str | None = None) -> None:
        self.properties: dict = {}
        if json_path:
            self.load(json_path)

    def load(self, json_path: str) -> None:
        with open(json_path, "r", encoding="utf-8") as file_handle:
            self.properties = json.load(file_handle)

    def get_property(self, name: str):
        return self.properties.get(name)
