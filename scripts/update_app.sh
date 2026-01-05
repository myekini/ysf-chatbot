#!/bin/bash
set -e

# Navigate to app directory
cd ~/ysf-chatbot

# Pull latest changes
git pull origin main

# Rebuild and restart containers
docker compose up -d --build --remove-orphans

# Prune unused images to save space
docker image prune -f
