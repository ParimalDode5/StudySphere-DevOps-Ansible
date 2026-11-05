
variable "nginx_image" {
  description = "Nginx Docker image"
  type        = string
  default     = "nginx:stable-alpine"
}

variable "container_name" {
  description = "StudySphere container name"
  type        = string
  default     = "studysphere-terraform-nginx"
}

variable "network_name" {
  description = "Docker network name"
  type        = string
  default     = "studysphere-terraform-network"
}

variable "host_port" {
  description = "Host port exposed for StudySphere"
  type        = number
  default     = 8082

  validation {
    condition     = var.host_port >= 1024 && var.host_port <= 65535
    error_message = "Host port must be between 1024 and 65535."
  }
}

variable "website_host_path" {
  description = "Absolute WSL path containing deployed StudySphere files"
  type        = string
  default     = "/var/www/studysphere"

  validation {
    condition = (
      startswith(var.website_host_path, "/") &&
      fileexists("${var.website_host_path}/index.html")
    )
    error_message = "The website directory must be an absolute path containing index.html."
  }
}
