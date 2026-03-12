# Abbreviation_Usage_Policy

**Governance Domain:** Runtime  
**Scope:** All source modules, governance documents, headers, identifiers, and artifacts  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Runtime  
**Registry:** `_Dev_Resources/Repo_Governance/Runtime/Abbreviations.json`

---

## 1. Purpose

This policy governs the use of abbreviations across all LOGOS repository content. It ensures consistent, unambiguous, and canonically-registered abbreviation usage in all contexts: source code identifiers, comments, docstrings, governance documents, headers, protocol references, and output artifacts.

This policy extends the abbreviation validation rules in `Development_Rules.json → automated_normalization_appendix → phase5_rewrite_contract_binding → mandatory_abbreviation_validation`.

---

## 2. Canonical Registry

The authoritative abbreviation registry is:

```
/workspaces/Logos/_Dev_Resources/Repo_Governance/Runtime/Abbreviations.json
```

All abbreviation lookups, validations, and updates must reference this file.

---

## 3. Core Rules

### 3.1 If Abbreviation Exists in Registry

- Use the canonical long form when writing prose or comments.
- Use the canonical abbreviated form when writing identifiers, filenames, or header fields.
- Abbreviated form in identifiers and filenames MUST be ALL-CAPS.
- Do NOT invent alternative expansions if the registry already defines one.

### 3.2 If Abbreviation Does NOT Exist in Registry

1. **Default to the abbreviated form** in identifiers and code.
2. **Log the missing expansion** — record the abbreviation in the active governance report under `missing_abbreviations`.
3. **Request long-form definition** from the repository architect.
4. **Update the registry** — once the long form is approved, add it to `Abbreviations.json` before the next normalization pass.
5. Do NOT guess or infer a long form that is not confirmed by the architect.

### 3.3 Prohibited Usage

| Prohibited | Correct Alternative |
|---|---|
| Mixed case for known abbreviations (`Rge`, `Pxl`, `Iel`) | ALL-CAPS: `RGE`, `PXL`, `IEL` |
| Invented expansions not in registry | Use abbreviated form; log and request definition |
| Incorrect long-form expansions | Replace with registry long form |
| Redundant long-forms (e.g., `PXL (Protocol Extension Layer) Layer`) | `PXL Layer` or just `PXL` |
| Abbreviation in prose without long-form on first use (in docs) | Spell out on first use, then abbreviate |

---

## 4. Context-Specific Rules

### 4.1 Source Code Identifiers

```python
# CORRECT
ast_walker = ASTWalker()
rge_packet = parse_rge_packet(data)
OUTPUT_ROOT = Path(...)

# INCORRECT
ast_Walker = AstWalker()  # mixed case
rge_pkt = ...             # only if 'PKT' is not in registry
```

### 4.2 Docstrings and Comments

- Use canonical long form on first occurrence per function/class/module.
- Use abbreviated form (ALL-CAPS) for subsequent references.
- Do not mix registered and unregistered abbreviated forms in the same docstring.

### 4.3 Filenames and Directories

- Abbreviations in filenames: ALL-CAPS.
- `AST_Walker.py`, `RGE_Packet_Parser.py`, `PXL_Gate/`

### 4.4 Header Fields

- Header field values use the canonical long form when describing behavior.
- Header field keys use identifier conventions (snake_case).

### 4.5 Governance Documents

- Abbreviations defined in the registry are introduced with long form + parenthetical abbreviation on first use per section:  
  `Probabilistic Execution Layer (PXL)`
- Subsequent uses in the same section use the abbreviation.

### 4.6 JSON Artifacts

- JSON key names use `snake_case`, not abbreviations (e.g., `"import_type"` not `"IMPT"`)
- JSON values may use registered abbreviations where they are semantic labels (e.g., `"FAIL_CLOSED"`, `"PXL"`)

---

## 5. Validation During Normalization

During Phase 5 automated normalization (per `Development_Rules.json`):

1. Extract all abbreviation-like tokens (consecutive uppercase letters ≥ 2 chars) from the file.
2. Look each up in `Abbreviations.json`.
3. For found tokens: verify correct casing (ALL-CAPS) and no incorrect long-form expansion.
4. For not-found tokens: log as `missing_abbreviation`; do not expand or correct; flag for architect review.
5. Mixed or conflicting abbreviation patterns in a single file trigger FULL REWRITE escalation.

---

## 6. Registry Update Process

When a new abbreviation is approved for registration:

1. Add the entry to `Abbreviations.json` following the existing schema.
2. Record the addition in the active governance report.
3. Update any existing files (during the next normalization pass) that use the now-registered abbreviation incorrectly.
4. The registry is the single source of truth; no file-level or comment-level overrides are permitted.

---

## 7. Common Registered Abbreviations (Non-Exhaustive)

The following abbreviations are known to be registered. Consult `Abbreviations.json` for the complete list and canonical long forms:

| Abbreviation | Domain |
|---|---|
| `PXL` | Proof/protocol execution layer |
| `IEL` | Inference/execution layer |
| `RGE` | Reasoning/governance engine |
| `MSPC` | Multi-step protocol controller |
| `AST` | Abstract syntax tree |
| `CLI` | Command-line interface |
| `UTC` | Coordinated universal time |
| `LOGOS` | Repository canonical name |

For full expansions, always consult `Abbreviations.json` directly.

---

## 8. Cross-References

| Document | Location |
|---|---|
| Abbreviations.json (registry) | `Repo_Governance/Runtime/Abbreviations.json` |
| Naming_Convention_Enforcement.md | `Repo_Governance/Runtime/` |
| Development_Rules.json (§phase5_rewrite_contract_binding) | `Repo_Governance/Developer/` |
