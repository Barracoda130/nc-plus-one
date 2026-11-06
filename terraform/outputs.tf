output "server_ssh_connections" {
  value = "ssh -i ~/.ssh/neptune-laptop.pem ubuntu@${aws_instance.public-servers[0].public_ip}"
}
