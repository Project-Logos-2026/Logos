SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Runtime_Contract
ARTIFACT_NAME: EXECUTION_ENVIRONMENT
VERSION: 1.0
DATE: 2026-03-11
AUTHORITY: Architect
SUBSYSTEM: Execution_Context

---------------------------------------------------------------------

PURPOSE

Defines the runtime environment requirements for AP_V2 tooling execution.

---------------------------------------------------------------------

ENVIRONMENT REQUIREMENTS

Python_Version: 3.10+
Node_Version: N/A
Shell: bash
OS: Linux (Debian)
Working_Directory: /workspaces/ARCHON_PRIME

---------------------------------------------------------------------

REQUIRED ENVIRONMENT VARIABLES

AP_SYSTEM_ROOT        Root path of the ARCHON_PRIME repository
AP_CONFIG_PATH        Path to AP_SYSTEM_CONFIG
AP_ARTIFACT_ROUTER    Path to artifact router configuration
AP_LOG_LEVEL          Execution log verbosity (INFO | DEBUG | WARN)

---------------------------------------------------------------------

EXECUTION CONSTRAINTS

• All tooling must run from AP_SYSTEM_ROOT
• No writes outside AP_SYSTEM_ROOT are permitted
• Artifact router must be initialized before any write operations
• Simulation mode must be validated before mutation mode activates

---------------------------------------------------------------------

FAILURE BEHAVIOR

If environment verification fails:

• Halt execution immediately
• Write failure event to execution log
• Do not proceed to artifact discovery phase
