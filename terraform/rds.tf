resource "aws_db_instance" "default" {
  allocated_storage   = 20
  db_name             = local.database_name
  engine              = "postgres"
  engine_version      = "14.24"
  instance_class      = "db.t4g.micro"
  username            = local.database_username
  password            = local.database_password
  skip_final_snapshot = true

  db_subnet_group_name   = module.vpc.database_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds.id]
}
