# VPC
resource "google_compute_network" "vpc" {
  name                    = "spg-vpc"
  auto_create_subnetworks = "false"
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "spg-subnet"
  network       = google_compute_network.vpc.id
  region        = "southamerica-east1"
  ip_cidr_range = "10.10.0.0/24"
}

resource "google_container_cluster" "primary" {
  name                     = "spg-cluster"
  deletion_protection      = false
  remove_default_node_pool = true
  initial_node_count       = 1
  location                 = "southamerica-east1-a"
  cluster_autoscaling {
    enabled = false
  }
  vertical_pod_autoscaling {
    enabled = false
  }
  # Disable managed Prometheus
  monitoring_config {
    managed_prometheus {
      enabled = false
    }
  }



  # Disable default logging
  logging_config {
    enable_components = []
  }

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


  release_channel {
    channel = "STABLE"
  }

  network    = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.subnet.id
}

data "google_container_engine_versions" "gke_version" {
  location       = "southamerica-east1-a"
  version_prefix = "1.27."
}

# Separately Managed Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "spg-node-pool"
  location   = "southamerica-east1-a"
  cluster    = google_container_cluster.primary.name
  node_count = 3

  version = data.google_container_engine_versions.gke_version.release_channel_latest_version["STABLE"]

  node_config {
    kubelet_config {
      cpu_manager_policy = "static"
    }
    oauth_scopes = []
    disk_size_gb = 50
    preemptible  = true
    machine_type = "e2-standard-8"
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
