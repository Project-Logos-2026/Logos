# File: Conflict_Resolver.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Detects contradictions among active signals, applies precedence
#   logic to resolve them, and produces resolved, blocked, and
#   escalation outputs. No compilation occurs until conflict
#   resolution passes.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

from Multi_Process_Signal_Compiler.Signals.Signal_Envelope import SignalEnvelope
from Multi_Process_Signal_Compiler.Resolution.Precedence_Rules import select_winner


@dataclass
class ResolutionResult:
    resolved: List[SignalEnvelope] = field(default_factory=list)
    blocked: List[SignalEnvelope] = field(default_factory=list)
    escalations: List[Dict[str, Any]] = field(default_factory=list)
    conflicts_detected: int = 0
    conflicts_resolved: int = 0


class ConflictResolver:
    def __init__(self) -> None:
        self._conflict_keys_extractor = _default_conflict_key

    def resolve(self, signals: List[SignalEnvelope]) -> ResolutionResult:
        result = ResolutionResult()

        if not signals:
            return result

        buckets: Dict[str, List[SignalEnvelope]] = {}
        no_key: List[SignalEnvelope] = []

        for sig in signals:
            key = self._conflict_keys_extractor(sig)
            if key is None:
                no_key.append(sig)
            else:
                buckets.setdefault(key, []).append(sig)

        result.resolved.extend(no_key)

        for key, group in buckets.items():
            if len(group) == 1:
                result.resolved.append(group[0])
                continue

            result.conflicts_detected += len(group) - 1

            winner = group[0]
            for candidate in group[1:]:
                winner = select_winner(winner, candidate)

            result.resolved.append(winner)
            result.conflicts_resolved += len(group) - 1

            for sig in group:
                if sig.signal_id != winner.signal_id:
                    result.blocked.append(sig)

            if len(group) > 2:
                result.escalations.append({
                    "conflict_key": key,
                    "signal_count": len(group),
                    "winner_id": winner.signal_id,
                    "blocked_ids": [
                        s.signal_id for s in group
                        if s.signal_id != winner.signal_id
                    ],
                })

        return result


def _default_conflict_key(envelope: SignalEnvelope) -> str | None:
    payload = envelope.payload
    target = payload.get("target")
    domain = payload.get("domain")
    if target and domain:
        return f"{domain}::{target}"
    if target:
        return f"_::{target}"
    return None
