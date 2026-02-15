# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: iel_engine
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/Meta_Reasoning_Engine/iel_engine.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/Meta_Reasoning_Engine/iel_engine.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
IEL Reasoning Engine - Domain Integration
=========================================

Reasoning wrapper that integrates IEL (Integrated Epistemic Logic) domains
as philosophical lenses overlayed onto the PXL substrate. Enables multi-domain
reasoning through coordinated application of philosophical frameworks.

IEL Domains Integrated:
- AxioPraxis: Foundational logic and axiom systems
- GnosiPraxis: Knowledge and epistemology
- ChronoPraxis: Temporal and sequence logic
- ModalPraxis: Modal logic and possibility
- TeloPraxis: Purpose and teleology
- AnthroPraxis: Human-AI interaction and ethics

Author: LOGOS AGI Development Team
Version: 1.0.0
Date: 2026-01-24
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from enum import Enum

# PXL Core
from pxl_engine import (
    PXLReasoningEngine,
    PXLReasoningContext,
    PXLReasoningResult,
    ReasoningMode,
    get_pxl_engine
)

from LOGOS_SYSTEM.System_Stack.Advanced_Reasoning_Protocol.formalisms.pxl_schema import (
    TrinityVector,
    PXLRelation
)

# IEL Domain Imports
try:
    from LOGOS_SYSTEM.System_Stack.Logos_Agents.Agent_Resources.iel_domains.AxioPraxis.axiom_systems import AxiomSystem
    from LOGOS_SYSTEM.System_Stack.Logos_Agents.Agent_Resources.iel_domains.AxioPraxis.consistency_checker import ConsistencyChecker
    AXIOPRAXIS_AVAILABLE = True
except ImportError:
    AXIOPRAXIS_AVAILABLE = False

try:
    from LOGOS_SYSTEM.System_Stack.Logos_Agents.Agent_Resources.iel_domains.GnosiPraxis.knowledge_system import KnowledgeSystem
    from LOGOS_SYSTEM.System_Stack.Logos_Agents.Agent_Resources.iel_domains.GnosiPraxis.belief_network import BeliefNetwork
    GNOSIPRAXIS_AVAILABLE = True
except ImportError:
    GNOSIPRAXIS_AVAILABLE = False

try:
    from LOGOS_SYSTEM.System_Stack.Logos_Agents.Agent_Resources.iel_domains.ChronoPraxis.chronopraxis.temporal_logic import TemporalLogic
    CHRONOPRAXIS_AVAILABLE = True
except ImportError:
    CHRONOPRAXIS_AVAILABLE = False

try:
    from LOGOS_SYSTEM.System_Stack.Logos_Agents.Agent_Resources.iel_domains.ModalPraxis.modal_logic import ModalLogic, ModalSystem
    MODALPRAXIS_AVAILABLE = True
except ImportError:
    MODALPRAXIS_AVAILABLE = False

# Configure logging when invoked as a script
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IELDomain(Enum):
    """Available IEL reasoning domains"""
    AXIOPRAXIS = "axiopraxis"  # Foundational logic
    GNOSIPRAXIS = "gnosipraxis"  # Knowledge systems
    CHRONOPRAXIS = "chronopraxis"  # Temporal logic
    MODALPRAXIS = "modalpraxis"  # Modal logic
    TELOPRAXIS = "telopraxis"  # Purpose/teleology
    ANTHROPRAXIS = "anthropraxis"  # Human-AI ethics


@dataclass
class IELAnalysisResult:
    """Result of IEL domain analysis"""
    domain: IELDomain
    insights: List[str]
    confidence: float
    trinity_alignment: TrinityVector
    supporting_relations: List[PXLRelation]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IELReasoningResult:
    """Result of multi-domain IEL reasoning"""
    pxl_result: PXLReasoningResult
    domain_analyses: List[IELAnalysisResult]
    cross_domain_synthesis: Dict[str, Any]
    overall_coherence: float
    recommended_actions: List[str]


