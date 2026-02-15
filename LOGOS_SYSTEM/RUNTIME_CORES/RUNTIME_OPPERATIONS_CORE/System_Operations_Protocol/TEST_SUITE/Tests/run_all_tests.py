# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""
LOGOS_MODULE_METADATA
---------------------
module_name: run_all_tests
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/TEST_SUITE/run_all_tests.py.
agent_binding: None
protocol_binding: None
runtime_classification: test_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/TEST_SUITE/run_all_tests.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""Custom test runner for LOGOS System generated tests.

Discovers test_*.py modules under Test_Suite/Tests, executes their run_tests()
function, aggregates results, and writes machine-readable JSON to Logs/.
"""


from . import test_agent_deployment_safety
from . import test_phase_d_runtime_spine
from . import common
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


# --- GOVERNED SKIP REGISTRY (REBUILD PHASE) ---
_SKIP_REGISTRY_PATH = ROOT / "skip_registry.json"
_SKIP_MODULES: Dict[str, str] = {}

if _SKIP_REGISTRY_PATH.exists():
    try:
        _data = json.loads(_SKIP_REGISTRY_PATH.read_text())
    except Exception:
        _data = {}
    for group in _data.values():
        for mod in group.get("modules", []):
            _SKIP_MODULES[mod] = group.get("reason", "Skipped by registry")


def _skip_reason(err_msg: str) -> str | None:
    """Return skip reason if the error message references a known missing module."""

    for mod, reason in _SKIP_MODULES.items():
        if mod in err_msg:
            return reason
    return None
# --- END GOVERNED SKIP REGISTRY ---


def _ensure_paths() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    # assume canonical imports; no sys.path manipulation


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
    static_registry = {
        "Test_Suite.Tests.test_agent_deployment_safety": test_agent_deployment_safety,
        "Test_Suite.Tests.test_phase_d_runtime_spine": test_phase_d_runtime_spine,
        "Test_Suite.Tests.common": common,
    }
    module = static_registry.get(module_name)
    if module is None:
        return [{
            "module": module_name,
            "test": "import",
            "status": "SKIP",
            "exception_type": "ModuleNotFoundError",
            "exception_message": f"Module {module_name} not found in static registry.",
            "timestamp": time.time(),
        }]
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
        reason = _skip_reason(str(exc))
        status = "SKIP" if reason else "FAIL"
        msg = reason if reason else str(exc)
        return [
            {
                "module": module_name,
                "test": "run_tests_execution",
                "status": status,
                "exception_type": type(exc).__name__,
                "exception_message": msg,
                "timestamp": time.time(),
            }
        ]


def main() -> None:
    _ensure_paths()
    results: List[Dict[str, Any]] = []

    for module_name in _discover_tests():
        results.extend(_run_module(module_name))

    # Normalize governed skips for any failures emitted by downstream tests.
    for entry in results:
        if entry.get("status") != "FAIL":
            continue
        reason = _skip_reason(str(entry.get("exception_message", "")))
        if reason:
            entry["status"] = "SKIP"
            entry["exception_message"] = reason

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    failed = total - passed - skipped

    log_payload: Dict[str, Any] = {
        "run_timestamp": time.time(),
        "total_tests": total,
        "passed": passed,
        "skipped": skipped,
        "failed": failed,
        "results": results,
    }

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_payload, f, indent=2)


if __name__ == "__main__":
    main()
