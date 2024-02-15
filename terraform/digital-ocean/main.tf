resource "digitalocean_kubernetes_cluster" "spg-cluster" {
  name    = "spg-cluster"
  region  = "nyc1"
  version = "1.27.10-do.0"
  ha = false
  auto_upgrade = false
  destroy_all_associated_resources = true
  node_pool {
    name       = "spg-pool"
    size       = "s-4vcpu-8gb"
    node_count = var.node_count
    auto_scale = false
  }
}
