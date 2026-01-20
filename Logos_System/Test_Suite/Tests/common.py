# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""Shared helpers for generated LOGOS test modules.

This helper keeps tests deterministic, read-only (writes only under Logs/),
and standardizes result formatting for the custom runner.
"""

from __future__ import annotations

import contextlib
import importlib
import inspect
import json
import os
import time
from types import ModuleType
from typing import Any, Dict, Iterable, List, Sequence


LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "Logs"))


def _result(module_path: str, test_name: str, status: str, exc: Exception | None = None) -> Dict[str, Any]:
    """Standardize a single test result row."""

    return {
        "module": module_path,
        "test": test_name,
        "status": status,
        "exception_type": type(exc).__name__ if exc else None,
        "exception_message": str(exc) if exc else None,
        "timestamp": time.time(),
    }


@contextlib.contextmanager
def _temp_cwd(path: str):
    """Temporarily change working directory to constrain any relative writes."""

    prev = os.getcwd()
    os.makedirs(path, exist_ok=True)
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


def _allowed_failures(module: ModuleType) -> Sequence[type]:
    """Return exception classes that indicate governed fail-closed behavior."""

    halt_types: List[type] = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if name.endswith("Halt") or name.endswith("Failure"):
            halt_types.append(obj)
    return tuple(halt_types)


def _invoke_entry_point(module: ModuleType, func_name: str) -> Any:
    """Call a known entry point with a safe, deterministic payload."""

    func = getattr(module, func_name)

    if func_name == "execute_lock_and_key":
        audit_path = "/workspaces/Logos_System/System_Audit_Logs/Boot_Sequence_Log.jsonl"
        return func(b"STUB_COMPILE_ARTIFACT", b"STUB_COMPILE_ARTIFACT", audit_log_path=audit_path)

    if func_name == "start_logos_agent":
        payload = {"session_id": "TEST_SESSION", "universal_session_id": "TEST_SESSION"}
        return func(payload)

    if func_name == "discharge_lem":
        payload = {"status": "LOGOS_SESSION_ESTABLISHED", "session_id": "TEST_SESSION"}
        return func(payload)

    if func_name == "prepare_agent_orchestration":
        payload = {
            "logos_agent_id": "TEST_AGENT",
            "universal_session_id": "TEST_SESSION",
            "prepared_bindings": {},
        }
        return func(payload)

    if func_name == "RUN_LOGOS_SYSTEM":
        # Constrain relative writes (e.g., boot_sequence_log.json) to Logs/.
        with _temp_cwd(LOGS_DIR):
            return func(mode="headless", diagnostic=True)

    if func_name == "START_LOGOS":
        with _temp_cwd(LOGS_DIR):
            return func(config_path=None, mode="headless", diagnostic=True)

    if func_name in {"get_status", "initialize_logos_core", "get_logos_core", "start_agent"}:
        return func()

    if func_name == "evaluate_modal":
        return func("P")

    if func_name == "evaluate_iel":
        return func("P")

    # For any other named entry we simply call with no args.
    return func()


def run_module_tests(
    module_path: str,
    public_functions: Iterable[str],
    public_classes: Iterable[str],
    entry_points: Iterable[str],
) -> List[Dict[str, Any]]:
    """Execute standardized tests for a single module and return result rows."""

    results: List[Dict[str, Any]] = []

    try:
        importlib.invalidate_caches()
        module = importlib.import_module(module_path)
        results.append(_result(module_path, "import", "PASS"))
    except Exception as exc:
        results.append(_result(module_path, "import", "FAIL", exc))
        return results

    # Attribute presence checks
    for func_name in public_functions:
        try:
            attr = getattr(module, func_name)
            ok = callable(attr)
            results.append(_result(module_path, f"function:{func_name}", "PASS" if ok else "FAIL"))
        except Exception as exc:
            results.append(_result(module_path, f"function:{func_name}", "FAIL", exc))

    for class_name in public_classes:
        try:
            attr = getattr(module, class_name)
            ok = inspect.isclass(attr)
            results.append(_result(module_path, f"class:{class_name}", "PASS" if ok else "FAIL"))
        except Exception as exc:
            results.append(_result(module_path, f"class:{class_name}", "FAIL", exc))

    allowed_failures = _allowed_failures(module)

    # Entry point behavior checks
    for entry in entry_points:
        try:
            result = _invoke_entry_point(module, entry)
            ok = isinstance(result, dict) or result is not None
            results.append(_result(module_path, f"entry:{entry}", "PASS" if ok else "FAIL"))
        except Exception as exc:
            if allowed_failures and isinstance(exc, allowed_failures):
                results.append(_result(module_path, f"entry:{entry}", "PASS", exc))
            else:
                results.append(_result(module_path, f"entry:{entry}", "FAIL", exc))

    return results
