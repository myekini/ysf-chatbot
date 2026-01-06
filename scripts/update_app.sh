#!/bin/bash
set -e

# Navigate to app directory
cd ~/ysf-chatbot

# Pulling changes is handled by the CI pipeline before running this script

# Stop running containers to release ports
docker compose down || true

# Rebuild and restart containers
docker compose up -d --build --remove-orphans

# Prune unused images to save space
docker image prune -f
