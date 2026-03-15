#!/usr/bin/env python3
"""
ARCHON PRIME — AST Symbol Extractor
======================================
Extracts all top-level and class-level symbols (functions, classes,
constants, type aliases) from every Python file in the target.
Writes: ast_symbol_index.json
"""
import argparse
import ast
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"
OUTPUT_ROOT = Path(os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT))
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
RUN_TS = datetime.now(timezone.utc).isoformat()

SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", ".mypy_cache"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon AST symbol extractor")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def annotation_to_str(node: ast.expr | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def extract_symbols(path: Path) -> list[dict]:
    symbols: list[dict] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception:
        return symbols

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [
                {"name": a.arg, "annotation": annotation_to_str(a.annotation)}
                for a in node.args.args
            ]
            symbols.append({
                "kind": "function",
                "name": node.name,
                "lineno": node.lineno,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
                "args": args,
                "return_annotation": annotation_to_str(node.returns),
                "decorators": [ast.unparse(d) for d in node.decorator_list],
                "docstring": ast.get_docstring(node),
                "is_private": node.name.startswith("_"),
            })
        elif isinstance(node, ast.ClassDef):
            bases = [ast.unparse(b) for b in node.bases]
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = [a.arg for a in item.args.args]
                    methods.append({
                        "name": item.name,
                        "lineno": item.lineno,
                        "args": args,
                        "is_property": any(
                            (ast.unparse(d) if hasattr(ast, "unparse") else "") == "property"
                            for d in item.decorator_list
                        ),
                    })
            symbols.append({
                "kind": "class",
                "name": node.name,
                "lineno": node.lineno,
                "bases": bases,
                "methods": methods,
                "docstring": ast.get_docstring(node),
                "is_private": node.name.startswith("_"),
            })
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    symbols.append({
                        "kind": "constant",
                        "name": target.id,
                        "lineno": node.lineno,
                    })
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            symbols.append({
                "kind": "annotated_var",
                "name": node.target.id,
                "lineno": node.lineno,
                "annotation": annotation_to_str(node.annotation),
            })
    return symbols


def run(target: Path, out_dir: Path) -> None:
    print(f"[ast_symbol_extractor] Scanning: {target}")
    results: list[dict] = []
    total_symbols = 0

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            fp = Path(root) / fn
            rel = str(fp.relative_to(target))
            symbols = extract_symbols(fp)
            total_symbols += len(symbols)
            results.append({
                "file": rel,
                "module": rel.removesuffix(".py").replace(os.sep, "."),
                "symbol_count": len(symbols),
                "symbols": symbols,
            })

    write_json(out_dir, "ast_symbol_index.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_processed": len(results),
        "total_symbols": total_symbols,
        "modules": results,
    })
    print(f"  Files: {len(results)}  Symbols: {total_symbols}")


def main() -> None:
    args = parse_args()
    target = Path(args.target).resolve()
    out_dir = Path(args.output)
    if not target.exists():
        print(f"[FATAL] Target not found: {target}", file=sys.stderr)
        sys.exit(1)
    run(target, out_dir)


if __name__ == "__main__":
    main()
