# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
Causal Reasoning Engine - Cause-effect chain analysis
"""

from __future__ import annotations

from typing import Any, Dict, List, Set


class CausalEngine:
    """
    Causal reasoning engine for identifying cause-effect relationships.
    
    Builds causal graphs and analyzes intervention effects.
    """
    
    def analyze(self, events: List[str], relations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze causal relationships between events.
        
        Args:
            events: List of event names
            relations: List of {cause: str, effect: str, strength: float}
            
        Returns:
            {
                "engine": "causal",
                "causal_graph": Dict,
                "causal_chains": List,
                "root_causes": List[str],
                "final_effects": List[str],
                "intervention_points": List[str]
            }
        """
        if not events or not relations:
            return {
                "engine": "causal",
                "causal_graph": {},
                "causal_chains": [],
                "root_causes": [],
                "final_effects": [],
                "intervention_points": []
            }
        
        # Build adjacency list for causal graph
        causal_graph = {event: [] for event in events}
        for relation in relations:
            cause = relation.get("cause")
            effect = relation.get("effect")
            strength = relation.get("strength", 1.0)
            
            if cause in causal_graph:
                causal_graph[cause].append({
                    "effect": effect,
                    "strength": strength
                })
        
        # Identify root causes (no incoming edges)
        effects_set = set(rel.get("effect") for rel in relations)
        root_causes = [e for e in events if e not in effects_set]
        
        # Identify final effects (no outgoing edges)
        causes_set = set(rel.get("cause") for rel in relations)
        final_effects = [e for e in events if e not in causes_set]
        
        # Find causal chains (paths from roots to finals)
        causal_chains = []
        for root in root_causes:
            chains = self._find_chains(root, final_effects, causal_graph, set())
            causal_chains.extend(chains)
        
        # Identify key intervention points (high out-degree nodes)
        intervention_points = self._find_intervention_points(causal_graph)
        
        return {
            "engine": "causal",
            "causal_graph": {k: v for k, v in causal_graph.items() if v},
            "causal_chains": causal_chains[:10],  # Limit to top 10
            "root_causes": root_causes,
            "final_effects": final_effects,
            "intervention_points": intervention_points[:5]
        }
    
    def _find_chains(
        self,
        current: str,
        targets: List[str],
        graph: Dict[str, List[Dict]],
        visited: Set[str],
        path: List[str] = None
    ) -> List[List[str]]:
        """Find all chains from current to any target"""
        if path is None:
            path = []
        
        path = path + [current]
        
        if current in targets:
            return [path]
        
        if current in visited:
            return []
        
        visited.add(current)
        
        chains = []
        for neighbor in graph.get(current, []):
            effect = neighbor["effect"]
            if effect not in visited:
                new_chains = self._find_chains(effect, targets, graph, visited.copy(), path)
                chains.extend(new_chains)
        
        return chains
    
    def _find_intervention_points(self, graph: Dict[str, List[Dict]]) -> List[str]:
        """Find nodes with highest causal influence (out-degree * avg strength)"""
        influence_scores = {}
        
        for node, effects in graph.items():
            if effects:
                out_degree = len(effects)
                avg_strength = sum(e["strength"] for e in effects) / len(effects)
                influence_scores[node] = out_degree * avg_strength
        
        # Sort by influence score
        sorted_nodes = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)
        return [node for node, score in sorted_nodes]
