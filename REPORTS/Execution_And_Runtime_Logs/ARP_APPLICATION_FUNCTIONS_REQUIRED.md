# ARP Application Functions — Design Register (Design-Only)

## Purpose
Define the governed application functions required to replace embedded
heuristic logic in ARP prototype engines. These functions are prerequisites
for proof projection and attestation.

## Constraints
- Design-only (no implementation)
- No new axioms
- No new IEL domains
- No runtime wiring
- Must be enforceable by Runtime_Control later

## Required Application Functions

### AF-PXL-VALIDATE
**Source:** pxl_engine.py  
**Responsibility:**  
- Orchestrate heuristic validation calls
- Enforce epistemic labeling (heuristic vs proof-backed)
- Attach proof obligation IDs (if/when available)

---

### AF-PXL-CACHE-POLICY
**Source:** pxl_engine.py  
**Responsibility:**  
- Govern cache usage
- Prevent cached results from being treated as authoritative
- Enforce downgrade on stale or missing proofs

---

### AF-IEL-DOMAIN-SELECT
**Source:** iel_engine.py  
**Responsibility:**  
- Select and activate IEL domains explicitly
- Declare domain boundaries for each reasoning pass

---

### AF-IEL-SYNTHESIZE
**Source:** iel_engine.py  
**Responsibility:**  
- Perform heuristic domain synthesis
- Prohibit epistemic escalation beyond heuristic status

---

### AF-MATH-SIMILARITY
**Source:** math_engine.py  
**Responsibility:**  
- Compute heuristic similarity / weighting
- Remain replaceable by proof-backed category laws later

---

### AF-UNIFIED-AGGREGATE
**Source:** unified_reasoning.py  
**Responsibility:**  
- Aggregate cross-engine outputs
- Enforce weakest-epistemic-rule
- Prevent confidence inflation

---

### AF-EPISTEMIC-DOWNGRADE
**Source:** unified_reasoning.py  
**Responsibility:**  
- Ensure combined outputs cannot exceed weakest input status
- Enforce labeling and audit metadata

## Status
- DESIGN REGISTER ONLY
- No implementation authorized
- Proof projection remains blocked until these functions exist and are governed