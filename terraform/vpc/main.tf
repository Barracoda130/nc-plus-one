resource "aws_vpc" "vpc" {
  cidr_block = var.cidr_block

  tags = merge(var.tags, {
    Name = "${local._name_prefix}${var.name}"
  })
}

resource "aws_subnet" "public_subnets" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(var.tags, {
    Name = "${local._name_prefix}public-${count.index + 1}"
  })
}

resource "aws_subnet" "private_subnets" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(var.tags, {
    Name = "${local._name_prefix}private-${count.index + 1}"
  })
}

resource "aws_subnet" "database_subnets" {
  count             = length(var.database_subnet_cidrs)
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.database_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(var.tags, {
    Name = "${local._name_prefix}database-${count.index + 1}"
  })
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
  tags = merge(var.tags, {
    Name = "${local._name_prefix}main"
  })
}


resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  route {
    cidr_block = aws_vpc.vpc.cidr_block
    gateway_id = "local"
  }
  tags = merge(var.tags, {
    Name = "${local._name_prefix}public"
  })
}

resource "aws_route_table" "database" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = aws_vpc.vpc.cidr_block
    gateway_id = "local"
  }

  tags = var.tags
}

resource "aws_route_table_association" "database" {
  count          = length(aws_subnet.database_subnets)
  subnet_id      = aws_subnet.database_subnets[count.index].id
  route_table_id = aws_route_table.database.id
}


resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public_subnets)
  subnet_id      = aws_subnet.public_subnets[count.index].id
  route_table_id = aws_route_table.public.id
}



resource "aws_db_subnet_group" "main_db_subnet_group" {
  count      = length(var.database_subnet_cidrs) > 0 ? 1 : 0
  name       = "${local._name_prefix}main"
  subnet_ids = aws_subnet.database_subnets[*].id

  tags = merge(var.tags, {
    Name = "${local._name_prefix}main"
  })
}


