# SHARED_AA_SCHEMA_APPENDIX.md

## Purpose
Defines all Append Artifact (AA) classes used across LOGOS passive and active runtime.

This appendix is binding for ARP, MTP, SCP, SOP, EMP, and Logos Protocol.

---

## Base Append Artifact (AA)

### Required Fields
- aa_id (crypto hash)
- parent_smp_id (crypto hash)
- originating_protocol
- originating_agent
- timestamp
- semantic_family_id
- classification_state (provisional | conditional | rejected)
- confidence_metrics (domain-scoped)
- stop_condition (satisfied | stalled | context_required)

AA is immutable once written.

---

## SMP-AA

Extension of AA:
- smp_version_pointer
- delta_summary
- enrichment_summary

Used by protocols to append structured work products to SMPs.

---

## I2AA (Meaning / Transformation)

Adds:
- semantic_deficit_map
- enrichment_actions_taken
- privation_compression_summary

---

## I3AA (Reasoning)

Adds:
- reasoning_gaps
- conflict_sets
- aggregation_confidence
- meta_reasoning_flags

---

## I1AA (Signal / Constraint)

Adds:
- stability_metrics
- constraint_satisfaction_map
- convergence_summary
- fractal_depth_reached

---

## Cryptographic Requirements
- All AAs must be signed by the originating agent
- Logos verifies signatures before consideration

---

END APPENDIX
