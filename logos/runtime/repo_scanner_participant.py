import os
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol.SOP_Nexus.SOP_Nexus import NexusParticipant
from logos.imports.runtime import StatePacket
import time
from logos.imports.runtime import NexusParticipant

class RepoScannerParticipant(NexusParticipant):

    participant_id = "repo_scanner"

    def __init__(self, root="."):
        self.root = root
        self.nexus = None
        self.scanned = False

    def register(self, nexus_handle):
        self.nexus = nexus_handle

    def project_state(self):

        # only scan once
        if self.scanned:
            return None

        modules = []

        for root, dirs, files in os.walk(self.root):

            for f in files:
                if f.endswith(".py"):
                    modules.append(os.path.join(root, f))

        self.scanned = True

        return StatePacket(
            source_id=self.participant_id,
            payload={
                "type": "repo_scan",
                "content": "repository structure discovery",
                "module_count": len(modules),
                "modules": modules[:25]  # limit payload size
            },
            timestamp=time.time(),
            causal_intent="repo_structure_discovery"
        )

    def execute_tick(self, context):

        packet = self.project_state()

        if packet is not None and self.nexus is not None:
            self.nexus.emit(packet.payload, packet.causal_intent)
