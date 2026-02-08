locals {
  hub_contract = {
    env                      = var.env_name
    onprem_cidr              = var.onprem_cidr
    gateway_sku              = var.gateway_sku
    enable_bgp               = var.enable_bgp
    gateway_transit_enabled  = var.gateway_transit_enabled
    tunnel_count             = var.tunnel_count
  }
}

output "hub_contract" {
  value = local.hub_contract
}
