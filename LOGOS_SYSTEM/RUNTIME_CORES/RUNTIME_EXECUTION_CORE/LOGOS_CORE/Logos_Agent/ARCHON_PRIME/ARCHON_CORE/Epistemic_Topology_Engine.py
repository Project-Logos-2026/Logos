"""
Epistemic_Topology_Engine
Creates the global epistemic graph.

Integrates outputs from all analysis engines into a system-level
epistemic graph of nodes and support edges.
"""


class EpistemicTopologyEngine:

    def build_graph(self, artifacts):
        nodes = []
        edges = []

        for artifact in artifacts:
            node_id = artifact.get("principle_id") or artifact.get("logic_family")
            nodes.append(node_id)

            if "source_count" in artifact:
                edges.append((node_id, "supports"))

        return {
            "nodes": nodes,
            "edges": edges,
        }
