# Create a DB subnet group
resource "aws_db_subnet_group" "main" {
  name       = var.db_subnet_group_name
  subnet_ids = data.aws_subnet_ids.private.ids

  tags = merge(
    {
      Name = var.db_subnet_group_name
    },
    var.tags
  )
}

# Fetch subnet IDs
data "aws_subnet_ids" "private" {
  vpc_id = var.vpc_id
}

# Create RDS instance
resource "aws_db_instance" "default" {
  allocated_storage = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  db_name               = var.db_name
  engine                = var.db_engine
  engine_version        = var.db_engine_version
  instance_class        = var.db_instance_class
  username              = var.db_username
  password              = var.db_password
  multi_az              = var.multi_az
  publicly_accessible = var.publicly_accessible
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = var.security_group_ids
  port = var.db_port
  backup_retention_period = var.backup_retention_period
  skip_final_snapshot     = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot == false ? "${var.final_snapshot_identifier_prefix}-${timestamp()}" : null # Generate unique snapshot name if not skipping
  deletion_protection     = var.deletion_protection

  tags = merge(
    {
      Name = "${var.db_name}-db"
    },
    var.tags
  )
}

#Example security group.  This is just an example, you will want to tailor to your needs.
resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Allow inbound traffic to RDS instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = var.db_port
    to_port     = var.db_port
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] #Replace with your VPC's CIDR.
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    {
      Name = "rds_sg"
    },
    var.tags
  )
}