try:
    import hcl2
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing dependency: python-hcl2. Run `pip install -r requirements.txt`."
    ) from exc


def _normalize_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def read_tfvars(path):
    with path.open("r", encoding="utf-8") as handle:
        data = hcl2.load(handle)

    out = {
        "env_name": "",
        "onprem_cidr": "",
        "hub_to_spoke_allow_gateway_transit": False,
        "spoke_to_hub_use_remote_gateways": False,
        "allow_forwarded_traffic": False,
        "hub_gateway_sku": "",
        "hub_enable_bgp": False,
        "hub_gateway_transit_enabled": False,
        "hub_tunnel_count": 0,
    }
    for key, value in data.items():
        if key in ("subnets", "routes"):
            continue
        out[key] = value

    out["subnets"] = _normalize_list(data.get("subnets"))
    out["routes"] = _normalize_list(data.get("routes"))
    return out
