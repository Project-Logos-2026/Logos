# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: iterative_loop
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
  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_transform/iterative_loop.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .transform_registry import TransformRegistry, default_registry
from .transform_types import TransformOutcome, TransformStep


@dataclass(frozen=True)
class LoopConfig:
    max_iters: int = 3
    stop_on_no_change: bool = True


def run_iterative_stabilization(
    *,
    payload: Any,
    context: Dict[str, Any],
    registry: Optional[TransformRegistry] = None,
    config: Optional[LoopConfig] = None,
) -> TransformOutcome:
    """
    Bounded iterative stabilization loop.
    Applies default safe transforms in a fixed order unless overridden.
    No heavy reasoning. No hallucination. No rebuilds.
    """
    reg = registry or default_registry()
    cfg = config or LoopConfig()

    steps: List[TransformStep] = []
    cur = payload
    changed_any = False

    order = ["normalize", "reframe", "decompose", "annotate"]

    for _ in range(max(1, cfg.max_iters)):
        iter_changed = False

        for name in order:
            fn = reg.get(name)
            if not fn:
                continue
            new_cur, step = fn(cur, context)
            steps.append(step)
            if step.applied and new_cur is not cur:
                cur = new_cur
                iter_changed = True
                changed_any = True

        if cfg.stop_on_no_change and not iter_changed:
            break

    score_vector = {
        "coherence": 0.0,
        "conservation": 1.0 if changed_any else 0.8,
        "feasibility": 0.8,
    }

    status = "ok" if changed_any else "partial"
    summary = "Applied safe stabilization transforms." if changed_any else "No eligible transforms changed the payload."

    return TransformOutcome(
        payload=cur,
        steps=steps,
        score_vector=score_vector,
        status=status,
        summary=summary,
    )
