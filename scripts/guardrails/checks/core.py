from pathlib import Path
from collections import Counter
from scripts.guardrails.checks.tfvars import read_tfvars

ONPREM_NEXT_HOP_REQUIRED = "VirtualNetworkGateway"

def _check_peering_route_effective(env):
    # For on-prem via hub gateway:
    # - hub->spoke must allow gateway transit
    # - spoke->hub must use remote gateways
    if not env["hub_to_spoke_allow_gateway_transit"] or not env["spoke_to_hub_use_remote_gateways"]:
        return ["peering_route_effective"]
    return []

def _check_forwarded_traffic_required(env):
    if not env["allow_forwarded_traffic"]:
        return ["forwarded_traffic_disabled"]
    return []

def _check_udr_association_missing(env):
    # app and data subnets must have route table association
    required = ("app", "data")
    by_name = {s["name"]: s for s in env["subnets"]}
    missing = [n for n in required if n not in by_name or not by_name[n]["associate_route_table"]]
    if missing:
        return ["udr_association_missing"]
    return []

def _check_hub_gateway_contract(env):
    fails = []
    if not env.get("hub_gateway_transit_enabled", False):
        fails.append("hub_gateway_transit_disabled")
    if not env.get("hub_enable_bgp", False):
        fails.append("hub_bgp_disabled")
    tunnel_count = env.get("hub_tunnel_count", 0)
    if not isinstance(tunnel_count, (int, float)) or tunnel_count < 2:
        fails.append("hub_tunnel_count_low")
    sku = str(env.get("hub_gateway_sku", ""))
    if not sku.startswith("VpnGw"):
        fails.append("hub_gateway_sku_invalid")
    return fails

def _check_env_routing_contract_drift(envs):
    # Expect dev/staging/prod to share the same peering intent for this lab.
    dev = envs.get("dev")
    if not dev:
        return []
    expected = (
        dev["hub_to_spoke_allow_gateway_transit"],
        dev["spoke_to_hub_use_remote_gateways"],
        dev["allow_forwarded_traffic"],
        dev.get("hub_gateway_transit_enabled"),
        dev.get("hub_enable_bgp"),
        dev.get("hub_gateway_sku"),
        dev.get("hub_tunnel_count"),
        dev.get("onprem_cidr"),
    )
    fails = []
    for name, e in envs.items():
        got = (
            e["hub_to_spoke_allow_gateway_transit"],
            e["spoke_to_hub_use_remote_gateways"],
            e["allow_forwarded_traffic"],
            e.get("hub_gateway_transit_enabled"),
            e.get("hub_enable_bgp"),
            e.get("hub_gateway_sku"),
            e.get("hub_tunnel_count"),
            e.get("onprem_cidr"),
        )
        if got != expected:
            fails.append("env_routing_contract_drift")
            break
    return fails

def _check_effective_route_gap_latent(env):
    # Latent check: only meaningful once peering + association are corrected.
    # Ensure on-prem route exists AND uses expected next hop.
    routes = [r for r in env["routes"] if r["address_prefix"] == env["onprem_cidr"]]
    if not routes:
        return ["effective_route_gap"]
    if any(r["next_hop_type"] != ONPREM_NEXT_HOP_REQUIRED for r in routes):
        return ["effective_route_gap"]
    return []

CHECKS_STAGE1 = [
    _check_peering_route_effective,
    _check_forwarded_traffic_required,
    _check_udr_association_missing,
]

CHECKS_STAGE2 = [
    _check_hub_gateway_contract,
    _check_effective_route_gap_latent,
]

def run_all(iac_root: Path):
    envs = {}
    for env_dir in (iac_root / "envs").iterdir():
        if not env_dir.is_dir():
            continue
        tfvars = env_dir / "terraform.tfvars"
        if tfvars.exists():
            env = read_tfvars(tfvars)
            envs[env["env_name"]] = env

    failures = []

    # Stage 1 checks (surface)
    for env_name, env in envs.items():
        for check in CHECKS_STAGE1:
            failures += check(env)

    failures += _check_env_routing_contract_drift(envs)

    stage1_failed = len(failures) > 0

    # Stage 2 latent check (only after stage 1 is clean)
    stage2_skipped = stage1_failed
    if not stage1_failed:
        for env_name, env in envs.items():
            for check in CHECKS_STAGE2:
                failures += check(env)

    c = Counter(failures)
    return {
        "failed": sum(c.values()),
        "passed": 0 if c else 1,
        "skipped": 0 if not stage2_skipped else len(CHECKS_STAGE2) * len(envs),
        "stage1_failed": stage1_failed,
        "stage2_skipped": stage2_skipped,
        "failures": dict(c),
    }
