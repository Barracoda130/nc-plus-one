
module "vpc" {
  source = "/home/lcomp/terraform_modules/vpc"

  name       = "main"
  cidr_block = "10.0.0.0/16"

  public_subnet_cidrs = ["10.0.0.0/24", "10.0.1.0/24", "10.0.2.0/24"]

  private_subnet_cidrs = []

  database_subnet_cidrs = ["10.0.20.0/24", "10.0.21.0/24"]

  availability_zones = ["eu-west-2a", "eu-west-2b", "eu-west-2c"]

  name_prefix = "nc-plus-one"
}
