"""Stage 13-16 smoke test — topology graph."""
import sys
sys.path.insert(0, "/workspaces/Logos")

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Edge import RGEFieldEdge
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Node import RGEFieldNode
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Graph import RGEFieldGraph
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import RGEFieldTopology
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Graph_Builder import RGEGraphBuilder
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Graph_Traversal import RGEGraphTraversal

results = {}

# --- Import test ---
results["import_test"] = "PASS"

# --- Edge creation test ---
try:
    edge = RGEFieldEdge(source_node="A", target_node="B")
    assert edge.source_node == "A"
    assert edge.target_node == "B"
    assert edge.weight == 1.0
    assert edge.metadata == {}

    edge_w = RGEFieldEdge(source_node="X", target_node="Y", weight=0.5, metadata={"k": "v"})
    assert edge_w.weight == 0.5
    assert edge_w.metadata["k"] == "v"

    # frozen — mutation must raise
    tried = False
    try:
        edge.weight = 9.9  # type: ignore[misc]
    except Exception:
        tried = True
    assert tried

    results["edge_creation_test"] = "PASS"
except Exception as e:
    results["edge_creation_test"] = f"FAIL: {e}"

# --- Graph storage test ---
try:
    graph = RGEFieldGraph()
    node_a = RGEFieldNode(node_id="A")
    node_b = RGEFieldNode(node_id="B")
    graph.add_node(node_a)
    graph.add_node(node_b)
    assert "A" in graph.nodes
    assert "B" in graph.nodes

    e1 = RGEFieldEdge(source_node="A", target_node="B")
    e2 = RGEFieldEdge(source_node="A", target_node="B", weight=2.0)
    graph.add_edge(e1)
    graph.add_edge(e2)
    assert len(graph.edges) == 2

    from_a = graph.get_edges_from("A")
    assert len(from_a) == 2
    assert graph.get_edges_from("B") == []

    results["graph_storage_test"] = "PASS"
except Exception as e:
    results["graph_storage_test"] = f"FAIL: {e}"

# --- Builder connection test ---
try:
    topology = RGEFieldTopology()
    topology.create_node("A")
    topology.create_node("B")

    graph2 = RGEFieldGraph()
    builder = RGEGraphBuilder(topology, graph2)
    builder.connect_nodes("A", "B")
    builder.connect_nodes("A", "B", weight=0.75)

    assert len(graph2.edges) == 2
    assert graph2.edges[0].weight == 1.0
    assert graph2.edges[1].weight == 0.75

    # missing node raises ValueError
    raised = False
    try:
        builder.connect_nodes("A", "GHOST")
    except ValueError:
        raised = True
    assert raised

    raised2 = False
    try:
        builder.connect_nodes("GHOST", "A")
    except ValueError:
        raised2 = True
    assert raised2

    results["builder_connection_test"] = "PASS"
except Exception as e:
    results["builder_connection_test"] = f"FAIL: {e}"

# --- Traversal neighbors test ---
try:
    topology3 = RGEFieldTopology()
    topology3.create_node("A")
    topology3.create_node("B")
    topology3.create_node("C")

    graph3 = RGEFieldGraph()
    builder3 = RGEGraphBuilder(topology3, graph3)
    builder3.connect_nodes("A", "B")
    builder3.connect_nodes("A", "C")

    traversal = RGEGraphTraversal(graph3)
    nbrs = traversal.neighbors("A")
    assert set(nbrs) == {"B", "C"}
    assert traversal.neighbors("B") == []
    assert traversal.neighbors("MISSING") == []

    results["traversal_neighbors_test"] = "PASS"
except Exception as e:
    results["traversal_neighbors_test"] = f"FAIL: {e}"

for k, v in results.items():
    print(f"{k}: {v}")

all_passed = all(v == "PASS" for v in results.values())
sys.exit(0 if all_passed else 1)
