
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "= 4.6.0"
    }
  }
}

# Connect Terraform to Docker Desktop
provider "docker" {}

# Resource 1: Download the Nginx Docker image
resource "docker_image" "studysphere_nginx" {
  name         = var.nginx_image
  keep_locally = true
}

# Resource 2: Create a dedicated Docker network
resource "docker_network" "studysphere_network" {
  name   = var.network_name
  driver = "bridge"
}

# Resource 3: Create the StudySphere container
resource "docker_container" "studysphere" {
  name  = var.container_name
  image = docker_image.studysphere_nginx.image_id

  restart = "unless-stopped"

  # Publish Nginx on localhost:8082
  ports {
    internal = 80
    external = var.host_port
    ip       = "127.0.0.1"
  }

  # Mount the existing StudySphere website
  volumes {
    host_path      = var.website_host_path
    container_path = "/usr/share/nginx/html"
    read_only      = true
  }

  # Connect container to the dedicated network
  networks_advanced {
    name = docker_network.studysphere_network.name
  }
}
