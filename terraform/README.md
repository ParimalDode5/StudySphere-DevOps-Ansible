
# StudySphere Infrastructure Provisioning with Terraform

## Overview

This project demonstrates Infrastructure as Code (IaC) using Terraform and Docker.

Terraform provisions and manages the infrastructure required to run the StudySphere website in a Docker container.

## Technologies

- Terraform
- Docker Desktop
- Docker Provider
- Nginx

## Infrastructure Resources

1. Docker Image: nginx:stable-alpine
2. Docker Network: studysphere-terraform-network
3. Docker Container: studysphere-terraform-nginx

## Deployment Configuration

The existing StudySphere website directory is mounted into the Nginx container in read-only mode.

Host directory: /var/www/studysphere

Container directory: /usr/share/nginx/html

Application URL: http://localhost:8082

## Terraform Commands

Initialize Terraform:

    terraform init

Format configuration:

    terraform fmt -recursive

Validate configuration:

    terraform validate

Preview infrastructure changes:

    terraform plan

Provision resources:

    terraform apply

Display outputs:

    terraform output

Destroy Terraform-managed resources:

    terraform destroy

## Result

Terraform provisions a Docker image, a dedicated Docker network and an Nginx container.

The StudySphere website can be accessed independently through port 8082.

This practical demonstrates Infrastructure as Code and automated resource provisioning using Terraform.
