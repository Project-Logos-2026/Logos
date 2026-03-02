
from typing import Optional, List
from .SMP_Schema import SMP, AppendArtifact
from .SMP_Store import SMPStore

class UWMReadAPI:
    def __init__(self, store: SMPStore, allowed_roles=None):
        self._store = store
        if allowed_roles is None:
            self._allowed_roles = {"logos_agent"}
        else:
            self._allowed_roles = set(allowed_roles)

    def get_smp(self, smp_id: str, requester_role: str) -> Optional[SMP]:
        if requester_role not in self._allowed_roles:
            return None
        return self._store.get_smp(smp_id)

    def get_aas_for_smp(self, smp_id: str, requester_role: str) -> List[AppendArtifact]:
        if requester_role not in self._allowed_roles:
            return []
        smp = self._store.get_smp(smp_id)
        if not smp:
            return []
        return [self._store._aas[aa_hash] for aa_hash in smp.append_artifacts.aa_hashes if aa_hash in self._store._aas]

    def get_smps_by_classification(self, classification_state: str, requester_role: str) -> List[SMP]:
        if requester_role not in self._allowed_roles:
            return []
        return self._store.get_smps_by_classification(classification_state)

    def get_smp_count(self, requester_role: str) -> int:
        if requester_role not in self._allowed_roles:
            return 0
        return self._store.get_smp_count()

    def get_aa_count(self, requester_role: str) -> int:
        if requester_role not in self._allowed_roles:
            return 0
        return self._store.get_aa_count()
