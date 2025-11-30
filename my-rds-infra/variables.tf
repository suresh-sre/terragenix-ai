# AWS Region
variable "aws_region" {
  type        = string
  description = "The AWS region to deploy resources to."
  default     = "us-east-1" # Change this to your desired region
}

# RDS Instance Configuration
variable "db_name" {
  type        = string
  description = "The name of the database."
  default     = "mydb"
}

variable "db_instance_class" {
  type        = string
  description = "The instance class for the RDS instance."
  default     = "db.t3.small"
}

variable "db_engine" {
  type        = string
  description = "The database engine to use."
  default     = "mysql"
}

variable "db_engine_version" {
  type        = string
  description = "The version of the database engine."
  default     = "8.0"
}

variable "db_username" {
  type        = string
  description = "The database username."
  default     = "admin"
  sensitive   = true
}

variable "db_password" {
  type        = string
  description = "The database password."
  sensitive   = true
}

variable "allocated_storage" {
  type        = number
  description = "The allocated storage size (in GB)."
  default     = 20
}

variable "max_allocated_storage" {
  type        = number
  description = "The maximum allocated storage size (in GB) for auto-scaling."
  default     = 100 # Adjust as needed
}

variable "multi_az" {
  type        = bool
  description = "Enable multi-AZ deployment for high availability."
  default     = false
}

variable "publicly_accessible" {
  type        = bool
  description = "Whether the database is publicly accessible (not recommended for production)."
  default     = false
}

variable "vpc_id" {
  type        = string
  description = "The ID of the VPC to deploy the database into."
}

variable "db_subnet_group_name" {
  type        = string
  description = "The name of the DB subnet group."
}

variable "security_group_ids" {
  type        = list(string)
  description = "A list of security group IDs to associate with the database."
}

variable "deletion_protection" {
  type        = bool
  description = "Enable deletion protection to prevent accidental deletion."
  default     = true
}

variable "db_port" {
  type        = number
  description = "The port the database listens on."
  default     = 3306
}

variable "backup_retention_period" {
  type        = number
  description = "The number of days to retain backups for."
  default     = 7
}

variable "skip_final_snapshot" {
  type        = bool
  description = "Whether to skip the final snapshot on deletion.  Setting to false can be problematic with deletion protection."
  default     = true
}

variable "final_snapshot_identifier_prefix" {
  type        = string
  description = "Prefix for the final snapshot identifier."
  default     = "final-snapshot"
}

variable "tags" {
  type        = map(string)
  description = "A map of tags to apply to the RDS instance."
  default = {
    Environment = "Production"
    Terraform   = "true"
  }
}