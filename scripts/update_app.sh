#!/bin/bash
set -e

# Navigate to app directory
cd ~/ysf-chatbot

# Pulling changes is handled by the CI pipeline before running this script

# Aggressive cleanup to free disk space
echo "Cleaning up Docker resources..."
docker system prune -af --volumes || true
docker builder prune -af || true

# Stop running containers to release ports
docker compose down || true

# Rebuild and restart containers
docker compose up -d --build --remove-orphans

# Prune unused images to save space
docker image prune -f
