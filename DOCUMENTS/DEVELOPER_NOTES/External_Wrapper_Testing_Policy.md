# External Wrapper Testing Policy

External enhancement wrappers (Torch, Transformers, Spacy, Prophet, etc.)
are present in the repository but are not required for core runtime validation.

Tests marked `external_wrapper` are skipped by default.

To run full-stack integration testing:

1. Install required external libraries.
2. Run:
   pytest -m external_wrapper

SOP governs runtime invocation and permissioning of external integrations.
Skipping these tests does not affect core LOGOS invariants.
