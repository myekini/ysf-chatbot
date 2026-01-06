# SSL/HTTPS Setup for chatbot.sabisave.info

This guide will help you set up SSL/HTTPS for your chatbot using Nginx and Let's Encrypt.

## Prerequisites

- Your domain `chatbot.sabisave.info` should already be pointing to your EC2 instance IP (`51.20.134.50`)
- Verify DNS propagation by running: `nslookup chatbot.sabisave.info`

## Setup Instructions

### Step 1: SSH into your EC2 instance

```bash
ssh -i "ecommerce_key.pem" ec2-user@51.20.134.50
```

### Step 2: Navigate to the project directory

```bash
cd ~/ysf-chatbot
```

### Step 3: Pull the latest changes

```bash
git fetch origin main
git reset --hard origin/main
```

### Step 4: Update the setup script with your email

Edit the SSL setup script to add your email address:

```bash
nano scripts/setup_ssl.sh
```

Find this line:
```bash
sudo certbot --nginx -d chatbot.sabisave.info --non-interactive --agree-tos --email your-email@example.com --redirect
```

Replace `your-email@example.com` with your actual email address, then save (Ctrl+X, Y, Enter).

### Step 5: Make the script executable and run it

```bash
chmod +x scripts/setup_ssl.sh
sudo ./scripts/setup_ssl.sh
```

The script will:
1. Install Nginx
2. Install Certbot (Let's Encrypt client)
3. Configure Nginx as a reverse proxy
4. Obtain and install SSL certificate
5. Set up automatic certificate renewal

### Step 6: Verify it's working

Visit: **https://chatbot.sabisave.info**

You should see:
- 🔒 A padlock icon in your browser
- Your chatbot running over HTTPS
- HTTP automatically redirecting to HTTPS

## Troubleshooting

### If DNS is not propagated yet:

Wait 5-10 minutes and check:
```bash
nslookup chatbot.sabisave.info
```

### If Certbot fails:

Make sure port 80 is open in your EC2 Security Group:
- Go to AWS Console → EC2 → Security Groups
- Add inbound rule: HTTP (port 80) from 0.0.0.0/0
- Add inbound rule: HTTPS (port 443) from 0.0.0.0/0

### Check Nginx status:

```bash
sudo systemctl status nginx
```

### View Nginx logs:

```bash
sudo tail -f /var/log/nginx/chatbot_error.log
```

## Certificate Renewal

Let's Encrypt certificates are valid for 90 days. The setup script configures automatic renewal, but you can manually renew with:

```bash
sudo certbot renew
```

## Architecture

```
Internet (HTTPS/443)
    ↓
Nginx (Reverse Proxy)
    ↓
Docker Container (Flask App on port 5000)
```
