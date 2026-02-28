from __future__ import annotations
'\nLOGOS_MODULE_METADATA\n---------------------\nmodule_name: aa\nruntime_layer: inferred\nrole: inferred\nagent_binding: None\nprotocol_binding: None\nboot_phase: inferred\nexpected_imports: []\nprovides: []\ndepends_on_runtime_state: False\nfailure_mode:\n  type: unknown\n  notes: ""\nrewrite_provenance:\n  source: System_Stack/Logos_Agents/I2_Agent/protocol_operations/aa.py\n  rewrite_phase: Phase_B\n  rewrite_timestamp: 2026-02-06T00:00:00Z\nobservability:\n  log_channel: None\n  metrics: disabled\n---------------------\n'
'\nAppend Artifact (AA) schema and builder for the I2 agent context.\n\nThis module is intentionally non-transformative. It packages AA metadata\nand content for downstream governance evaluation without mutating SMPs.\n'
from dataclasses import dataclass, field
import json
from pathlib import Path
from LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.repo_root import _find_repo_root
import time
import uuid
from typing import Any, Dict, List, Optional
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I2_Agent.I2_Agent_Infra.diagnostics.errors import SchemaError
import os
from pathlib import Path
def _build_aa_hash(payload: dict) -> str:
    # Import safe_hash here to avoid circular import issues
    from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I2_Agent.I2_Agent_Infra.config.hashing import safe_hash as infra_safe_hash
    import json
    return infra_safe_hash(_stable_json(payload))
def _validate_required(value: Any, field_name: str) -> None:
    if value is None or (isinstance(value, str) and (not value.strip())):
        raise SchemaError(f'AA missing {field_name}')
ALLOWED_AA_TYPES = {'I1AA', 'I2AA', 'I3AA', 'LogosAA', 'ProtocolAA'}
ALLOWED_ORIGIN_TYPES = {'agent', 'protocol'}
ALLOWED_CLASSIFICATION = {'rejected', 'conditional', 'provisional', 'canonical'}
ALLOWED_VERIFICATION_STAGE = {'ingress', 'post-triune', 'pre-canonicalization'}


@dataclass(frozen=True)
class AppendArtifact:
    aa_id: str
    aa_type: str
    aa_origin_type: str
    originating_entity: str
    bound_smp_id: str
    bound_smp_hash: str
    creation_timestamp: float
    aa_hash: str
    classification_state: str
    promotion_context: Dict[str, Any]
    origin_signature: str
    cross_validation_signatures: List[str]
    verification_stage: str
    metadata_header: Dict[str, Any]
    content: Dict[str, Any] = field(default_factory=dict)
    diff_references: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'aa_id': self.aa_id,
            'aa_type': self.aa_type,
            'aa_origin_type': self.aa_origin_type,
            'originating_entity': self.originating_entity,
            'bound_smp_id': self.bound_smp_id,
            'bound_smp_hash': self.bound_smp_hash,
            'creation_timestamp': self.creation_timestamp,
            'aa_hash': self.aa_hash,
            'classification_state': self.classification_state,
            'promotion_context': self.promotion_context,
            'origin_signature': self.origin_signature,
            'cross_validation_signatures': list(self.cross_validation_signatures),
            'verification_stage': self.verification_stage,
            'metadata_header': self.metadata_header,
            'content': self.content,
            'diff_references': self.diff_references
        }

def _normalize_list(values: Optional[List[Any]]) -> List[str]:
    if not values:
        return []
    return [str(v) for v in values if v is not None]

def _stable_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=True)

    # see above for new implementation

def _validate_enum(value: str, allowed: set, field_name: str) -> None:
    if value not in allowed:
        raise SchemaError(f'AA {field_name} must be one of: {sorted(allowed)}')

    # see above for new implementation

