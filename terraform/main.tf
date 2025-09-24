provider "google" {
  project = "hardy-antonym-471808-u8"
}

resource "google_cloud_run_v2_service" "web" {
  name     = "dithering-apis-web"
  location = "europe-west1"
  client   = "terraform"

  template {
    containers {
      image = "europe-west1-docker.pkg.dev/hardy-antonym-471808-u8/niotir/fastapi_dithering_web:v0.4.4"
    }
  }
}


resource "google_cloud_run_v2_service_iam_member" "web_noauth" {
  location = google_cloud_run_v2_service.web.location
  name     = google_cloud_run_v2_service.web.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

