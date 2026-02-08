# Timeline (sanitized)

- T+00: Prod smoke tests fail for on‑prem CIDR reachability
- T+10: Initial assumption: DNS or firewall regression (ruled out)
- T+25: Peering and UDR configuration reviewed; “looks correct”
- T+40: CI guardrails identify contract violations across envs
- T+60: Root cause isolated to routing effectiveness / transit expectations
