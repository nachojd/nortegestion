#!/bin/bash
# Norte Gestión - Hetzner Server Setup Script
# Run this script on your Hetzner server (Ubuntu)

set -e

echo "🏗️  Norte Gestión - Hetzner Server Setup"
echo "======================================"

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/norte-gestion
sudo chown $USER:$USER /opt/norte-gestion
cd /opt/norte-gestion

# Basic firewall setup
echo "🔒 Configuring basic firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp  # Django backend (temporary)
sudo ufw allow 3000/tcp  # Next.js frontend (temporary) 
sudo ufw --force enable

# Create logs directory
sudo mkdir -p /var/log/django
sudo chown $USER:$USER /var/log/django

# Install fail2ban for security
echo "🛡️  Installing fail2ban..."
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Create fail2ban configuration for nginx
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 6

[nginx-badbots]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 2

[nginx-noproxy]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 2
EOF

sudo systemctl restart fail2ban

# Set up log rotation
sudo tee /etc/logrotate.d/norte-gestion > /dev/null <<EOF
/var/log/django/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF

echo ""
echo "✅ Hetzner server setup completed!"
echo ""
echo "📝 Next steps:"
echo "   1. Upload your Norte Gestión project to /opt/norte-gestion/"
echo "   2. Copy .env.hetzner to .env"
echo "   3. Update SECRET_KEY and passwords in .env"
echo "   4. Run: docker-compose -f docker-compose.hetzner.yml --env-file .env up -d"
echo "   5. Run: ./scripts/migrate_to_production.sh"
echo ""
echo "🔐 Security recommendations:"
echo "   - Change default SSH port"
echo "   - Set up SSH key authentication"
echo "   - Configure domain and SSL certificate"
echo "   - Set up monitoring (optional)"
echo ""
echo "🌐 After deployment, your app will be available at:"
echo "   http://5.161.102.34"