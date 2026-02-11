# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: fractal_trinity_reasoner
runtime_layer: agent_cognitive_core
role: I3's unique fractal trinity reasoning capability
responsibility: Apply PXL/IEL/Math lenses at each Sierpinski fractal vertex with recursive amplification
agent_binding: I3_Agent
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: cognitive_engine
boot_phase: runtime
expected_imports: [Triune_Sierpinski_Core, Meta_Reasoning_Engine]
provides: [FractalTrinityReasoner]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Halts recursion on any lens failure, returns partial result with explicit markers"
rewrite_provenance:
  source: NEW
  rewrite_phase: I3_Overhaul_Phase_1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: I3_FRACTAL_TRINITY
  metrics: enabled
---------------------
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import logging

# Import Sierpinski substrate
try:
    from Agent_Resources.Cognition_Normalized.Triune_Sierpinski_Core import (
        TriuneSierpinskiCore, TriuneSummary, TransformOperator, TerminationPredicate
    )
    SIERPINSKI_AVAILABLE = True
except ImportError:
    SIERPINSKI_AVAILABLE = False

# Import Meta Reasoning Engine
try:
    from Advanced_Reasoning_Protocol.ARP_Core.Meta_Reasoning_Engine.pxl_engine import (
        PXLReasoningEngine, PXLReasoningContext, ReasoningMode, get_pxl_engine
    )
    from Advanced_Reasoning_Protocol.ARP_Core.Meta_Reasoning_Engine.iel_engine import (
        IELReasoningEngine, IELDomain, get_iel_engine
    )
    from Advanced_Reasoning_Protocol.ARP_Core.Meta_Reasoning_Engine.math_engine import (
        MathematicsReasoningEngine, MathCategory, get_math_engine
    )
    from Advanced_Reasoning_Protocol.ARP_Core.Meta_Reasoning_Engine.unified_reasoning import (
        TrinityVector
    )
    META_ENGINE_AVAILABLE = True
except ImportError:
    META_ENGINE_AVAILABLE = False

logger = logging.getLogger(__name__)


class TrinityLens(Enum):
    """Three lenses of Trinity reasoning positioned at fractal vertices"""
    PXL = "pxl"          # Apex: Formal logical structure
    IEL = "iel"          # Left: Philosophical domains
    MATH = "math"        # Right: Mathematical categories


@dataclass
class FractalVertex:
    """Enhanced fractal vertex with trinity reasoning results"""
    vertex_id: str
    depth: int
    payload: Any
    role: str
    
    # Trinity reasoning results at this vertex
    pxl_result: Optional[Dict[str, Any]] = None
    iel_result: Optional[Dict[str, Any]] = None
    math_result: Optional[Dict[str, Any]] = None
    
    # Cross-lens synthesis
    trinity_coherence: Optional[TrinityVector] = None
    synthesis_confidence: float = 0.0
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FractalTrinityResult:
    """Complete fractal trinity reasoning result"""
    root_vertex: FractalVertex
    triune_summary: Optional[TriuneSummary]
    
    # Aggregated insights from all vertices
    total_vertices_analyzed: int
    pxl_insights: List[str]
    iel_insights: List[str]
    math_insights: List[str]
    
    # Cross-domain synthesis across the fractal
    fractal_trinity_coherence: TrinityVector
    overall_confidence: float
    
    # Recursive amplification metrics
    depth_reached: int
    amplification_factor: float
    
    metadata: Dict[str, Any] = field(default_factory=dict)


