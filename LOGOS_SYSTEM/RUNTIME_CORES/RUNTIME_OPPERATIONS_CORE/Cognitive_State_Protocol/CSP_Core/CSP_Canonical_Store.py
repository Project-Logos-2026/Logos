
from typing import Dict, List, Optional
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.\
Cognitive_State_Protocol.CSP_Core.Unified_Working_Memory.SMP_Schema import SMP


class CSPCanonicalStore:

    def __init__(self):
        self._store: Dict[str, SMP] = {}

    def store(self, csmp: SMP):
        if csmp.header.classification_state != "canonical":
            raise ValueError("Only canonical SMPs allowed.")
        if csmp.header.smp_id in self._store:
            raise ValueError("Duplicate canonical SMP id.")
        self._store[csmp.header.smp_id] = csmp

    def get(self, csmp_id: str) -> Optional[SMP]:
        return self._store.get(csmp_id)

    def list_all(self) -> List[SMP]:
        return list(self._store.values())

    def count(self) -> int:
        return len(self._store)

    def get_governance_adapter(self):
        """
        Returns a read-only CanonicalGovernanceAdapter.
        This is the only sanctioned external exposure boundary.
        """
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.\
Cognitive_State_Protocol.CSP_Core.Canonical_Governance_Adapter \
import CanonicalGovernanceAdapter

        return CanonicalGovernanceAdapter(self)
