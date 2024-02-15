# VPC
resource "google_compute_network" "vpc" {
  name                    = "spg-vpc"
  auto_create_subnetworks = "false"
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "spg-subnet"
  network       = google_compute_network.vpc.id
  region        = var.region
  ip_cidr_range = "10.10.0.0/24"
}

resource "google_container_cluster" "primary" {
  name                     = "spg-cluster"
  deletion_protection      = false
  remove_default_node_pool = true
  initial_node_count       = 1
  location                 = var.region
  cluster_autoscaling {
    enabled = false
  }
  vertical_pod_autoscaling {
    enabled = false
  }
  logging_service    = "none"
  monitoring_service = "none"
  addons_config {
    horizontal_pod_autoscaling {
      disabled = true
    }
    http_load_balancing {
      disabled = true
    }
  }
  #to change
  service_external_ips_config {
    enabled = false
  }

  network    = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.subnet.id
}

data "google_container_engine_versions" "gke_version" {
  location       = var.region
  version_prefix = "1.27."
}

# Separately Managed Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "spg-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  version = data.google_container_engine_versions.gke_version.release_channel_latest_version["STABLE"]
  node_config {
    kubelet_config {
      cpu_manager_policy = "static"
    }
    oauth_scopes = []
    disk_size_gb = 50
    preemptible  = true
    machine_type = "e2-standard-4"
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
