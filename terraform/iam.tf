

resource "aws_iam_instance_profile" "public_server" {
  name = "nc-plus-one-public-server"
  role = aws_iam_role.public_server.name
}

data "aws_iam_policy_document" "db_credentials" {
  statement {
    sid       = "2"
    actions   = ["secretsmanager:GetSecretValue", ]
    resources = ["arn:aws:secretsmanager:eu-west-2:265779924106:secret:nc-plus-one/db-credentials-yl12vl", ]
  }
}

data "aws_iam_policy_document" "github_token" {
  statement {
    sid       = "1"
    actions   = ["secretsmanager:GetSecretValue", ]
    resources = ["arn:aws:secretsmanager:eu-west-2:265779924106:secret:github-key-0gvhOZ", ]
  }
}

data "aws_iam_policy_document" "jwt_secret" {
  statement {
    sid       = "3"
    actions   = ["secretsmanager:GetSecretValue", ]
    resources = ["arn:aws:secretsmanager:eu-west-2:265779924106:secret:nc-plus-one/jwt-secret-RfAgGH", ]
  }
}

resource "aws_iam_role_policy" "github_token_secret" {
  role = aws_iam_role.public_server.id

  policy = data.aws_iam_policy_document.github_token.json
}

resource "aws_iam_role_policy" "db_credentials_secret" {
  role = aws_iam_role.public_server.id

  policy = data.aws_iam_policy_document.db_credentials.json
}

resource "aws_iam_role_policy" "jwt_secret" {
  role = aws_iam_role.public_server.id

  policy = data.aws_iam_policy_document.jwt_secret.json
}

resource "aws_iam_role" "public_server" {
  name = "nc-plus-one-public-server"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = "sts:AssumeRole"

      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}
