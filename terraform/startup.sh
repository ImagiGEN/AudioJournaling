#! /bin/bash
sudo apt update -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo groupadd docker
sudo usermod -aG docker $USER
if [ $(getent group docker) ]; then
  echo "group exists."
else
  newgrp docker
fi
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo apt install make
cd /home/ubuntu/app && sudo make build-up
