# Security Policy — LOGOS System

## Scope

LOGOS is a **non-executing, non-autonomous analytical framework**.
Security concerns here are **conceptual and governance-related**, not operational.

---

## Threat Model

Primary risks addressed by LOGOS governance:

- Implicit escalation from analysis to authority
- Simulation mistaken for execution
- Overclaiming certainty or intent
- Boundary collapse between descriptive and prescriptive output

---

## Security Posture

- Deny-by-default
- Fail-closed
- No autonomous continuation
- No hidden state or background execution

---

## Reporting Issues

If you identify:
- Boundary violations
- Ambiguous language implying agency
- Documentation drift that weakens constraints

Report them as **governance issues**, not vulnerabilities.

---

## What LOGOS Is Not Securing

LOGOS does not:
- Handle credentials
- Manage secrets
- Execute code
- Control systems

Traditional application security practices may be irrelevant here.
