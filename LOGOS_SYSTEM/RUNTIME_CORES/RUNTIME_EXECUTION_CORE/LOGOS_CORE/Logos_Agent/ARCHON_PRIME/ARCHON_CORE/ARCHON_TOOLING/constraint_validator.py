"""
Architectural Constraint Validator
Scans the repository for constraint violations based on LOGOS layer rules.

Current rules
-------------
1. Runtime cores must not import dev tooling.
2. Governance modules must not import runtime execution modules directly.
3. No module may contain bare ``exec()`` or ``eval()`` calls.
"""

from pathlib import Path
from typing import List, Dict
import ast


class ConstraintValidator:

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)

    def validate(self) -> List[Dict]:
        """
        Run all constraint checks and return every violation found.

        Returns
        -------
        list of dicts:
            { "file": str, "rule": str, "issue": str, "line": int|None }
        """
        violations: List[Dict] = []
        for file in self.repo_root.rglob("*.py"):
            try:
                text = file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            path_str = str(file)

            # Rule 1 — Runtime cores must not reference dev tooling
            if "RUNTIME_CORES" in path_str and "DEV_TOOLS" in text:
                violations.append({
                    "file": path_str,
                    "rule": "R1",
                    "issue": "Runtime core importing dev tooling",
                    "line": None,
                })

            # Rule 2 — Governance modules must not directly import runtime execution
            if "_Governance" in path_str and "RUNTIME_EXECUTION_CORE" in text:
                violations.append({
                    "file": path_str,
                    "rule": "R2",
                    "issue": "Governance module referencing runtime execution core",
                    "line": None,
                })

            # Rule 3 — No bare exec/eval (AST-level check)
            try:
                tree = ast.parse(text)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        func = node.func
                        name = (
                            func.id
                            if isinstance(func, ast.Name)
                            else getattr(func, "attr", None)
                        )
                        if name in ("exec", "eval"):
                            violations.append({
                                "file": path_str,
                                "rule": "R3",
                                "issue": f"Bare {name}() call detected",
                                "line": node.lineno,
                            })
            except SyntaxError:
                pass

        return violations
