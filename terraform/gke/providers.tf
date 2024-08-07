terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  project = "daniel-spg"
  region  = "us-central1"
  zone    = "us-central1-c"
}
