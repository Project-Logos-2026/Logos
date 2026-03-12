# Directory_Creation_Authorization_Rules

**Governance Domain:** Developer  
**Scope:** `/workspaces/Logos/_Dev_Resources` and all governed repository roots  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Developer  

---

## 1. Purpose

This document defines the authorization requirements for creating new directories within governed repository roots. Unauthorized directory creation is a governance violation.

---

## 2. Governing Principle

> NO new directory may be created under any governed root unless:
> - it is **explicitly authorized by a prompt** from the repository owner or architect, OR
> - it is **explicitly approved by the repository architect** in a governance artifact.

This rule applies to all automated agents, tooling scripts, and manual operations.

---

## 3. Governed Roots

The following repository roots are governed by this rule:

| Root | Governance Owner |
|---|---|
| `_Dev_Resources/` | Developer Governance |
| `_Reports/` | Developer Governance |
| `LOGOS_SYSTEM/` | Runtime Governance |
| `STARTUP/` | Runtime Governance (Coq stack extension) |
| `_Governance/` | Governance Governance |

---

## 4. Pre-Authorized Directories

The following directories are permanently authorized and require no further approval to populate with files:

| Directory | Authorization Basis |
|---|---|
| `_Dev_Resources/Dev_Tools/Runtime_Tools/<existing subcategories>/` | Established in prior canonicalization step |
| `_Dev_Resources/Dev_Tools/Repo_Governance_Tools/` | Established in prior canonicalization step |
| `_Dev_Resources/Repo_Governance/Developer/` | Established in this governance step |
| `_Dev_Resources/Repo_Governance/Runtime/` | Established in this governance step |
| `_Dev_Resources/Repo_Inventory/Master_Indexes/Environment/` | Authorized in this governance step |
| `_Dev_Resources/Repo_Inventory/Master_Indexes/Runtime/` | Authorized in this governance step |
| `_Dev_Resources/Repo_Inventory/Master_Manifests/` | Authorized in this governance step |
| `_Dev_Resources/Reports/Tool_Outputs/Runtime/` | Established in prior canonicalization step |
| `_Dev_Resources/Reports/_Dev_Governance/` | Established in prior canonicalization step |
| `_Dev_Resources/QUARANTINE/` | Established by Development_Rules.json routing rules |

---

## 5. Prohibited Actions

The following actions are prohibited without explicit authorization:

1. Creating any new top-level directory under `_Dev_Resources/`.
2. Creating new subdirectories under `Processing_Center/` at any level.
3. Creating new subcategory directories under `Dev_Tools/Runtime_Tools/` (beyond the existing nine).
4. Creating any directory under `_Reports/` that does not exist and has not been authorized.
5. Creating any directory inside `Repo_Governance/Header_Schemas/`.

---

## 6. Authorization Request Process

When a new directory is deemed necessary:

1. **Identify:** State the proposed path, purpose, and which governance domain it belongs to.
2. **Justify:** Explain why an existing directory is insufficient.
3. **Request:** Submit the request explicitly in the active prompt or as a governance artifact.
4. **Receive authorization:** Explicit human confirmation is required before creation.
5. **Document:** Record the authorization in the relevant governance document (append to this file under §7 or to the applicable domain document).
6. **Create:** Create the directory only after step 5 is complete.

---

## 7. Authorization Log

| Date (UTC) | Path Created | Authorizing Prompt / Artifact |
|---|---|---|
| 2026-03-12 | `_Dev_Resources/Repo_Inventory/` | Step 2 canonicalization prompt |
| 2026-03-12 | `_Dev_Resources/Repo_Inventory/Master_Indexes/` | Step 2 canonicalization prompt |
| 2026-03-12 | `_Dev_Resources/Repo_Inventory/Master_Indexes/Environment/` | Step 2 canonicalization prompt |
| 2026-03-12 | `_Dev_Resources/Repo_Inventory/Master_Indexes/Runtime/` | Step 2 canonicalization prompt |
| 2026-03-12 | `_Dev_Resources/Repo_Inventory/Master_Manifests/` | Step 2 canonicalization prompt |
| 2026-03-12 | `_Dev_Resources/Repo_Governance/Developer/` | Prior canonicalization + Step 2 governance prompt |
| 2026-03-12 | `_Dev_Resources/Repo_Governance/Runtime/` | Prior canonicalization + Step 2 governance prompt |
| 2026-03-12 | `_Dev_Resources/Reports/Tool_Outputs/Runtime/` | Prior Runtime_Tools canonicalization step |
| 2026-03-12 | `_Dev_Resources/Reports/_Dev_Governance/` | Prior Runtime_Tools canonicalization step |

---

## 8. Naming Requirements for Authorized Directories

When a new directory is authorized:

- Use `Title_Case_With_Underscores` for the directory name.
- Abbreviations in directory names MUST be ALL-CAPS.
- Directory names must be concise and reflect content type.
- Comply with `Naming_Convention_Enforcement.md` (see `Repo_Governance/Runtime/`).

---

## 9. Cross-References

| Document | Location |
|---|---|
| Dev_Resources_Directory_Contract.md | `Repo_Governance/Developer/` |
| Dev_Resources_Freeze_Protocol.md | `Repo_Governance/Developer/` |
| Development_Rules.json | `Repo_Governance/Developer/` |
| Naming_Convention_Enforcement.md | `Repo_Governance/Runtime/` |
