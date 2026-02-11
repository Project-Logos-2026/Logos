# File: Precedence_Rules.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Defines the precedence ordering used by the Conflict Resolver
#   to determine which signal takes priority when contradictions
#   are detected. Ordering is deterministic and derived from
#   authority level, confidence, and temporal recency.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

from Multi_Process_Signal_Compiler.Signals.Signal_Envelope import (
    AuthorityLevel,
    SignalEnvelope,
)

_AUTHORITY_RANK = {
    AuthorityLevel.SYSTEM: 0,
    AuthorityLevel.GOVERNANCE: 1,
    AuthorityLevel.PROTOCOL: 2,
    AuthorityLevel.AGENT: 3,
    AuthorityLevel.ADVISORY: 4,
    AuthorityLevel.UNCLASSIFIED: 5,
}


def authority_rank(envelope: SignalEnvelope) -> int:
    return _AUTHORITY_RANK.get(envelope.authority, 99)


def compare(a: SignalEnvelope, b: SignalEnvelope) -> int:
    rank_a = authority_rank(a)
    rank_b = authority_rank(b)
    if rank_a != rank_b:
        return -1 if rank_a < rank_b else 1

    if a.confidence != b.confidence:
        return -1 if a.confidence > b.confidence else 1

    if a.timestamp != b.timestamp:
        return -1 if a.timestamp > b.timestamp else 1

    return 0


def select_winner(a: SignalEnvelope, b: SignalEnvelope) -> SignalEnvelope:
    result = compare(a, b)
    if result <= 0:
        return a
    return b
