
import time
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

class SMPValidationError(Exception):
    pass

@dataclass(frozen=True)
class SMPHeader:
    smp_id: str
    smp_type: str
    classification_state: str
    created_at: float
    created_by: str
    session_id: str

@dataclass(frozen=True)
class SMPProvenance:
    source: str
    acquisition_path: str
    content_hash: str
    chain_of_custody: List[str]

@dataclass(frozen=True)
class SMPConfidence:
    status: str
    confidence: float

@dataclass(frozen=True)
class SMPPrivation:
    redaction_compatible: bool
    quarantine_compatible: bool
    partial_elision_allowed: bool

@dataclass(frozen=True)
class SMPAppendArtifacts:
    aa_hashes: List[str] = field(default_factory=list)
    aa_count: int = 0
    last_aa_added_at: Optional[float] = None

@dataclass(frozen=True)
class AppendArtifact:
    aa_id: str
    bound_smp_id: str
    aa_type: str
    originating_entity: str
    content: Dict[str, Any]
    creation_timestamp: float
    aa_hash: str

@dataclass(frozen=True)
class SMP:
    header: SMPHeader
    provenance: SMPProvenance
    confidence: SMPConfidence
    privation: SMPPrivation
    payload: Dict[str, Any]
    append_artifacts: SMPAppendArtifacts

    def validate(self, previous_classification: Optional[str] = None):
        if not isinstance(self.payload, dict):
            raise SMPValidationError("Payload must be a dict.")
        if not self.privation:
            raise SMPValidationError("Privation must be present.")
        if previous_classification is not None:
            from .Classification_Tracker import validate_transition
            validate_transition(previous_classification, self.header.classification_state)
        if self.append_artifacts.aa_count != len(self.append_artifacts.aa_hashes):
            raise SMPValidationError("AppendArtifacts count/hash mismatch.")
        # Append-only invariant
        if previous_classification == "canonical" and self.header.classification_state != "canonical":
            raise SMPValidationError("No regression from canonical allowed.")
        return True
