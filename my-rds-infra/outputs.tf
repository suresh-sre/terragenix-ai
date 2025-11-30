output "db_instance_address" {
  value       = aws_db_instance.default.address
  description = "The address of the RDS instance."
}

output "db_instance_port" {
  value       = aws_db_instance.default.port
  description = "The port of the RDS instance."
}

output "db_instance_username" {
  value       = aws_db_instance.default.username
  description = "The username for the RDS instance."
  sensitive   = true
}

output "db_name" {
  value = aws_db_instance.default.db_name
  description = "The database name."
}