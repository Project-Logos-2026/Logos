# File: Signal_Ingress.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Signal ingress handler for the MSPC pipeline. Accepts raw inputs
#   from heterogeneous sources, validates structural requirements,
#   normalizes them into SignalEnvelopes, and forwards to the
#   Signal Registry. Malformed inputs are rejected fail-closed.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from Multi_Process_Signal_Compiler.Signals.Signal_Envelope import (
    AuthorityLevel,
    SignalEnvelope,
    SignalSource,
    create_envelope,
)


class IngressValidationError(Exception):
    pass


class SignalIngress:
    def __init__(self, max_queue_size: int = 4096) -> None:
        self._max_queue_size = max_queue_size
        self._pending: List[SignalEnvelope] = []
        self._rejected: List[Dict[str, Any]] = []
        self._total_ingested: int = 0
        self._total_rejected: int = 0

    def ingest(self, raw_signal: Dict[str, Any]) -> Tuple[bool, Optional[SignalEnvelope]]:
        if len(self._pending) >= self._max_queue_size:
            self._record_rejection(raw_signal, "backpressure: queue full")
            return False, None

        try:
            envelope = self._normalize(raw_signal)
        except (IngressValidationError, TypeError, ValueError, KeyError) as exc:
            self._record_rejection(raw_signal, str(exc))
            return False, None

        self._pending.append(envelope)
        self._total_ingested += 1
        return True, envelope

    def drain(self) -> List[SignalEnvelope]:
        batch = list(self._pending)
        self._pending.clear()
        return batch

    def pending_count(self) -> int:
        return len(self._pending)

    def stats(self) -> Dict[str, int]:
        return {
            "total_ingested": self._total_ingested,
            "total_rejected": self._total_rejected,
            "pending": len(self._pending),
        }

    def recent_rejections(self, limit: int = 10) -> List[Dict[str, Any]]:
        return list(self._rejected[-limit:])

    def _normalize(self, raw: Dict[str, Any]) -> SignalEnvelope:
        if not isinstance(raw, dict):
            raise IngressValidationError("Raw signal must be a dict")

        payload = raw.get("payload")
        if not isinstance(payload, dict):
            raise IngressValidationError("Signal payload must be a dict")

        source_str = raw.get("source", "unknown")
        try:
            source = SignalSource(source_str)
        except ValueError:
            source = SignalSource.UNKNOWN

        authority_str = raw.get("authority", "unclassified")
        try:
            authority = AuthorityLevel(authority_str)
        except ValueError:
            authority = AuthorityLevel.UNCLASSIFIED

        confidence = raw.get("confidence", 1.0)
        if not isinstance(confidence, (int, float)):
            confidence = 1.0
        confidence = max(0.0, min(1.0, float(confidence)))

        supersedes = raw.get("supersedes")
        if supersedes is not None and not isinstance(supersedes, str):
            supersedes = None

        metadata = raw.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}

        return create_envelope(
            source=source,
            authority=authority,
            payload=payload,
            confidence=confidence,
            supersedes=supersedes,
            metadata=metadata,
        )

    def _record_rejection(self, raw: Any, reason: str) -> None:
        self._total_rejected += 1
        self._rejected.append({
            "reason": reason,
            "raw_type": type(raw).__name__,
        })
