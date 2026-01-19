from __future__ import annotations
# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: check_run_cycle_prereqs
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/System_Operations_Protocol/Optimization/check_run_cycle_prereqs.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""Quick diagnostic for tooling required by tools/run_cycle.sh."""


import importlib
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
repo_str = str(REPO_ROOT)
if repo_str not in sys.path:
    sys.path.insert(0, repo_str)

LOGOS_AGI_PATH = REPO_ROOT / "external" / "Logos_AGI"
if LOGOS_AGI_PATH.exists():
    logos_str = str(LOGOS_AGI_PATH)
    if logos_str not in sys.path:
        sys.path.insert(0, logos_str)

try:
    from LOGOS_AGI.settings import analytics as analytics_settings
except ImportError:  # pragma: no cover - settings optional during early bootstrap
    analytics_settings = None

REQUIRED = {
    "numpy": "Install via `pip install numpy` to enable fractal toolkit imports.",
}

OPTIONAL = {
    "requests": "Used by ARP external validation hooks.",
    "yaml": "Enables SOP configuration parsing (PyYAML).",
    "pandas": "Powers analytics dataframes for SCP/ARP reporting.",
    "statsmodels": "Provides regression and correlation tooling for analytics.",
    "LOGOS_AGI.analytics": (
        "Shared analytics helpers; ensures regression adapters import cleanly."
    ),
    "System_Operations_Protocol.infrastructure.agent_system.base_nexus": (
        "Confirms LOGOS_AGI stack is importable for nexus operations."
    ),
    "plugins.enhanced_uip_integration_plugin": (
        "Optional UIP plugin; absence logs warnings."
    ),
    "plugins.uip_integration_plugin": (
        "Optional UIP plugin; absence just logs warnings."
    ),
}


def _check(modules: Iterable[str]) -> dict[str, bool]:
    status: dict[str, bool] = {}
    for name in modules:
        try:
            importlib.import_module(name)
        except ModuleNotFoundError:
            status[name] = False
        else:
            status[name] = True
    return status


def main() -> int:
    required = _check(REQUIRED)
    optional = _check(OPTIONAL)

    missing_required = [name for name, ok in required.items() if not ok]
    missing_optional = [name for name, ok in optional.items() if not ok]

    if missing_required:
        print("Missing required modules:")
        for name in missing_required:
            print(f"  - {name}: {REQUIRED[name]}")
    else:
        print("All required modules available.")

    if missing_optional:
        print("\nOptional modules not found (functionality degraded but not fatal):")
        for name in missing_optional:
            print(f"  - {name}: {OPTIONAL[name]}")
    else:
        print("\nAll optional modules available.")

    try:
        from LOGOS_AGI.analytics import capabilities
    except ImportError:
        print("\nAnalytics helpers unavailable (LOGOS_AGI.analytics import failed).")
    else:
        caps = capabilities()
        print("\nAnalytics capability summary:")
        if analytics_settings is not None:
            print(f"  - analytics enabled: {analytics_settings.ENABLE_ANALYTICS}")
            print(f"  - statsmodels toggle: {analytics_settings.ENABLE_STATS_MODELS}")
        print(f"  - pandas: {caps.pandas}")
        print(f"  - statsmodels: {caps.statsmodels}")
        print(f"  - full stack ready: {caps.available}")

    return 1 if missing_required else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCheck interrupted.")
        sys.exit(130)
