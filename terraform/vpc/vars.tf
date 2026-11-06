variable "cidr_block" {
  description = "The CIDR block for the VPC (defaults to 10.0.0.0/16)"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "List of CIDR blocks for private subnets"
  type        = list(string)
}

variable "database_subnet_cidrs" {
  description = "List of CIDR blocks for database subnets"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "A map of tags to assign to all resources"
  type        = map(string)
  default     = {}
}

variable "name" {
  description = "The name of the VPC (defaults to main)"
  type        = string
  default     = "main"
}

variable "availability_zones" {
  description = "List of availability zones for the subnets"
  type        = list(string)
  default     = ["eu-west-2a", "eu-west-2b"]
}

resource "random_string" "prefix" {
  length  = 8
  special = false
  upper   = false

}

variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = ""
}

locals {
  _name_prefix = var.name_prefix == "" ? "${random_string.prefix.result}-" : "${var.name_prefix}-"
}





