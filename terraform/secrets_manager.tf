data "aws_secretsmanager_secret" "database_credentials" {
  arn = "arn:aws:secretsmanager:eu-west-2:265779924106:secret:nc-plus-one/db-credentials-yl12vl"
}


data "aws_secretsmanager_secret_version" "database_credentials" {
  secret_id = data.aws_secretsmanager_secret.database_credentials.id
}

locals {
  database_name     = jsondecode(data.aws_secretsmanager_secret_version.database_credentials.secret_string)["DB_NAME"]
  database_username = jsondecode(data.aws_secretsmanager_secret_version.database_credentials.secret_string)["DB_USERNAME"]
  database_password = jsondecode(data.aws_secretsmanager_secret_version.database_credentials.secret_string)["DB_PASSWORD"]
}
