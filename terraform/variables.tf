variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnets" {
  default = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "private_subnets" {
  default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "availability_zones" {
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "db_master_user" {
  description = "The master username for the RDS instance"
  type        = string
}

variable "db_master_password" {
  description = "The master password for the RDS instance"
  type        = string
  sensitive   = true
}

variable "db_user" {
  description = "The IAM authenticated database user"
  type        = string
}

variable "region" {
  description = "The AWS region"
  type        = string
  default     = "us-east-1"
}

variable "account_id" {
  description = "The AWS account ID"
  type        = string
  default = "408007299814"
}
