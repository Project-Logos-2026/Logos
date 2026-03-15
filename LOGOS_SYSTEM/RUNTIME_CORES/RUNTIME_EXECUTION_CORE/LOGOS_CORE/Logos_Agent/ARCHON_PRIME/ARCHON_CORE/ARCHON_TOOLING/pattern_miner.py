"""
Knowledge Pattern Miner
Identifies recurring naming and structural patterns across all Python
files in the repository.

Surfaces the most frequent function names (likely canonical design
patterns) and the most imported external modules (dependency heat-map).
"""

from collections import Counter
from pathlib import Path
from typing import List, Tuple
import ast


class PatternMiner:

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)

    def mine(self, top_n: int = 20) -> dict:
        """
        Mine recurring function-name and import patterns.

        Parameters
        ----------
        top_n : number of top results to return for each category

        Returns
        -------
        dict with keys:
            function_patterns  - list of (name, count) for repeated function names
            import_patterns    - list of (module, count) for most-imported modules
        """
        function_names: List[str] = []
        import_targets: List[str] = []

        for file in self.repo_root.rglob("*.py"):
            try:
                source = file.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(source)
            except Exception:
                continue

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    function_names.append(node.name)

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        import_targets.append(alias.name.split(".")[0])

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        import_targets.append(node.module.split(".")[0])

        return {
            "function_patterns": Counter(function_names).most_common(top_n),
            "import_patterns": Counter(import_targets).most_common(top_n),
        }
