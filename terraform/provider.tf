terraform {
  required_version = "=1.8.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "aws-terraform-state-2024"
    key            = "fargate-demo/state.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
  }

}

provider "aws" {
  region = "us-east-1" # Change to your desired region
}