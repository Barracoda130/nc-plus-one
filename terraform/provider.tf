terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    http = {
      source = "hashicorp/http"
    }
  }
  backend "s3" {
    bucket = "terraform-states-265779924106-eu-west-2-an"
    key    = "nc-plus-one/terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      project = "nc-plus-one"
      company = "nc"
      repo    = "nc-plus-one"
    }
  }
}

provider "http" {}

data "http" "my_ip" {
  url = "https://api.ipify.org"
}

locals {
  my_ip_cidr = "${chomp(data.http.my_ip.response_body)}/32"
}
