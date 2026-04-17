# Terraform RDS Module

This Terraform module deploys an RDS instance on AWS.

## Prerequisites

*   Terraform installed (>= 1.0)
*   AWS account configured with appropriate credentials
*   VPC and Subnets configured in AWS
*   Security Group created in AWS

## Usage

1.  Clone this repository.
2.  Copy `terraform.tfvars.example` to `terraform.tfvars` and update the variable values to match your desired configuration.
3.  Initialize Terraform:
    bash
    terraform init
    
4.  Plan the changes:
    bash
    terraform plan
    
5.  Apply the changes:
    bash
    terraform apply
    

## Variable Descriptions

| Variable                     | Description                                                                      | Default Value     |
| ---------------------------- | -------------------------------------------------------------------------------- | ----------------- |
| `aws_region`                 | The AWS region to deploy resources to.                                          | `us-east-1`       |
| `db_name`                    | The name of the database.                                                        | `mydb`            |
| `db_instance_class`          | The instance class for the RDS instance.                                          | `db.t3.small`     |
| `db_engine`                  | The database engine to use.                                                       | `mysql`           |
| `db_engine_version`          | The version of the database engine.                                                  | `8.0`             |
| `db_username`                | The database username.                                                             | `admin`           |
| `db_password`                | The database password.                                                             | (Required)        |
| `allocated_storage`          | The allocated storage size (in GB).                                                 | `20`              |
| `max_allocated_storage`          | The maximum allocated storage size (in GB) for auto-scaling.                                                 | `100`              |
| `multi_az`                   | Enable multi-AZ deployment for high availability.                                  | `false`           |
| `publicly_accessible`        | Whether the database is publicly accessible (not recommended for production).         | `false`           |
| `vpc_id`                     | The ID of the VPC to deploy the database into.                                     | (Required)        |
| `db_subnet_group_name`       | The name of the DB subnet group.                                                      | (Required)        |
| `security_group_ids`         | A list of security group IDs to associate with the database.                         | (Required)        |
| `deletion_protection`        | Enable deletion protection to prevent accidental deletion.                            | `true`            |
| `db_port`          | The port the database listens on.                                                        | `3306`            |
| `backup_retention_period`          | The number of days to retain backups for.                                                        | `7`            |
| `skip_final_snapshot`        | Whether to skip the final snapshot on deletion.                                  | `true`            |
| `final_snapshot_identifier_prefix`          | Prefix for the final snapshot identifier.                                                        | `final-snapshot`            |
| `tags`                       | A map of tags to apply to the RDS instance.                                          | (See `variables.tf`)|

## Deployment Steps

1.  **Configure AWS Credentials:** Ensure that your AWS credentials are properly configured, either through environment variables, IAM roles, or the AWS CLI.
2.  **Create or Identify VPC and Subnets:**  Ensure a VPC exists with private subnets for the RDS instance.  The subnets should be identified by ID.
3.  **Create a DB Subnet Group:**  Create a DB Subnet Group in AWS that includes the private subnets in your VPC.
4.  **Create a Security Group:**  Create a Security Group that allows inbound traffic on port 3306 (or your chosen `db_port`) from your application servers or other trusted sources. For simplicity, an example is provided that allows traffic from the VPC CIDR range.  Modify as appropriate for production.
5.  **Update `terraform.tfvars`:**  Update the `terraform.tfvars` file with the correct values for your environment, including VPC ID, subnet IDs, security group IDs, database credentials, and any other desired configurations.
6.  **Initialize Terraform:** `terraform init`
7.  **Plan and Apply:**  `terraform plan` and `terraform apply` to deploy the RDS instance.

## Important Considerations

*   **Security:**  The example Security Group provided is for demonstration purposes. In a production environment, restrict access to the RDS instance to only the necessary sources.
*   **Password Management:**  Avoid storing passwords directly in Terraform files.  Use a secrets management solution like AWS Secrets Manager or HashiCorp Vault.
*   **Backup and Recovery:**  Ensure that you have a proper backup and recovery strategy in place for your database.
*   **Monitoring:**  Implement monitoring and alerting to track the performance and health of your RDS instance.
*   **Deletion Protection:**  Deletion protection is enabled by default to prevent accidental deletion.  Disable this only when necessary and with caution.
*   **Final Snapshot:** The `skip_final_snapshot` variable is set to `true` by default, this is to avoid issues with deletion protection preventing the destruction of the terraform state. When set to `false` a final snapshot will be created before deletion.  If `deletion_protection` is set to `true`, this operation will fail unless the deletion protection is disabled first.