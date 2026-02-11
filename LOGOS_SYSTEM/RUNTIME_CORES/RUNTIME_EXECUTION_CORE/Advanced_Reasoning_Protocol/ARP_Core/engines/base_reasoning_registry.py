# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: base_reasoning_registry
runtime_layer: protocol_execution
role: Base reasoning engine orchestrator
responsibility: Orchestrate 12 foundational reasoning engines and collect structured outputs
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [all_reasoning_engines]
provides: [reason]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Failed engines emit error markers, do not halt entire pipeline"
rewrite_provenance:
  source: NEW
  rewrite_phase: ARP_Overhaul_Phase_1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: ARP_BASE_REASONING
  metrics: enabled
---------------------
"""

from __future__ import annotations

from typing import Any, Dict, List, Set
from enum import Enum
import logging

# Import all 12 engines
from ...ARP_Tools.reasoning_engines.logical.deductive_engine import DeductiveEngine
from ...ARP_Tools.reasoning_engines.logical.abductive_engine import AbductiveEngine
from ...ARP_Tools.reasoning_engines.logical.inductive_engine import InductiveEngine
from ...ARP_Tools.reasoning_engines.probabilistic.bayesian_engine import BayesianEngine
from ...ARP_Tools.reasoning_engines.probabilistic.causal_engine import CausalEngine
from ...ARP_Tools.reasoning_engines.relational_structural.topological_engine import TopologicalEngine
from ...ARP_Tools.reasoning_engines.relational_structural.graph_engine import GraphEngine
from ...ARP_Tools.reasoning_engines.relational_structural.relational_engine import RelationalEngine
from ...ARP_Tools.reasoning_engines.semantic.analogical_engine import AnagogicalEngine
from ...ARP_Tools.reasoning_engines.semantic.metaphorical_engine import MetaphoricalEngine
from ...ARP_Tools.reasoning_engines.constraint.consistency_engine import ConsistencyEngine
from ...ARP_Tools.reasoning_engines.constraint.invariant_engine import InvariantEngine

logger = logging.getLogger(__name__)


class EngineType(Enum):
    DEDUCTIVE = "deductive"
    ABDUCTIVE = "abductive"
    INDUCTIVE = "inductive"
    BAYESIAN = "bayesian"
    CAUSAL = "causal"
    TOPOLOGICAL = "topological"
    GRAPH = "graph"
    RELATIONAL = "relational"
    ANALOGICAL = "analogical"
    METAPHORICAL = "metaphorical"
    CONSISTENCY = "consistency"
    INVARIANT = "invariant"


class ComputeMode(Enum):
    LIGHTWEIGHT = "lightweight"
    BALANCED = "balanced"
    HIGH_RIGOR = "high_rigor"


# Engine selection per compute mode
ENGINE_SELECTION = {
    ComputeMode.LIGHTWEIGHT: {
        EngineType.DEDUCTIVE,
        EngineType.BAYESIAN,
        EngineType.TOPOLOGICAL,
        EngineType.CONSISTENCY
    },
    ComputeMode.BALANCED: {
        EngineType.DEDUCTIVE,
        EngineType.ABDUCTIVE,
        EngineType.INDUCTIVE,
        EngineType.BAYESIAN,
        EngineType.CAUSAL,
        EngineType.TOPOLOGICAL,
        EngineType.GRAPH,
        EngineType.RELATIONAL,
        EngineType.ANALOGICAL,
        EngineType.CONSISTENCY,
        EngineType.INVARIANT,
        EngineType.METAPHORICAL
    },
    ComputeMode.HIGH_RIGOR: set(EngineType)  # All 12
}


class BaseReasoningRegistry:
    """
    Registry and orchestrator for 12 base reasoning engines.
    
    Responsibilities:
    - Instantiate engines based on compute mode
    - Route AACED packet to appropriate engines
    - Collect and structure engine outputs
    - Track provenance
    """
    
    def __init__(self, mode: ComputeMode = ComputeMode.BALANCED):
        self.mode = mode
        self.active_engines = ENGINE_SELECTION[mode]
        
        # Instantiate engines
        self.engines = {
            EngineType.DEDUCTIVE: DeductiveEngine(),
            EngineType.ABDUCTIVE: AbductiveEngine(),
            EngineType.INDUCTIVE: InductiveEngine(),
            EngineType.BAYESIAN: BayesianEngine(),
            EngineType.CAUSAL: CausalEngine(),
            EngineType.TOPOLOGICAL: TopologicalEngine(),
            EngineType.GRAPH: GraphEngine(),
            EngineType.RELATIONAL: RelationalEngine(),
            EngineType.ANALOGICAL: AnagogicalEngine(),
            EngineType.METAPHORICAL: MetaphoricalEngine(),
            EngineType.CONSISTENCY: ConsistencyEngine(),
            EngineType.INVARIANT: InvariantEngine()
        }
        
        logger.info(f"BaseReasoningRegistry initialized (mode={mode.value}, active={len(self.active_engines)})")
    
    def reason(
        self,
        aaced_packet: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute base reasoning across active engines.
        
        Returns:
            BaseReasoningPacket with engine_results + provenance
        """
        engine_results = {}
        provenance = []
        
        for engine_type in self.active_engines:
            try:
                engine = self.engines[engine_type]
                result = self._invoke_engine(engine, engine_type, aaced_packet, context)
                engine_results[engine_type.value] = result
                
                provenance.append({
                    "engine": engine_type.value,
                    "status": "success",
                    "output_keys": list(result.keys())
                })
                
            except Exception as e:
                logger.warning(f"Engine {engine_type.value} failed: {e}")
                engine_results[engine_type.value] = {
                    "status": "failed",
                    "error": str(e)
                }
                provenance.append({
                    "engine": engine_type.value,
                    "status": "failed",
                    "error": str(e)
                })
        
        return {
            "status": "success",
            "engine_results": engine_results,
            "provenance": provenance
        }
    
    def _invoke_engine(
        self,
        engine: Any,
        engine_type: EngineType,
        aaced_packet: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route AACED packet to appropriate engine method"""
        
        # Extract relevant data based on engine type
        if engine_type in {EngineType.DEDUCTIVE, EngineType.ABDUCTIVE, EngineType.INDUCTIVE}:
            # Logical engines: extract statements/premises
            premises = self._extract_premises(aaced_packet, context)
            if engine_type == EngineType.DEDUCTIVE:
                conclusion = aaced_packet.get("task", "")
                return engine.analyze(premises, conclusion)
            elif engine_type == EngineType.ABDUCTIVE:
                observations = self._extract_observations(aaced_packet)
                rules = context.get("rules", [])
                return engine.analyze(observations, rules)
            else:  # Inductive
                examples = self._extract_examples(aaced_packet, context)
                return engine.analyze(examples)
        
        elif engine_type in {EngineType.BAYESIAN, EngineType.CAUSAL}:
            # Probabilistic engines
            evidence = self._extract_evidence(aaced_packet, context)
            if engine_type == EngineType.BAYESIAN:
                priors = context.get("priors", {})
                return engine.analyze(priors, evidence)
            else:  # Causal
                events = self._extract_events(aaced_packet)
                relations = self._extract_relations(aaced_packet, context)
                return engine.analyze(events, relations)
        
        elif engine_type in {EngineType.TOPOLOGICAL, EngineType.GRAPH, EngineType.RELATIONAL}:
            # Structural engines
            nodes, edges = self._extract_graph_structure(aaced_packet, context)
            if engine_type == EngineType.TOPOLOGICAL:
                return engine.analyze(nodes, edges)
            elif engine_type == EngineType.GRAPH:
                return engine.analyze(nodes, edges)
            else:  # Relational
                triples = self._extract_triples(aaced_packet, context)
                return engine.analyze(triples)
        
        elif engine_type in {EngineType.ANALOGICAL, EngineType.METAPHORICAL}:
            # Semantic engines
            concepts = self._extract_concepts(aaced_packet)
            if engine_type == EngineType.ANALOGICAL:
                source_domain = aaced_packet.get("source_domain", "")
                target_domain = aaced_packet.get("task", "")
                return engine.analyze(source_domain, target_domain, concepts)
            else:  # Metaphorical
                return engine.analyze(concepts)
        
        elif engine_type in {EngineType.CONSISTENCY, EngineType.INVARIANT}:
            # Constraint engines
            if engine_type == EngineType.CONSISTENCY:
                statements = self._extract_statements(aaced_packet, context)
                return engine.analyze(statements)
            else:  # Invariant
                axioms = context.get("axioms", [])
                state = aaced_packet.get("state", {})
                return engine.analyze(axioms, state)
        
        else:
            return {"status": "unknown_engine_type"}
    
    # Helper methods for data extraction
    def _extract_premises(self, aaced: Dict, ctx: Dict) -> List[str]:
        return ctx.get("premises", []) + aaced.get("statements", [])
    
    def _extract_observations(self, aaced: Dict) -> List[str]:
        return aaced.get("observations", [])
    
    def _extract_examples(self, aaced: Dict, ctx: Dict) -> List[Any]:
        return aaced.get("examples", [])
    
    def _extract_evidence(self, aaced: Dict, ctx: Dict) -> Dict[str, Any]:
        return aaced.get("evidence", {})
    
    def _extract_events(self, aaced: Dict) -> List[str]:
        return aaced.get("events", [])
    
    def _extract_relations(self, aaced: Dict, ctx: Dict) -> List[Dict[str, Any]]:
        return aaced.get("relations", [])
    
    def _extract_graph_structure(self, aaced: Dict, ctx: Dict):
        nodes = aaced.get("nodes", [])
        edges = aaced.get("edges", [])
        return nodes, edges
    
    def _extract_triples(self, aaced: Dict, ctx: Dict) -> List[tuple]:
        return aaced.get("triples", [])
    
    def _extract_concepts(self, aaced: Dict) -> List[str]:
        return aaced.get("concepts", [])
    
    def _extract_statements(self, aaced: Dict, ctx: Dict) -> List[str]:
        return aaced.get("statements", [])
