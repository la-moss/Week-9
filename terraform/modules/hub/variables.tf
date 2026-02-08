variable "env_name" { type = string }
variable "onprem_cidr" { type = string }

variable "gateway_sku" { type = string }
variable "enable_bgp" { type = bool }
variable "gateway_transit_enabled" { type = bool }
variable "tunnel_count" { type = number }
