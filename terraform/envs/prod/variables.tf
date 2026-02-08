variable "env_name" { type = string }
variable "onprem_cidr" { type = string }

variable "hub_to_spoke_allow_gateway_transit" { type = bool }
variable "spoke_to_hub_use_remote_gateways" { type = bool }
variable "allow_forwarded_traffic" { type = bool }

variable "hub_gateway_sku" { type = string }
variable "hub_enable_bgp" { type = bool }
variable "hub_gateway_transit_enabled" { type = bool }
variable "hub_tunnel_count" { type = number }

variable "subnets" {
  type = list(object({
    name = string
    associate_route_table = bool
  }))
}

variable "routes" {
  type = list(object({
    name          = string
    address_prefix = string
    next_hop_type  = string
  }))
}
