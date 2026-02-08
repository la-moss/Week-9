# Ticket: On‑prem reachability missing in one environment

**Severity:** SEV-2  
**Area:** Platform Networking  
**Summary:** One environment cannot reach the on‑prem dependency CIDR via the hub.

## Symptoms (sanitized)
- Dev reaches on‑prem CIDR successfully (expected).
- Prod fails reachability tests to the same on‑prem CIDR (unexpected).
- DNS resolution is consistent across envs.
- No apply errors were observed; CI blocks on guardrails.

## Request
Restore routing consistency and ensure on‑prem reachability intent is encoded and verifiable pre‑merge.

## Constraints
- Offline-only validation
- Guardrails must be spoiler-free (counts only)
