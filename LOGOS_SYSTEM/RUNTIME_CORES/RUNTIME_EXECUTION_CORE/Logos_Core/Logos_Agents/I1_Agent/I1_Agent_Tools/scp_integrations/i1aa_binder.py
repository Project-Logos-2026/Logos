# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED

"""I1AA assembly from SCP analysis results."""

from __future__ import annotations
from typing import Any, Dict, List
import time


class I1AABinder:
    """Assembles governance-compliant I1AA from SCP analysis."""
    
    def bind(
        self,
        smp_id: str,
        mvs_result: Dict[str, Any],
        bdn_result: Dict[str, Any],
        sign_grounding: Dict[str, Any],
        privation_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Bind all layers into I1AA per governance schema."""
        
        contradictions = self._detect_contradictions(
            mvs_result, bdn_result, sign_grounding
        )
        
        confidence = self._calibrate_confidence(
            mvs_result, bdn_result, sign_grounding, contradictions
        )
        
        return {
            "protocol": "SCP",
            "type": "AA_PRE_STRUCTURED",
            "status": "compiled",
            "aa_type": "I1AA",
            "aa_origin_type": "agent",
            "originating_entity": "I1_Agent",
            "bound_smp_id": smp_id,
            "creation_timestamp": time.time(),
            "fractal_configuration": {
                "privation_depth": privation_profile.get("depth_level", "unknown"),
                "mvs_depth_explored": mvs_result.get("meta", {}).get("depth_explored", 0),
                "bdn_nodes_generated": bdn_result.get("meta", {}).get("node_count", 0)
            },
            "modal_analysis_summary": {
                "mvs_coherence": mvs_result.get("coherence_score", 0.0),
                "modal_status": mvs_result.get("meta", {}).get("modal_status", "unknown"),
                "creative_hypotheses_count": len(mvs_result.get("meta", {}).get("hypotheses", []))
            },
            "causal_chain_findings": {
                "bdn_stability": bdn_result.get("stability_score", 0.0),
                "genealogy_depth": bdn_result.get("meta", {}).get("genealogy_depth", 0),
                "transformations_applied": bdn_result.get("meta", {}).get("transformations_applied", [])
            },
            "salvageability_assessment": {
                "salvageable": bdn_result.get("meta", {}).get("recomposition_converged", False),
                "confidence": confidence,
                "sign_grounding_quality": sign_grounding.get("epistemic_status", "unknown")
            },
            "analysis_stack": {
                "mvs": mvs_result.get("meta", {}),
                "bdn": bdn_result.get("meta", {}),
                "sign_grounding": sign_grounding
            },
            "validation_conflicts": contradictions,
            "meta_reasoning_flags": self._extract_meta_flags(contradictions, confidence),
            "overall_confidence": confidence,
            "provenance_trace": {
                "smp_intake": "semantic_analysis_applied",
                "mvs_analysis": "real_fractal_modal_space",
                "bdn_analysis": "real_banach_decomposition",
                "sign_grounding": "mvs_sign_resolution"
            }
        }
    
    def _detect_contradictions(
        self,
        mvs_result: Dict,
        bdn_result: Dict,
        sign_grounding: Dict
    ) -> List[Dict[str, Any]]:
        """Detect contradictions across layers."""
        contradictions = []
        
        mvs_coherence = mvs_result.get("coherence_score", 1.0)
        bdn_stability = bdn_result.get("stability_score", 1.0)
        
        if mvs_coherence < 0.3 and bdn_stability > 0.7:
            contradictions.append({
                "type": "mvs_bdn_mismatch",
                "severity": "medium",
                "detail": "MVS reports low coherence but BDN reports high stability"
            })
        
        return contradictions
    
    def _calibrate_confidence(
        self,
        mvs_result: Dict,
        bdn_result: Dict,
        sign_grounding: Dict,
        contradictions: List
    ) -> float:
        """Calibrate overall confidence score."""
        mvs_conf = mvs_result.get("coherence_score", 0.5)
        bdn_conf = bdn_result.get("stability_score", 0.5)
        
        calibrated = (mvs_conf * 0.6) + (bdn_conf * 0.4)
        
        penalty = len(contradictions) * 0.1
        calibrated = max(0.0, calibrated - penalty)
        
        return round(calibrated, 3)
    
    def _extract_meta_flags(
        self,
        contradictions: List,
        confidence: float
    ) -> List[str]:
        """Extract meta-reasoning flags."""
        flags = []
        
        if contradictions:
            flags.append("CONTRADICTIONS_DETECTED")
        
        if confidence < 0.3:
            flags.append("LOW_CONFIDENCE")
        
        return flags
