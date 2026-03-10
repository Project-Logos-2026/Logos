# File: MSPC_Audit_Log.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Append-only audit log for the MSPC protocol. Records all
#   significant pipeline events including signal ingestion,
#   conflict resolution decisions, compilation outcomes, artifact
#   emissions, and error conditions. The log is immutable once
#   written; entries cannot be modified or deleted.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class AuditEventType(Enum):
    SIGNAL_INGESTED = "signal_ingested"
    SIGNAL_REJECTED = "signal_rejected"
    SIGNAL_REGISTERED = "signal_registered"
    SIGNAL_SUPERSEDED = "signal_superseded"
    CONFLICT_DETECTED = "conflict_detected"
    CONFLICT_RESOLVED = "conflict_resolved"
    CONFLICT_ESCALATED = "conflict_escalated"
    COMPILATION_STARTED = "compilation_started"
    COMPILATION_COMPLETED = "compilation_completed"
    COMPILATION_ERROR = "compilation_error"
    ARTIFACT_EMITTED = "artifact_emitted"
    TICK_STARTED = "tick_started"
    TICK_COMPLETED = "tick_completed"
    STATE_TRANSITION = "state_transition"
    RUNTIME_ERROR = "runtime_error"
    RUNTIME_HALT = "runtime_halt"


@dataclass(frozen=True)
class AuditEntry:
    sequence_number: int
    event_type: AuditEventType
    timestamp: float
    tick_number: int
    session_id: str
    detail: Dict[str, Any]
    entry_hash: str


class MSPCAuditLog:
    def __init__(self, session_id: str) -> None:
        self._session_id = session_id
        self._entries: List[AuditEntry] = []
        self._sequence: int = 0

    def record(
        self,
        event_type: AuditEventType,
        tick_number: int,
        detail: Optional[Dict[str, Any]] = None,
    ) -> AuditEntry:
        self._sequence += 1
        ts = time.time()
        detail = detail or {}

        hash_input = (
            f"{self._sequence}:{event_type.value}:{ts}:"
            f"{self._session_id}:{str(sorted(detail.items()))}"
        )
        entry_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        entry = AuditEntry(
            sequence_number=self._sequence,
            event_type=event_type,
            timestamp=ts,
            tick_number=tick_number,
            session_id=self._session_id,
            detail=detail,
            entry_hash=entry_hash,
        )
        self._entries.append(entry)
        return entry

    def query(
        self,
        event_type: Optional[AuditEventType] = None,
        since_tick: Optional[int] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        results = self._entries
        if event_type is not None:
            results = [e for e in results if e.event_type == event_type]
        if since_tick is not None:
            results = [e for e in results if e.tick_number >= since_tick]
        return results[-limit:]

    def total_entries(self) -> int:
        return len(self._entries)

    def latest(self, count: int = 10) -> List[AuditEntry]:
        return list(self._entries[-count:])

    def integrity_check(self) -> bool:
        for entry in self._entries:
            hash_input = (
                f"{entry.sequence_number}:{entry.event_type.value}:"
                f"{entry.timestamp}:{entry.session_id}:"
                f"{str(sorted(entry.detail.items()))}"
            )
            expected = hashlib.sha256(hash_input.encode()).hexdigest()
            if expected != entry.entry_hash:
                return False
        return True

    def summary(self) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for entry in self._entries:
            counts[entry.event_type.value] = counts.get(entry.event_type.value, 0) + 1
        return {
            "session_id": self._session_id,
            "total_entries": len(self._entries),
            "event_counts": counts,
            "integrity_valid": self.integrity_check(),
        }
