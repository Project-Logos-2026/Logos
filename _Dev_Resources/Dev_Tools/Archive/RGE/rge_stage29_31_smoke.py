"""Stage 29-31 smoke test — RGE Bootstrap and Runtime Activation."""
import sys
import time
sys.path.insert(0, "/workspaces/Logos")

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import RGECognitionSignal
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Interface import RGERuntimeInterface
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Bootstrap.RGE_Bridge_Nexus import RGEBridgeNexus
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Bootstrap.RGE_Runtime_Bootstrap import RGERuntimeBootstrap
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Bootstrap.RGE_Activation_Manager import RGEActivationManager
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import RGEFieldTopology
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Graph import RGEFieldGraph
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Graph_Builder import RGEGraphBuilder
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Location_Map import RGEPacketLocationMap
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Node_Packet_Accessor import RGENodePacketAccessor
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Propagator import RGEPacketPropagator
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Recursion_Field_Engine import RGERecursionFieldEngine
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Signal_Broadcaster import RGESignalBroadcaster

results = {}
results["import_test"] = "PASS"

# ---------------------------------------------------------------------------
# Concrete runtime for testing
# ---------------------------------------------------------------------------
class _TestRuntime(RGERuntimeInterface):
    def __init__(self):
        self.received = []
    def handle_signal(self, signal: RGECognitionSignal) -> None:
        self.received.append(signal)

# ---------------------------------------------------------------------------
# Test 1: bridge nexus creates and binds channel and dispatcher
# ---------------------------------------------------------------------------
try:
    nexus = RGEBridgeNexus()
    channel = nexus.get_channel()
    dispatcher = nexus.get_dispatcher()

    assert channel is not None
    assert dispatcher is not None

    # Confirm dispatcher is attached: emit via channel triggers dispatch
    rt = _TestRuntime()
    dispatcher.register_runtime(rt)

    sig = RGECognitionSignal(packet_id="p1", source_node="A", destination_node="B", timestamp=1.0)
    channel.emit(sig)

    assert len(rt.received) == 1
    assert rt.received[0] is sig

    results["activation_test"] = "PASS"
except Exception as e:
    results["activation_test"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Test 2: bootstrap initializes nexus and registry shares same dispatcher
# ---------------------------------------------------------------------------
try:
    bootstrap = RGERuntimeBootstrap()
    nexus2 = bootstrap.initialize_runtime()

    assert nexus2 is not None
    assert nexus2.get_channel() is not None
    assert nexus2.get_dispatcher() is not None

    # Registry's dispatcher must be the same object as nexus dispatcher
    registry_dispatcher = bootstrap.registry.get_dispatcher()
    assert registry_dispatcher is nexus2.get_dispatcher()

    # Register via registry; signal via channel should reach the runtime
    rt2 = _TestRuntime()
    bootstrap.registry.register_runtime(rt2)

    sig2 = RGECognitionSignal(packet_id="p2", source_node="X", destination_node="Y", timestamp=2.0)
    nexus2.get_channel().emit(sig2)

    assert len(rt2.received) == 1
    assert rt2.received[0] is sig2

    results["registry_validation"] = "PASS"
except Exception as e:
    results["registry_validation"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Test 3: activation manager entry point
# ---------------------------------------------------------------------------
try:
    manager = RGEActivationManager()
    assert manager.get_nexus() is None  # not yet activated

    nexus3 = manager.activate()
    assert nexus3 is not None
    assert manager.get_nexus() is nexus3

    # Channel and dispatcher accessible after activation
    assert nexus3.get_channel() is not None
    assert nexus3.get_dispatcher() is not None

    # Runtime subscriber receives signal through activated channel
    rt3 = _TestRuntime()
    nexus3.get_dispatcher().register_runtime(rt3)

    sig3 = RGECognitionSignal(packet_id="p3", source_node="M", destination_node="N", timestamp=3.0)
    nexus3.get_channel().emit(sig3)

    assert len(rt3.received) == 1
    assert rt3.received[0] is sig3

    results["subscriber_activation_test"] = "PASS"
except Exception as e:
    results["subscriber_activation_test"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Test 4: full signal propagation through engine after activation
# ---------------------------------------------------------------------------
try:
    manager4 = RGEActivationManager()
    nexus4 = manager4.activate()

    # Build field
    topo = RGEFieldTopology()
    topo.create_node("A")
    topo.create_node("B")
    graph = RGEFieldGraph()
    builder = RGEGraphBuilder(topo, graph)
    builder.connect_nodes("A", "B")
    loc = RGEPacketLocationMap()
    acc = RGENodePacketAccessor(topo)
    propagator = RGEPacketPropagator(topo, graph, acc, loc)

    acc.add_packet("A", "pkt-boot")
    loc.set_location("pkt-boot", "A")

    # Wire broadcaster to nexus channel
    broadcaster = RGESignalBroadcaster(broadcast_channel=nexus4.get_channel())

    rt4 = _TestRuntime()
    nexus4.get_dispatcher().register_runtime(rt4)

    engine = RGERecursionFieldEngine(
        propagator=propagator,
        broadcaster=broadcaster,
        runtime_dispatcher=nexus4.get_dispatcher(),
    )
    engine.propagate_packet("pkt-boot")

    assert loc.get_location("pkt-boot") == "B"
    # Signal received by runtime subscriber (engine dispatches directly to
    # dispatcher, which delivers to rt4)
    assert len(rt4.received) >= 1
    sig4 = rt4.received[0]
    assert sig4.packet_id == "pkt-boot"
    assert sig4.source_node == "A"
    assert sig4.destination_node == "B"
    assert sig4.timestamp > 0.0

    results["signal_propagation_test"] = "PASS"
except Exception as e:
    results["signal_propagation_test"] = f"FAIL: {e}"

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
for k, v in results.items():
    print(f"{k}: {v}")

all_passed = all(v == "PASS" for v in results.values())
sys.exit(0 if all_passed else 1)
