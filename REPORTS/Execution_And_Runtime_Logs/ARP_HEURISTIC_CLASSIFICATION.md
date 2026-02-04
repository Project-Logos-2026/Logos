# ARP Heuristic Classification (Design-Only)

**Scope:** DEV_RESOURCES/IN_DEV_BLUEPRINTS/INTEGRATIONS/PROTOTYPES
**Engines:** pxl_engine.py, iel_engine.py, math_engine.py, unified_reasoning.py
**Posture:** Deny-by-default; no runtime wiring; no autonomy; no proofs assumed.
**Heuristic Rule:** All current outputs are heuristic. Terms such as "valid", "sound", "necessary", "consistent" MUST NOT be used unless explicitly linked to a concrete proof artifact.

---

## Epistemic Role by Engine (Heuristic Only)
- pxl_engine.py — PXL relation mapping and coherence scoring (heuristic).
- iel_engine.py — IEL domain lens application and narrative synthesis (heuristic).
- math_engine.py — Math lens scaffolding and similarity weighting (heuristic).
- unified_reasoning.py — Orchestrates cross-engine aggregation (heuristic). No component emits proof-backed guarantees.

## Global Constraints
- No claim of validity/soundness/necessity absent explicit proof linkage.
- Cache hits, scores, and coherence metrics are heuristic summaries, not theorems.
- No Coq artifacts are currently integrated; proof-backed results are unavailable.

## pxl_engine.py — Required Future Changes (when authorized)
- Cache returns: label as "previous heuristic result"; do not mark valid/consistent without proof reference.
- Modal consistency: mark as "simplified heuristic check"; remove/improve default-true semantics unless backed by modal proof obligations.
- Necessity inference: explicitly tag as non-axiomatic heuristic mapping (string match → necessity relation) until Coq proof exists.
- Result payload: separate heuristic scores from any future proof-backed flags; require proof reference IDs for any non-heuristic claim.

## Proof Linkage Placeholders (expected, not present)
- PXL relation soundness: expected Coq module `PXL_Relation_Soundness.v` (placeholder).
- Trinity coherence invariants: expected Coq module `Trinity_Coherence_Invariants.v` (placeholder).
- Modal necessity/possibility soundness: expected Coq module `PXL_Modal_Soundness.v` (placeholder).
- IEL domain consistency: expected Coq module `IEL_Domain_Consistency.v` (placeholder).
- Math lens category laws: expected Coq module `Math_Category_Soundness.v` (placeholder).

### Mapping Slots (engine output → proof obligation ID)
- pxl_engine: `relation.validate()` → OBL-PXL-REL-SOUND (pending Coq proof ref)
- pxl_engine: modal consistency check → OBL-PXL-MOD-SAFE (pending)
- pxl_engine: necessity relation mapping → OBL-PXL-NEC-JUST (pending)
- iel_engine: domain synthesis scoring → OBL-IEL-DOM-CONSIST (pending)
- math_engine: category application weighting → OBL-MATH-CAT-LAWFUL (pending)
- unified_reasoning: cross-engine aggregation → OBL-UNIFIED-COMB-SAFE (pending)

## Non-Canonical / Excluded
- reasoning_demo.py — NON-CANONICAL; EXCLUDED FROM ARP AND RUNTIME. Use only as a demo; no epistemic authority.

## Safe Normalization Summary
- Treat all current engine outputs as heuristic guidance only.
- Require explicit proof artifact references before any use of "valid", "sound", or "necessary" in outputs or metadata.
- Future integration must bind each output to a proof obligation ID and a concrete Coq artifact before upgrading epistemic status.
