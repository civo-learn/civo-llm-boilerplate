resource "helm_release" "ollama-ui" {
  count            = var.deploy_ollama_ui ? 1 : 0
  name             = "ollama-ui"
  chart            = "../helm/ollama-ui/"
  namespace        = "ollama-ui"
  create_namespace = true
  replace          = true
  depends_on       = [local_file.cluster-config]
  timeout          = 900 # 15 minutes in seconds

  set_list {
    name  = "webui.defaultModels"
    value = var.default_models
  }

  set {
    name = "webui.image.tag"
    value = var.ollama_ui_image_version
  }

}

data "kubernetes_service" "ollama-ui" {
  metadata {
    name      = "open-webui"
    namespace = "ollama-ui"
  }

  depends_on = [helm_release.ollama-ui]
}