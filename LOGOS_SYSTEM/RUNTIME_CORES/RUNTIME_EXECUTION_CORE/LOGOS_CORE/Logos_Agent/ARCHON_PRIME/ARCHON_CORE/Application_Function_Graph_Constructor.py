"""
Application_Function_Graph_Constructor
Builds the execution topology from a codebase.

Parses Python source and maps every function definition and its
direct call dependencies into a DRAC execution graph.
"""

import ast


class ApplicationFunctionGraphConstructor:

    def build(self, source_code: str):
        tree = ast.parse(source_code)
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "line_start": node.lineno,
                    "dependencies": self._calls(node),
                })

        return functions

    def _calls(self, node: ast.FunctionDef):
        calls = []
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                if hasattr(sub.func, "id"):
                    calls.append(sub.func.id)
        return calls
