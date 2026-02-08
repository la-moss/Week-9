variable "env_name" { type = string }
variable "onprem_cidr" { type = string }

# Subnets in this spoke; association is part of the contract.
variable "subnets" {
  type = list(object({
    name = string
    associate_route_table = bool
  }))
}

# Route table routes to on-prem. Offline model only.
variable "routes" {
  type = list(object({
    name          = string
    address_prefix = string
    next_hop_type  = string
  }))
}
