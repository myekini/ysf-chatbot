#!/bin/bash
set -e

# Navigate to app directory
cd ~/ysf-chatbot

# Pulling changes is handled by the CI pipeline before running this script

# Check if we need to rebuild (Dockerfile or requirements.txt changed)
REBUILD_NEEDED=false

if git diff HEAD@{1} HEAD --name-only | grep -q "Dockerfile\|requirements.txt\|frontend/\|src/\|app.py"; then
    echo "📦 Dependencies changed - full rebuild required"
    REBUILD_NEEDED=true
else
    echo "✅ No dependency changes - quick update"
    REBUILD_NEEDED=false
fi

# Stop running containers
echo "Stopping containers..."
docker compose down || true

if [ "$REBUILD_NEEDED" = true ]; then
    # Full rebuild with cleanup
    echo "🧹 Cleaning up old images..."
    docker system prune -af --volumes || true
    docker builder prune -af || true
    
    echo "🔨 Building new image..."
    docker compose build --no-cache
else
    # Quick update - just restart with existing image
    echo "🚀 Quick restart with existing image..."
fi

# Start containers
echo "▶️ Starting containers..."
docker compose up -d

# Light cleanup (only dangling images)
echo "🧹 Light cleanup..."
docker image prune -f

echo "✅ Deployment complete!"
