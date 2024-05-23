
# Fargate Web App with RDS MySQL

This repository contains the code and configuration for a web application running on AWS Fargate with a MySQL database hosted on AWS RDS. The repository is structured to facilitate local development using Docker Compose and deployment to AWS using Terraform.

## Architecture Diagram
![alt text](https://raw.githubusercontent.com/lkravi/fargate-web-app/main/fargate_web_app.png)

## Table of Contents

- [Project Structure](#project-structure)
- [Local Setup Guide](#local-setup-guide)
- [Building the AWS Fargate Environment with Terraform](#building-the-aws-fargate-environment-with-terraform)
- [Important Files](#important-files)
- [License](#license)

## Project Structure

```
.
├── LICENSE
├── backend
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── ...
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── src
│   └── ...
├── init.sql
├── terraform
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── ...
```

### Folders and Important Files

- **backend/**: Contains the Flask backend application, its Dockerfile, and dependencies.
  - `app.py`: The main application file for the Flask backend.
  - `requirements.txt`: Python dependencies for the backend application.
  - `Dockerfile`: Dockerfile to containerize the backend application.

- **frontend/**: Contains the frontend application and its Dockerfile.
  - `src`: Source code of the Vue.js application.
  - `vue.config.js`: Configuration file for Vue CLI.
  - `Dockerfile`:  Dockerfile for the Vue.js application.

- **init.sql**: SQL script to initialize the MySQL database with the required schema and seed data.

- **terraform/**: Contains Terraform configuration files for deploying the application to AWS Fargate.
  - `main.tf`: Main Terraform configuration file.
  - `variables.tf`: Defines input variables for Terraform.
  - `outputs.tf`: Defines outputs from the Terraform configuration.

- **docker-compose.yml**: Docker Compose file to set up the local development environment.

## Local Setup Guide

### Prerequisites

- Docker
- Docker Compose

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/lkravi/fargate-web-app.git
   cd fargate-web-app
   ```

2. **Ensure MySQL is not running locally** (to avoid port conflicts):
   ```sh
   sudo systemctl stop mysql
   ```

3. **Build and run the containers**:
   ```sh
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend: `http://localhost:8080`
   - Backend: `http://localhost:5001`

### Seed Data and Database Initialization

The MySQL container will automatically run the `init.sql` script located in the root directory, initializing the database with the required schema and seed data.

## Building the AWS Fargate Environment with Terraform

### Prerequisites

- AWS CLI configured with appropriate credentials.
- Terraform installed.

### Steps

1. **Navigate to the terraform directory**:
   ```sh
   cd terraform
   ```

2. **Initialize Terraform**:
   ```sh
   terraform init
   ```

3. **Create a `terraform.tfvars` file**:
   ```sh
   cat <<EOF > terraform.tfvars
   region = "us-east-1"
   vpc_cidr = "10.0.0.0/16"
   public_subnets = ["10.0.1.0/24"]
   private_subnets = ["10.0.2.0/24"]
   db_user = "tf_rds_user1"
   db_password = "your_password"
   db_master_user = "master_user"
   db_master_password = "master_password"
   EOF
   ```

4. **Apply the Terraform configuration**:
   ```sh
   terraform apply
   ```

5. **Verify the deployment**:
   - After the Terraform apply completes, check the AWS Management Console to verify the resources have been created.
   - Access the application via the ALB DNS name provided in the Terraform outputs.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the [LICENSE](./LICENSE) file for details.

---

By following this guide, you should be able to set up the application locally for development and deploy it to AWS using Terraform. The provided configurations and scripts aim to streamline both local development and cloud deployment processes.
