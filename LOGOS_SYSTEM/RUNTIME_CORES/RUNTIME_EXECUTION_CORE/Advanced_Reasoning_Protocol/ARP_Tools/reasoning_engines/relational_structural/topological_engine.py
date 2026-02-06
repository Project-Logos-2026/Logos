from __future__ import annotations

from typing import Any, Dict, List


class TopologicalEngine:
    def analyze(self, nodes: List[str], edges: List[Dict[str, str]]) -> Dict[str, Any]:
        adj = {n: set() for n in nodes}
        for edge in edges:
            src = edge.get("source")
            tgt = edge.get("target")
            if src in adj and tgt in adj:
                adj[src].add(tgt)
        connectivity = all(adj.values()) if adj else False
        return {"engine": "topological", "connected": connectivity, "node_count": len(nodes)}
