resource "civo_network" "network" {
  label = "${var.cluster_name}-network"
}