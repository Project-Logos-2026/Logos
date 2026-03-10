# File: Signal_Envelope.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Defines the SignalEnvelope dataclass, the canonical wrapper for all
#   inputs entering the MSPC pipeline. Every external input is normalized
#   into a SignalEnvelope before any processing occurs.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class SignalSource(Enum):
    FILESYSTEM = "filesystem"
    AGENT = "agent"
    HUMAN_DIRECTIVE = "human_directive"
    TELEMETRY = "telemetry"
    RUNTIME_DIAGNOSTIC = "runtime_diagnostic"
    PROTOCOL_OUTPUT = "protocol_output"
    UNKNOWN = "unknown"


class AuthorityLevel(Enum):
    SYSTEM = "system"
    GOVERNANCE = "governance"
    PROTOCOL = "protocol"
    AGENT = "agent"
    ADVISORY = "advisory"
    UNCLASSIFIED = "unclassified"


@dataclass(frozen=True)
class SignalEnvelope:
    signal_id: str
    source: SignalSource
    authority: AuthorityLevel
    timestamp: float
    payload_hash: str
    payload: Dict[str, Any]
    confidence: float = 1.0
    supersedes: Optional[str] = None
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


def create_envelope(
    source: SignalSource,
    authority: AuthorityLevel,
    payload: Dict[str, Any],
    confidence: float = 1.0,
    supersedes: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> SignalEnvelope:
    if not isinstance(payload, dict):
        raise TypeError("Signal payload must be a dict")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("Confidence must be in [0.0, 1.0]")

    payload_bytes = str(sorted(payload.items())).encode("utf-8")
    payload_hash = hashlib.sha256(payload_bytes).hexdigest()

    return SignalEnvelope(
        signal_id=str(uuid.uuid4()),
        source=source,
        authority=authority,
        timestamp=time.time(),
        payload_hash=payload_hash,
        payload=payload,
        confidence=confidence,
        supersedes=supersedes,
        version=1,
        metadata=metadata or {},
    )
