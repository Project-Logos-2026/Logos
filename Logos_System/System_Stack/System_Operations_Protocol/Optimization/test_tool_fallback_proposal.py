# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_tool_fallback_proposal
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
  source: System_Stack/System_Operations_Protocol/Optimization/test_tool_fallback_proposal.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""Ensure failed tools surface fallback proposals without execution."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.start_agent import RuntimeContext, dispatch_tool


def main() -> int:
    os.environ["LOGOS_ENABLE_WEB_RETRIEVAL"] = "0"
    ctx = RuntimeContext(attestation_hash="dev", mission_profile_hash="dev")
    ctx.objective_class = "STATUS"
    payload = json.dumps({"url": ""})
    _ = dispatch_tool("retrieve.web", payload, ctx=ctx)

    proposals = ctx.fallback_proposals or []
    if not proposals:
        print("FAIL: no fallback proposal surfaced")
        return 1
    latest = proposals[-1]
    if latest.get("fallback_from") != "retrieve.web":
        print(f"FAIL: fallback_from mismatch: {latest}")
        return 1
    if len(ctx.tool_validation_events or []) != 1:
        print("FAIL: fallback triggered extra executions")
        return 1
    print("PASS: fallback proposal recorded without execution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
