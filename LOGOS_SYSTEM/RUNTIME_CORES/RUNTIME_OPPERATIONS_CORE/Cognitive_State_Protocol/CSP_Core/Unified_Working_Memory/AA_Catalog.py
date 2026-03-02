from typing import Dict, List
from .SMP_Schema import AppendArtifact
import collections

class AACatalog:
    def __init__(self):
        self._catalog: Dict[str, AppendArtifact] = {}
        self._index: Dict[str, List[str]] = collections.defaultdict(list)

    def add_aa(self, aa: AppendArtifact):
        self._catalog[aa.aa_id] = aa
        self._index[aa.bound_smp_id].append(aa.aa_id)

    def get_aa(self, aa_id: str) -> AppendArtifact:
        return self._catalog.get(aa_id)

    def get_aa_by_smp(self, smp_id: str) -> List[AppendArtifact]:
        return [self._catalog[aa_id] for aa_id in self._index.get(smp_id, [])]

    def get_ordered_by_timestamp(self) -> List[AppendArtifact]:
        return sorted(self._catalog.values(), key=lambda aa: aa.creation_timestamp)
