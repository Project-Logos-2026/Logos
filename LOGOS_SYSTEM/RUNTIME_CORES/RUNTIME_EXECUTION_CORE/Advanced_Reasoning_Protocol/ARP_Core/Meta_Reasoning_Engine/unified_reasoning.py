# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: unified_reasoning
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/Meta_Reasoning_Engine/unified_reasoning.py.
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/Meta_Reasoning_Engine/unified_reasoning.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Unified Reasoning Engine - PXL+IEL+Math Synthesis
================================================

Complete reasoning system that synthesizes PXL substrate, IEL philosophical
domains, and Mathematical categories into Trinity-grounded unified analysis.

Enables cross-domain amplification through:
- IEL-Math category mapping
- Philosophical-mathematical synthesis
- Trinity-coherence optimization
- Multi-lens reasoning integration

Author: LOGOS AGI Development Team
Version: 1.0.0
Date: 2026-01-24
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum

# Core engines
from pxl_engine import (
    PXLReasoningEngine,
    PXLReasoningContext,
    PXLReasoningResult,
    ReasoningMode,
    get_pxl_engine
)

from iel_engine import (
    IELReasoningEngine,
    IELDomain,
    IELReasoningResult,
    get_iel_engine
)

from math_engine import (
    MathematicsReasoningEngine,
    MathCategory,
    MathReasoningResult,
    get_math_engine
)

from LOGOS_SYSTEM.System_Stack.Advanced_Reasoning_Protocol.formalisms.pxl_schema import (
    TrinityVector,
    PXLRelation
)

# Configure logging when invoked as a script
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================================================================
# IEL-MATH CATEGORY MAPPING
# =========================================================================

IEL_MATH_MAPPING = {
    # AxioPraxis: Foundational logic and axiom systems
    IELDomain.AXIOPRAXIS: [
        MathCategory.BOOLEAN_LOGIC,  # Propositional logic
        MathCategory.TYPE_THEORY,    # Type-theoretic foundations
        MathCategory.CATEGORY_THEORY # Abstract foundational structures
    ],
    
    # GnosiPraxis: Knowledge and epistemology
    IELDomain.GNOSIPRAXIS: [
        MathCategory.TOPOLOGY,       # Knowledge space topology
        MathCategory.MEASURE_THEORY, # Belief quantification
        MathCategory.CATEGORY_THEORY # Knowledge category structures
    ],
    
    # ChronoPraxis: Temporal and sequence logic
    IELDomain.CHRONOPRAXIS: [
        MathCategory.ALGEBRA,        # Temporal algebras
        MathCategory.TOPOLOGY,       # Temporal topology
        MathCategory.CORE           # Sequential analysis
    ],
    
    # ModalPraxis: Modal logic and possibility
    IELDomain.MODALPRAXIS: [
        MathCategory.BOOLEAN_LOGIC,  # Modal propositional logic
        MathCategory.TOPOLOGY,       # Possible world topology
        MathCategory.ALGEBRA        # Modal algebras
    ],
    
    # TeloPraxis: Purpose and teleology
    IELDomain.TELOPRAXIS: [
        MathCategory.OPTIMIZATION,   # Goal optimization
        MathCategory.CATEGORY_THEORY,# Teleological categories
        MathCategory.MEASURE_THEORY # Value measures
    ],
    
    # AnthroPraxis: Human-AI interaction and ethics
    IELDomain.ANTHROPRAXIS: [
        MathCategory.OPTIMIZATION,   # Ethical optimization
        MathCategory.MEASURE_THEORY, # Utility measures
        MathCategory.CORE           # Fundamental human values
    ]
}


# Reverse mapping: Math -> IEL
MATH_IEL_MAPPING = {}
for iel, maths in IEL_MATH_MAPPING.items():
    for math in maths:
        if math not in MATH_IEL_MAPPING:
            MATH_IEL_MAPPING[math] = []
        MATH_IEL_MAPPING[math].append(iel)


@dataclass
class CrossDomainSynthesis:
    """Result of cross-domain synthesis between IEL and Math"""
    iel_domain: IELDomain
    math_category: MathCategory
    synergy_score: float
    amplified_insights: List[str]
    formal_support: Dict[str, Any]
    philosophical_grounding: Dict[str, Any]


@dataclass
class UnifiedReasoningResult:
    """Complete unified reasoning result"""
    pxl_result: PXLReasoningResult
    iel_result: IELReasoningResult
    math_result: MathReasoningResult
    cross_domain_syntheses: List[CrossDomainSynthesis]
    trinity_coherence: TrinityVector
    overall_confidence: float
    key_insights: List[str]
    proven_theorems: List[str]
    recommended_actions: List[str]


