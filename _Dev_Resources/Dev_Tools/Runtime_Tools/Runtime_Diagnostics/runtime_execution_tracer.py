"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: runtime_execution_tracer.py
tool_category: Runtime_Diagnostics
tool_subcategory: live_execution_tracing

purpose:
Runtime execution tracer using sys.settrace. Records call edges between
LOGOS_SYSTEM modules during live execution of a target entry script.
Outputs a JSON trace log of all call events matching the target prefix.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python runtime_execution_tracer.py --entry-script STARTUP/START_LOGOS.py

output_artifacts:
runtime_execution_trace.json

dependencies:
sys, json, argparse, pathlib, runpy

safety_classification:
READ_ONLY
"""

import sys
import json
import argparse
import runpy
from pathlib import Path

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


class ExecutionTracer:
    """Collects call-edge records via sys.settrace."""

    def __init__(self, target_prefix: str) -> None:
        self.target_prefix = target_prefix
        self.call_edges: list[dict] = []
        self._call_stack: list[str] = []

    def trace_calls(self, frame, event: str, _arg):
        filename = frame.f_code.co_filename
        qualname = frame.f_code.co_qualname if hasattr(frame.f_code, "co_qualname") else frame.f_code.co_name

        if self.target_prefix and self.target_prefix not in filename:
            return self.trace_calls  # keep tracing but don't record

        module = frame.f_globals.get("__name__", "<unknown>")
        func = qualname

        if event == "call":
            caller = self._call_stack[-1] if self._call_stack else None
            edge = {
                "event": "call",
                "module": module,
                "function": func,
                "file": filename,
                "line": frame.f_lineno,
                "caller": caller,
            }
            self.call_edges.append(edge)
            self._call_stack.append(f"{module}.{func}")

        elif event == "return":
            if self._call_stack:
                self._call_stack.pop()

        return self.trace_calls


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Runtime execution tracer via sys.settrace."
    )
    parser.add_argument(
        "--entry-script",
        required=True,
        help="Entry-point .py file to execute and trace (relative to repo root).",
    )
    parser.add_argument(
        "--target-prefix",
        default="LOGOS_SYSTEM",
        help="Only record calls from files containing this path substring (default: LOGOS_SYSTEM).",
    )
    parser.add_argument(
        "--repo-root",
        default="/workspaces/Logos",
        help="Repository root (default: /workspaces/Logos).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    entry = repo_root / args.entry_script

    if not entry.exists():
        print(f"ERROR: Entry script not found: {entry}")
        raise SystemExit(1)

    tracer = ExecutionTracer(target_prefix=args.target_prefix)

    print(f"Tracing execution of: {entry}")
    print(f"Target prefix filter: '{args.target_prefix}'")

    sys.settrace(tracer.trace_calls)
    try:
        runpy.run_path(str(entry), run_name="__main__")
    except SystemExit:
        pass
    except Exception as exc:
        print(f"  Warning: entry script raised {type(exc).__name__}: {exc}")
    finally:
        sys.settrace(None)

    report = {
        "tool": "runtime_execution_tracer",
        "entry_script": str(entry.relative_to(repo_root)),
        "target_prefix": args.target_prefix,
        "total_call_edges": len(tracer.call_edges),
        "call_edges": tracer.call_edges,
    }
    write_report("runtime_execution_trace.json", report)
    print(f"Total call edges recorded: {len(tracer.call_edges)}")


if __name__ == "__main__":
    main()
