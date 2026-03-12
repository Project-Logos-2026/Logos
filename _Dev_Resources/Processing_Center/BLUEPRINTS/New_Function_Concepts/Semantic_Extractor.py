SYSTEM_SPEC — Semantic_Extraction_Engine
CANONICAL_TARGET: MSPC
ROLE: Deterministic semantic ingestion subsystem
STATUS: Proposed

OBJECTIVE
Build a continuous, deterministic semantic ingestion subsystem inside MSPC that:
1. reads governance artifacts, philosophical corpus, and codebase content in sequence
2. segments content into meaning windows rather than token fragments
3. derives semantic nuggets in natural language, lambda calculus, and PXL form
4. emits provisional EAs backed by SMP+AA pairs
5. feeds every tick output to MSPC and EMP

CANONICAL SOURCE ORDER
1. Governance artifacts
2. Philosophical corpus
3. Codebase

ROTATION RULE
- Run on a configurable tick cycle
- Default tick interval: 5 seconds
- Source family rotates every 1 hour
- On hour boundary:
  - close current AA segment
  - open new AA segment
  - reset source-family segment state
This prevents mixed-source epistemic muddying inside a single append stream.

SEMANTIC WINDOW RULES
- minimum window: 2 sentences
- preferred window: 2–4 sentences
- may extend to complete a logical clause
- never emit sentence fragments unless source artifact itself is fragmentary
- treat connectors as clause extenders:
  because, therefore, thus, hence, if, then, implies, consequently

INPUT TYPES
- .md governance documents
- philosophical corpus text
- code comments / docstrings / function bodies / signatures
- formal notation blocks when available

CORE OUTPUT UNIT
Semantic_Nugget
Fields:
- nugget_id
- source_type
- source_path
- line_range
- natural_language
- semantic_tag
- lambda_expression
- pxl_formalism
- extraction_confidence
- provenance_hash

ARTIFACT MODEL
The extractor does not invent new artifact classes.
It writes into protocol backend EAs:

EA
  SMP (immutable anchor + metadata only)
  AA  (append-only content stream, hash-bound to SMP)

SMP METADATA
- smp_id
- author
- recipient
- source_family
- source_paths_used
- extractor_id
- tick_counter
- aa_pointer
- created_at
- updated_at
Only metadata mutates.

AA HEADER
- aa_id
- bound_smp_id
- hash
- status=provisional
- append_permissions=[extractor_id, owning_protocol]

AA APPEND PAYLOAD
- semantic_nugget
- lambda_expression
- pxl_formalism
- semantic_tag
- source_reference

PIPELINE
1. scheduler selects next source family
2. ingestion loader pulls next eligible segment
3. semantic window builder constructs meaning window
4. semantic parser derives semantic nugget
5. lambda formatter builds lambda expression
6. pxl formatter builds PXL expression
7. EA writer appends to MSPC backend EA
8. EA writer appends same nugget to EMP backend EA
9. SMP metadata tick counter increments
10. logs + manifests update

VALIDATION
- fail closed on parse corruption
- do not emit partial malformed nugget
- if lambda or PXL generation fails:
  - mark nugget incomplete
  - optionally append as natural-language-only if governance allows
  - otherwise discard and log failure

BACKEND OUTPUTS
MSPC backend:
- semantic append EA
- semantic journal
- primitive staging entries

EMP backend:
- epistemic append EA
- formal candidate staging entries

FUTURE EXTENSIONS
- direct MTP handoff formatter
- AP routing if AP exists in-repo; otherwise self-route
- passive mode prioritization schedule