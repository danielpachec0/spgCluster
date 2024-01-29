resource "digitalocean_kubernetes_cluster" "spg-cluster" {
  name    = "spg-cluster"
  region  = "nyc1"
  version = "1.22.8-do.1"
  node_pool {
    name       = "spg-pool"
    size       = "s-2vcpu-2gb"
    node_count = var.node_count
  }

