"""Stage 17-20 smoke test — packet propagation."""
import sys, time
sys.path.insert(0, "/workspaces/Logos")

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import RGEPacketBase
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Types import RGEPacketType
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Registry import RGEPacketRegistry
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import RGEFieldTopology
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Graph import RGEFieldGraph
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Graph_Builder import RGEGraphBuilder
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Location_Map import RGEPacketLocationMap
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Node_Packet_Accessor import RGENodePacketAccessor
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Propagator import RGEPacketPropagator
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Recursion_Field_Engine import RGERecursionFieldEngine

results = {}
results["import_test"] = "PASS"

# --- Location tracking test ---
try:
    loc = RGEPacketLocationMap()
    loc.set_location("p1", "node_A")
    assert loc.get_location("p1") == "node_A"
    assert loc.get_location("ghost") is None

    loc.set_location("p1", "node_B")
    assert loc.get_location("p1") == "node_B"

    loc.remove("p1")
    assert loc.get_location("p1") is None
    loc.remove("p1")  # idempotent remove

    results["location_tracking_test"] = "PASS"
except Exception as e:
    results["location_tracking_test"] = f"FAIL: {e}"

# --- Node accessor test ---
try:
    topo = RGEFieldTopology()
    topo.create_node("A")
    accessor = RGENodePacketAccessor(topo)

    accessor.add_packet("A", "pkt-1")
    accessor.add_packet("A", "pkt-2")
    assert set(accessor.get_packets("A")) == {"pkt-1", "pkt-2"}

    # idempotent add
    accessor.add_packet("A", "pkt-1")
    assert accessor.get_packets("A").count("pkt-1") == 1

    accessor.remove_packet("A", "pkt-1")
    assert "pkt-1" not in accessor.get_packets("A")

    # double remove is safe
    accessor.remove_packet("A", "pkt-1")

    # unknown node returns []
    assert accessor.get_packets("MISSING") == []

    # auto-create node on add_packet
    accessor.add_packet("NEW_NODE", "pkt-x")
    assert topo.get_node("NEW_NODE") is not None
    assert "pkt-x" in accessor.get_packets("NEW_NODE")

    results["node_accessor_test"] = "PASS"
except Exception as e:
    results["node_accessor_test"] = f"FAIL: {e}"

# --- Propagation movement test ---
try:
    topo2 = RGEFieldTopology()
    topo2.create_node("A")
    topo2.create_node("B")

    graph = RGEFieldGraph()
    builder = RGEGraphBuilder(topo2, graph)
    builder.connect_nodes("A", "B")

    loc2 = RGEPacketLocationMap()
    acc2 = RGENodePacketAccessor(topo2)
    propagator = RGEPacketPropagator(topo2, graph, acc2, loc2)

    # Place packet in A
    acc2.add_packet("A", "pkt-99")
    loc2.set_location("pkt-99", "A")

    propagator.propagate("pkt-99")

    assert loc2.get_location("pkt-99") == "B"
    assert "pkt-99" not in acc2.get_packets("A")
    assert "pkt-99" in acc2.get_packets("B")

    # no location raises ValueError
    raised = False
    try:
        propagator.propagate("ghost")
    except ValueError:
        raised = True
    assert raised

    # no neighbors raises ValueError
    topo3 = RGEFieldTopology()
    topo3.create_node("LONE")
    graph3 = RGEFieldGraph()
    acc3 = RGENodePacketAccessor(topo3)
    loc3 = RGEPacketLocationMap()
    prop3 = RGEPacketPropagator(topo3, graph3, acc3, loc3)
    acc3.add_packet("LONE", "pkt-lone")
    loc3.set_location("pkt-lone", "LONE")
    raised2 = False
    try:
        prop3.propagate("pkt-lone")
    except ValueError:
        raised2 = True
    assert raised2

    results["propagation_test"] = "PASS"
except Exception as e:
    results["propagation_test"] = f"FAIL: {e}"

# --- Engine propagation hook test ---
try:
    # No propagator — RuntimeError on call
    engine_no_prop = RGERecursionFieldEngine()
    assert engine_no_prop.propagator is None
    raised = False
    try:
        engine_no_prop.propagate_packet("any")
    except RuntimeError:
        raised = True
    assert raised

    # With propagator injected
    topo4 = RGEFieldTopology()
    topo4.create_node("A")
    topo4.create_node("B")
    graph4 = RGEFieldGraph()
    builder4 = RGEGraphBuilder(topo4, graph4)
    builder4.connect_nodes("A", "B")

    loc4 = RGEPacketLocationMap()
    acc4 = RGENodePacketAccessor(topo4)
    prop4 = RGEPacketPropagator(topo4, graph4, acc4, loc4)

    acc4.add_packet("A", "pkt-eng")
    loc4.set_location("pkt-eng", "A")

    engine = RGERecursionFieldEngine(propagator=prop4)
    assert engine.propagator is prop4

    engine.propagate_packet("pkt-eng")
    assert loc4.get_location("pkt-eng") == "B"
    assert "pkt-eng" in acc4.get_packets("B")

    results["engine_hook_test"] = "PASS"
except Exception as e:
    results["engine_hook_test"] = f"FAIL: {e}"

for k, v in results.items():
    print(f"{k}: {v}")

all_passed = all(v == "PASS" for v in results.values())
sys.exit(0 if all_passed else 1)
