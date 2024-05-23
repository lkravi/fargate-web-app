resource "aws_lambda_function" "init_rds_user" {
  s3_bucket       = aws_s3_bucket.lambda_bucket.bucket
  s3_key          = aws_s3_object.lambda_zip.key
  function_name   = "initRdsUser"
  role            = aws_iam_role.lambda_execution_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.8"
  timeout         = 60
  vpc_config {
    subnet_ids         = module.vpc.private_subnets
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      DB_ENDPOINT        = split(":", aws_db_instance.mysql.endpoint)[0]
      DB_MASTER_USER     = var.db_master_user
      DB_MASTER_PASSWORD = var.db_master_password
      DB_USER            = var.db_user
    }
  }
}


resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "tf-rds-init-lambda-deployment-bucket"
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "lambda/lambda.zip"
  source = "lambda/lambda_v7.zip"
}

resource "null_resource" "invoke_lambda" {
  provisioner "local-exec" {
    command = <<EOT
      aws lambda invoke \
        --function-name ${aws_lambda_function.init_rds_user.function_name} \
        --payload '{}' \
        response.json
    EOT
  }

  depends_on = [aws_db_instance.mysql]
}
