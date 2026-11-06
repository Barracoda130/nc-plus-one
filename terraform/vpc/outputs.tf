output "public_subnets" {
  value = aws_subnet.public_subnets
}

output "private_subnets" {
  value = aws_subnet.private_subnets
}

output "database_subnets" {
  value = aws_subnet.database_subnets
}

output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "database_subnet_group" {
  value = length(var.database_subnet_cidrs) > 0 ? aws_db_subnet_group.main_db_subnet_group[0] : null
}

output "cidr_block" {
  value = aws_vpc.vpc.cidr_block
}
