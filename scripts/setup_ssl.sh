#!/bin/bash
set -e

echo "=========================================="
echo "Setting up SSL/HTTPS for chatbot.sabisave.info"
echo "=========================================="

# Update system
echo "Updating system packages..."
sudo yum update -y

# Install Nginx
echo "Installing Nginx..."
sudo yum install -y nginx

# Install Certbot for Let's Encrypt
echo "Installing Certbot..."
sudo yum install -y certbot python3-certbot-nginx

# Stop Nginx temporarily
sudo systemctl stop nginx || true

# Update docker-compose to expose port 5000 instead of 80
echo "Updating Docker Compose configuration..."
cd /home/ec2-user/ysf-chatbot
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
      # Add other environment variables here
    restart: always
EOF


# Define Docker Compose command
if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "Docker Compose not found. Installing standalone binary..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo "Using Docker Compose command: $DOCKER_COMPOSE_CMD"

# Restart Docker containers with new port mapping
echo "Restarting Docker containers..."
$DOCKER_COMPOSE_CMD down || true
$DOCKER_COMPOSE_CMD up -d --build

# Copy Nginx configuration
echo "Configuring Nginx..."
sudo cp nginx/chatbot.conf /etc/nginx/conf.d/chatbot.conf

# Test Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# Start Nginx
echo "Starting Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

# Obtain SSL certificate from Let's Encrypt
echo "Obtaining SSL certificate..."
sudo certbot --nginx -d chatbot.sabisave.info --non-interactive --agree-tos --email your-email@example.com --redirect

# Set up automatic renewal
echo "Setting up automatic SSL renewal..."
sudo systemctl enable certbot-renew.timer || true

echo "=========================================="
echo "✅ SSL/HTTPS setup complete!"
echo "Your chatbot is now available at:"
echo "https://chatbot.sabisave.info"
echo "=========================================="
