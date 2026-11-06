
data "github_branch" "main" {
  repository = "nc-plus-one"
  branch     = "main"
}

locals {
  app_commit_sha = var.app_commit_sha != "" ? var.app_commit_sha : data.github_branch.main.sha
  #   app_commit_sha = var.app_commit_sha
}



resource "aws_instance" "public-servers" {
  count = length(module.vpc.public_subnets)

  ami                         = "ami-0bce970415466784a"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  subnet_id                   = module.vpc.public_subnets[count.index].id
  key_name                    = "neptune-laptop"
  vpc_security_group_ids = [aws_security_group.allow_all_outbound.id,
    aws_security_group.allow_ssh.id,
    aws_security_group.database_access.id,
  aws_security_group.allow_http_from_lb.id]

  user_data = templatefile("./scripts/launch.sh",
    {
      DB_HOST        = aws_db_instance.default.address
      APP_COMMIT_SHA = local.app_commit_sha
  })
  user_data_replace_on_change = true

  iam_instance_profile = aws_iam_instance_profile.public_server.id
}
