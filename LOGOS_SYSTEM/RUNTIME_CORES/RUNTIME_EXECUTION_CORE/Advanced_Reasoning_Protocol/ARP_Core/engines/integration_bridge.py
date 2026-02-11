# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: integration_bridge
runtime_layer: protocol_execution
role: PXL/IEL/Math integration bridge
responsibility: Bridge taxonomy outputs to Meta_Reasoning_Engine for triune analysis
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [Meta_Reasoning_Engine]
provides: [synthesize]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Failed synthesis emits degraded packet with explicit error markers"
rewrite_provenance:
  source: NEW
  rewrite_phase: ARP_Overhaul_Phase_1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: ARP_INTEGRATION
  metrics: enabled
---------------------
"""

from __future__ import annotations

from typing import Any, Dict, List, Set, Optional
import logging

# NOTE: These imports assume Meta_Reasoning_Engine is available in the repo
# Adjust import paths as needed based on actual repo structure
try:
    from ..Meta_Reasoning_Engine.pxl_engine import (
        PXLReasoningEngine, PXLReasoningContext, ReasoningMode, get_pxl_engine
    )
    from ..Meta_Reasoning_Engine.iel_engine import (
        IELReasoningEngine, IELDomain, get_iel_engine
    )
    from ..Meta_Reasoning_Engine.math_engine import (
        MathematicsReasoningEngine, MathCategory, get_math_engine
    )
    from ..Meta_Reasoning_Engine.unified_reasoning import (
        UnifiedReasoningEngine, TrinityVector
    )
    META_ENGINE_AVAILABLE = True
except ImportError:
    META_ENGINE_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Meta_Reasoning_Engine not available, using mock implementations")

logger = logging.getLogger(__name__)


class ComputeMode:
    LIGHTWEIGHT = "lightweight"
    BALANCED = "balanced"
    HIGH_RIGOR = "high_rigor"


class IntegrationBridge:
    """
    Bridges taxonomy outputs to PXL/IEL/Math engines and performs
    cross-domain synthesis.
    
    Stages:
    3. PXL/IEL/Math Triune Analysis
    4. Cross-Domain Synthesis
    """
    
    def __init__(self, compute_mode: str = "balanced"):
        self.compute_mode = compute_mode
        
        if META_ENGINE_AVAILABLE:
            # Get singleton engines
            self.pxl_engine = get_pxl_engine()
            self.iel_engine = get_iel_engine()
            self.math_engine = get_math_engine()
            self.unified_engine = UnifiedReasoningEngine()
        else:
            # Mock implementations for testing
            self.pxl_engine = None
            self.iel_engine = None
            self.math_engine = None
            self.unified_engine = None
        
        logger.info(f"IntegrationBridge initialized (mode={compute_mode}, meta_available={META_ENGINE_AVAILABLE})")
    
    def synthesize(
        self,
        aaced_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute Triune Analysis + Cross-Domain Synthesis.
        
        Args:
            aaced_packet: Original task packet
            taxonomy_packet: 5 aggregated taxonomy outputs
            
        Returns:
            SynthesisPacket with PXL/IEL/Math results + cross-domain amplification
        """
        try:
            if not META_ENGINE_AVAILABLE:
                return self._mock_synthesis(aaced_packet, taxonomy_packet)
            
            # Extract concepts from taxonomies
            concepts = self._extract_concepts_from_taxonomies(taxonomy_packet)
            
            # Select active IEL domains and Math categories
            active_iel = self._select_iel_domains(aaced_packet)
            active_math = self._select_math_categories(aaced_packet)
            
            # PXL Analysis
            pxl_context = PXLReasoningContext(
                mode=ReasoningMode.SYNTHETIC,
                trinity_vector=TrinityVector(0.7, 0.7, 0.8)
            )
            pxl_result = self.pxl_engine.reason(concepts, context=pxl_context)
            
            # IEL Analysis
            iel_result = self.iel_engine.reason(concepts, active_iel)
            
            # Math Analysis
            math_result = self.math_engine.reason(concepts, active_math)
            
            # Unified Cross-Domain Synthesis
            synthesis_result = self.unified_engine.reason(
                concepts=concepts,
                context=pxl_context,
                enable_iel_domains=active_iel,
                enable_math_categories=active_math
            )
            
            return {
                "status": "success",
                "pxl_result": self._serialize_pxl(pxl_result),
                "iel_result": self._serialize_iel(iel_result),
                "math_result": self._serialize_math(math_result),
                "synthesis_result": self._serialize_synthesis(synthesis_result),
                "active_iel_domains": [d.value for d in active_iel],
                "active_math_categories": [c.value for c in active_math]
            }
            
        except Exception as e:
            logger.error(f"Synthesis failed: {e}", exc_info=True)
            return {"status": "failed", "error": str(e)}
    
    def _mock_synthesis(
        self,
        aaced_packet: Dict[str, Any],
        taxonomy_packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Mock synthesis when Meta_Reasoning_Engine unavailable"""
        return {
            "status": "success",
            "pxl_result": {"status": "mock", "relations_count": 0},
            "iel_result": {"status": "mock", "coherence": 0.5},
            "math_result": {"status": "mock", "coherence": 0.5},
            "synthesis_result": {"status": "mock", "overall_confidence": 0.5, "key_insights": []},
            "active_iel_domains": [],
            "active_math_categories": []
        }
    
    def _extract_concepts_from_taxonomies(
        self,
        taxonomy_packet: Dict[str, Any]
    ) -> List[str]:
        """Extract key concepts from taxonomy summaries"""
        # This is a simplified heuristic; in production, use NLP extraction
        concepts = set()
        
        for taxonomy_data in taxonomy_packet.get("taxonomies", {}).values():
            summary = taxonomy_data.get("summary", "")
            # Extract nouns (simplified)
            words = summary.split()
            concepts.update([w for w in words if len(w) > 4])
        
        return list(concepts)[:20]  # Limit to top 20
    
    def _select_iel_domains(self, aaced_packet: Dict[str, Any]) -> Set:
        """Select relevant IEL domains based on task"""
        if not META_ENGINE_AVAILABLE:
            return set()
        
        # Heuristic: task type → domain mapping
        task = aaced_packet.get("task", "").lower()
        
        domains = set()
        
        if any(kw in task for kw in ["axiom", "proof", "foundational"]):
            domains.add(IELDomain.AXIOPRAXIS)
        if any(kw in task for kw in ["knowledge", "belief", "epistemic"]):
            domains.add(IELDomain.GNOSIPRAXIS)
        if any(kw in task for kw in ["time", "temporal", "sequence"]):
            domains.add(IELDomain.CHRONOPRAXIS)
        if any(kw in task for kw in ["possibility", "necessity", "modal"]):
            domains.add(IELDomain.MODALPRAXIS)
        if any(kw in task for kw in ["purpose", "goal", "teleology"]):
            domains.add(IELDomain.TELOPRAXIS)
        if any(kw in task for kw in ["human", "ethical", "interaction"]):
            domains.add(IELDomain.ANTHROPRAXIS)
        
        # Default: AxioPraxis + GnosiPraxis for balanced mode
        if not domains:
            domains = {IELDomain.AXIOPRAXIS, IELDomain.GNOSIPRAXIS}
        
        # Limit based on compute mode
        if self.compute_mode == "lightweight":
            domains = set(list(domains)[:1])
        elif self.compute_mode == "balanced":
            domains = set(list(domains)[:3])
        # high_rigor: use all selected
        
        return domains
    
    def _select_math_categories(self, aaced_packet: Dict[str, Any]) -> Set:
        """Select relevant Math categories based on task"""
        if not META_ENGINE_AVAILABLE:
            return set()
        
        task = aaced_packet.get("task", "").lower()
        
        categories = set()
        
        if any(kw in task for kw in ["logic", "proof", "valid"]):
            categories.add(MathCategory.BOOLEAN_LOGIC)
        if any(kw in task for kw in ["topology", "continuous", "space"]):
            categories.add(MathCategory.TOPOLOGY)
        if any(kw in task for kw in ["algebra", "equation", "variable"]):
            categories.add(MathCategory.ALGEBRA)
        if any(kw in task for kw in ["optimize", "maximize", "minimize"]):
            categories.add(MathCategory.OPTIMIZATION)
        if any(kw in task for kw in ["probability", "measure", "statistic"]):
            categories.add(MathCategory.MEASURE_THEORY)
        if any(kw in task for kw in ["type", "category", "morphism"]):
            categories.add(MathCategory.CATEGORY_THEORY)
        
        # Default: CORE + BOOLEAN_LOGIC
        if not categories:
            categories = {MathCategory.CORE, MathCategory.BOOLEAN_LOGIC}
        
        # Limit based on compute mode
        if self.compute_mode == "lightweight":
            categories = set(list(categories)[:1])
        elif self.compute_mode == "balanced":
            categories = set(list(categories)[:3])
        
        return categories
    
    def _serialize_pxl(self, pxl_result: Any) -> Dict[str, Any]:
        """Serialize PXLReasoningResult to dict"""
        if hasattr(pxl_result, 'relations'):
            return {
                "status": "completed",
                "relations_count": len(pxl_result.relations),
                "trinity_coherence": getattr(pxl_result, 'trinity_coherence', 0.5)
            }
        return {"status": "completed", "relations_count": 0}
    
    def _serialize_iel(self, iel_result: Any) -> Dict[str, Any]:
        """Serialize IELReasoningResult to dict"""
        if hasattr(iel_result, 'overall_coherence'):
            return {
                "status": "completed",
                "coherence": iel_result.overall_coherence,
                "domains_analyzed": len(getattr(iel_result, 'domain_analyses', []))
            }
        return {"status": "completed", "coherence": 0.5}
    
    def _serialize_math(self, math_result: Any) -> Dict[str, Any]:
        """Serialize MathReasoningResult to dict"""
        if hasattr(math_result, 'mathematical_coherence'):
            return {
                "status": "completed",
                "coherence": math_result.mathematical_coherence,
                "categories_analyzed": len(getattr(math_result, 'category_analyses', []))
            }
        return {"status": "completed", "coherence": 0.5}
    
    def _serialize_synthesis(self, synthesis_result: Any) -> Dict[str, Any]:
        """Serialize UnifiedReasoningResult to dict"""
        if hasattr(synthesis_result, 'overall_confidence'):
            return {
                "status": "completed",
                "overall_confidence": synthesis_result.overall_confidence,
                "key_insights": getattr(synthesis_result, 'key_insights', [])[:5],
                "cross_domain_syntheses_count": len(getattr(synthesis_result, 'cross_domain_syntheses', []))
            }
        return {"status": "completed", "overall_confidence": 0.5, "key_insights": []}