class UnifiedReasoningEngine:
    """
    Unified Reasoning Engine
    
    Integrates PXL substrate, IEL domains, and Math categories into
    a complete Trinity-grounded reasoning system with cross-domain
    amplification and synthesis.
    """
    
    def __init__(
        self,
        pxl_engine: Optional[PXLReasoningEngine] = None,
        iel_engine: Optional[IELReasoningEngine] = None,
        math_engine: Optional[MathematicsReasoningEngine] = None
    ):
        """Initialize unified reasoning engine"""
        self.pxl_engine = pxl_engine or get_pxl_engine()
        self.iel_engine = iel_engine or get_iel_engine(self.pxl_engine)
        self.math_engine = math_engine or get_math_engine(self.pxl_engine)
        
        self.logger = logging.getLogger(__name__)
        
        # Cross-domain mapping
        self.iel_math_map = IEL_MATH_MAPPING
        self.math_iel_map = MATH_IEL_MAPPING
        
        # Statistics
        self.reasoning_operations = 0
        self.synthesis_operations = 0
        
        self.logger.info("Unified Reasoning Engine initialized")
    
    def reason(
        self,
        concepts: List[str],
        context: Optional[PXLReasoningContext] = None,
        active_iel_domains: Optional[Set[IELDomain]] = None,
        active_math_categories: Optional[Set[MathCategory]] = None,
        enable_synthesis: bool = True
    ) -> UnifiedReasoningResult:
        """
        Execute unified reasoning across all three layers
        
        Args:
            concepts: Concepts to reason about
            context: PXL reasoning context
            active_iel_domains: IEL domains to apply
            active_math_categories: Math categories to apply
            enable_synthesis: Whether to perform cross-domain synthesis
            
        Returns:
            UnifiedReasoningResult with complete analysis
        """
        self.reasoning_operations += 1
        
        try:
            # Layer 1: PXL Substrate Reasoning
            self.logger.info("Executing PXL substrate reasoning...")
            pxl_result = self.pxl_engine.reason(concepts, context)
            
            if not pxl_result.success:
                self.logger.warning("PXL reasoning failed, aborting")
                return self._create_failed_result(pxl_result)
            
            # Layer 2: IEL Domain Reasoning
            self.logger.info("Applying IEL domain lenses...")
            iel_result = self.iel_engine.reason(
                concepts,
                active_iel_domains,
                context
            )
            
            # Layer 3: Mathematical Category Reasoning
            self.logger.info("Applying mathematical category lenses...")
            math_result = self.math_engine.reason(
                concepts,
                active_math_categories,
                context
            )
            
            # Cross-Domain Synthesis
            cross_syntheses = []
            if enable_synthesis:
                self.logger.info("Performing cross-domain synthesis...")
                cross_syntheses = self._synthesize_cross_domain(
                    iel_result,
                    math_result,
                    pxl_result
                )
                self.synthesis_operations += 1
            
            # Calculate unified Trinity coherence
            trinity_coherence = self._calculate_unified_trinity_coherence(
                pxl_result,
                iel_result,
                math_result
            )
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(
                pxl_result,
                iel_result,
                math_result,
                cross_syntheses
            )
            
            # Extract key insights
            key_insights = self._extract_key_insights(
                iel_result,
                math_result,
                cross_syntheses
            )
            
            # Collect proven theorems
            proven_theorems = math_result.proven_theorems
            
            # Generate unified recommendations
            recommendations = self._generate_unified_recommendations(
                iel_result,
                math_result,
                cross_syntheses,
                overall_confidence
            )
            
            result = UnifiedReasoningResult(
                pxl_result=pxl_result,
                iel_result=iel_result,
                math_result=math_result,
                cross_domain_syntheses=cross_syntheses,
                trinity_coherence=trinity_coherence,
                overall_confidence=overall_confidence,
                key_insights=key_insights,
                proven_theorems=proven_theorems,
                recommended_actions=recommendations
            )
            
            self.logger.info(
                f"Unified reasoning completed: "
                f"{len(cross_syntheses)} syntheses, "
                f"confidence={overall_confidence:.3f}"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Unified reasoning failed: {e}")
            raise
    
    def _synthesize_cross_domain(
        self,
        iel_result: IELReasoningResult,
        math_result: MathReasoningResult,
        pxl_result: PXLReasoningResult
    ) -> List[CrossDomainSynthesis]:
        """Perform cross-domain synthesis between IEL and Math"""
        
        syntheses = []
        
        # Find IEL-Math correspondences
        for iel_analysis in iel_result.domain_analyses:
            iel_domain = iel_analysis.domain
            
            # Get corresponding math categories
            corresponding_math = self.iel_math_map.get(iel_domain, [])
            
            for math_analysis in math_result.category_analyses:
                if math_analysis.category in corresponding_math:
                    # Create synthesis
                    synthesis = self._create_synthesis(
                        iel_analysis,
                        math_analysis,
                        pxl_result
                    )
                    
                    if synthesis:
                        syntheses.append(synthesis)
        
        # Sort by synergy score
        syntheses.sort(key=lambda s: s.synergy_score, reverse=True)
        
        return syntheses
    
    def _create_synthesis(
        self,
        iel_analysis,
        math_analysis,
        pxl_result: PXLReasoningResult
    ) -> Optional[CrossDomainSynthesis]:
        """Create a cross-domain synthesis"""
        
        try:
            # Calculate synergy score
            synergy = self._calculate_synergy(
                iel_analysis.confidence,
                math_analysis.confidence,
                iel_analysis.trinity_alignment,
                math_analysis.trinity_alignment
            )
            
            # Amplified insights (combine both perspectives)
            amplified_insights = []
            
            # Philosophical insights with mathematical support
            for iel_insight in iel_analysis.insights:
                if math_analysis.theorems_applied:
                    amplified_insights.append(
                        f"{iel_insight} (mathematically verified: "
                        f"{math_analysis.theorems_applied[0]})"
                    )
            
            # Mathematical theorems with philosophical grounding
            for theorem in math_analysis.theorems_applied:
                if iel_analysis.insights:
                    amplified_insights.append(
                        f"{theorem} (philosophically grounded: "
                        f"{iel_analysis.domain.value})"
                    )
            
            # Formal mathematical support
            formal_support = {
                "theorems": math_analysis.theorems_applied,
                "proofs": len(math_analysis.proofs_generated),
                "formal_properties": math_analysis.formal_properties
            }
            
            # Philosophical grounding
            philosophical_grounding = {
                "domain": iel_analysis.domain.value,
                "insights": iel_analysis.insights,
                "supporting_relations": len(iel_analysis.supporting_relations)
            }
            
            return CrossDomainSynthesis(
                iel_domain=iel_analysis.domain,
                math_category=math_analysis.category,
                synergy_score=synergy,
                amplified_insights=amplified_insights,
                formal_support=formal_support,
                philosophical_grounding=philosophical_grounding
            )
            
        except Exception as e:
            self.logger.error(f"Synthesis creation failed: {e}")
            return None
    
    def _calculate_synergy(
        self,
        iel_confidence: float,
        math_confidence: float,
        iel_trinity: TrinityVector,
        math_trinity: TrinityVector
    ) -> float:
        """Calculate synergy score between IEL and Math analysis"""
        
        # Confidence synergy (multiplicative)
        confidence_synergy = iel_confidence * math_confidence
        
        # Trinity alignment synergy
        trinity_coherence = iel_trinity.coherence_with(math_trinity)
        
        # Combined synergy (weighted)
        synergy = 0.6 * confidence_synergy + 0.4 * trinity_coherence
        
        return synergy
    
    def _calculate_unified_trinity_coherence(
        self,
        pxl_result: PXLReasoningResult,
        iel_result: IELReasoningResult,
        math_result: MathReasoningResult
    ) -> TrinityVector:
        """Calculate unified Trinity coherence across all layers"""
        
        # PXL Trinity alignment
        pxl_trinity = pxl_result.context.trinity_vector
        
        # IEL Trinity alignment (average)
        if iel_result.domain_analyses:
            iel_e = sum(a.trinity_alignment.essence for a in iel_result.domain_analyses)
            iel_g = sum(a.trinity_alignment.generation for a in iel_result.domain_analyses)
            iel_t = sum(a.trinity_alignment.temporal for a in iel_result.domain_analyses)
            n = len(iel_result.domain_analyses)
            iel_trinity = TrinityVector(iel_e/n, iel_g/n, iel_t/n)
        else:
            iel_trinity = TrinityVector(0.5, 0.5, 0.5)
        
        # Math Trinity alignment (average)
        if math_result.category_analyses:
            math_e = sum(a.trinity_alignment.essence for a in math_result.category_analyses)
            math_g = sum(a.trinity_alignment.generation for a in math_result.category_analyses)
            math_t = sum(a.trinity_alignment.temporal for a in math_result.category_analyses)
            n = len(math_result.category_analyses)
            math_trinity = TrinityVector(math_e/n, math_g/n, math_t/n)
        else:
            math_trinity = TrinityVector(0.5, 0.5, 0.5)
        
        # Unified Trinity (weighted average)
        unified = TrinityVector(
            essence=0.3 * pxl_trinity.essence + 0.4 * iel_trinity.essence + 0.3 * math_trinity.essence,
            generation=0.3 * pxl_trinity.generation + 0.4 * iel_trinity.generation + 0.3 * math_trinity.generation,
            temporal=0.3 * pxl_trinity.temporal + 0.4 * iel_trinity.temporal + 0.3 * math_trinity.temporal
        )
        
        return unified
    
    def _calculate_overall_confidence(
        self,
        pxl_result: PXLReasoningResult,
        iel_result: IELReasoningResult,
        math_result: MathReasoningResult,
        syntheses: List[CrossDomainSynthesis]
    ) -> float:
        """Calculate overall reasoning confidence"""
        
        # PXL confidence
        pxl_conf = pxl_result.trinity_coherence
        
        # IEL confidence
        iel_conf = iel_result.overall_coherence
        
        # Math confidence
        math_conf = math_result.mathematical_coherence
        
        # Synthesis confidence (bonus for high synergy)
        if syntheses:
            synthesis_conf = sum(s.synergy_score for s in syntheses) / len(syntheses)
            synthesis_bonus = 0.1 * synthesis_conf
        else:
            synthesis_bonus = 0.0
        
        # Weighted confidence
        overall = (
            0.25 * pxl_conf +
            0.35 * iel_conf +
            0.3 * math_conf +
            synthesis_bonus
        )
        
        return min(1.0, overall)
    
    def _extract_key_insights(
        self,
        iel_result: IELReasoningResult,
        math_result: MathReasoningResult,
        syntheses: List[CrossDomainSynthesis]
    ) -> List[str]:
        """Extract key insights from unified analysis"""
        
        insights = []
        
        # Top IEL insights
        for analysis in iel_result.domain_analyses[:3]:
            if analysis.insights:
                insights.append(f"[{analysis.domain.value}] {analysis.insights[0]}")
        
        # Top math insights
        for analysis in math_result.category_analyses[:3]:
            if analysis.theorems_applied:
                insights.append(f"[{analysis.category.value}] {analysis.theorems_applied[0]}")
        
        # Top synthesis insights
        for synthesis in syntheses[:3]:
            if synthesis.amplified_insights:
                insights.append(f"[SYNTHESIS] {synthesis.amplified_insights[0]}")
        
        return insights
    
    def _generate_unified_recommendations(
        self,
        iel_result: IELReasoningResult,
        math_result: MathReasoningResult,
        syntheses: List[CrossDomainSynthesis],
        confidence: float
    ) -> List[str]:
        """Generate unified recommendations"""
        
        recommendations = []
        
        # Confidence-based recommendations
        if confidence > 0.8:
            recommendations.append("HIGH CONFIDENCE: Proceed with synthesis conclusions")
        elif confidence > 0.6:
            recommendations.append("MODERATE CONFIDENCE: Validate key assumptions")
        else:
            recommendations.append("LOW CONFIDENCE: Gather additional evidence")
        
        # IEL recommendations
        recommendations.extend(iel_result.recommended_actions[:2])
        
        # Synthesis-based recommendations
        if syntheses and syntheses[0].synergy_score > 0.7:
            recommendations.append(
                f"Strong synergy detected between {syntheses[0].iel_domain.value} "
                f"and {syntheses[0].math_category.value} - leverage this alignment"
            )
        
        # Mathematical verification recommendations
        if math_result.formal_verification.get("soundness", False):
            recommendations.append("Mathematical soundness verified - conclusions are well-founded")
        
        return recommendations
    
    def _create_failed_result(self, pxl_result: PXLReasoningResult) -> UnifiedReasoningResult:
        """Create failed result when PXL reasoning fails"""
        return UnifiedReasoningResult(
            pxl_result=pxl_result,
            iel_result=None,
            math_result=None,
            cross_domain_syntheses=[],
            trinity_coherence=TrinityVector(0, 0, 0),
            overall_confidence=0.0,
            key_insights=[],
            proven_theorems=[],
            recommended_actions=["PXL reasoning failed - review input concepts"]
        )
    
    def get_mapping_info(self) -> Dict[str, Any]:
        """Get information about IEL-Math mapping"""
        return {
            "iel_to_math": {
                iel.value: [m.value for m in maths]
                for iel, maths in self.iel_math_map.items()
            },
            "math_to_iel": {
                math.value: [i.value for i in iels]
                for math, iels in self.math_iel_map.items()
            }
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get unified engine statistics"""
        return {
            "unified_operations": self.reasoning_operations,
            "synthesis_operations": self.synthesis_operations,
            "pxl_stats": self.pxl_engine.get_statistics(),
            "available_iel_domains": len(self.iel_engine.domains),
            "available_math_categories": len(self.math_engine.math_systems)
        }


# Global unified engine instance
_unified_engine = None

def get_unified_engine() -> UnifiedReasoningEngine:
    """Get or create global unified engine instance"""
    global _unified_engine
    if _unified_engine is None:
        _unified_engine = UnifiedReasoningEngine()
    return _unified_engine


__all__ = [
    "UnifiedReasoningEngine",
    "UnifiedReasoningResult",
    "CrossDomainSynthesis",
    "IEL_MATH_MAPPING",
    "MATH_IEL_MAPPING",
    "get_unified_engine"
]
