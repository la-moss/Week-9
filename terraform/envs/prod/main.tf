module "peering" {
  source = "../../modules/peering"

  hub_to_spoke_allow_gateway_transit = var.hub_to_spoke_allow_gateway_transit
  spoke_to_hub_use_remote_gateways   = var.spoke_to_hub_use_remote_gateways
  allow_forwarded_traffic            = var.allow_forwarded_traffic
}

module "spoke" {
  source    = "../../modules/spoke"
  env_name  = var.env_name
  onprem_cidr = var.onprem_cidr
  subnets   = var.subnets
  routes    = var.routes
}

module "hub" {
  source    = "../../modules/hub"
  env_name  = var.env_name
  onprem_cidr = var.onprem_cidr

  gateway_sku             = var.hub_gateway_sku
  enable_bgp              = var.hub_enable_bgp
  gateway_transit_enabled = var.hub_gateway_transit_enabled
  tunnel_count            = var.hub_tunnel_count
}

output "env_summary" {
  value = {
    env     = var.env_name
    onprem  = var.onprem_cidr
    peering = module.peering.peering_intent
    hub     = module.hub.hub_contract
    spoke   = module.spoke.spoke_contract
  }
}