def build_append_artifact(*, aa_type: str, aa_origin_type: str, originating_entity: str, bound_smp_id: str, bound_smp_hash: str, classification_state: str, promotion_context: Optional[Dict[str, Any]]=None, origin_signature: str='', verification_stage: str='ingress', content: Optional[Dict[str, Any]]=None, diff_references: Optional[Dict[str, Any]]=None, cross_validation_signatures: Optional[List[Any]]=None, metadata_header: Optional[Dict[str, Any]]=None, aa_id: Optional[str]=None, creation_timestamp: Optional[float]=None) -> AppendArtifact:
    """
    Build a non-authoritative AA record with a stable AA hash.
    """
    _validate_required(aa_type, 'aa_type')
    _validate_required(aa_origin_type, 'aa_origin_type')
    _validate_required(originating_entity, 'originating_entity')
    _validate_required(bound_smp_id, 'bound_smp_id')
    _validate_required(bound_smp_hash, 'bound_smp_hash')
    _validate_required(classification_state, 'classification_state')
    _validate_required(verification_stage, 'verification_stage')
    _validate_enum(aa_type, ALLOWED_AA_TYPES, 'aa_type')
    _validate_enum(aa_origin_type, ALLOWED_ORIGIN_TYPES, 'aa_origin_type')
    _validate_enum(classification_state, ALLOWED_CLASSIFICATION, 'classification_state')
    _validate_enum(verification_stage, ALLOWED_VERIFICATION_STAGE, 'verification_stage')
    aa_id = aa_id or str(uuid.uuid4())
    ts = float(creation_timestamp) if creation_timestamp is not None else time.time()
    promotion_context = promotion_context or {}
    content = content or {}
    diff_references = diff_references or {}
    cross_validation_signatures = _normalize_list(cross_validation_signatures)
    if not isinstance(promotion_context, dict):
        raise SchemaError('AA promotion_context must be a dict')
    if not isinstance(content, dict):
        raise SchemaError('AA content must be a dict')
    if not isinstance(diff_references, dict):
        raise SchemaError('AA diff_references must be a dict')
    normalized_header = _normalize_metadata_header(metadata_header, classification_state)
    canonical_payload = {'aa_id': aa_id, 'aa_type': aa_type, 'aa_origin_type': aa_origin_type, 'originating_entity': originating_entity, 'bound_smp_id': bound_smp_id, 'bound_smp_hash': bound_smp_hash, 'creation_timestamp': ts, 'classification_state': classification_state, 'promotion_context': promotion_context, 'origin_signature': origin_signature, 'cross_validation_signatures': cross_validation_signatures, 'verification_stage': verification_stage, 'metadata_header': normalized_header, 'content': content, 'diff_references': diff_references}
    aa_hash = _build_aa_hash(canonical_payload)
    return AppendArtifact(aa_id=aa_id, aa_type=aa_type, aa_origin_type=aa_origin_type, originating_entity=originating_entity, bound_smp_id=bound_smp_id, bound_smp_hash=bound_smp_hash, creation_timestamp=ts, aa_hash=aa_hash, classification_state=classification_state, promotion_context=promotion_context, origin_signature=origin_signature, cross_validation_signatures=cross_validation_signatures, verification_stage=verification_stage, metadata_header=normalized_header, content=content, diff_references=diff_references)
ALLOWED_EPISTEMIC_STATUS = {'REJECTED', 'PROVISIONAL', 'CONDITIONAL', 'CANONICAL'}
ALLOWED_PROOF_COVERAGE = {'UNPROVEN', 'PARTIALLY_PROVEN', 'FULLY_PROVEN', 'PROVEN_FALSE'}
ALLOWED_DEPENDENCY_SHAPE = {'LINGUISTIC_DEPENDENT', 'INFERENTIAL_DEPENDENT', 'EVIDENCE_DEPENDENT', 'AXIOMATIC_DEPENDENT'}

def _normalize_metadata_header(header: Optional[Dict[str, Any]], classification_state: str) -> Dict[str, Any]:
    if header is None:
        status = (classification_state or 'PROVISIONAL').strip().upper()
        header = {'epistemic_status': status}
    if not isinstance(header, dict):
        raise SchemaError('metadata_header must be a dict')
    status = header.get('epistemic_status')
    if not isinstance(status, str) or not status.strip():
        raise SchemaError('metadata_header.epistemic_status is required')
    normalized_status = status.strip().upper()
    if normalized_status not in ALLOWED_EPISTEMIC_STATUS:
        raise SchemaError('metadata_header.epistemic_status invalid')
    header['epistemic_status'] = normalized_status
    proof_coverage = header.get('proof_coverage')
    if proof_coverage is not None:
        if not isinstance(proof_coverage, str) or not proof_coverage.strip():
            raise SchemaError('metadata_header.proof_coverage must be a non-empty string')
        proof_coverage = proof_coverage.strip().upper()
        if proof_coverage not in ALLOWED_PROOF_COVERAGE:
            raise SchemaError('metadata_header.proof_coverage invalid')
        header['proof_coverage'] = proof_coverage
    dependency_shape = header.get('dependency_shape')
    if dependency_shape is not None:
        if not isinstance(dependency_shape, str) or not dependency_shape.strip():
            raise SchemaError('metadata_header.dependency_shape must be a non-empty string')
        dependency_shape = dependency_shape.strip().upper()
        if dependency_shape not in ALLOWED_DEPENDENCY_SHAPE:
            raise SchemaError('metadata_header.dependency_shape invalid')
        header['dependency_shape'] = dependency_shape
    semantic_projection = header.get('semantic_projection', [])
    header['semantic_projection'] = _normalize_semantic_projection(semantic_projection)
    return header

def _normalize_semantic_projection(value: Any) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise SchemaError('metadata_header.semantic_projection must be a list')
    projections = [str(item).strip().upper() for item in value if str(item).strip()]
    if not projections:
        return []
    registered = _load_semantic_projection_families()
    unregistered = [item for item in projections if item not in registered]
    if unregistered:
        raise SchemaError(f'semantic_projection unregistered: {sorted(set(unregistered))}')
    return projections

def _load_semantic_projection_families() -> set[str]:
    root = _find_repo_root()
    manifest_path = Path(root) / "_Governance" / "Semantic_Projection_Manifest.json"
    if not manifest_path.exists():
        raise SchemaError("Semantic_Projection_Manifest.json missing")
    with manifest_path.open('r', encoding='utf-8') as handle:
        payload = json.load(handle)
    families = payload.get('families') if isinstance(payload, dict) else None
    if not isinstance(families, dict):
        raise SchemaError('Semantic_Projection_Manifest.json invalid')
    return {str(key).upper() for key in families.keys()}
