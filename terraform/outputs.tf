
output "container_name" {
  description = "Name of the created StudySphere container"
  value       = docker_container.studysphere.name
}

output "docker_network" {
  description = "Name of the created Docker network"
  value       = docker_network.studysphere_network.name
}

output "nginx_image" {
  description = "Nginx image used by the container"
  value       = docker_image.studysphere_nginx.name
}

output "website_url" {
  description = "URL to access the Terraform-managed website"
  value       = "http://localhost:${var.host_port}"
}
