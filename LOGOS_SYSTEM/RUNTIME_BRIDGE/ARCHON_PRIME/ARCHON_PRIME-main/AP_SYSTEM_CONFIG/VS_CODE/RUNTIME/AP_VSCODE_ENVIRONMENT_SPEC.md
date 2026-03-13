# AP_VSCODE_ENVIRONMENT_SPEC

Artifact ID: OPS-ENV-001  
System: ARCHON_PRIME  
Platform: VS Code / Codespaces  
Artifact Type: Execution Environment Specification  
Status: Active

---

## Purpose

This document defines the required runtime environment for the ARCHON_PRIME execution agent.

The goal is deterministic execution across all VS Code and Codespaces environments.

---

## Required Environment

Operating System  
Linux (Codespaces compatible)

Python  
Python 3.11+ recommended  
Python 3.12 verified

Working Directory

/workspaces/ARCHON_PRIME/

---

## Required System Tools

The following tools must be available:

python  
pip  
git  
tree  
jq  
ripgrep

---

## Recommended Python Toolchain

ruff  
black  
mypy  
pytest  
coverage

---

## VS Code Extensions

Required:

ms-python.python  
ms-python.vscode-pylance  
charliermarsh.ruff  
ms-python.black-formatter  

Recommended:

eamodio.gitlens  
redhat.vscode-yaml  
eriklynd.json-tools  

Optional:

ms-azuretools.vscode-docker  
ms-vscode.makefile-tools

---

## Environment Verification

During session initialization the execution agent must confirm:

Python version  
Working directory  
Repository accessibility  
Required directories present

Failure to satisfy environment requirements must halt execution.