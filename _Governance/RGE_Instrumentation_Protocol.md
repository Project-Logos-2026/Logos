# RGE Instrumentation Protocol

**Status:** AUTHORITATIVE  
**Scope:** Toggle-controlled instrumentation for RGE scoring modules  
**Authority:** Governance. Instrumentation is observational only.

---

## 1. Purpose

This protocol defines the rules governing optional instrumentation within RGE scoring modules. Instrumentation captures per-evaluation breakdowns for observability without affecting scoring behavior.

---

## 2. Toggle Semantics

Instrumentation is controlled by a constructor flag:

    enable_instrumentation: bool = False

When False:
- No intermediate data structures are allocated.
- No per-pair detail lists are constructed.
- No instrumentation report is generated.
- The scoring code path is identical to non-instrumented execution minus a single boolean branch.
- get_last_instrumentation_report() returns None.

When True:
- Per-pair intermediate values are captured from the identical variables used in scoring computation.
- An instrumentation report is generated after each compute_score call.
- The report is replaced on each call. No cross-tick accumulation.
- get_last_instrumentation_report() returns the report from the most recent call.

---

## 3. Deterministic Ordering Requirement

All per-pair details in the instrumentation report must follow a deterministic order. Pair iteration order is defined by the tuple index ordering of the recursion layer registry: for i in range(n), for j in range(i+1, n). Pair keys use canonical alphabetical sorting via _generate_pair_key.

No random ordering. No set iteration. No hash-dependent ordering.

---

## 4. No Side Effects Rule

Instrumentation must not:

- Print to stdout or stderr.
- Write to disk.
- Log to global logging frameworks.
- Mutate the telemetry snapshot.
- Mutate the configuration snapshot.
- Alter the score returned by compute_score.
- Communicate with any external system.
- Affect the behavior of any other scoring module.

Instrumentation is a pure observer.

---

## 5. Report Schema

The instrumentation report is a dictionary with the following exact structure:

    {
        "delta_dimensionality": int,
        "pair_count": int,
        "layers": [str, ...],
        "strain_gates": {
            "LAYER_NAME": float,
            ...
        },
        "pairs": [
            {
                "pair": "LAYER_A|LAYER_B",
                "residual_raw": float,
                "residual_normalized": float,
                "g_i": float,
                "g_j": float,
                "weight": float,
                "contribution": float
            },
            ...
        ],
        "total_coupling_penalty": float
    }

All floats in the report must be finite. All floats must be the exact values computed during scoring. No recomputation. No rounding. No approximation.

---

## 6. Prohibition Against Runtime Mutation

Instrumentation reports must never be used to:

- Modify scoring weights.
- Adjust coupling parameters.
- Influence topology selection.
- Override Logos authority.
- Trigger governance state changes.
- Feed back into telemetry production.

Instrumentation data may be read by external audit processes. It may not feed back into the runtime loop.

---

## 7. Observational-Only Intent

The sole purpose of instrumentation is to enable post-hoc analysis of scoring behavior. It exists to answer the question: "What contributed to this topology selection?" It does not exist to influence future selections.

Any use of instrumentation data to modify runtime behavior constitutes a governance violation.
