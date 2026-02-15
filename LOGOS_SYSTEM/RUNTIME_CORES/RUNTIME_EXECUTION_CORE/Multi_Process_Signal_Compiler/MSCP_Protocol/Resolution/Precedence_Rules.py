from __future__ import annotations
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Signals.Signal_Envelope import AuthorityLevel, SignalEnvelope
_AUTHORITY_RANK = {AuthorityLevel.SYSTEM: 0, AuthorityLevel.GOVERNANCE: 1, AuthorityLevel.PROTOCOL: 2, AuthorityLevel.AGENT: 3, AuthorityLevel.ADVISORY: 4, AuthorityLevel.UNCLASSIFIED: 5}

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