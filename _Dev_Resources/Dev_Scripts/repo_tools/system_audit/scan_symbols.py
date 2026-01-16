#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from _common import iter_files, read_text, write_json
try:
    from ._diagnostic_record import diag
except ImportError:  # script execution fallback
    from _diagnostic_record import diag

def scan_symbols(repo: Path, targets: List[Path] | None = None) -> Dict[str, Any]:
    classes: List[Dict[str, Any]] = []
    functions: List[Dict[str, Any]] = []
    globals_: List[Dict[str, Any]] = []
    diagnostics: List[Dict[str, Any]] = []

    py_files = list(targets) if targets else list(iter_files(repo, suffix=".py"))
    for p in py_files:
        src = read_text(p)
        try:
            tree = ast.parse(src, filename=str(p))
        except SyntaxError:
            diagnostics.append(diag(
                error_type="SyntaxError",
                line=1,
                char_start=0,
                char_end=0,
                details="failed to parse",
                source="scan_symbols",
            ))
            continue

        rel = str(p.relative_to(repo))

        # globals: top-level assignments
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = []
                if isinstance(node, ast.Assign):
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            targets.append(t.id)
                else:
                    if isinstance(node.target, ast.Name):
                        targets.append(node.target.id)
                for name in targets:
                    cs = getattr(node, "col_offset", 0)
                    ce = cs + len(name)
                    rec = diag(
                        error_type="GlobalDefinition",
                        line=getattr(node, "lineno", 0) or 1,
                        char_start=cs,
                        char_end=ce,
                        details=f"global {name}",
                        source="scan_symbols",
                    )
                    globals_.append({
                        **rec,
                        "file": rel,
                        "name": name,
                        "kind": type(node).__name__,
                    })

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = []
                for b in node.bases:
                    if isinstance(b, ast.Name):
                        bases.append(b.id)
                    elif isinstance(b, ast.Attribute):
                        bases.append(getattr(b, "attr", ""))
                    else:
                        bases.append(type(b).__name__)
                methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                cs = getattr(node, "col_offset", 0)
                ce = cs + len(node.name)
                rec = diag(
                    error_type="ClassDefinition",
                    line=getattr(node, "lineno", 0) or 1,
                    char_start=cs,
                    char_end=ce,
                    details=f"class {node.name}",
                    source="scan_symbols",
                )
                classes.append({
                    **rec,
                    "file": rel,
                    "line": getattr(node, "lineno", 0),
                    "class_name": node.name,
                    "bases": bases,
                    "methods": methods,
                    "decorators": [getattr(d, "id", getattr(d, "attr", type(d).__name__)) for d in node.decorator_list],
                })
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Only count top-level functions
                if isinstance(getattr(node, "parent", None), ast.ClassDef):
                    continue
                cs = getattr(node, "col_offset", 0)
                ce = cs + len(node.name)
                rec = diag(
                    error_type="FunctionDefinition",
                    line=getattr(node, "lineno", 0) or 1,
                    char_start=cs,
                    char_end=ce,
                    details=f"function {node.name}",
                    source="scan_symbols",
                )
                functions.append({
                    **rec,
                    "file": rel,
                    "line": getattr(node, "lineno", 0),
                    "function_name": node.name,
                    "args": [a.arg for a in node.args.args],
                    "decorators": [getattr(d, "id", getattr(d, "attr", type(d).__name__)) for d in node.decorator_list],
                    "async": isinstance(node, ast.AsyncFunctionDef),
                })

        # annotate parents to distinguish methods
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                setattr(child, "parent", parent)

    return {"classes": classes, "functions": functions, "globals": globals_, "diagnostics": diagnostics}

def main(argv=None) -> int:
    import sys

    args = argv if argv is not None else sys.argv[1:]
    repo = Path("/workspaces/Logos_System").resolve()
    if args:
        targets = [Path(a).resolve() for a in args]
        sym = scan_symbols(repo, targets)
        print(json.dumps(sym.get("diagnostics", []), indent=2))
        return 0

    base = Path("/workspaces/Logos_System/_Reports/SYSTEM_AUDIT/03_symbol_inventory")
    sym = scan_symbols(repo)
    write_json(base / "classes.json", sym["classes"])
    write_json(base / "functions.json", sym["functions"])
    write_json(base / "globals.json", sym["globals"])
    # placeholders (populated later by refactor tooling)
    write_json(base / "methods.json", {"note": "methods are included per-class in classes.json"})
    write_json(base / "deprecated_candidates.json", {"note": "populate after dead-code + import reachability analysis"})
    print(base)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
