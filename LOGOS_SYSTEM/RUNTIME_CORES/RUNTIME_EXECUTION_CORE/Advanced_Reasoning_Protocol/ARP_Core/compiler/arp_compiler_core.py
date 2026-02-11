# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 2.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: arp_compiler_core
runtime_layer: protocol_execution
role: ARP compiler orchestrator
responsibility: Compile AACED packets into I3AA artifacts via multi-stage reasoning pipeline
agent_binding: I3_Agent
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [base_reasoning_registry, taxonomy_aggregator, integration_bridge, unified_binder]
provides: [compile]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Halts on stage failure, emits degraded I3AA with explicit error markers"
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/compiler/arp_compiler_core.py
  rewrite_phase: ARP_Overhaul_Phase_1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: ARP_COMPILER
  metrics: enabled
---------------------
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from enum import Enum
import time
import logging

from ..engines.base_reasoning_registry import BaseReasoningRegistry
from ..engines.taxonomy_aggregator import TaxonomyAggregator
from ..engines.integration_bridge import IntegrationBridge
from ..engines.unified_binder import UnifiedBinder

logger = logging.getLogger(__name__)


class ComputeMode(Enum):
    LIGHTWEIGHT = "lightweight"
    BALANCED = "balanced"
    HIGH_RIGOR = "high_rigor"


class ARPCompilerCore:
    """
    ARP Compiler Core - Multi-Stage Reasoning Pipeline
    
    Pipeline:
    1. Base Reasoning (12 engines) → BaseReasoningPacket
    2. Taxonomical Aggregation (5 taxonomies) → TaxonomyPacket
    3. PXL/IEL/Math Triune Analysis → TriuneAnalysisPacket
    4. Cross-Domain Synthesis → SynthesisPacket
    5. Unified Reasoning Binder → I3AA
    
    Fail-closed: Each stage has explicit error handling. Degraded outputs
    are preferred over hallucinated completions.
    """
    
    def __init__(
        self,
        compute_mode: ComputeMode = ComputeMode.BALANCED,
        enable_provenance: bool = True
    ) -> None:
        self.compute_mode = compute_mode
        self.enable_provenance = enable_provenance
        
        # Stage 1: Base reasoning
        self.base_registry = BaseReasoningRegistry(mode=compute_mode)
        
        # Stage 2: Taxonomical aggregation
        self.taxonomy_aggregator = TaxonomyAggregator()
        
        # Stage 3+4: Triune + Synthesis
        self.integration_bridge = IntegrationBridge(compute_mode=compute_mode)
        
        # Stage 5: Unified binder
        self.unified_binder = UnifiedBinder()
        
        logger.info(f"ARPCompilerCore initialized (mode={compute_mode.value})")
    
    def compile(
        self,
        aaced_packet: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Compile AACED packet into I3AA artifact.
        
        Args:
            aaced_packet: Input from I3 Agent containing task + context
            context: Optional additional context
            
        Returns:
            I3AA-structured artifact ready for SMP append
        """
        context = context or {}
        start_time = time.time()
        
        try:
            # Stage 1: Base Reasoning
            logger.debug("Stage 1: Base Reasoning")
            base_packet = self._stage1_base_reasoning(aaced_packet, context)
            
            if base_packet.get("status") == "failed":
                return self._emit_degraded_i3aa(
                    aaced_packet, context,
                    failure_stage="base_reasoning",
                    failure_reason=base_packet.get("error", "unknown")
                )
            
            # Stage 2: Taxonomical Aggregation
            logger.debug("Stage 2: Taxonomical Aggregation")
            taxonomy_packet = self._stage2_taxonomy_aggregation(base_packet)
            
            if taxonomy_packet.get("status") == "failed":
                return self._emit_degraded_i3aa(
                    aaced_packet, context,
                    failure_stage="taxonomy_aggregation",
                    failure_reason=taxonomy_packet.get("error", "unknown")
                )
            
            # Stage 3+4: Triune Analysis + Cross-Domain Synthesis
            logger.debug("Stage 3+4: Triune Analysis + Synthesis")
            synthesis_packet = self._stage3_4_triune_synthesis(
                aaced_packet, taxonomy_packet
            )
            
            if synthesis_packet.get("status") == "failed":
                return self._emit_degraded_i3aa(
                    aaced_packet, context,
                    failure_stage="triune_synthesis",
                    failure_reason=synthesis_packet.get("error", "unknown")
                )
            
            # Stage 5: Unified Reasoning Binder
            logger.debug("Stage 5: Unified Binder")
            i3aa = self._stage5_unified_binding(
                aaced_packet, context, base_packet, taxonomy_packet, synthesis_packet
            )
            
            elapsed = time.time() - start_time
            i3aa["compilation_time_seconds"] = elapsed
            
            logger.info(f"ARP compilation complete ({elapsed:.2f}s)")
            return i3aa
            
        except Exception as e:
            logger.error(f"ARP compilation failed: {e}", exc_info=True)
            return self._emit_degraded_i3aa(
                aaced_packet, context,
                failure_stage="unexpected_exception",
                failure_reason=str(e)
            )
    
    def _stage1_base_reasoning(
        self,
        aaced_packet: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute Stage 1: Base Reasoning (12 engines)"""
        try:
            return self.base_registry.reason(aaced_packet, context)
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _stage2_taxonomy_aggregation(
        self,
        base_packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute Stage 2: Taxonomical Aggregation (5 outputs)"""
        try:
            return self.taxonomy_aggregator.aggregate(base_packet)
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _stage3_4_triune_synthesis(
        self,
        aaced_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute Stage 3+4: Triune Analysis + Cross-Domain Synthesis"""
        try:
            return self.integration_bridge.synthesize(aaced_packet, taxonomy_packet)
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _stage5_unified_binding(
        self,
        aaced_packet: Dict[str, Any],
        context: Dict[str, Any],
        base_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any],
        synthesis_packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute Stage 5: Unified Reasoning Binder → I3AA"""
        return self.unified_binder.bind(
            aaced_packet=aaced_packet,
            context=context,
            base_packet=base_packet,
            taxonomy_packet=taxonomy_packet,
            synthesis_packet=synthesis_packet
        )
    
    def _emit_degraded_i3aa(
        self,
        aaced_packet: Dict[str, Any],
        context: Dict[str, Any],
        failure_stage: str,
        failure_reason: str
    ) -> Dict[str, Any]:
        """
        Emit a degraded I3AA artifact that explicitly marks failure.
        
        Fail-closed principle: Better to admit inability than hallucinate.
        """
        return {
            "protocol": "ARP",
            "type": "AA_PRE_STRUCTURED",
            "status": "degraded",
            "failure_stage": failure_stage,
            "failure_reason": failure_reason,
            "analysis_stack": {
                "pxl": {"status": "unavailable"},
                "iel": {"status": "unavailable"},
                "mathematical": {"status": "unavailable"},
                "unified": {"status": "unavailable"}
            },
            "i3aa_fields": {
                "reasoning_domains_used": [],
                "aggregation_summary": f"FAILED at {failure_stage}: {failure_reason}",
                "validation_conflicts": [
                    {
                        "type": "pipeline_failure",
                        "stage": failure_stage,
                        "reason": failure_reason
                    }
                ],
                "meta_reasoning_flags": ["DEGRADED_OUTPUT", "FAIL_CLOSED"]
            },
            "bound_smp_id": aaced_packet.get("smp_id", "unknown"),
            "creation_timestamp": time.time()
        }
