# Dev_Resources_Directory_Contract

**Governance Domain:** Developer  
**Scope:** `/workspaces/Logos/_Dev_Resources`  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Developer  

---

## 1. Purpose

This document defines the canonical directory structure, subdomain assignments, and mutation rules for the `_Dev_Resources` root. It is the binding contract for all directory and file placement decisions within `_Dev_Resources`.

---

## 2. Canonical Directory Map

```
_Dev_Resources/
├── Dev_Tools/                      # All dev tooling scripts
│   ├── Archive/                    # Frozen archived scripts (read-only)
│   │   ├── P1-5/                   # Archived P1-5 migration scripts
│   │   └── RGE/                    # Archived RGE scripts
│   ├── Repo_Governance_Tools/      # Governance validation tools (empty — pending population)
│   └── Runtime_Tools/              # Active runtime tooling modules
│       ├── Architecture_Validation/
│       ├── Code_Extraction/
│       ├── Dependency_Analysis/
│       ├── Dev_Utilities/
│       ├── Migration/
│       ├── Repo_Audit/
│       ├── Report_Generation/
│       ├── Runtime_Diagnostics/
│       └── Static_Analysis/
├── Processing_Center/              # IMMUTABLE DIRECTORY SKELETON (see §4)
│   ├── BLUEPRINTS/                 # Protocol blueprint staging (mutable contents)
│   │   ├── ARP/
│   │   ├── CSP/
│   │   ├── DRAC/
│   │   ├── EMP/
│   │   ├── Epistemic_Artifacts/
│   │   ├── I2/
│   │   ├── Logos_Core/
│   │   ├── MSPC/
│   │   ├── MTP/
│   │   ├── P1-5/
│   │   │   └── Audits/
│   │   ├── RGE/
│   │   ├── SCP/
│   │   └── SOP/
│   └── STAGING/                    # Pipeline staging (mutable contents)
│       ├── In_Process/
│       │   ├── EXTRACT_LOGIC/
│       │   ├── KEEP_VERIFY/
│       │   └── NORMALIZE_INTGRATE/
│       ├── Inspection_Targets/
│       ├── Post_Processing/
│       └── Pre-Processing/
│           ├── agent/
│           ├── math/
│           ├── reasoning/
│           ├── safety/
│           ├── semantic/
│           ├── utility/
│           └── utils/
├── Repo_Governance/                # Governance policy artifacts
│   ├── Developer/                  # Developer environment governance
│   ├── Header_Schemas/             # FROZEN — do not modify
│   └── Runtime/                    # Runtime module governance
├── Repo_Inventory/                 # Deterministic repository indexing
│   ├── Master_Indexes/
│   │   ├── Environment/
│   │   └── Runtime/
│   └── Master_Manifests/
├── Tool_Index/                     # Tool registry and capability index
└── QUARANTINE/                     # Hazardous or in-transition items
```

---

## 3. Subdomain Assignments

| Directory | Purpose | Mutation Class |
|---|---|---|
| `Dev_Tools/Archive/` | Frozen archived scripts | IMMUTABLE |
| `Dev_Tools/Repo_Governance_Tools/` | Governance tooling | CONTROLLED |
| `Dev_Tools/Runtime_Tools/` | Active runtime tooling | MUTABLE (authorized) |
| `Processing_Center/` | Protocol staging skeleton | IMMUTABLE SKELETON |
| `Processing_Center/BLUEPRINTS/*` | Blueprint file contents | MUTABLE CONTENTS ONLY |
| `Processing_Center/STAGING/*` | Staging pipeline contents | MUTABLE CONTENTS ONLY |
| `Repo_Governance/Header_Schemas/` | Header schema definitions | FROZEN |
| `Repo_Governance/Developer/` | Developer governance docs | CONTROLLED |
| `Repo_Governance/Runtime/` | Runtime governance docs | CONTROLLED |
| `Repo_Inventory/` | Index and manifest artifacts | APPEND-ONLY |
| `Tool_Index/` | Tool registry artifacts | CONTROLLED |
| `QUARANTINE/` | Hazardous items | MUTABLE (quarantine ops) |

---

## 4. Immutability Rules

### 4.1 Archive (Frozen)

- `Dev_Tools/Archive/P1-5/` and `Dev_Tools/Archive/RGE/` are frozen artifacts.
- No file inside Archive may be modified, renamed, or deleted.
- Archive is read-only reference material.

### 4.2 Processing_Center (Skeleton Immutable)

The following Processing_Center directories MUST NOT be deleted, renamed, or restructured:

- `Processing_Center/` (root)
- `Processing_Center/BLUEPRINTS/` (directory only)
- `Processing_Center/STAGING/` (directory only)
- `Processing_Center/STAGING/In_Process/`
- `Processing_Center/STAGING/Inspection_Targets/`
- `Processing_Center/STAGING/Post_Processing/`
- `Processing_Center/STAGING/Pre-Processing/`

File contents inside these directories may change during pipeline operations.

### 4.3 Header_Schemas (Frozen)

- `Repo_Governance/Header_Schemas/` is permanently frozen.
- No file may be added, modified, or deleted within this directory.
- Schema changes require a governance exception process.

---

## 5. Placement Rules

- All new runtime tooling scripts → `Dev_Tools/Runtime_Tools/<subcategory>/`
- All new governance tools → `Dev_Tools/Repo_Governance_Tools/`
- All index and manifest artifacts → `Repo_Inventory/Master_Indexes/` or `Repo_Inventory/Master_Manifests/`
- All tool registry updates → `Tool_Index/`
- All hazardous or in-transition items → `QUARANTINE/`
- System documentation for shipping → `DOCUMENTS/` (repo root level, not in `_Dev_Resources`)

---

## 6. Prohibited Placements

- No reports or output artifacts may be created outside `_Dev_Resources/Reports/`. All report output routes to `_Dev_Resources/Reports/`.
- No `_reports/` subdirectory may be created anywhere.
- No new top-level directories may be added under `_Dev_Resources` without explicit architect authorization.

---

## 7. Cross-References

| Document | Location |
|---|---|
| Directory_Creation_Authorization_Rules.md | `Repo_Governance/Developer/` |
| Dev_Resources_Freeze_Protocol.md | `Repo_Governance/Developer/` |
| Development_Rules.json | `Repo_Governance/Developer/` |
