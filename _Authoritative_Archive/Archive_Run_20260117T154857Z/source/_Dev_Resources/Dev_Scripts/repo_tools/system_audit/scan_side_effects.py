#!/usr/bin/env python3
"""
Phase 4 — Side-effects scan (schema diagnostics)

Flags suspicious module-level calls (e.g., subprocess/os/requests/print/open) and
syntax errors. Non-mutating; intended for per-file CLI use in orchestrator. When
run without arguments, emits repository-wide report for legacy dashboards.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import List

from _common import iter_files, read_text, write_json
try:
    from ._diagnostic_record import diag
except ImportError:  # script execution fallback
    from _diagnostic_record import diag

SUSPICIOUS_FUNCS = {
    "print",
    "open",
    "os.system",
    "os.popen",
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "requests.get",
    "requests.post",
    "requests.put",
    "requests.delete",
    "httpx.get",
    "httpx.post",
    "sys.exit",
}

def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parts = []
        cur = node
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
        parts.reverse()
        return ".".join(parts)
    return ""

def scan_side_effects(repo: Path, targets: List[Path] | None = None) -> List[dict]:
    diags: List[dict] = []
    py_files = list(targets) if targets else list(iter_files(repo, suffix=".py"))
    for p in py_files:
        try:
            src = read_text(p)
        except Exception:
            continue
        try:
            tree = ast.parse(src, filename=str(p))
        except SyntaxError:
            diags.append(diag(
                error_type="SyntaxError",
                line=1,
                char_start=0,
                char_end=0,
                details="failed to parse",
                severity="high",
                source="scan_side_effects",
            ))
            continue

        lines = src.splitlines()
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                name = _call_name(node.value.func)
                if name in SUSPICIOUS_FUNCS:
                    lineno = getattr(node, "lineno", 1) or 1
                    cs = getattr(node, "col_offset", 0)
                    line_txt = lines[lineno - 1] if lineno - 1 < len(lines) else ""
                    ce = cs + len(line_txt.rstrip("\n")) if line_txt else cs
                    diags.append(diag(
                        error_type="SideEffect",
                        line=lineno,
                        char_start=cs,
                        char_end=ce,
                        details=f"module-level call {name}",
                        severity="high",
                        source="scan_side_effects",
                    ))
    return diags


def main(argv=None) -> int:
    import sys

    args = argv if argv is not None else sys.argv[1:]
    repo = Path("/workspaces/Logos_System").resolve()
    if args:
        targets = [Path(a).resolve() for a in args]
        diags = scan_side_effects(repo, targets)
        print(json.dumps(diags, indent=2))
        return 0

    base = Path("/workspaces/Logos_System/_Reports/SYSTEM_AUDIT/04_side_effects")
    diags = scan_side_effects(repo)
    write_json(base / "side_effects.json", diags)
    print(base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
