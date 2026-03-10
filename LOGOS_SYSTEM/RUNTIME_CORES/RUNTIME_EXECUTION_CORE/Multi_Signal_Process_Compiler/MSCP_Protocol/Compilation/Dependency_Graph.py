from __future__ import annotations
from collections import deque
from typing import Any, Dict, List, Optional, Set
# from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Signals.Signal_Envelope import SignalEnvelope  # If this fails, try relative import below:
from ..Signals.Signal_Envelope import SignalEnvelope

class CyclicDependencyError(Exception):
    pass

class DependencyGraph:

    def __init__(self) -> None:
        self._adjacency: Dict[str, Set[str]] = {}
        self._nodes: Dict[str, SignalEnvelope] = {}

    def add_node(self, envelope: SignalEnvelope) -> None:
        sid = envelope.signal_id
        if sid not in self._adjacency:
            self._adjacency[sid] = set()
        self._nodes[sid] = envelope

    def add_edge(self, from_id: str, depends_on_id: str) -> None:
        if from_id not in self._adjacency:
            self._adjacency[from_id] = set()
        self._adjacency[from_id].add(depends_on_id)

    def build_from_signals(self, signals: List[SignalEnvelope]) -> None:
        self._adjacency.clear()
        self._nodes.clear()
        for sig in signals:
            self.add_node(sig)
        for sig in signals:
            deps = sig.payload.get('depends_on')
            if isinstance(deps, list):
                for dep_id in deps:
                    if isinstance(dep_id, str) and dep_id in self._nodes:
                        self.add_edge(sig.signal_id, dep_id)

    def topological_order(self) -> List[str]:
        in_degree: Dict[str, int] = {n: 0 for n in self._adjacency}
        for node, deps in self._adjacency.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[node] = in_degree.get(node, 0)
        reverse_adj: Dict[str, Set[str]] = {n: set() for n in self._adjacency}
        for node, deps in self._adjacency.items():
            for dep in deps:
                if dep in reverse_adj:
                    reverse_adj[dep].add(node)
        in_deg: Dict[str, int] = {n: 0 for n in self._adjacency}
        for node, deps in self._adjacency.items():
            for dep in deps:
                if dep in in_deg:
                    pass
            in_deg[node] = len([d for d in deps if d in self._adjacency])
        queue: deque[str] = deque()
        for node, deg in in_deg.items():
            if deg == 0:
                queue.append(node)
        order: List[str] = []
        while queue:
            current = queue.popleft()
            order.append(current)
            for dependent in reverse_adj.get(current, set()):
                in_deg[dependent] -= 1
                if in_deg[dependent] == 0:
                    queue.append(dependent)
        if len(order) != len(self._adjacency):
            processed = set(order)
            cycle_members = [n for n in self._adjacency if n not in processed]
            raise CyclicDependencyError(f'Cyclic dependency detected among: {cycle_members}')
        return order

    def get_envelope(self, signal_id: str) -> Optional[SignalEnvelope]:
        return self._nodes.get(signal_id)

    def node_count(self) -> int:
        return len(self._nodes)

    def edge_count(self) -> int:
        return sum((len(deps) for deps in self._adjacency.values()))