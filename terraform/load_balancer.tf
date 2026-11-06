resource "aws_lb_target_group" "public-servers" {
  name     = "public-servers"
  port     = 80
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    path = "/health"
  }
}

resource "aws_lb_target_group_attachment" "public-servers" {
  count            = length(aws_instance.public-servers)
  target_group_arn = aws_lb_target_group.public-servers.arn
  target_id        = aws_instance.public-servers[count.index].id
  port             = 80
}

resource "aws_lb" "public-servers" {
  name               = "public-servers"
  internal           = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.allow_http_inbound.id,
  aws_security_group.allow_all_outbound.id]
  subnets = [for subnet in module.vpc.public_subnets : subnet.id]

  enable_deletion_protection = true

  #   access_logs {
  #     bucket  = aws_s3_bucket.lb_logs.id
  #     prefix  = "test-lb"
  #     enabled = true
  #   }

  #   tags = {
  #     Environment = "production"
  #   }
}

resource "aws_lb_listener" "public-servers" {
  load_balancer_arn = aws_lb.public-servers.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.public-servers.arn
  }
}
