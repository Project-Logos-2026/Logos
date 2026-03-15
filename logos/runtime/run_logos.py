from logos.runtime.unified_nexus import get_nexus
from logos.runtime.repo_scanner_participant import RepoScannerParticipant
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Nexus.SCP_Nexus import MREHalt
import time


def main():

    protocol = "SCP"

    print(f"Initializing {protocol} Nexus...")
    nexus = get_nexus(protocol)

    print("Nexus initialized:", nexus)
    print("MRE methods:", dir(nexus.mre))

    scanner = RepoScannerParticipant(".")
    nexus.register_participant(scanner)

    if hasattr(nexus, "tick"):

        print("Starting tick loop...")

        for _ in range(20):
            try:
                nexus.tick()
            except MREHalt as e:
                print(f"MRE halted tick loop: {e}")
                break
            time.sleep(0.1)

        print("Tick loop finished.")

    else:

        print("No tick() method available.")
        print("Available methods:", dir(nexus))


if __name__ == "__main__":
    main()