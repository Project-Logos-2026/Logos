# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
Graph Reasoning Engine - Path and centrality analysis
"""

from __future__ import annotations
from typing import Any, Dict, List, Set


class GraphEngine:
    """Graph analysis for connectivity, paths, and centrality."""
    
    def analyze(self, nodes: List[str], edges: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze graph structure.
        
        Returns:
            {
                "engine": "graph",
                "node_count": int,
                "edge_count": int,
                "connected_components": int,
                "shortest_paths_sample": List,
                "centrality_scores": Dict[str, float]
            }
        """
        if not nodes:
            return {"engine": "graph", "node_count": 0, "edge_count": 0}
        
        # Build adjacency list
        adj = {n: set() for n in nodes}
        for edge in edges:
            src, tgt = edge.get("source"), edge.get("target")
            if src in adj and tgt in adj:
                adj[src].add(tgt)
                adj[tgt].add(src)  # Undirected
        
        # Count connected components
        visited = set()
        components = 0
        for node in nodes:
            if node not in visited:
                self._dfs(node, adj, visited)
                components += 1
        
        # Compute centrality (degree centrality)
        centrality = {n: len(neighbors) for n, neighbors in adj.items()}
        
        return {
            "engine": "graph",
            "node_count": len(nodes),
            "edge_count": len(edges),
            "connected_components": components,
            "centrality_scores": dict(sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5])
        }
    
    def _dfs(self, node: str, adj: Dict, visited: Set):
        """Depth-first search for component detection"""
        visited.add(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                self._dfs(neighbor, adj, visited)
