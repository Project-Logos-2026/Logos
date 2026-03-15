"""
Function Primitive Extractor
Walks all Python files in the repo and extracts every function primitive:
  name, file, argument list, and line number.
"""

import ast
from pathlib import Path


class PrimitiveExtractor:

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.primitives: list = []

    def extract(self) -> list:
        """
        Extract all function primitives from the repository.

        Returns
        -------
        list of dicts, each with keys: name, file, args, line
        """
        for file in self.repo_root.rglob("*.py"):
            self._analyze_file(file)

        return self.primitives

    def _analyze_file(self, file: Path) -> None:
        try:
            source = file.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source)
        except Exception:
            return

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                primitive = {
                    "name": node.name,
                    "file": str(file),
                    "args": [a.arg for a in node.args.args],
                    "line": node.lineno,
                }
                self.primitives.append(primitive)
