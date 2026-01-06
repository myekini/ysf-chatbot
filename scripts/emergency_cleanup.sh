#!/bin/bash
set -e

echo "=========================================="
echo "🧹 EC2 Disk Space Cleanup & Optimization"
echo "=========================================="

# Show current disk usage
echo "📊 Current disk usage:"
df -h /

# Stop all Docker containers
echo "🛑 Stopping all containers..."
docker stop $(docker ps -aq) 2>/dev/null || true

# Remove all containers
echo "🗑️ Removing all containers..."
docker rm $(docker ps -aq) 2>/dev/null || true

# Remove all images
echo "🗑️ Removing all images..."
docker rmi $(docker images -q) 2>/dev/null || true

# Remove all volumes
echo "🗑️ Removing all volumes..."
docker volume rm $(docker volume ls -q) 2>/dev/null || true

# Remove all build cache
echo "🗑️ Removing build cache..."
docker builder prune -af || true

# System-wide prune
echo "🗑️ System-wide cleanup..."
docker system prune -af --volumes || true

# Clean up old logs
echo "🗑️ Cleaning up old logs..."
sudo find /var/log -type f -name "*.log" -mtime +7 -delete 2>/dev/null || true
sudo journalctl --vacuum-time=7d 2>/dev/null || true

# Clean up package cache
echo "🗑️ Cleaning package cache..."
sudo yum clean all 2>/dev/null || true

# Show final disk usage
echo ""
echo "📊 Final disk usage:"
df -h /

echo ""
echo "✅ Cleanup complete!"
echo "=========================================="
