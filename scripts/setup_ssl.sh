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
cd ~/ysf-chatbot
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

# Restart Docker containers with new port mapping
echo "Restarting Docker containers..."
docker compose down || true
docker compose up -d --build

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
