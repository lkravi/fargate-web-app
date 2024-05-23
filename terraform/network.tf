module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.1" # Check for the latest version on the Terraform Registry

  name                 = "main-vpc"
  cidr                 = var.vpc_cidr
  azs                  = var.availability_zones
  public_subnets       = var.public_subnets
  private_subnets      = var.private_subnets

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_db_subnet_group" "mydb" {
  name       = "mydb-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "mydb-subnet-group"
  }
}