resource "helm_release" "app" {
  count            = var.deploy_app ? 1 : 0
  name             = "app"
  chart            = "../helm/app/"
  namespace        = "apps"
  create_namespace = true
  replace          = true
  depends_on       = [local_file.cluster-config]
}