"""
Semantic Repository Graph Builder
Constructs a directed semantic graph of all Python modules in the repo:
  nodes  — module paths and function-definition symbols
  edges  — import relationships and definition relationships
"""

import ast
from pathlib import Path
from collections import defaultdict


class SemanticRepoGraph:

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.nodes: set = set()
        self.edges: dict = defaultdict(list)

    def build(self) -> dict:
        """
        Walk every .py file under repo_root and build the graph.

        Returns
        -------
        dict with keys:
            nodes  - list of module paths and function symbols
            edges  - dict mapping module -> list of (rel, target) tuples
        """
        for file in self.repo_root.rglob("*.py"):
            self._analyze_file(file)

        return {
            "nodes": list(self.nodes),
            "edges": dict(self.edges),
        }

    def _analyze_file(self, file: Path) -> None:
        try:
            source = file.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source)
        except Exception:
            return

        module = str(file.relative_to(self.repo_root))
        self.nodes.add(module)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.edges[module].append(("imports", alias.name))

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.edges[module].append(("imports", node.module))

            elif isinstance(node, ast.FunctionDef):
                symbol = f"{module}:{node.name}"
                self.nodes.add(symbol)
                self.edges[module].append(("defines", node.name))
