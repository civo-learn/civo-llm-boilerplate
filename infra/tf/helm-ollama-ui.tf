resource "helm_release" "ollama-ui" {
  count            = var.deploy_ollama_ui ? 1 : 0
  name = "ollama-ui"
  chart      = "../helm/ollama-ui/"
  namespace        = "ollama-ui"
  create_namespace = true
  replace = true
}
