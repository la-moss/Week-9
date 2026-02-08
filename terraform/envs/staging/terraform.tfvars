env_name = "staging"
onprem_cidr = "10.99.0.0/16"

hub_to_spoke_allow_gateway_transit = true
spoke_to_hub_use_remote_gateways   = false
allow_forwarded_traffic            = true

hub_gateway_sku             = "VpnGw1"
hub_enable_bgp              = true
hub_gateway_transit_enabled = true
hub_tunnel_count            = 2

subnets = [
  { name = "app",  associate_route_table = true },
  { name = "data", associate_route_table = true },
]

routes = [
  { name = "to-onprem", address_prefix = "10.99.0.0/16", next_hop_type = "VirtualNetworkGateway" },
]
