terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project = "fleet-respect-484204-r9"
  region  = "us-central1"
}

resource "google_storage_bucket" "terraform_storage" {
  name          = "fleet-respect-484204-r9-terraform-storage"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = "demo_dataset"


}

