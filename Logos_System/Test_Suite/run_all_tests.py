# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""Custom test runner for LOGOS System generated tests.

Discovers test_*.py modules under Test_Suite/Tests, executes their run_tests()
function, aggregates results, and writes machine-readable JSON to Logs/.
"""

from __future__ import annotations

import importlib
import json
import os
import pkgutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "Tests"
LOGS_DIR = ROOT / "Logs"
LOG_PATH = LOGS_DIR / "test_run_log.json"


def _ensure_paths() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    # Ensure repository root is on sys.path for imports.
    repo_root = ROOT.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def _discover_tests() -> List[str]:
    """Return fully qualified module names for test_*.py under Tests/."""

    prefix = "Test_Suite.Tests"
    discovered: List[str] = []
    for module_info in pkgutil.iter_modules([str(TESTS_DIR)]):
        if not module_info.name.startswith("test_"):
            continue
        discovered.append(f"{prefix}.{module_info.name}")
    return sorted(discovered)


def _run_module(module_name: str) -> List[Dict[str, Any]]:
    """Import a test module and execute its run_tests() function."""

    try:
        module = importlib.import_module(module_name)
    except Exception as exc:
        return [
            {
                "module": module_name,
                "test": "import",
                "status": "FAIL",
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "timestamp": time.time(),
            }
        ]

    run_tests = getattr(module, "run_tests", None)
    if not callable(run_tests):
        return [
            {
                "module": module_name,
                "test": "run_tests_missing",
                "status": "FAIL",
                "exception_type": None,
                "exception_message": "run_tests() not found",
                "timestamp": time.time(),
            }
        ]

    try:
        return run_tests()
    except Exception as exc:
        return [
            {
                "module": module_name,
                "test": "run_tests_execution",
                "status": "FAIL",
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "timestamp": time.time(),
            }
        ]


def main() -> None:
    _ensure_paths()
    results: List[Dict[str, Any]] = []

    for module_name in _discover_tests():
        results.extend(_run_module(module_name))

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    log_payload: Dict[str, Any] = {
        "run_timestamp": time.time(),
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_payload, f, indent=2)


if __name__ == "__main__":
    main()
