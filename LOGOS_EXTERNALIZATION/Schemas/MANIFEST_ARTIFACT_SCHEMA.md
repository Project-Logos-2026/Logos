# PHASE 5 — MANIFEST ARTIFACT SCHEMA

## 1. Purpose and Authority

This document defines the canonical artifact schema for all Phase 5 manifests in the LOGOS Natural Language Externalization layer.

Manifests are authoritative registries that enumerate and describe artifacts generated within a specific Phase-5 layer.

This schema is design-time authoritative, fail-closed, and immutable once approved.

All Phase-5 manifests MUST conform exactly to this schema.

## 2. Scope

This schema applies only to:
- Phase 5
- Registry / manifest artifacts
- Non-executing, non-runtime metadata

It does not apply to:
- Template artifacts
- Runtime logic
- Meaning translation
- Proofs or audits

## 3. Canonical Location

All Phase-5 manifest artifacts MUST be stored under:

 /workspaces/Logos/LOGOS_EXTERNALIZATION/manifests/

Subdirectories MAY be introduced in later phases, but are not required at Phase 5.

## 4. Manifest File Types

Phase-5 manifests MUST be stored as JSON files.

Markdown is prohibited for manifest instances.

Schemas governing manifests may be Markdown.

## 5. Required Manifest Structure

Each manifest MUST contain the following top-level fields:

- manifest_name
- phase
- layer
- artifact_class
- authority
- version
- generated_at
- governed_by_schema
- entries

No additional top-level fields are permitted.

## 6. Field Definitions

- manifest_name: string (UPPER_SNAKE_CASE)
- phase: integer (must equal 5)
- layer: string (Natural_Language_Externalization)
- artifact_class: string (e.g. Template_Primitive)
- authority: string (LOGOS_Phase_5)
- version: string (semantic, starting at "1.0.0")
- generated_at: ISO-8601 timestamp
- governed_by_schema: string (absolute path to schema)
- entries: array of artifact descriptors

## 7. Entry Descriptor Structure

Each entry in `entries` MUST contain:

- identifier
- file_name
- primitive
- description
- status

No additional fields are permitted.

## 8. Constraints

Manifests MUST:
- Be deterministic
- Be exhaustive for their declared scope
- Contain no inferred or computed data
- Contain no runtime state

## 9. Validation Rules

A manifest is invalid if:
- Any required field is missing
- Any extra field is present
- Any entry references a non-existent artifact
- The governed_by_schema path is incorrect

Invalid manifests MUST NOT be loaded or referenced.

## 10. Final Invariant

Manifests are registries, not logic.
Schemas govern manifests.
Governance overrides convenience.
