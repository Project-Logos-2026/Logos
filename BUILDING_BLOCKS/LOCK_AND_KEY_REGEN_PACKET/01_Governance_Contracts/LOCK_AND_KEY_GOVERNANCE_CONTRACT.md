LOCK_AND_KEY_GOVERNANCE_CONTRACT
================================

Purpose
-------
This contract defines the complete, exclusive, and non-bypassable lock-and-key
boot authorization system for LOGOS. It supersedes all prior lock-and-key
governance. No legacy semantics apply.

Foundational Principles
-----------------------
1. No unilateral authority.
2. No implicit trust.
3. No runtime escalation.
4. No semantic mutation prior to lawful boot.
5. Fail-closed at every stage.

Root of Trust
-------------
The Root Session Nonce (RSN), generated once per boot by SOP, is the sole root
of trust. All authority, identity, and verification derive from RSN.

Stage Hashing
-------------
Each boot stage MUST derive its identity hash deterministically:

StageHash = H(RSN || StageID || TranscriptHash)

Equality of StageHashes is forbidden. Only commutation is admissible.

Commutation
-----------
Commutation is defined as SOP-verifiable proof that two StageHashes:
- derive from the same RSN
- satisfy order-independent derivation constraints

Lock–Key Phases
---------------
Phase 1: PXL Gate Verification
Phase 2: Runtime Compiler Verification (EMP)
Phase 3: SOP Commutation Check
Phase 4: Session Hash ID (SHID) Derivation
Phase 5: Dual Independent LEM Discharge
Phase 6: SOP LEM Commutation Check
Phase 7: Cross-Domain Identity Issuance
Phase 8: Spin-Up Verification Artifact Emission

LEM Discharge
-------------
LEM MUST be discharged twice:
- Agentic (Logos Agent)
- Non-agentic (EMP)

Neither discharge may observe the other.

Identity Issuance
-----------------
Agents may not issue agent IDs.
Protocols may not issue protocol IDs.
IDs are issued cross-domain and registered by SOP.

Prohibitions
------------
- No component may boot without RSN-derived authorization.
- No component may act without SHID.
- No semantic processing occurs prior to full lock–key success.

Audit
-----
All successful boots MUST emit a Spin-Up Verification Artifact (SVA).