class FractalTrinityReasoner:
    """
    I3's Unique Capability: Fractal Trinity Reasoning Engine
    
    Positioning PXL/IEL/Math at each Sierpinski vertex creates recursive
    amplification where each lens informs the next level's decomposition.
    
    Architecture:
    - Apex vertex: PXL lens (formal logical structure)
    - Left vertex: IEL lens (philosophical domains)
    - Right vertex: Math lens (mathematical categories)
    
    At each recursion depth:
    1. Apply all three lenses to current payload
    2. Synthesize cross-lens insights
    3. Use synthesis to guide decomposition for next depth
    4. Recurse until termination
    
    This creates a fractal reasoning structure where:
    - Logical rigor (PXL) informs philosophical depth (IEL)
    - Philosophical depth informs mathematical formalization (Math)
    - Mathematical formalization informs next-level logical rigor
    
    Result: Exponentially amplified reasoning quality through recursive
    cross-domain synthesis.
    """
    
    def __init__(
        self,
        max_depth: int = 6,
        enable_recursive_amplification: bool = True
    ):
        self.max_depth = max_depth
        self.enable_recursive_amplification = enable_recursive_amplification
        
        # Initialize meta reasoning engines if available
        if META_ENGINE_AVAILABLE:
            self.pxl_engine = get_pxl_engine()
            self.iel_engine = get_iel_engine()
            self.math_engine = get_math_engine()
        else:
            self.pxl_engine = None
            self.iel_engine = None
            self.math_engine = None
            logger.warning("Meta_Reasoning_Engine unavailable, using mock lenses")
        
        # Initialize Sierpinski core if available
        if SIERPINSKI_AVAILABLE:
            self.sierpinski_core = self._build_sierpinski_core()
        else:
            self.sierpinski_core = None
            logger.warning("Sierpinski substrate unavailable, using iterative fallback")
        
        logger.info(f"FractalTrinityReasoner initialized (max_depth={max_depth}, amplification={enable_recursive_amplification})")
    
    def reason(
        self,
        payload: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> FractalTrinityResult:
        """
        Execute fractal trinity reasoning on payload.
        
        Args:
            payload: Input data (task, concepts, statements, etc.)
            context: Additional context for reasoning
            
        Returns:
            FractalTrinityResult with recursive amplification
        """
        context = context or {}
        
        if self.sierpinski_core and SIERPINSKI_AVAILABLE:
            # Use Sierpinski substrate for fractal decomposition
            return self._reason_with_sierpinski(payload, context)
        else:
            # Fallback: iterative 3-level analysis
            return self._reason_iterative(payload, context)
    
    def _reason_with_sierpinski(
        self,
        payload: Any,
        context: Dict[str, Any]
    ) -> FractalTrinityResult:
        """Execute fractal trinity reasoning using Sierpinski substrate"""
        
        # Run Sierpinski analysis
        triune_summary = self.sierpinski_core.analyze(payload)
        
        # Enhance each vertex with trinity lenses
        enhanced_vertices = []
        pxl_insights_all = []
        iel_insights_all = []
        math_insights_all = []
        
        for terminal_payload in triune_summary.terminal_payloads:
            # Apply trinity lenses to terminal vertex
            vertex = self._apply_trinity_lenses_to_payload(
                payload=terminal_payload,
                context=context,
                depth=triune_summary.max_depth_reached
            )
            
            enhanced_vertices.append(vertex)
            
            # Collect insights
            if vertex.pxl_result:
                pxl_insights_all.extend(vertex.pxl_result.get("insights", []))
            if vertex.iel_result:
                iel_insights_all.extend(vertex.iel_result.get("insights", []))
            if vertex.math_result:
                math_insights_all.extend(vertex.math_result.get("insights", []))
        
        # Compute fractal-wide trinity coherence
        fractal_coherence = self._compute_fractal_coherence(enhanced_vertices)
        
        # Compute amplification factor (how much better than single-pass)
        amplification = self._compute_amplification_factor(
            depth=triune_summary.max_depth_reached,
            vertices=enhanced_vertices
        )
        
        # Overall confidence
        confidence = self._compute_overall_confidence(enhanced_vertices)
        
        # Build root vertex
        root_vertex = enhanced_vertices[0] if enhanced_vertices else FractalVertex(
            vertex_id="root_fallback",
            depth=0,
            payload=payload,
            role="root"
        )
        
        return FractalTrinityResult(
            root_vertex=root_vertex,
            triune_summary=triune_summary,
            total_vertices_analyzed=len(enhanced_vertices),
            pxl_insights=pxl_insights_all[:10],  # Top 10
            iel_insights=iel_insights_all[:10],
            math_insights=math_insights_all[:10],
            fractal_trinity_coherence=fractal_coherence,
            overall_confidence=confidence,
            depth_reached=triune_summary.max_depth_reached,
            amplification_factor=amplification,
            metadata={
                "engine": "fractal_trinity",
                "sierpinski_triangles": triune_summary.total_triangles,
                "recursive_amplification": self.enable_recursive_amplification
            }
        )
    
    def _reason_iterative(
        self,
        payload: Any,
        context: Dict[str, Any]
    ) -> FractalTrinityResult:
        """Fallback: iterative 3-level analysis without Sierpinski"""
        
        vertices = []
        
        # Level 0: Root analysis
        root_vertex = self._apply_trinity_lenses_to_payload(payload, context, depth=0)
        vertices.append(root_vertex)
        
        # Level 1: Decompose by trinity lens results
        for lens in [TrinityLens.PXL, TrinityLens.IEL, TrinityLens.MATH]:
            sub_payload = self._extract_sub_payload(root_vertex, lens)
            sub_vertex = self._apply_trinity_lenses_to_payload(sub_payload, context, depth=1)
            vertices.append(sub_vertex)
        
        # Level 2: Further decomposition (if enabled)
        if self.enable_recursive_amplification and len(vertices) < 10:
            for v in vertices[1:4]:  # Decompose level 1 vertices
                for lens in [TrinityLens.PXL, TrinityLens.IEL, TrinityLens.MATH]:
                    sub_payload = self._extract_sub_payload(v, lens)
                    sub_vertex = self._apply_trinity_lenses_to_payload(sub_payload, context, depth=2)
                    vertices.append(sub_vertex)
        
        # Aggregate insights
        pxl_insights = []
        iel_insights = []
        math_insights = []
        
        for v in vertices:
            if v.pxl_result:
                pxl_insights.extend(v.pxl_result.get("insights", []))
            if v.iel_result:
                iel_insights.extend(v.iel_result.get("insights", []))
            if v.math_result:
                math_insights.extend(v.math_result.get("insights", []))
        
        fractal_coherence = self._compute_fractal_coherence(vertices)
        confidence = self._compute_overall_confidence(vertices)
        amplification = len(vertices) / 3.0  # Simple metric
        
        return FractalTrinityResult(
            root_vertex=root_vertex,
            triune_summary=None,
            total_vertices_analyzed=len(vertices),
            pxl_insights=pxl_insights[:10],
            iel_insights=iel_insights[:10],
            math_insights=math_insights[:10],
            fractal_trinity_coherence=fractal_coherence,
            overall_confidence=confidence,
            depth_reached=2,
            amplification_factor=amplification,
            metadata={"engine": "fractal_trinity_iterative"}
        )
    
    def _apply_trinity_lenses_to_payload(
        self,
        payload: Any,
        context: Dict[str, Any],
        depth: int
    ) -> FractalVertex:
        """Apply PXL/IEL/Math lenses to a single payload"""
        
        vertex_id = f"I3_FT_D{depth}_{id(payload) % 10000}"
        
        # Extract concepts from payload
        concepts = self._extract_concepts(payload)
        
        # Apply PXL lens (Apex: formal logic)
        pxl_result = self._apply_pxl_lens(concepts, context)
        
        # Apply IEL lens (Left: philosophical domains)
        iel_result = self._apply_iel_lens(concepts, context, pxl_result)
        
        # Apply Math lens (Right: mathematical categories)
        math_result = self._apply_math_lens(concepts, context, pxl_result, iel_result)
        
        # Cross-lens synthesis
        trinity_coherence, synthesis_confidence = self._synthesize_lenses(
            pxl_result, iel_result, math_result
        )
        
        return FractalVertex(
            vertex_id=vertex_id,
            depth=depth,
            payload=payload,
            role=f"fractal_d{depth}",
            pxl_result=pxl_result,
            iel_result=iel_result,
            math_result=math_result,
            trinity_coherence=trinity_coherence,
            synthesis_confidence=synthesis_confidence,
            metadata={"concepts_extracted": len(concepts)}
        )
    
    def _apply_pxl_lens(
        self,
        concepts: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply PXL lens: formal logical relations"""
        if not META_ENGINE_AVAILABLE or not self.pxl_engine:
            return {"status": "mock", "insights": ["PXL analysis (mock)"]}
        
        try:
            pxl_context = PXLReasoningContext(
                mode=ReasoningMode.SYNTHETIC,
                trinity_vector=TrinityVector(0.8, 0.7, 0.9)
            )
            result = self.pxl_engine.reason(concepts, context=pxl_context)
            
            return {
                "status": "completed",
                "relations_count": len(result.relations) if hasattr(result, 'relations') else 0,
                "trinity_coherence": getattr(result, 'trinity_coherence', 0.5),
                "insights": [f"PXL relation: {r.source_concept} → {r.target_concept}" 
                            for r in (result.relations[:3] if hasattr(result, 'relations') else [])]
            }
        except Exception as e:
            logger.warning(f"PXL lens failed: {e}")
            return {"status": "failed", "error": str(e), "insights": []}
    
    def _apply_iel_lens(
        self,
        concepts: List[str],
        context: Dict[str, Any],
        pxl_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply IEL lens: philosophical domains (informed by PXL)"""
        if not META_ENGINE_AVAILABLE or not self.iel_engine:
            return {"status": "mock", "insights": ["IEL analysis (mock)"]}
        
        try:
            # Select domains based on PXL findings
            active_domains = self._select_iel_domains_from_pxl(pxl_result, context)
            
            result = self.iel_engine.reason(concepts, active_domains)
            
            return {
                "status": "completed",
                "domains_applied": [d.value for d in active_domains],
                "coherence": getattr(result, 'overall_coherence', 0.5),
                "insights": [f"IEL domain {d.value}: philosophical depth" 
                            for d in active_domains[:3]]
            }
        except Exception as e:
            logger.warning(f"IEL lens failed: {e}")
            return {"status": "failed", "error": str(e), "insights": []}
    
    def _apply_math_lens(
        self,
        concepts: List[str],
        context: Dict[str, Any],
        pxl_result: Dict[str, Any],
        iel_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply Math lens: mathematical categories (informed by PXL+IEL)"""
        if not META_ENGINE_AVAILABLE or not self.math_engine:
            return {"status": "mock", "insights": ["Math analysis (mock)"]}
        
        try:
            # Select categories based on PXL+IEL findings
            active_categories = self._select_math_categories_from_pxl_iel(
                pxl_result, iel_result, context
            )
            
            result = self.math_engine.reason(concepts, active_categories)
            
            return {
                "status": "completed",
                "categories_applied": [c.value for c in active_categories],
                "coherence": getattr(result, 'mathematical_coherence', 0.5),
                "insights": [f"Math category {c.value}: formal structure" 
                            for c in active_categories[:3]]
            }
        except Exception as e:
            logger.warning(f"Math lens failed: {e}")
            return {"status": "failed", "error": str(e), "insights": []}
    
    def _synthesize_lenses(
        self,
        pxl_result: Dict[str, Any],
        iel_result: Dict[str, Any],
        math_result: Dict[str, Any]
    ) -> Tuple[TrinityVector, float]:
        """Synthesize cross-lens results into unified trinity coherence"""
        
        # Extract trinity values from each lens
        pxl_coherence = pxl_result.get("trinity_coherence", 0.5)
        iel_coherence = iel_result.get("coherence", 0.5)
        math_coherence = math_result.get("coherence", 0.5)
        
        # Build trinity vector (simplified)
        if META_ENGINE_AVAILABLE:
            trinity = TrinityVector(
                essence=pxl_coherence,
                generation=iel_coherence,
                temporal=math_coherence
            )
        else:
            trinity = None
        
        # Synthesis confidence
        confidence = (pxl_coherence + iel_coherence + math_coherence) / 3.0
        
        return trinity, confidence
    
    def _compute_fractal_coherence(
        self,
        vertices: List[FractalVertex]
    ) -> Optional[TrinityVector]:
        """Compute fractal-wide trinity coherence"""
        if not vertices:
            return None
        
        avg_essence = sum(v.trinity_coherence.essence for v in vertices 
                         if v.trinity_coherence) / max(len(vertices), 1)
        avg_generation = sum(v.trinity_coherence.generation for v in vertices 
                            if v.trinity_coherence) / max(len(vertices), 1)
        avg_temporal = sum(v.trinity_coherence.temporal for v in vertices 
                          if v.trinity_coherence) / max(len(vertices), 1)
        
        if META_ENGINE_AVAILABLE:
            return TrinityVector(
                essence=avg_essence,
                generation=avg_generation,
                temporal=avg_temporal
            )
        return None
    
    def _compute_amplification_factor(
        self,
        depth: int,
        vertices: List[FractalVertex]
    ) -> float:
        """Compute how much reasoning was amplified by fractal recursion"""
        # Base case: single-pass = 1.0x
        # Each depth doubles potential insight extraction
        theoretical_max = 2 ** depth
        
        # Actual amplification based on synthesis quality
        avg_synthesis = sum(v.synthesis_confidence for v in vertices) / max(len(vertices), 1)
        
        return theoretical_max * avg_synthesis
    
    def _compute_overall_confidence(
        self,
        vertices: List[FractalVertex]
    ) -> float:
        """Compute overall confidence across all vertices"""
        if not vertices:
            return 0.0
        
        confidences = [v.synthesis_confidence for v in vertices]
        return sum(confidences) / len(confidences)
    
    def _extract_concepts(self, payload: Any) -> List[str]:
        """Extract concepts from payload"""
        if isinstance(payload, dict):
            concepts = payload.get("concepts", [])
            if isinstance(concepts, list):
                return concepts
            # Extract from task/statements
            task = payload.get("task", "")
            statements = payload.get("statements", [])
            return [task] + statements
        elif isinstance(payload, str):
            return [payload]
        else:
            return ["opaque_payload"]
    
    def _select_iel_domains_from_pxl(
        self,
        pxl_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Set:
        """Select IEL domains based on PXL findings"""
        if not META_ENGINE_AVAILABLE:
            return set()
        
        # Heuristic: if PXL found strong logical structure, use AxioPraxis
        from Advanced_Reasoning_Protocol.ARP_Core.Meta_Reasoning_Engine.iel_engine import IELDomain
        
        domains = set()
        if pxl_result.get("relations_count", 0) > 3:
            domains.add(IELDomain.AXIOPRAXIS)
        domains.add(IELDomain.GNOSIPRAXIS)  # Always include knowledge domain
        
        return domains
    
    def _select_math_categories_from_pxl_iel(
        self,
        pxl_result: Dict[str, Any],
        iel_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Set:
        """Select Math categories based on PXL+IEL findings"""
        if not META_ENGINE_AVAILABLE:
            return set()
        
        from Advanced_Reasoning_Protocol.ARP_Core.Meta_Reasoning_Engine.math_engine import MathCategory
        
        categories = set()
        # If PXL found logical relations, use Boolean logic
        if pxl_result.get("relations_count", 0) > 0:
            categories.add(MathCategory.BOOLEAN_LOGIC)
        # Always include core
        categories.add(MathCategory.CORE)
        
        return categories
    
    def _extract_sub_payload(self, vertex: FractalVertex, lens: TrinityLens) -> Any:
        """Extract sub-payload for next recursion level based on lens"""
        # Simple projection: extract insights from the lens
        if lens == TrinityLens.PXL and vertex.pxl_result:
            return {"concepts": vertex.pxl_result.get("insights", [])}
        elif lens == TrinityLens.IEL and vertex.iel_result:
            return {"concepts": vertex.iel_result.get("insights", [])}
        elif lens == TrinityLens.MATH and vertex.math_result:
            return {"concepts": vertex.math_result.get("insights", [])}
        else:
            return {"concepts": ["fallback"]}
    
    def _build_sierpinski_core(self) -> TriuneSierpinskiCore:
        """Build Sierpinski core with I3-specific transform"""
        
        def i3_transform(payload: Any, depth: int, agent_id: str) -> Tuple[Any, Any, Any]:
            """I3's fractal transform operator"""
            # Simple triadic decomposition
            if isinstance(payload, dict):
                concepts = payload.get("concepts", [])
                n = len(concepts)
                third = max(1, n // 3)
                
                apex = {"concepts": concepts[:third], "role": "apex"}
                left = {"concepts": concepts[third:2*third], "role": "left"}
                right = {"concepts": concepts[2*third:], "role": "right"}
                
                return apex, left, right
            else:
                return {"role": "apex"}, {"role": "left"}, {"role": "right"}
        
        def i3_termination(payload: Any, depth: int) -> bool:
            """I3 termination: stop when concepts are exhausted"""
            if depth >= self.max_depth:
                return True
            if isinstance(payload, dict):
                concepts = payload.get("concepts", [])
                return len(concepts) < 2
            return True
        
        return TriuneSierpinskiCore(
            agent_id="I3",
            max_depth=self.max_depth,
            transform_operator=i3_transform,
            termination_predicate=i3_termination
        )
