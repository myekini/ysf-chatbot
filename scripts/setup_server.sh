#!/bin/bash
set -e

# Update system
sudo yum update -y

# Install Git and Docker
sudo yum install -y git docker

# Start Docker service
sudo service docker start
sudo systemctl enable docker

# Add user to docker group (so you don't need sudo for docker commands)
sudo usermod -a -G docker ec2-user

# Install Docker Compose (V2)
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose

# Apply group changes to current session (or tell user to re-login)
echo "Setup complete. Please log out and log back in, or run 'newgrp docker' to use docker without sudo."
