# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: unified_binder
runtime_layer: protocol_execution
role: Unified reasoning binder
responsibility: Final I3AA assembly with contradiction detection and confidence calibration
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: []
provides: [bind]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Always emits I3AA, degraded if necessary"
rewrite_provenance:
  source: NEW
  rewrite_phase: ARP_Overhaul_Phase_1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: ARP_BINDER
  metrics: enabled
---------------------
"""

from __future__ import annotations

from typing import Any, Dict, List
import time
import logging

logger = logging.getLogger(__name__)


class UnifiedBinder:
    """
    Unified Reasoning Binder - Stage 5
    
    Responsibilities:
    - Contradiction detection across all layers
    - Confidence calibration
    - Meta-level consistency checks
    - I3AA artifact assembly per governance schema
    """
    
    def bind(
        self,
        aaced_packet: Dict[str, Any],
        context: Dict[str, Any],
        base_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any],
        synthesis_packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Bind all analysis layers into final I3AA artifact.
        
        Args:
            aaced_packet: Original task
            context: Additional context
            base_packet: Stage 1 output
            taxonomy_packet: Stage 2 output
            synthesis_packet: Stage 3+4 output
            
        Returns:
            I3AA-structured artifact conforming to governance schema
        """
        
        # Step 1: Detect contradictions
        contradictions = self._detect_contradictions(
            base_packet, taxonomy_packet, synthesis_packet
        )
        
        # Step 2: Calibrate confidence
        overall_confidence = self._calibrate_confidence(
            taxonomy_packet, synthesis_packet, contradictions
        )
        
        # Step 3: Extract meta-reasoning flags
        meta_flags = self._extract_meta_flags(
            base_packet, taxonomy_packet, synthesis_packet, contradictions
        )
        
        # Step 4: Build provenance trace
        provenance_trace = self._build_provenance(
            base_packet, taxonomy_packet, synthesis_packet
        )
        
        # Step 5: Assemble I3AA per governance schema
        i3aa = self._assemble_i3aa(
            aaced_packet=aaced_packet,
            context=context,
            base_packet=base_packet,
            taxonomy_packet=taxonomy_packet,
            synthesis_packet=synthesis_packet,
            contradictions=contradictions,
            overall_confidence=overall_confidence,
            meta_flags=meta_flags,
            provenance_trace=provenance_trace
        )
        
        return i3aa
    
    def _detect_contradictions(
        self,
        base_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any],
        synthesis_packet: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect contradictions across reasoning layers"""
        
        contradictions = []
        
        # Extract conflicts from taxonomy aggregation
        for taxonomy_name, taxonomy_data in taxonomy_packet.get("taxonomies", {}).items():
            conflicts = taxonomy_data.get("conflicts", [])
            for conflict in conflicts:
                contradictions.append({
                    "type": "taxonomy_conflict",
                    "taxonomy": taxonomy_name,
                    "conflict": conflict,
                    "severity": "medium"
                })
        
        # Check for consistency engine violations
        engine_results = base_packet.get("engine_results", {})
        consistency_result = engine_results.get("consistency", {})
        if consistency_result.get("contradictions"):
            for contradiction in consistency_result["contradictions"]:
                contradictions.append({
                    "type": "logical_contradiction",
                    "source": "consistency_engine",
                    "detail": contradiction,
                    "severity": "high"
                })
        
        # Check for invariant violations
        invariant_result = engine_results.get("invariant", {})
        if invariant_result.get("violations"):
            for violation in invariant_result["violations"]:
                contradictions.append({
                    "type": "invariant_violation",
                    "source": "invariant_engine",
                    "detail": violation,
                    "severity": "high"
                })
        
        return contradictions
    
    def _calibrate_confidence(
        self,
        taxonomy_packet: Dict[str, Any],
        synthesis_packet: Dict[str, Any],
        contradictions: List[Dict[str, Any]]
    ) -> float:
        """Calibrate overall confidence score"""
        
        # Base confidence from probabilistic taxonomy
        taxonomies = taxonomy_packet.get("taxonomies", {})
        prob_conf_taxonomy = taxonomies.get("PROBABILISTIC_CONFIDENCE", {})
        base_confidence = prob_conf_taxonomy.get("aggregated_score", 0.5)
        
        # Boost from synthesis
        synthesis_result = synthesis_packet.get("synthesis_result", {})
        synthesis_confidence = synthesis_result.get("overall_confidence", 0.5)
        
        # Weighted average
        calibrated = (base_confidence * 0.6) + (synthesis_confidence * 0.4)
        
        # Penalty for contradictions
        high_severity_count = sum(1 for c in contradictions if c.get("severity") == "high")
        medium_severity_count = sum(1 for c in contradictions if c.get("severity") == "medium")
        
        penalty = (high_severity_count * 0.15) + (medium_severity_count * 0.05)
        calibrated = max(0.0, calibrated - penalty)
        
        return round(calibrated, 3)
    
    def _extract_meta_flags(
        self,
        base_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any],
        synthesis_packet: Dict[str, Any],
        contradictions: List[Dict[str, Any]]
    ) -> List[str]:
        """Extract meta-reasoning flags"""
        
        flags = []
        
        # Flag if any stage had failures
        if base_packet.get("status") != "success":
            flags.append("BASE_REASONING_PARTIAL_FAILURE")
        
        if taxonomy_packet.get("status") != "success":
            flags.append("TAXONOMY_AGGREGATION_FAILURE")
        
        if synthesis_packet.get("status") != "success":
            flags.append("SYNTHESIS_FAILURE")
        
        # Flag contradictions
        if contradictions:
            flags.append("CONTRADICTIONS_DETECTED")
            if any(c.get("severity") == "high" for c in contradictions):
                flags.append("HIGH_SEVERITY_CONTRADICTIONS")
        
        # Flag low confidence
        taxonomies = taxonomy_packet.get("taxonomies", {})
        for taxonomy_name, taxonomy_data in taxonomies.items():
            score = taxonomy_data.get("aggregated_score", 0.0)
            if score < 0.3:
                flags.append(f"LOW_CONFIDENCE_{taxonomy_name}")
        
        return flags
    
    def _build_provenance(
        self,
        base_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any],
        synthesis_packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build complete provenance trace"""
        
        return {
            "base_reasoning": {
                "engines_invoked": [
                    p["engine"] for p in base_packet.get("provenance", [])
                ],
                "engine_count": len(base_packet.get("engine_results", {}))
            },
            "taxonomy_aggregation": {
                "taxonomies_produced": list(taxonomy_packet.get("taxonomies", {}).keys()),
                "taxonomy_count": len(taxonomy_packet.get("taxonomies", {}))
            },
            "triune_synthesis": {
                "pxl_status": synthesis_packet.get("pxl_result", {}).get("status", "unknown"),
                "iel_domains": synthesis_packet.get("active_iel_domains", []),
                "math_categories": synthesis_packet.get("active_math_categories", [])
            }
        }
    
    def _assemble_i3aa(
        self,
        aaced_packet: Dict[str, Any],
        context: Dict[str, Any],
        base_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any],
        synthesis_packet: Dict[str, Any],
        contradictions: List[Dict[str, Any]],
        overall_confidence: float,
        meta_flags: List[str],
        provenance_trace: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assemble final I3AA artifact per governance schema"""
        
        # Extract reasoning domains used
        reasoning_domains = []
        reasoning_domains.extend(provenance_trace["base_reasoning"]["engines_invoked"])
        reasoning_domains.extend(provenance_trace["triune_synthesis"]["iel_domains"])
        reasoning_domains.extend(provenance_trace["triune_synthesis"]["math_categories"])
        
        # Build aggregation summary
        taxonomies = taxonomy_packet.get("taxonomies", {})
        aggregation_summary = "; ".join([
            f"{name}: {data.get('summary', 'N/A')}"
            for name, data in taxonomies.items()
        ])
        
        # Assemble validation conflicts
        validation_conflicts = contradictions
        
        # Build I3AA structure conforming to governance schema
        i3aa = {
            # Protocol metadata
            "protocol": "ARP",
            "type": "AA_PRE_STRUCTURED",
            "status": "compiled",
            
            # Core AA fields (per SMP_Agent_AA_Schemas.md)
            "aa_type": "I3AA",
            "aa_origin_type": "protocol",
            "originating_entity": "Advanced_Reasoning_Protocol",
            "bound_smp_id": aaced_packet.get("smp_id", "unknown"),
            "creation_timestamp": time.time(),
            
            # I3AA-specific fields (per governance schema)
            "reasoning_domains_used": reasoning_domains,
            "aggregation_summary": aggregation_summary,
            "validation_conflicts": validation_conflicts,
            "meta_reasoning_flags": meta_flags,
            
            # Full analysis stack for auditability
            "analysis_stack": {
                "base_reasoning": base_packet,
                "taxonomy_aggregation": taxonomy_packet,
                "triune_synthesis": synthesis_packet
            },
            
            # Confidence and provenance
            "overall_confidence": overall_confidence,
            "provenance_trace": provenance_trace,
            
            # Trinity coherence (if available)
            "trinity_coherence": synthesis_packet.get("synthesis_result", {}).get("trinity_coherence", None)
        }
        
        return i3aa
