
import uuid
import time
import hashlib
from typing import Dict, List, Any, Optional
from .SMP_Schema import SMP, SMPHeader, SMPProvenance, SMPConfidence, SMPPrivation, SMPAppendArtifacts, AppendArtifact, SMPValidationError
from .Classification_Tracker import validate_transition

class SMPStoreError(Exception):
    pass

class SMPStore:
    def __init__(self):
        self._smps: Dict[str, SMP] = {}
        self._aas: Dict[str, AppendArtifact] = {}

    def create_smp(self, smp_type: str, payload: Dict[str, Any], session_id: str, source: str) -> SMP:
        smp_id = str(uuid.uuid4())
        now = time.time()
        header = SMPHeader(
            smp_id=smp_id,
            smp_type=smp_type,
            classification_state="conditional",
            created_at=now,
            created_by=source,
            session_id=session_id
        )
        provenance = SMPProvenance(
            source=source,
            acquisition_path="direct",
            content_hash=hashlib.sha256(str(payload).encode()).hexdigest(),
            chain_of_custody=[source]
        )
        confidence = SMPConfidence(
            status="initial",
            confidence=1.0
        )
        privation = SMPPrivation(
            redaction_compatible=True,
            quarantine_compatible=False,
            partial_elision_allowed=False
        )
        append_artifacts = SMPAppendArtifacts()
        smp = SMP(
            header=header,
            provenance=provenance,
            confidence=confidence,
            privation=privation,
            payload=payload,
            append_artifacts=append_artifacts
        )
        smp.validate()
        self._smps[smp_id] = smp
        return smp

    def append_aa(self, bound_smp_id: str, aa_type: str, originating_entity: str, content: Dict[str, Any]) -> AppendArtifact:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_agent_write_boundary
        validate_agent_write_boundary(bound_smp_id, aa_type)
        if bound_smp_id not in self._smps:
            raise SMPStoreError("SMP not found.")
        smp = self._smps[bound_smp_id]
        if smp.header.classification_state == "canonical":
            raise SMPStoreError("Cannot append AA to canonical SMP.")
        aa_id = str(uuid.uuid4())
        now = time.time()
        aa_hash = hashlib.sha256((str(aa_id) + str(content)).encode()).hexdigest()
        aa = AppendArtifact(
            aa_id=aa_id,
            bound_smp_id=bound_smp_id,
            aa_type=aa_type,
            originating_entity=originating_entity,
            content=content,
            creation_timestamp=now,
            aa_hash=aa_hash
        )
        aa_hashes = list(smp.append_artifacts.aa_hashes) + [aa_hash]
        aa_count = smp.append_artifacts.aa_count + 1
        last_aa_added_at = now
        new_append_artifacts = SMPAppendArtifacts(
            aa_hashes=aa_hashes,
            aa_count=aa_count,
            last_aa_added_at=last_aa_added_at
        )
        new_smp = SMP(
            header=smp.header,
            provenance=smp.provenance,
            confidence=smp.confidence,
            privation=smp.privation,
            payload=smp.payload,
            append_artifacts=new_append_artifacts
        )
        new_smp.validate(previous_classification=smp.header.classification_state)
        self._smps[bound_smp_id] = new_smp
        self._aas[aa_hash] = aa
        return aa

    def promote_classification(self, smp_id: str, target_state: str) -> SMP:
        if smp_id not in self._smps:
            raise SMPStoreError("SMP not found.")
        smp = self._smps[smp_id]
        current = smp.header.classification_state
        validate_transition(current, target_state)
        new_header = SMPHeader(
            smp_id=smp.header.smp_id,
            smp_type=smp.header.smp_type,
            classification_state=target_state,
            created_at=smp.header.created_at,
            created_by=smp.header.created_by,
            session_id=smp.header.session_id
        )
        new_smp = SMP(
            header=new_header,
            provenance=smp.provenance,
            confidence=smp.confidence,
            privation=smp.privation,
            payload=smp.payload,
            append_artifacts=smp.append_artifacts
        )
        new_smp.validate(previous_classification=current)
        self._smps[smp_id] = new_smp
        return new_smp

    def reject_smp(self, smp_id: str):
        if smp_id in self._smps:
            smp = self._smps[smp_id]
            new_header = SMPHeader(
                smp_id=smp.header.smp_id,
                smp_type=smp.header.smp_type,
                classification_state="rejected",
                created_at=smp.header.created_at,
                created_by=smp.header.created_by,
                session_id=smp.header.session_id
            )
            new_smp = SMP(
                header=new_header,
                provenance=smp.provenance,
                confidence=smp.confidence,
                privation=smp.privation,
                payload=smp.payload,
                append_artifacts=smp.append_artifacts
            )
            new_smp.validate(previous_classification=smp.header.classification_state)
            self._smps[smp_id] = new_smp

    def get_smp(self, smp_id: str) -> Optional[SMP]:
        return self._smps.get(smp_id)

    def get_smps_by_classification(self, classification_state: str) -> List[SMP]:
        return [smp for smp in self._smps.values() if smp.header.classification_state == classification_state]

    def get_smp_count(self) -> int:
        return len(self._smps)

    def get_aa_count(self) -> int:
        return len(self._aas)
