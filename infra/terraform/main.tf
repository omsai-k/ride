terraform {
  required_version = ">= 1.6.0"
}

provider "google" {
  project = "ride-project"
  region  = "us-central1"
}

resource "google_compute_network" "ride_vpc" {
  name                    = "ride-vpc"
  auto_create_subnetworks = true
}
