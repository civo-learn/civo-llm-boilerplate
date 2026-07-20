# Output the ollama-ui service IP
output "ollama_ui_service_ip" {
  value = var.deploy_ollama_ui ? data.kubernetes_service.ollama-ui.status.0.load_balancer.0.ingress.0.ip : null
}

# Output the web app load balancer public IP
output "ollama_app_load_balancer_ip" {
  value = var.deploy_app ? try(data.kubernetes_service.app.status[0].load_balancer[0].ingress[0].ip, null) : null
}
