# File: MSPC_Config.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Runtime configuration for the MSPC protocol. Defines all tunable
#   parameters, execution mode toggles, and invariant thresholds.
#   Configuration is immutable once loaded for a given session.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ExecutionMode(Enum):
    CONTINUOUS = "continuous"
    ON_DEMAND = "on_demand"
    HYBRID = "hybrid"


class FailurePolicy(Enum):
    HALT = "halt"
    DISCARD_AND_LOG = "discard_and_log"


@dataclass(frozen=True)
class MSPCConfig:
    execution_mode: ExecutionMode = ExecutionMode.ON_DEMAND
    tick_interval_seconds: float = 1.0
    max_signals_per_tick: int = 256
    max_compilation_depth: int = 64
    max_pending_signals: int = 4096
    conflict_resolution_timeout_seconds: float = 5.0
    failure_policy: FailurePolicy = FailurePolicy.HALT
    enable_telemetry: bool = True
    enable_audit_log: bool = True
    artifact_hash_algorithm: str = "sha256"
    artifact_version_prefix: str = "mspc-v"
    backpressure_threshold: float = 0.85
    session_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


def load_config(overrides: Optional[Dict[str, Any]] = None) -> MSPCConfig:
    base = {}
    if overrides:
        for k, v in overrides.items():
            if k == "execution_mode" and isinstance(v, str):
                base[k] = ExecutionMode(v)
            elif k == "failure_policy" and isinstance(v, str):
                base[k] = FailurePolicy(v)
            else:
                base[k] = v
    return MSPCConfig(**base)
