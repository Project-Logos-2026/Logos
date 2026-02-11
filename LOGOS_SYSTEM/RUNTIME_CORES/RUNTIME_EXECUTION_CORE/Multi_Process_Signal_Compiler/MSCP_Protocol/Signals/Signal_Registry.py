# File: Signal_Registry.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Signal registry for the MSPC pipeline. Canonicalizes incoming
#   SignalEnvelopes, deduplicates by payload hash, manages version
#   chains via supersession tracking, and maintains the stable
#   signal universe for downstream compilation stages.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from Multi_Process_Signal_Compiler.Signals.Signal_Envelope import SignalEnvelope


class SignalRegistry:
    def __init__(self) -> None:
        self._by_id: Dict[str, SignalEnvelope] = {}
        self._by_hash: Dict[str, str] = {}
        self._supersession_chain: Dict[str, str] = {}
        self._superseded_ids: Set[str] = set()
        self._registration_order: List[str] = []

    def register(self, envelope: SignalEnvelope) -> bool:
        if envelope.signal_id in self._by_id:
            return False

        existing_id = self._by_hash.get(envelope.payload_hash)
        if existing_id is not None and existing_id not in self._superseded_ids:
            if envelope.supersedes != existing_id:
                return False

        if envelope.supersedes:
            if envelope.supersedes in self._by_id:
                self._superseded_ids.add(envelope.supersedes)
                self._supersession_chain[envelope.supersedes] = envelope.signal_id

        self._by_id[envelope.signal_id] = envelope
        self._by_hash[envelope.payload_hash] = envelope.signal_id
        self._registration_order.append(envelope.signal_id)
        return True

    def register_batch(self, envelopes: List[SignalEnvelope]) -> Dict[str, bool]:
        results: Dict[str, bool] = {}
        for env in envelopes:
            results[env.signal_id] = self.register(env)
        return results

    def get(self, signal_id: str) -> Optional[SignalEnvelope]:
        return self._by_id.get(signal_id)

    def active_signals(self) -> List[SignalEnvelope]:
        return [
            self._by_id[sid]
            for sid in self._registration_order
            if sid not in self._superseded_ids and sid in self._by_id
        ]

    def is_superseded(self, signal_id: str) -> bool:
        return signal_id in self._superseded_ids

    def successor_of(self, signal_id: str) -> Optional[str]:
        return self._supersession_chain.get(signal_id)

    def total_registered(self) -> int:
        return len(self._by_id)

    def active_count(self) -> int:
        return sum(
            1 for sid in self._by_id
            if sid not in self._superseded_ids
        )

    def snapshot(self) -> Dict[str, Any]:
        return {
            "total_registered": self.total_registered(),
            "active_count": self.active_count(),
            "superseded_count": len(self._superseded_ids),
        }
