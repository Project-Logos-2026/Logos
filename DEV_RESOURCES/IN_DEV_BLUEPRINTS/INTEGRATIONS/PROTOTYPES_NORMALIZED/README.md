# ARP Normalized Prototypes (Design-Only)

## Status
- Design-only
- Deny-by-default
- No runtime wiring
- No proof projection
- No autonomy

These files are normalized shells produced to validate the rewrite framework
and prepare for governed Application Function (AF) implementation.

## Canonical Files and AF Mapping

### pxl_engine.py
- AF-PXL-VALIDATE
- AF-PXL-CACHE-POLICY

### iel_engine.py
- AF-IEL-DOMAIN-SELECT
- AF-IEL-SYNTHESIZE

### math_engine.py
- AF-MATH-SIMILARITY

### unified_reasoning.py
- AF-UNIFIED-AGGREGATE
- AF-EPISTEMIC-DOWNGRADE

## Non-Canonical
- reasoning_demo.py
  - NON-CANONICAL
  - Excluded from ARP and runtime
  - Retained for historical/demo reference only

## Notes
- No logic is implemented here.
- All reasoning must be implemented in governed AFs.
- Proof projection remains blocked until AFs exist and are governed.

## Interfaces
See:
- LOGOS_SYSTEM/RUNTIME/Runtime_Reasoning/ARP/Application_Functions/INTERFACES.md

These interfaces define the only authorized I/O contracts for AFs.
No logic may exist outside these contracts.
