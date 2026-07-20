resource "helm_release" "ollama" {
  count = var.deploy_ollama ? 1 : 0
  name  = "ollama"

  repository = "https://otwld.github.io/ollama-helm/"
  chart      = "ollama"
  version    = "1.67.0"
  wait       = true

  timeout          = 900 # 15 minutes

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

}