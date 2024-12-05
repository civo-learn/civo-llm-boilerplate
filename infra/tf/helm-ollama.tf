resource "helm_release" "ollama" {
  count = var.deploy_ollama ? 1 : 0
  name  = "ollama"

  repository = "https://otwld.github.io/ollama-helm/"
  chart      = "ollama"
  wait       = true

  namespace        = "ollama"
  create_namespace = true

  values = [
    "${file("values/ollama-values.yaml")}"
  ]

  set_list {
    name  = "ollama.models.pull"
    value = var.default_models
  }

  depends_on = [
    kubernetes_daemonset.nvidia-device-plugin-daemonset
  ]

  # set a 15 minute timeout for the helm release
  timeout = 900 # 15 minutes in seconds
}