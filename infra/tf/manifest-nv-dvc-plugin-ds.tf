

resource "kubernetes_daemonset" "nvidia-device-plugin-daemonset" {
  count            = var.deploy_nv_device_plugin_ds ? 1 : 0
  metadata {
    name      = "nvidia-device-plugin-daemonset"
    namespace = "kube-system"
  }

depends_on = [ local_file.cluster-config ]

  spec {
    selector {
      match_labels = {
        name = "nvidia-device-plugin-ds"
      }
    }

    template {
      metadata {
        labels = {
          name = "nvidia-device-plugin-ds"
        }
      }

      spec {
        toleration {
          key      = "nvidia.com/gpu"
          operator = "Exists"
          effect   = "NoSchedule"
        }

        priority_class_name = "system-node-critical"

        container {
          image = "nvcr.io/nvidia/k8s-device-plugin:v0.14.5"
          name  = "nvidia-device-plugin-ctr"

          env {
            name  = "FAIL_ON_INIT_ERROR"
            value = "false"
          }

          security_context {
            allow_privilege_escalation = false
            capabilities {
              drop = ["ALL"]
            }
          }

          volume_mount {
            name       = "device-plugin"
            mount_path = "/var/lib/kubelet/device-plugins"
          }
        }

        volume {
          name = "device-plugin"

          host_path {
            path = "/var/lib/kubelet/device-plugins"
          }
        }
      }
    }
  }
}
