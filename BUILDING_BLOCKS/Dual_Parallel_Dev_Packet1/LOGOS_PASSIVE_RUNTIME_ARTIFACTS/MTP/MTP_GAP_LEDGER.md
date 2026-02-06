# MTP_GAP_LEDGER.md

## Purpose
This document enumerates **all work required to reach MTP feature-completeness** under LOGOS V1.

This is a build checklist, not a design document.

---

## CORE GAPS (BLOCKING)

- [ ] SMP header injection system
- [ ] Canonical SMP schema finalization
- [ ] Translation Compiler normalization
- [ ] AA storage container implementation
- [ ] AA catalog linking (hash-based)
- [ ] Non-canonical SMP classification (provisional / conditional / rejected)

---

## ARTIFACT GAPS

- [ ] AA canonical schema
- [ ] I2AA canonical schema
- [ ] AA cryptographic binding rules
- [ ] AA provenance metadata schema

---

## TOOLING GAPS

- [ ] Formal logic translation adapters
  - [ ] PXL projection
  - [ ] IEL overlay generation
- [ ] Multi-lens semantic expansion coordination
- [ ] External library allowlist + gating

---

## PASSIVE RUNTIME GAPS (P2)

- [ ] I₂ + MTP passive workflow implementation
- [ ] Promotion-condition tagging system
- [ ] I2AA generation logic
- [ ] Promotion request packaging to Logos
- [ ] Priority scheduling (provisional > conditional > rejected)

---

## INTERFACE GAPS (DEFERRED)

(Deferred until SOP / EMP finalized)

- [ ] SOP ↔ MTP persistence boundary enforcement
- [ ] EMP consumption of AA / I2AA
- [ ] Canonical promotion handoff to CSP

---

## DOCUMENTATION GAPS

- [ ] MTP MANIFEST.md
- [ ] ORDER_OF_OPERATIONS.md
- [ ] RUNTIME_ROLE.md
- [ ] GOVERNANCE_SCOPE.md
- [ ] METADATA.json

---

END DOCUMENT
