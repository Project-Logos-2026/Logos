"""Stage 21-24 smoke test — cognition signal broadcasting."""
import sys, time
sys.path.insert(0, "/workspaces/Logos")

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import RGECognitionSignal
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Channel import RGECognitionChannel
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Signal_Broadcaster import RGESignalBroadcaster
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import RGEFieldTopology
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Graph import RGEFieldGraph
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Graph_Builder import RGEGraphBuilder
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Location_Map import RGEPacketLocationMap
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Node_Packet_Accessor import RGENodePacketAccessor
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Propagator import RGEPacketPropagator
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Recursion_Field_Engine import RGERecursionFieldEngine

results = {}
results["import_test"] = "PASS"

# --- Signal object creation test ---
try:
    ts = time.time()
    sig = RGECognitionSignal(
        packet_id="pkt-1",
        source_node="A",
        destination_node="B",
        timestamp=ts,
    )
    assert sig.packet_id == "pkt-1"
    assert sig.source_node == "A"
    assert sig.destination_node == "B"
    assert sig.timestamp == ts

    # frozen — mutation must raise
    raised = False
    try:
        sig.packet_id = "other"  # type: ignore[misc]
    except Exception:
        raised = True
    assert raised

    results["signal_emission_test"] = "PASS"
except Exception as e:
    results["signal_emission_test"] = f"FAIL: {e}"

# --- Subscriber registration and broadcaster emission test ---
try:
    received: list = []

    channel = RGECognitionChannel()
    channel.register_subscriber(lambda s: received.append(s))

    broadcaster = RGESignalBroadcaster(broadcast_channel=channel)

    sig1 = RGECognitionSignal(packet_id="p1", source_node="X", destination_node="Y", timestamp=0.0)
    sig2 = RGECognitionSignal(packet_id="p2", source_node="Y", destination_node="Z", timestamp=1.0)

    broadcaster.broadcast(sig1)
    broadcaster.broadcast(sig2)

    assert len(received) == 2
    assert received[0] is sig1
    assert received[1] is sig2

    # Multiple subscribers
    received2: list = []
    channel.register_subscriber(lambda s: received2.append(s))
    broadcaster.broadcast(sig1)
    assert len(received) == 3   # first subscriber got it again
    assert len(received2) == 1  # second subscriber got it once

    results["broadcaster_test"] = "PASS"
except Exception as e:
    results["broadcaster_test"] = f"FAIL: {e}"

# --- Engine propagation hook emits signal ---
try:
    topo = RGEFieldTopology()
    topo.create_node("A")
    topo.create_node("B")

    graph = RGEFieldGraph()
    builder = RGEGraphBuilder(topo, graph)
    builder.connect_nodes("A", "B")

    loc = RGEPacketLocationMap()
    acc = RGENodePacketAccessor(topo)
    propagator = RGEPacketPropagator(topo, graph, acc, loc)

    acc.add_packet("A", "pkt-eng")
    loc.set_location("pkt-eng", "A")

    captured: list = []
    channel2 = RGECognitionChannel()
    channel2.register_subscriber(lambda s: captured.append(s))
    broadcaster2 = RGESignalBroadcaster(broadcast_channel=channel2)

    engine = RGERecursionFieldEngine(propagator=propagator, broadcaster=broadcaster2)
    engine.propagate_packet("pkt-eng")

    # Packet moved
    assert loc.get_location("pkt-eng") == "B"

    # Signal emitted
    assert len(captured) == 1
    sig = captured[0]
    assert sig.packet_id == "pkt-eng"
    assert sig.source_node == "A"
    assert sig.destination_node == "B"
    assert sig.timestamp > 0.0

    # Without broadcaster — no signal, no error
    topo2 = RGEFieldTopology()
    topo2.create_node("A")
    topo2.create_node("B")
    graph2 = RGEFieldGraph()
    builder2 = RGEGraphBuilder(topo2, graph2)
    builder2.connect_nodes("A", "B")
    loc2 = RGEPacketLocationMap()
    acc2 = RGENodePacketAccessor(topo2)
    prop2 = RGEPacketPropagator(topo2, graph2, acc2, loc2)
    acc2.add_packet("A", "pkt-nb")
    loc2.set_location("pkt-nb", "A")

    engine_nb = RGERecursionFieldEngine(propagator=prop2)
    engine_nb.propagate_packet("pkt-nb")
    assert loc2.get_location("pkt-nb") == "B"

    results["engine_signal_test"] = "PASS"
except Exception as e:
    results["engine_signal_test"] = f"FAIL: {e}"

for k, v in results.items():
    print(f"{k}: {v}")

all_passed = all(v == "PASS" for v in results.values())
sys.exit(0 if all_passed else 1)
