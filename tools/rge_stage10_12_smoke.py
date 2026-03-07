"""Stage 10-12 smoke test — field topology."""
import sys, time
sys.path.insert(0, "/workspaces/Logos")

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import RGEPacketBase
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Types import RGEPacketType
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Registry import RGEPacketRegistry
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Node import RGEFieldNode
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import RGEFieldTopology
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Topology_Bridge import RGETopologyBridge

results = {}

# --- Node creation test ---
try:
    node = RGEFieldNode(node_id="n1")
    assert node.node_id == "n1"
    assert node.packets == []
    assert node.metadata == {}
    node.packets.append("pkt-x")
    assert "pkt-x" in node.packets
    results["node_creation_test"] = "PASS"
except Exception as e:
    results["node_creation_test"] = f"FAIL: {e}"

# --- Topology container test ---
try:
    topo = RGEFieldTopology()
    n = topo.create_node("node_a")
    assert topo.get_node("node_a") is n
    assert n in topo.all_nodes()
    assert topo.get_node("missing") is None
    results["topology_container_test"] = "PASS"
except Exception as e:
    results["topology_container_test"] = f"FAIL: {e}"

# --- Bridge assignment test ---
try:
    registry = RGEPacketRegistry()
    pkt = RGEPacketBase(
        packet_id="pkt-001",
        packet_type=RGEPacketType.TELEMETRY_SIGNAL,
        origin_system="test",
        creation_timestamp=time.time(),
        payload={"v": 1},
        tags=[],
        metadata={},
    )
    registry.register_packet(pkt)

    topo2 = RGEFieldTopology()
    bridge = RGETopologyBridge(registry, topo2)
    bridge.assign_packet_to_node("pkt-001", "node_1")

    node1 = topo2.get_node("node_1")
    assert node1 is not None
    assert "pkt-001" in node1.packets

    # idempotent
    bridge.assign_packet_to_node("pkt-001", "node_1")
    assert node1.packets.count("pkt-001") == 1

    # missing packet raises ValueError
    raised = False
    try:
        bridge.assign_packet_to_node("ghost", "node_1")
    except ValueError:
        raised = True
    assert raised

    results["bridge_assignment_test"] = "PASS"
except Exception as e:
    results["bridge_assignment_test"] = f"FAIL: {e}"

for k, v in results.items():
    print(f"{k}: {v}")

all_passed = all(v == "PASS" for v in results.values())
sys.exit(0 if all_passed else 1)
