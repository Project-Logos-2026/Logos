# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: taxonomy_aggregator
runtime_layer: protocol_execution
role: Taxonomical aggregation engine
responsibility: Aggregate 12 base engine outputs into 5 taxonomical streams
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: []
provides: [aggregate]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Failed taxonomies emit degraded outputs with explicit markers"
rewrite_provenance:
  source: NEW
  rewrite_phase: ARP_Overhaul_Phase_1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: ARP_TAXONOMY
  metrics: enabled
---------------------
"""

from __future__ import annotations

from typing import Any, Dict, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class TaxonomyOutput:
    """Single taxonomy output with aggregated signals"""
    name: str
    aggregated_score: float
    component_scores: Dict[str, float]
    conflicts: List[Dict[str, Any]]
    provenance: List[str]
    summary: str


class TaxonomyAggregator:
    """
    Aggregates 12 base engine outputs into 5 taxonomical outputs:
    1. LOGICAL_COHERENCE
    2. PROBABILISTIC_CONFIDENCE
    3. STRUCTURAL_INTEGRITY
    4. SEMANTIC_RICHNESS
    5. CONSTRAINT_SATISFACTION
    """
    
    # Mapping: Taxonomy → Source Engines
    TAXONOMY_SOURCES = {
        "LOGICAL_COHERENCE": ["deductive", "abductive", "inductive", "consistency"],
        "PROBABILISTIC_CONFIDENCE": ["bayesian", "causal"],
        "STRUCTURAL_INTEGRITY": ["topological", "graph", "relational"],
        "SEMANTIC_RICHNESS": ["analogical", "metaphorical"],
        "CONSTRAINT_SATISFACTION": ["consistency", "invariant"]
    }
    
    def aggregate(self, base_packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate base engine results into 5 taxonomies.
        
        Args:
            base_packet: BaseReasoningPacket from Stage 1
            
        Returns:
            TaxonomyPacket with 5 aggregated outputs
        """
        engine_results = base_packet.get("engine_results", {})
        
        taxonomies = {}
        
        for taxonomy_name, source_engines in self.TAXONOMY_SOURCES.items():
            try:
                taxonomy_output = self._aggregate_taxonomy(
                    taxonomy_name,
                    source_engines,
                    engine_results
                )
                taxonomies[taxonomy_name] = taxonomy_output.__dict__
            except Exception as e:
                logger.error(f"Failed to aggregate {taxonomy_name}: {e}")
                taxonomies[taxonomy_name] = self._degraded_taxonomy(taxonomy_name, str(e))
        
        return {
            "status": "success",
            "taxonomies": taxonomies
        }
    
    def _aggregate_taxonomy(
        self,
        taxonomy_name: str,
        source_engines: List[str],
        engine_results: Dict[str, Any]
    ) -> TaxonomyOutput:
        """Aggregate specific taxonomy from source engines"""
        
        component_scores = {}
        conflicts = []
        provenance = []
        
        for engine_name in source_engines:
            result = engine_results.get(engine_name, {})
            
            if result.get("status") == "failed":
                conflicts.append({
                    "engine": engine_name,
                    "reason": "engine_failure",
                    "error": result.get("error", "unknown")
                })
                continue
            
            # Extract score/confidence from engine result
            score = self._extract_score(result)
            component_scores[engine_name] = score
            provenance.append(engine_name)
        
        # Compute weighted aggregate
        if component_scores:
            aggregated_score = sum(component_scores.values()) / len(component_scores)
        else:
            aggregated_score = 0.0
            conflicts.append({
                "reason": "no_valid_engines",
                "taxonomy": taxonomy_name
            })
        
        summary = self._generate_summary(taxonomy_name, component_scores, conflicts)
        
        return TaxonomyOutput(
            name=taxonomy_name,
            aggregated_score=aggregated_score,
            component_scores=component_scores,
            conflicts=conflicts,
            provenance=provenance,
            summary=summary
        )
    
    def _extract_score(self, engine_result: Dict[str, Any]) -> float:
        """Extract numerical score from engine result"""
        # Try common score keys
        for key in ["confidence", "score", "strength", "plausibility", "validity"]:
            if key in engine_result:
                val = engine_result[key]
                if isinstance(val, (int, float)):
                    return float(val)
                elif isinstance(val, bool):
                    return 1.0 if val else 0.0
        
        # Default: heuristic based on result structure
        if engine_result.get("valid") or engine_result.get("coherent"):
            return 0.8
        elif engine_result.get("contradictions") or engine_result.get("violations"):
            return 0.3
        else:
            return 0.5  # Neutral
    
    def _generate_summary(
        self,
        taxonomy_name: str,
        component_scores: Dict[str, float],
        conflicts: List[Dict[str, Any]]
    ) -> str:
        """Generate human-readable summary"""
        if not component_scores:
            return f"{taxonomy_name}: No valid engine outputs"
        
        avg = sum(component_scores.values()) / len(component_scores)
        
        if conflicts:
            return f"{taxonomy_name}: Average {avg:.2f} with {len(conflicts)} conflicts"
        else:
            return f"{taxonomy_name}: Average {avg:.2f} (consensus)"
    
    def _degraded_taxonomy(self, taxonomy_name: str, error: str) -> Dict[str, Any]:
        """Emit degraded taxonomy output on aggregation failure"""
        return {
            "name": taxonomy_name,
            "aggregated_score": 0.0,
            "component_scores": {},
            "conflicts": [{"reason": "aggregation_failure", "error": error}],
            "provenance": [],
            "summary": f"{taxonomy_name}: FAILED - {error}"
        }
