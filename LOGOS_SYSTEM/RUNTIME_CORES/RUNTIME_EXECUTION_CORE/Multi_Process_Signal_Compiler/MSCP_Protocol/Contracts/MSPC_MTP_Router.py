# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MSPC_MTP_Router
runtime_layer: egress_routing
role: Subscription callback router
responsibility: Registered as a subscriber on MSPC_Subscription_API. Receives
    each EmittedArtifact, classifies via MSPC_Output_Contract, and routes
    COMPILED_MEANING artifacts into MTP egress via injected callable.
    All other classes ignored. No mutation of incoming artifacts.
    No broad exception swallowing. Constructor injection avoids cycles.
agent_binding: None
protocol_binding: Multi_Process_Signal_Compiler
runtime_classification: routing_adapter
boot_phase: Phase-6-Integration
expected_imports: [Artifact_Emitter, MSPC_Output_Contract]
provides: [MSPCMTPRouter, MSPCMTPRoutingError]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Classification or SMP build failure raises MSPCMTPRoutingError.
    MTP pipeline failures propagate from MTPNexus."
rewrite_provenance:
  source: Phase_6_MSPC_Topology_Enforcement
  rewrite_phase: Phase_6
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Artifact_Emitter import (
    EmittedArtifact,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Contracts.MSPC_Output_Contract import (
    OutputClass,
    classify_output,
)


class MSPCMTPRoutingError(Exception):
    pass


class MSPCMTPRouter:

    def __init__(
        self,
        mtp_process_fn: Callable[[Dict[str, Any]], Any],
        smp_builder_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> None:
        if mtp_process_fn is None:
            raise ValueError("mtp_process_fn must not be None")
        self._mtp_process = mtp_process_fn
        self._smp_builder = smp_builder_fn
        self._routed_count: int = 0
        self._skipped_count: int = 0

    def __call__(self, artifact: EmittedArtifact) -> None:
        classification = classify_output(artifact)

        if classification != OutputClass.COMPILED_MEANING:
            self._skipped_count += 1
            return

        smp_payload = self._build_smp_payload(artifact)
        self._mtp_process(smp_payload)
        self._routed_count += 1

    def _build_smp_payload(self, artifact: EmittedArtifact) -> Dict[str, Any]:
        if self._smp_builder is not None:
            result = self._smp_builder(artifact.content)
            if not isinstance(result, dict):
                raise MSPCMTPRoutingError(
                    f"smp_builder_fn returned {type(result).__name__}, expected dict"
                )
            status = result.get("status", "")
            if status != "success":
                raise MSPCMTPRoutingError(
                    f"SMP build failed: status={status}, reason={result.get('reason', 'unknown')}"
                )
            smp = result.get("smp")
            if smp is None:
                raise MSPCMTPRoutingError("SMP build returned None payload")
            return smp

        payload: Dict[str, Any] = dict(artifact.content)
        payload.setdefault("smp_id", artifact.artifact_id)
        payload["_mspc_provenance"] = {
            "emission_id": artifact.emission_id,
            "artifact_hash": artifact.artifact_hash,
            "version_tag": artifact.version_tag,
        }
        return payload

    @property
    def routed_count(self) -> int:
        return self._routed_count

    @property
    def skipped_count(self) -> int:
        return self._skipped_count
