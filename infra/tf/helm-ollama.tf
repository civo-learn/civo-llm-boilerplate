resource "helm_release" "ollama" {
  count            = var.deploy_ollama ? 1 : 0
  name = "ollama"

  repository = "https://otwld.github.io/ollama-helm/"
  chart      = "ollama"
  wait       = true

  namespace        = "ollama"
  create_namespace = true

  values = [
    "${file("values/ollama-values.yaml")}"
  ]

  depends_on = [
    kubernetes_daemonset.nvidia-device-plugin-daemonset
  ]



}