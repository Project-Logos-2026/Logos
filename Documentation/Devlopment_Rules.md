# Codespace Inbound Rules

These rules are the source of truth for this Logos_System codespace: routing, naming, and guardrails.

## Routing
- All reports and similar inbound artifacts go to `_Reports/`; do not create any `_reports` directories.
- All dev/support inbound items go to `_Dev_Resources/` in the appropriate subdirectory.
- If no suitable subdirectory exists under `_Reports/` or `_Dev_Resources/`, create a new one at that root and place the inbound item there.
- System documentation meant to ship with the codebase (readmes, tech sheets, ops/function docs) goes to `Documentation/`.
- Hazardous or in-transition items (task-specific moves, temporary holding) go to `_Dev_Resources/QUARANTINE/`.

## Naming
- Use Title_Case_Underscore for any new files or directories created under these locations.

## Notes
- Keep using the existing `_Reports/` and `_Dev_Resources/` roots; do not add new top-level variants.
- When adding new subdirectories for sorting, prefer concise names that reflect the content type.

## Coq Stack Guardrails (Lock & Key)
- Default posture: Coq-related paths are locked read-only via `_Dev_Resources/Dev_Scripts/repo_tools/lock_coq_stacks.sh lock`.
- Guarded paths: `/workspaces/Logos_System/PXL_Gate` and `/workspaces/Logos_System/Logos_System/System_Entry_Point/Runtime_Compiler`.
- Status: `_Dev_Resources/Dev_Scripts/repo_tools/lock_coq_stacks.sh status`.
- Temporary unlock requires the exact override token: `_Dev_Resources/Dev_Scripts/repo_tools/lock_coq_stacks.sh unlock "edit coq stacks"`.
- Relock after any edits: rerun the script with `lock` to restore read-only permissions.
