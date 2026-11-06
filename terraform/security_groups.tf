resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH from my IP"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Name = "allow-ssh"
  }
}


resource "aws_security_group" "allow_all_outbound" {
  name        = "allow_all_outbound"
  description = "Allows all outbound traffic"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Name = "allow-all-outbound"
  }
}

resource "aws_security_group" "allow_http_inbound" {
  name        = "allow_http_inbound"
  description = "Allows port 80 incoming"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Name = "allow-http-inbound"
  }
}

resource "aws_security_group" "rds" {
  name   = "rds"
  vpc_id = module.vpc.vpc_id
  tags = {
    Name = "rds"
  }
}

resource "aws_security_group" "database_access" {
  name        = "database_access"
  description = "Allow access to RDS from EC2 instances"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Name = "database-access"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_rds_inbound" {
  security_group_id            = aws_security_group.rds.id
  referenced_security_group_id = aws_security_group.database_access.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh_ingress" {
  security_group_id = aws_security_group.allow_ssh.id
  cidr_ipv4         = local.my_ip_cidr
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22

}


resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
  security_group_id = aws_security_group.allow_all_outbound.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_vpc_security_group_ingress_rule" "allow_http_inbound" {
  security_group_id = aws_security_group.allow_http_inbound.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
}



