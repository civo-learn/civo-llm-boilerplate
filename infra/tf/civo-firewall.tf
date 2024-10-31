# Create a default firewall
# Add your own secure values here before going to production
resource "civo_firewall" "firewall" {
    name = "${var.cluster_name}-firewall"
    network_id           = civo_network.network.id
    create_default_rules = true
}