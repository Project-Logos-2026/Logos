# Phase-2.1.1 SMP-AA Session Epistemic Substrate (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Scope: SMP/AA lifecycle, classification, promotion, and storage stratification.
Source: BUILDING_BLOCKS/SMP-AA-Complete_design_packet/README.md

## Core Decisions
- SMPs are the universal semantic substrate for communication, memory, and I/O.
- SMP classification is monotonic: rejected -> conditional -> provisional -> canonical.
- Canonical SMPs live only in CSP.
- Non-canonical SMPs and all AAs live in MTP Core.
- No SMP or AA is ever deleted; only reclassified, superseded, or archived.
- All semantic mutation occurs via AA merge; SMP payloads remain immutable.
- Agents never promote SMPs; they emit promotion-trigger AAs.
- Logos is the sole arbiter of promotion and system-wide reprocessing.
- Passive runtime epistemic cycling is orchestrated by Logos.

## Non-Goals
- No runtime enforcement logic.
- No protocol activation or authority escalation.
