# Phase-2.1.1 Shared Append Artifact (AA) Schema Appendix (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Source: BUILDING_BLOCKS/SMP-AA-Complete_design_packet/SHARED_AA_SCHEMA_APPENDIX.md

## Purpose and Scope
Append Artifacts (AAs) are the exclusive mechanism for post-creation cognition,
reasoning, validation, disagreement, enrichment, and confidence evaluation.

This appendix is binding across Logos Protocol, Logos Agent, I1/I2/I3 Agents,
SCP/ARP/MTP/EMP, and SOP governance and audit processes.

## Foundational Invariants
- SMPs are immutable after creation; payloads never change.
- All post-creation cognition occurs via AAs.
- Canonical knowledge is derived only via AA-based construction.

## AA Core Fields (AA_CORE)
- aa_id: unique AA identifier.
- aa_type: I1AA | I2AA | I3AA | LogosAA | ProtocolAA.
- aa_origin_type: agent | protocol.
- originating_entity: specific agent or protocol name.
- bound_smp_id: immutable SMP identity.
- bound_smp_hash: cryptographic hash of the bound SMP.
- creation_timestamp: AA creation time.
- aa_hash: cryptographic hash of this AA.
- classification_state: rejected | conditional | provisional | canonical.
- promotion_context: conditions satisfied or not satisfied.
- origin_signature: signature of the originating entity.
- cross_validation_signatures: optional validation signatures.
- verification_stage: ingress | post-triune | pre-canonicalization.

## Allowed Content
AAs may contain:
- analytic results
- domain-specific reasoning outputs
- validation findings
- conflict detection
- confidence metrics
- references to diffs
- references to other AAs
- recommendations (non-binding)

## Prohibited Content
AAs must not:
- modify SMP content
- overwrite SMP metadata
- collapse or consolidate other AAs
- directly promote an SMP
- invoke external libraries autonomously

## Diff Handling
- AAs do not contain SMP deltas.
- Diffs compare views, evaluation states, or analytic outcomes.
- Diffs are referenced, not embedded.

DIFF_REFERENCES:
- reference_view_id
- diff_reference_ids

## AA Cataloging Model
Each SMP maintains an append-only catalog of associated AAs.

SMP Header Fields:
- append_artifacts.aa_hashes
- append_artifacts.aa_count
- append_artifacts.last_aa_added_at

## AA Origin Classes
- Agent-generated AAs: I1, I2, I3, Logos Agent.
- Protocol-generated AAs: SCP, ARP, MTP, EMP.

## Promotion Semantics
- AAs support promotion and never cause promotion.
- Logos evaluates required AA types, criteria satisfaction, and conflicts.
- EMP proof artifacts are required for canonicalization.

## Canonicalization Rule
- Canonicalization does not mutate the original SMP.
- Canonicalization produces a new Canonical SMP (C-SMP).
- Canonical SMPs are closed to further AAs.
- Canonical SMPs live exclusively in CSP and retain derivation lineage.

## Governance Enforcement
Violations of this appendix are epistemic integrity failures and SOP triggers.
This appendix introduces no runtime logic or authority.
