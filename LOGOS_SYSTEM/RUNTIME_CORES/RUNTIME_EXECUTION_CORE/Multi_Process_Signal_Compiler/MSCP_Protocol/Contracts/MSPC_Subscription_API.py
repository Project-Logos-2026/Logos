# File: MSPC_Subscription_API.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Subscription API for external consumers of MSPC outputs. Supports
#   pull-based retrieval, event-based callback subscriptions, and
#   snapshot queries. MSPC does not depend on whether subscribers
#   exist; publication is unconditional.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

import uuid
from typing import Any, Callable, Dict, List, Optional

from Multi_Process_Signal_Compiler.Compilation.Artifact_Emitter import EmittedArtifact


class SubscriptionError(Exception):
    pass


SubscriberCallback = Callable[[EmittedArtifact], None]


class MSPCSubscriptionAPI:
    def __init__(self) -> None:
        self._subscribers: Dict[str, SubscriberCallback] = {}
        self._latest_batch: List[EmittedArtifact] = []
        self._cumulative: List[EmittedArtifact] = []
        self._publish_count: int = 0

    def subscribe(self, callback: SubscriberCallback) -> str:
        sub_id = str(uuid.uuid4())
        self._subscribers[sub_id] = callback
        return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        return self._subscribers.pop(subscription_id, None) is not None

    def publish(self, artifacts: List[EmittedArtifact]) -> int:
        self._latest_batch = list(artifacts)
        self._cumulative.extend(artifacts)
        self._publish_count += 1

        delivered = 0
        failed_subs: List[str] = []

        for sub_id, callback in self._subscribers.items():
            for artifact in artifacts:
                try:
                    callback(artifact)
                    delivered += 1
                except Exception:
                    failed_subs.append(sub_id)
                    break

        for sub_id in failed_subs:
            self._subscribers.pop(sub_id, None)

        return delivered

    def poll_latest(self) -> List[EmittedArtifact]:
        return list(self._latest_batch)

    def snapshot(self, limit: int = 100) -> List[EmittedArtifact]:
        return list(self._cumulative[-limit:])

    def subscriber_count(self) -> int:
        return len(self._subscribers)

    def stats(self) -> Dict[str, Any]:
        return {
            "subscriber_count": len(self._subscribers),
            "publish_count": self._publish_count,
            "cumulative_artifacts": len(self._cumulative),
            "latest_batch_size": len(self._latest_batch),
        }
