"""Stage 25-28 smoke test — Runtime Bridge Integration."""
import sys
import time
sys.path.insert(0, "/workspaces/Logos")

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import RGECognitionSignal
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Channel import RGECognitionChannel
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Signal_Broadcaster import RGESignalBroadcaster
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Interface import RGERuntimeInterface
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Subscriber import RGERuntimeSubscriber
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Dispatcher import RGERuntimeDispatcher
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Registry import RGERuntimeRegistry
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import RGEFieldTopology
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Graph import RGEFieldGraph
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Graph_Builder import RGEGraphBuilder
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Location_Map import RGEPacketLocationMap
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Node_Packet_Accessor import RGENodePacketAccessor
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Propagator import RGEPacketPropagator
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Recursion_Field_Engine import RGERecursionFieldEngine

results = {}
results["import_test"] = "PASS"

# ---------------------------------------------------------------------------
# Concrete runtime interface for testing
# ---------------------------------------------------------------------------
class _TestRuntime(RGERuntimeInterface):
    def __init__(self):
        self.received = []

    def handle_signal(self, signal: RGECognitionSignal) -> None:
        self.received.append(signal)


# ---------------------------------------------------------------------------
# Test 1: runtime interface registration and subscriber delivery
# ---------------------------------------------------------------------------
try:
    dispatcher = RGERuntimeDispatcher()
    rt = _TestRuntime()
    dispatcher.register_runtime(rt)

    sig = RGECognitionSignal(packet_id="p1", source_node="A", destination_node="B", timestamp=1.0)
    dispatcher.dispatch(sig)

    assert len(rt.received) == 1
    assert rt.received[0] is sig

    results["subscriber_test"] = "PASS"
except Exception as e:
    results["subscriber_test"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Test 2: multiple runtimes receive the same signal
# ---------------------------------------------------------------------------
try:
    dispatcher2 = RGERuntimeDispatcher()
    rt2a = _TestRuntime()
    rt2b = _TestRuntime()
    dispatcher2.register_runtime(rt2a)
    dispatcher2.register_runtime(rt2b)

    sig2 = RGECognitionSignal(packet_id="p2", source_node="X", destination_node="Y", timestamp=2.0)
    dispatcher2.dispatch(sig2)

    assert len(rt2a.received) == 1
    assert len(rt2b.received) == 1
    assert rt2a.received[0] is sig2
    assert rt2b.received[0] is sig2

    results["dispatcher_test"] = "PASS"
except Exception as e:
    results["dispatcher_test"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Test 3: channel emit triggers dispatcher
# ---------------------------------------------------------------------------
try:
    dispatcher3 = RGERuntimeDispatcher()
    rt3 = _TestRuntime()
    dispatcher3.register_runtime(rt3)

    channel = RGECognitionChannel(runtime_dispatcher=dispatcher3)

    normal_received = []
    channel.register_subscriber(lambda s: normal_received.append(s))

    sig3 = RGECognitionSignal(packet_id="p3", source_node="M", destination_node="N", timestamp=3.0)
    channel.emit(sig3)

    # Normal subscriber received it
    assert len(normal_received) == 1
    assert normal_received[0] is sig3

    # Runtime dispatcher also received it
    assert len(rt3.received) == 1
    assert rt3.received[0] is sig3

    # Test set_runtime_dispatcher path
    channel2 = RGECognitionChannel()
    rt3b = _TestRuntime()
    dispatcher3b = RGERuntimeDispatcher()
    dispatcher3b.register_runtime(rt3b)
    channel2.set_runtime_dispatcher(dispatcher3b)
    channel2.emit(sig3)
    assert len(rt3b.received) == 1

    results["signal_dispatch_test"] = "PASS"
except Exception as e:
    results["signal_dispatch_test"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Test 4: registry provides centralized access
# ---------------------------------------------------------------------------
try:
    registry = RGERuntimeRegistry()
    rt4 = _TestRuntime()
    registry.register_runtime(rt4)

    disp = registry.get_dispatcher()
    sig4 = RGECognitionSignal(packet_id="p4", source_node="C", destination_node="D", timestamp=4.0)
    disp.dispatch(sig4)

    assert len(rt4.received) == 1
    assert rt4.received[0] is sig4

    results["registry_test"] = "PASS"
except Exception as e:
    results["registry_test"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Test 5: engine propagation triggers runtime dispatcher
# ---------------------------------------------------------------------------
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

    # Wire up broadcaster and runtime dispatcher
    channel = RGECognitionChannel()
    broadcaster = RGESignalBroadcaster(broadcast_channel=channel)

    rt5 = _TestRuntime()
    dispatcher5 = RGERuntimeDispatcher()
    dispatcher5.register_runtime(rt5)

    engine = RGERecursionFieldEngine(
        propagator=propagator,
        broadcaster=broadcaster,
        runtime_dispatcher=dispatcher5,
    )
    engine.propagate_packet("pkt-eng")

    assert loc.get_location("pkt-eng") == "B"
    assert len(rt5.received) == 1
    sig5 = rt5.received[0]
    assert sig5.packet_id == "pkt-eng"
    assert sig5.source_node == "A"
    assert sig5.destination_node == "B"
    assert sig5.timestamp > 0.0

    # Without runtime_dispatcher — no error, no dispatch
    topo2 = RGEFieldTopology()
    topo2.create_node("A")
    topo2.create_node("B")
    graph2 = RGEFieldGraph()
    builder2 = RGEGraphBuilder(topo2, graph2)
    builder2.connect_nodes("A", "B")
    loc2 = RGEPacketLocationMap()
    acc2 = RGENodePacketAccessor(topo2)
    prop2 = RGEPacketPropagator(topo2, graph2, acc2, loc2)
    acc2.add_packet("A", "pkt-nd")
    loc2.set_location("pkt-nd", "A")
    channel2 = RGECognitionChannel()
    broadcaster2 = RGESignalBroadcaster(broadcast_channel=channel2)
    engine2 = RGERecursionFieldEngine(propagator=prop2, broadcaster=broadcaster2)
    engine2.propagate_packet("pkt-nd")
    assert loc2.get_location("pkt-nd") == "B"

    results["engine_runtime_test"] = "PASS"
except Exception as e:
    results["engine_runtime_test"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
for k, v in results.items():
    print(f"{k}: {v}")

all_passed = all(v == "PASS" for v in results.values())
sys.exit(0 if all_passed else 1)
