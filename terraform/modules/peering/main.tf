# Offline-safe modelling: no provider required for validate.
# These locals represent the intended peering posture.
locals {
  hub_to_spoke_allow_gateway_transit = var.hub_to_spoke_allow_gateway_transit
  spoke_to_hub_use_remote_gateways   = var.spoke_to_hub_use_remote_gateways
  allow_forwarded_traffic            = var.allow_forwarded_traffic
}

output "peering_intent" {
  value = {
    hub_to_spoke_allow_gateway_transit = local.hub_to_spoke_allow_gateway_transit
    spoke_to_hub_use_remote_gateways   = local.spoke_to_hub_use_remote_gateways
    allow_forwarded_traffic            = local.allow_forwarded_traffic
  }
}
