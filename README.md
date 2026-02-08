# Week 9 — Route Propagation

**Severity:** SEV-2  
**Service area:** Platform Networking  
**Scope:** Hub/Spoke + VNet peering + UDR associations + on‑prem connectivity

## Context

Read `scenario/ticket.md` and `scenario/timeline.md` first for the incident framing.

A platform rollout added a new dependency reachable via **on‑prem** through the hub.

On paper, everything is wired correctly:
- VNets are peered
- Route tables exist
- CIDRs are present in Terraform
- CI shows no syntax errors

Yet one environment cannot reach the dependency, while another can.

No runtime outage has occurred.  
CI/CD pipelines are blocked.  
Guardrails are failing.

## The Problem

This is not a DNS incident.

This is a **route effectiveness** problem:
routes exist, but traffic does not take the path you think it does.

The failure pattern is consistent with:
- peering transit settings not matching the intended routing model, and/or
- UDRs not being associated where the platform assumes they are, and/or
- on‑prem route next‑hop intent being inconsistent across environments.

## Constraints

- Offline validation only (`terraform init -backend=false`)
- Static analysis guardrails (no cloud credentials)
- Evidence-driven investigation (capture guardrail output)
- Preserve modularity and the hub/spoke intent

## Guardrails

**Fail:** `guardrail unmet: ...`  
**Pass:** `guardrail met`

Guardrail output is spoiler-free (counts only; no file paths).
Guardrails also validate the hub gateway contract (SKU/BGP/transit/tunnel count).

## Acceptance Criteria

- All guardrails pass
- Routing intent is explicit and consistent across environments
- UDR associations match subnet intent (no “it exists somewhere” routing)
- Peering transit settings align with the design (hub is actually a hub)
- On‑prem path is explicit (don’t rely on “it should just propagate”)
Start by comparing `terraform/envs/dev`, `staging`, and `prod` contracts for drift.

Evidence captured:
- guardrail outputs before/after
- environment routing contract evidence (dev/staging/prod)
- short routing intent note in-repo (1–2 paragraphs max)
- hub gateway contract evidence (SKU/BGP/transit/tunnel count)

## What NOT to Do

- “Fix” by widening CIDRs or adding blanket 0.0.0.0/0 routes
- Pin versions or add approval gates to hide the issue
- Assume that “routes exist” means “traffic flows”
- Treat it as a refactor-only exercise

## Repository Structure

```
terraform/
  modules/
    hub/
    spoke/
    peering/
  envs/
    dev/
    staging/
    prod/
scripts/guardrails/
  run.py
  checks/
scenario/
  ticket.md
  timeline.md
evidence/
  notes/
```

## Run (offline)

```bash
cd terraform/envs/dev
terraform init -backend=false
terraform validate

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/guardrails/run.py --iac-path terraform
```