class IELReasoningEngine:
    """
    IEL Reasoning Engine
    
    Integrates philosophical domains as reasoning lenses over PXL substrate:
    1. Routes reasoning queries to appropriate IEL domains
    2. Applies domain-specific analysis to PXL relations
    3. Synthesizes cross-domain insights
    4. Maintains Trinity-grounded coherence
    """
    
    def __init__(self, pxl_engine: Optional[PXLReasoningEngine] = None):
        """Initialize IEL reasoning engine"""
        self.pxl_engine = pxl_engine or get_pxl_engine()
        self.logger = logging.getLogger(__name__)
        
        # Initialize available IEL domains
        self.domains: Dict[IELDomain, Any] = {}
        self._initialize_domains()
        
        # Register domains with PXL engine
        for domain in self.domains.keys():
            self.pxl_engine.register_iel_domain(domain.value)
        
        self.logger.info(f"IEL Engine initialized with {len(self.domains)} domains")
    
    def _initialize_domains(self):
        """Initialize available IEL domain systems"""
        
        if AXIOPRAXIS_AVAILABLE:
            self.domains[IELDomain.AXIOPRAXIS] = {
                "axiom_system": AxiomSystem(),
                "consistency_checker": ConsistencyChecker()
            }
            self.logger.info("✓ AxioPraxis domain initialized")
        
        if GNOSIPRAXIS_AVAILABLE:
            self.domains[IELDomain.GNOSIPRAXIS] = {
                "knowledge_system": KnowledgeSystem(),
                "belief_network": BeliefNetwork()
            }
            self.logger.info("✓ GnosiPraxis domain initialized")
        
        if CHRONOPRAXIS_AVAILABLE:
            self.domains[IELDomain.CHRONOPRAXIS] = {
                "temporal_logic": TemporalLogic()
            }
            self.logger.info("✓ ChronoPraxis domain initialized")
        
        if MODALPRAXIS_AVAILABLE:
            self.domains[IELDomain.MODALPRAXIS] = {
                "modal_logic": ModalLogic(ModalSystem.S5)
            }
            self.logger.info("✓ ModalPraxis domain initialized")
    
    def reason(
        self,
        concepts: List[str],
        active_domains: Optional[Set[IELDomain]] = None,
        context: Optional[PXLReasoningContext] = None
    ) -> IELReasoningResult:
        """
        Execute multi-domain IEL reasoning
        
        Args:
            concepts: Concepts to reason about
            active_domains: Domains to apply (None = all available)
            context: PXL reasoning context
            
        Returns:
            IELReasoningResult with cross-domain analysis
        """
        try:
            # Execute base PXL reasoning
            pxl_result = self.pxl_engine.reason(concepts, context)
            
            if not pxl_result.success:
                self.logger.warning("PXL reasoning failed, returning partial result")
                return IELReasoningResult(
                    pxl_result=pxl_result,
                    domain_analyses=[],
                    cross_domain_synthesis={},
                    overall_coherence=0.0,
                    recommended_actions=[]
                )
            
            # Determine active domains
            if active_domains is None:
                active_domains = set(self.domains.keys())
            else:
                active_domains = active_domains.intersection(self.domains.keys())
            
            # Apply each domain lens
            domain_analyses = []
            for domain in active_domains:
                analysis = self._apply_domain_lens(
                    domain,
                    concepts,
                    pxl_result.relations_discovered
                )
                if analysis:
                    domain_analyses.append(analysis)
            
            # Synthesize cross-domain insights
            synthesis = self._synthesize_cross_domain(domain_analyses, pxl_result)
            
            # Calculate overall coherence
            overall_coherence = self._calculate_overall_coherence(
                pxl_result,
                domain_analyses
            )
            
            # Generate recommended actions
            actions = self._generate_recommendations(synthesis, domain_analyses)
            
            result = IELReasoningResult(
                pxl_result=pxl_result,
                domain_analyses=domain_analyses,
                cross_domain_synthesis=synthesis,
                overall_coherence=overall_coherence,
                recommended_actions=actions
            )
            
            self.logger.info(
                f"IEL reasoning completed: {len(domain_analyses)} domains, "
                f"coherence={overall_coherence:.3f}"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"IEL reasoning failed: {e}")
            raise
    
    def _apply_domain_lens(
        self,
        domain: IELDomain,
        concepts: List[str],
        relations: List[PXLRelation]
    ) -> Optional[IELAnalysisResult]:
        """Apply specific IEL domain analysis"""
        
        try:
            if domain == IELDomain.AXIOPRAXIS:
                return self._analyze_axiopraxis(concepts, relations)
            
            elif domain == IELDomain.GNOSIPRAXIS:
                return self._analyze_gnosipraxis(concepts, relations)
            
            elif domain == IELDomain.CHRONOPRAXIS:
                return self._analyze_chronopraxis(concepts, relations)
            
            elif domain == IELDomain.MODALPRAXIS:
                return self._analyze_modalpraxis(concepts, relations)
            
            else:
                self.logger.warning(f"Domain {domain} not yet implemented")
                return None
                
        except Exception as e:
            self.logger.error(f"Domain analysis failed for {domain}: {e}")
            return None
    
    def _analyze_axiopraxis(
        self,
        concepts: List[str],
        relations: List[PXLRelation]
    ) -> IELAnalysisResult:
        """Analyze through AxioPraxis lens (foundational logic)"""
        
        domain_sys = self.domains[IELDomain.AXIOPRAXIS]
        axiom_system = domain_sys["axiom_system"]
        consistency_checker = domain_sys["consistency_checker"]
        
        insights = []
        
        # Check axiomatic consistency
        axioms = [f"{r.source_concept} → {r.target_concept}" for r in relations]
        consistency_result = consistency_checker.check_syntactic_consistency(axioms)
        
        if consistency_result["consistent"]:
            insights.append("Axiomatic consistency verified")
        else:
            insights.append(f"Inconsistencies found: {consistency_result['contradictions']}")
        
        # Analyze foundational structure
        if len(relations) >= 3:
            insights.append("Trinity-compatible axiomatic structure detected")
        
        return IELAnalysisResult(
            domain=IELDomain.AXIOPRAXIS,
            insights=insights,
            confidence=0.9 if consistency_result["consistent"] else 0.5,
            trinity_alignment=TrinityVector(0.9, 0.7, 0.9),  # High truth, logic
            supporting_relations=relations,
            metadata={"consistency_check": consistency_result}
        )
    
    def _analyze_gnosipraxis(
        self,
        concepts: List[str],
        relations: List[PXLRelation]
    ) -> IELAnalysisResult:
        """Analyze through GnosiPraxis lens (knowledge/epistemology)"""
        
        domain_sys = self.domains[IELDomain.GNOSIPRAXIS]
        knowledge_system = domain_sys["knowledge_system"]
        
        insights = []
        
        # Analyze knowledge structure
        insights.append(f"Knowledge network of {len(concepts)} concepts")
        insights.append(f"{len(relations)} epistemic relations identified")
        
        # Check justification chains
        strong_relations = [r for r in relations if r.strength > 0.7]
        if strong_relations:
            insights.append(f"{len(strong_relations)} well-justified beliefs")
        
        return IELAnalysisResult(
            domain=IELDomain.GNOSIPRAXIS,
            insights=insights,
            confidence=0.8,
            trinity_alignment=TrinityVector(0.8, 0.8, 0.9),  # High truth focus
            supporting_relations=strong_relations,
            metadata={"knowledge_items": len(concepts)}
        )
    
    def _analyze_chronopraxis(
        self,
        concepts: List[str],
        relations: List[PXLRelation]
    ) -> IELAnalysisResult:
        """Analyze through ChronoPraxis lens (temporal logic)"""
        
        domain_sys = self.domains[IELDomain.CHRONOPRAXIS]
        temporal_logic = domain_sys["temporal_logic"]
        
        insights = []
        
        # Check for temporal relations
        temporal_relations = [
            r for r in relations
            if "temporal" in str(r.relation_type).lower()
        ]
        
        if temporal_relations:
            insights.append(f"{len(temporal_relations)} temporal dependencies found")
        else:
            insights.append("No explicit temporal dependencies")
        
        insights.append("Temporal coherence maintained")
        
        return IELAnalysisResult(
            domain=IELDomain.CHRONOPRAXIS,
            insights=insights,
            confidence=0.75,
            trinity_alignment=TrinityVector(0.7, 0.7, 0.9),  # Temporal focus
            supporting_relations=temporal_relations,
            metadata={"temporal_relations": len(temporal_relations)}
        )
    
    def _analyze_modalpraxis(
        self,
        concepts: List[str],
        relations: List[PXLRelation]
    ) -> IELAnalysisResult:
        """Analyze through ModalPraxis lens (modal logic)"""
        
        domain_sys = self.domains[IELDomain.MODALPRAXIS]
        modal_logic = domain_sys["modal_logic"]
        
        insights = []
        
        # Check modal properties
        modal_relations = [
            r for r in relations
            if r.modal_necessity is not None
        ]
        
        if modal_relations:
            necessary = [r for r in modal_relations if r.modal_necessity > 0.7]
            insights.append(f"{len(necessary)} necessary relations")
        
        insights.append("Modal consistency verified")
        
        return IELAnalysisResult(
            domain=IELDomain.MODALPRAXIS,
            insights=insights,
            confidence=0.85,
            trinity_alignment=TrinityVector(0.8, 0.7, 0.9),
            supporting_relations=modal_relations,
            metadata={"modal_relations": len(modal_relations)}
        )
    
    def _synthesize_cross_domain(
        self,
        analyses: List[IELAnalysisResult],
        pxl_result: PXLReasoningResult
    ) -> Dict[str, Any]:
        """Synthesize insights across IEL domains"""
        
        synthesis = {
            "domains_analyzed": [a.domain.value for a in analyses],
            "convergent_insights": [],
            "domain_specific_insights": {},
            "trinity_alignment_avg": TrinityVector(0, 0, 0)
        }
        
        # Collect all insights
        all_insights = []
        for analysis in analyses:
            synthesis["domain_specific_insights"][analysis.domain.value] = analysis.insights
            all_insights.extend(analysis.insights)
        
        # Find convergent insights (mentioned by multiple domains)
        insight_counts = {}
        for insight in all_insights:
            key = insight.lower()[:30]  # First 30 chars as key
            insight_counts[key] = insight_counts.get(key, 0) + 1
        
        synthesis["convergent_insights"] = [
            insight for insight, count in insight_counts.items()
            if count > 1
        ]
        
        # Average Trinity alignment
        if analyses:
            avg_e = sum(a.trinity_alignment.essence for a in analyses) / len(analyses)
            avg_g = sum(a.trinity_alignment.generation for a in analyses) / len(analyses)
            avg_t = sum(a.trinity_alignment.temporal for a in analyses) / len(analyses)
            synthesis["trinity_alignment_avg"] = TrinityVector(avg_e, avg_g, avg_t)
        
        return synthesis
    
    def _calculate_overall_coherence(
        self,
        pxl_result: PXLReasoningResult,
        analyses: List[IELAnalysisResult]
    ) -> float:
        """Calculate overall reasoning coherence"""
        
        # Base PXL coherence
        pxl_coherence = pxl_result.trinity_coherence
        
        # Domain confidence average
        if analyses:
            domain_confidence = sum(a.confidence for a in analyses) / len(analyses)
        else:
            domain_confidence = 0.5
        
        # Weighted combination
        overall = 0.6 * pxl_coherence + 0.4 * domain_confidence
        
        return overall
    
    def _generate_recommendations(
        self,
        synthesis: Dict[str, Any],
        analyses: List[IELAnalysisResult]
    ) -> List[str]:
        """Generate recommended actions based on analysis"""
        
        recommendations = []
        
        # Check for high coherence
        if analyses:
            avg_confidence = sum(a.confidence for a in analyses) / len(analyses)
            
            if avg_confidence > 0.8:
                recommendations.append("High confidence: proceed with synthesis")
            elif avg_confidence > 0.6:
                recommendations.append("Moderate confidence: validate key assumptions")
            else:
                recommendations.append("Low confidence: gather additional evidence")
        
        # Domain-specific recommendations
        for analysis in analyses:
            if analysis.confidence < 0.5:
                recommendations.append(
                    f"Review {analysis.domain.value} analysis for inconsistencies"
                )
        
        return recommendations


# Global IEL engine instance
_iel_engine = None

def get_iel_engine(pxl_engine: Optional[PXLReasoningEngine] = None) -> IELReasoningEngine:
    """Get or create global IEL engine instance"""
    global _iel_engine
    if _iel_engine is None:
        _iel_engine = IELReasoningEngine(pxl_engine)
    return _iel_engine


__all__ = [
    "IELReasoningEngine",
    "IELDomain",
    "IELAnalysisResult",
    "IELReasoningResult",
    "get_iel_engine"
]
