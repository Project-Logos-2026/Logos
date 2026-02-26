# HEADER_TYPE: GOVERNANCE_ARTIFACT
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: NON_EXECUTING
# MUTABILITY: IMMUTABLE_TEXT
# VERSION: 1.0.0
# PHASE: 7
# STEP: 2
# STATUS: ACTIVE

---

## Topology_Advice_Aa_Schema — Deterministic AA Payload Specification

### 1. Artifact Identity
- `aa_type`: "TOPOLOGY_ADVICE"
- `author_class`: "PROTOCOL"
- `author_id`: "RGE"
- `schema_version`: "1.0.0"

### 2. Canonical Payload Structure
#### 2.1 Canonical JSON Schema
```json
{
  "type": "object",
  "properties": {
    "schema_version": {
      "type": "string",
      "enum": ["1.0.0"],
      "description": "Schema version. Must be '1.0.0'."
    },
    "aa_type": {
      "type": "string",
      "enum": ["TOPOLOGY_ADVICE"],
      "description": "Artifact type. Must be 'TOPOLOGY_ADVICE'."
    },
    "author_class": {
      "type": "string",
      "enum": ["PROTOCOL"],
      "description": "Author class. Must be 'PROTOCOL'."
    },
    "author_id": {
      "type": "string",
      "enum": ["RGE"],
      "description": "Author identity. Must be 'RGE'."
    },
    "topology_id": {
      "type": "string",
      "description": "Unique identifier for topology instance."
    },
    "orchestration_tick": {
      "type": "integer",
      "description": "Orchestration tick number at time of advice."
    },
    "timestamp_utc": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 UTC timestamp."
    },
    "topology_configuration": {
      "type": "object",
      "description": "Canonical topology configuration object."
    },
    "derivation_context": {
      "type": "object",
      "description": "Contextual derivation metadata."
    },
    "confidence_metrics": {
      "type": "object",
      "description": "Confidence metrics and scores."
    },
    "status_context": {
      "type": "string",
      "enum": ["Provisional", "Conditional", "Rejected"],
      "description": "Status bucket. Must be one of the closed set."
    },
    "parent_hash_reference": {
      "type": "string",
      "description": "Hash of previous AA in chain. Null for chain root."
    }
  },
  "required": [
    "schema_version",
    "aa_type",
    "author_class",
    "author_id",
    "topology_id",
    "orchestration_tick",
    "timestamp_utc",
    "topology_configuration",
    "derivation_context",
    "confidence_metrics",
    "status_context",
    "parent_hash_reference"
  ],
  "additionalProperties": false
}
```

#### 2.2 Deterministic Constraints
- All fields must be present and match canonical types.
- No additional properties permitted.
- All string fields must be UTF-8, normalized, no whitespace drift.
- All timestamps must be ISO 8601 UTC.
- All objects must be deterministically serialized (sorted keys).

#### 2.3 Status Bucket Binding
- `status_context` must be one of: "Provisional", "Conditional", "Rejected".
- Alias normalization enforced (e.g., "Statues_Rejected" → "Rejected").
- Invalid status → reject artifact, fail-closed.

#### 2.4 Parent Hash Semantics
- `parent_hash_reference` must match current chain head.
- Null only for chain root.
- Chain linkage enforced by Router.
- Mismatch → reject, fail-closed.

#### 2.5 Prohibited Fields
- No runtime fields (e.g., issued_by, advice, phase, step, status).
- No mutable or inferred fields.
- No defaulting or inference permitted.

#### 2.6 Validation Responsibilities
- All payloads must be validated against this schema before Router acceptance.
- Non-conforming payloads are invalid and must be rejected.

#### 2.7 Freeze Criteria
- Schema is immutable once issued.
- Any updates require new schema_version and full governance review.

---

End of Topology_Advice_Aa_Schema — Deterministic AA Payload Specification.
