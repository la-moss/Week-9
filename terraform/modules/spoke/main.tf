locals {
  # Subnets that SHOULD have the route table associated.
  associated_subnets = [for s in var.subnets : s.name if s.associate_route_table]

  # On-prem routes that SHOULD exist in the route table.
  onprem_routes = [for r in var.routes : r if r.address_prefix == var.onprem_cidr]
}

output "spoke_contract" {
  value = {
    env               = var.env_name
    associated_subnets = local.associated_subnets
    onprem_routes      = local.onprem_routes
  }
}
