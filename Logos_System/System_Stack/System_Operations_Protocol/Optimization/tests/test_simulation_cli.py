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
module_name: test_simulation_cli
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
  source: System_Stack/System_Operations_Protocol/Optimization/tests/test_simulation_cli.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""Smoke tests for run_simulation_stub CLI."""


import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "run_simulation_stub.py"


def test_run_simulation_stub_writes_to_custom_log_dir() -> None:
    with TemporaryDirectory() as tmp:
        log_dir = Path(tmp)
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--steps",
                "2",
                "--no-ingest",
                "--log-dir",
                str(log_dir),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stderr
        stdout = result.stdout
        assert "[sim] wrote" in stdout
        log_file = log_dir / "gridworld_events.jsonl"
        assert log_file.exists()
        lines = log_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) >= 1
