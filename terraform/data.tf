data "external" "ip_address" {
  program = ["bash", "get_ip.sh"]
}

data "aws_caller_identity" "current" {}
