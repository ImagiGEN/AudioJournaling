
resource "google_compute_network" "vpc_network" {
  name = "demo-network"
}

resource "google_compute_firewall" "default" {
  name    = "demo-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["8090", "22", "8080"]

  }
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "default" {
  name         = "demo"
  machine_type = "n2-standard-2"
  zone         = var.zone

  tags = ["http-server", "https-server"]

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20230715"
      labels = {
        my_label = "demo-vm-disk"
      }
      size = 100
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }
  metadata = {
    ssh-keys = "ubuntu:${file("soundjot.pub")}"
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir -p /home/ubuntu/app/streamlit",
    ]
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }

  provisioner "file" {
    source      = "../.env"
    destination = "/home/ubuntu/app/.env"
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }


  provisioner "file" {
    source      = "../streamlit"
    destination = "/home/ubuntu/app"
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }

  provisioner "file" {
    source      = "../fastapi"
    destination = "/home/ubuntu/app"
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }

  provisioner "file" {
    source      = "../airflow"
    destination = "/home/ubuntu/app"
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }

  provisioner "file" {
    source      = "../Makefile"
    destination = "/home/ubuntu/app/Makefile"
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }
  provisioner "file" {
    source      = "../docker-compose-local.yml"
    destination = "/home/ubuntu/app/docker-compose-local.yml"
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }
  provisioner "file" {
    source      = "startup.sh"
    destination = "/home/ubuntu/app/startup.sh"
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }
  provisioner "remote-exec" {
    inline = [
      ". /home/ubuntu/app/startup.sh",
    ]
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("soundjot")
      agent       = "false"
      host        = google_compute_address.static.address
    }
  }
}

resource "google_compute_address" "static" {
  name = "ipv4-address"
}
