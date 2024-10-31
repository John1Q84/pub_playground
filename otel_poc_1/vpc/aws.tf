terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  alias   = "apne2"
  profile = "ram-test"
  region  = "ap-northeast-2"

}

data "aws_caller_identity" "current" {
}
