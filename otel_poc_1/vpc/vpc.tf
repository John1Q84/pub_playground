module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = join("-", [var.name_prefix, "vpc"])
  cidr = "10.0.0.0/16"

  azs              = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets   = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Terraform   = "true"
    Environment = "otel_poc"
  }
}
