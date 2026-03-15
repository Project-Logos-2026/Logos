# Unified Nexus Router

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Nexus.SCP_Nexus import StandardNexus as SCPNexus
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Advanced_Reasoning_Protocol.ARP_Nexus.ARP_Nexus import StandardNexus as ARPNexus
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol.SOP_Nexus.SOP_Nexus import StandardNexus as SOPNexus
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Cognitive_State_Protocol.CSP_Nexus.CSP_Nexus import StandardNexus as CSPNexus
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Epistemic_Monitoring_Protocol.EMP_Nexus.EMP_Nexus import StandardNexus as EMPNexus


NEXUS_REGISTRY = {
    "SCP": SCPNexus,
    "ARP": ARPNexus,
    "SOP": SOPNexus,
    "CSP": CSPNexus,
    "EMP": EMPNexus
}


def get_nexus(protocol: str):
    protocol = protocol.upper()

    if protocol not in NEXUS_REGISTRY:
        raise ValueError(f"Unknown nexus protocol: {protocol}")

    return NEXUS_REGISTRY[protocol]()
