#!/usr/bin/env python3
"""
ARCHON PRIME — Execution Surface Detector
==========================================
Identifies public execution surfaces in Python modules: CLI entry points,
HTTP/API handlers, event listeners, and exported public APIs. These are
the external-facing interfaces where execution can be triggered.
Writes: execution_surface.json
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

# Decorator patterns indicating HTTP/API handlers
API_DECORATORS = {"route", "get", "post", "put", "delete", "patch", "head", "options",
                  "app.route", "app.get", "app.post", "router.get", "router.post",
                  "handler", "endpoint", "api_view"}

# Decorator patterns for event handlers
EVENT_DECORATORS = {"on", "event", "listen", "subscriber", "receiver", "signal",
                    "on_event", "callback"}

# CLI-framework decorators
CLI_DECORATORS = {"command", "argument", "option", "click.command", "typer.command",
                  "subcommand", "cli.command"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon execution surface detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def decorator_name(dec: ast.expr) -> str:
    if isinstance(dec, ast.Name):
        return dec.id
    if isinstance(dec, ast.Attribute):
        return f"{decorator_name(dec.value)}.{dec.attr}"
    if isinstance(dec, ast.Call):
        return decorator_name(dec.func)
    return ""


def analyze_surface(path: Path, target: Path) -> dict:
    rel = str(path.relative_to(target))
    module = rel.removesuffix(".py").replace(os.sep, ".")
    result = {
        "file": rel,
        "module": module,
        "cli_entrypoints": [],
        "api_handlers": [],
        "event_handlers": [],
        "public_functions": [],
        "has_main_block": False,
        "all_block": [],
    }

    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception:
        return result

    # Check for __all__
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "__all__":
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        result["all_block"] = [
                            ast.unparse(elt) for elt in node.value.elts
                            if isinstance(elt, ast.Constant)
                        ]
        elif isinstance(node, ast.If):
            cond = ast.unparse(node.test)
            if "__name__" in cond and "__main__" in cond:
                result["has_main_block"] = True

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            dec_names = [decorator_name(d).lower() for d in node.decorator_list]
            is_api = any(d in API_DECORATORS or any(a in d for a in API_DECORATORS) for d in dec_names)
            is_event = any(d in EVENT_DECORATORS for d in dec_names)
            is_cli = any(d in CLI_DECORATORS or any(a in d for a in CLI_DECORATORS) for d in dec_names)
            is_public = not node.name.startswith("_")

            entry = {
                "name": node.name,
                "lineno": node.lineno,
                "decorators": [decorator_name(d) for d in node.decorator_list],
                "is_async": isinstance(node, ast.AsyncFunctionDef),
            }
            if is_cli:
                result["cli_entrypoints"].append(entry)
            elif is_api:
                result["api_handlers"].append(entry)
            elif is_event:
                result["event_handlers"].append(entry)
            elif is_public:
                result["public_functions"].append(node.name)

    return result


def run(target: Path, out_dir: Path) -> None:
    print(f"[execution_surface_detector] Scanning: {target}")
    modules = []
    totals = {"cli": 0, "api": 0, "event": 0, "main_block": 0}

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            info = analyze_surface(Path(root) / fn, target)
            totals["cli"] += len(info["cli_entrypoints"])
            totals["api"] += len(info["api_handlers"])
            totals["event"] += len(info["event_handlers"])
            if info["has_main_block"]:
                totals["main_block"] += 1
            modules.append(info)

    write_json(out_dir, "execution_surface.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_analyzed": len(modules),
        "summary": totals,
        "modules": modules,
    })
    print(f"  Files: {len(modules)}  CLI: {totals['cli']}  "
          f"API: {totals['api']}  Events: {totals['event']}  Main: {totals['main_block']}")


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
