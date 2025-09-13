# 🚀 Norte Gestión - Deployment Guide

## Hetzner CPX21 Production Deployment

### Server Information
- **IP:** 5.161.102.34
- **Server:** Ubuntu 22.04 LTS
- **Specs:** 3 vCPU, 4GB RAM, 80GB SSD

---

## 🏗️ Initial Server Setup

1. **Connect to server:**
```bash
ssh root@5.161.102.34
```

2. **Run server setup script:**
```bash
curl -fsSL https://raw.githubusercontent.com/your-repo/norte-gestion/main/scripts/hetzner_setup.sh | bash
```

Or manually copy and run `scripts/hetzner_setup.sh`

---

## 📦 Application Deployment

### 1. Upload Project Files

Upload your project to `/opt/nortegestion/`:

```bash
# Option A: Using git (recommended)
cd /opt/nortegestion
git clone https://github.com/your-repo/nortegestion.git .

# Option B: Using rsync/scp
rsync -avz --exclude-from='.gitignore' ./ root@5.161.102.34:/opt/nortegestion/
```

### 2. Configure Environment

```bash
cd /opt/nortegestion
cp .env.hetzner .env

# Edit the .env file with your production values
nano .env
```

**Important:** Update these values in `.env`:
- `SECRET_KEY` - Generate a new Django secret key
- `POSTGRES_PASSWORD` - Use a strong password
- `DOMAIN` - Add your domain when ready

### 3. Build and Start Services

```bash
# Build and start all services
docker-compose -f docker-compose.hetzner.yml --env-file .env up -d --build

# Check status
docker-compose -f docker-compose.hetzner.yml --env-file .env ps
```

### 4. Migrate Database

```bash
# Run the migration script
chmod +x scripts/*.sh
./scripts/migrate_to_production.sh
```

This will:
- Export data from SQLite
- Run Django migrations
- Import your 3000+ products to PostgreSQL
- Create superuser (optional)
- Collect static files
- Create initial backup

---

## 🔧 Service Management

### Start/Stop Services
```bash
# Start all services
docker-compose -f docker-compose.hetzner.yml --env-file .env up -d

# Stop all services
docker-compose -f docker-compose.hetzner.yml --env-file .env down

# Restart a specific service
docker-compose -f docker-compose.hetzner.yml --env-file .env restart backend
```

### View Logs
```bash
# All services
docker-compose -f docker-compose.hetzner.yml --env-file .env logs -f

# Specific service
docker-compose -f docker-compose.hetzner.yml --env-file .env logs -f backend
```

### Database Backup
```bash
# Manual backup
./scripts/backup_db.sh

# Setup automatic daily backup (crontab)
echo "0 2 * * * cd /opt/norte-gestion && ./scripts/backup_db.sh" | crontab -
```

---

## 🌐 Access Your Application

After successful deployment:

- **Frontend:** http://5.161.102.34
- **Backend API:** http://5.161.102.34:8000/api/
- **Django Admin:** http://5.161.102.34:8000/admin/

---

## 🔒 Security Configuration

### Firewall Status
```bash
sudo ufw status
```

### Update SSL (when domain is ready)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Update nginx configuration to enable SSL block
```

### Monitor Security
```bash
# Check fail2ban status
sudo fail2ban-client status

# Check fail2ban jails
sudo fail2ban-client status nginx-http-auth
```

---

## 🔧 Troubleshooting

### Check Service Health
```bash
# Check if all containers are running
docker ps

# Check container health
docker-compose -f docker-compose.hetzner.yml --env-file .env exec backend python manage.py check --deploy

# Test database connection
docker-compose -f docker-compose.hetzner.yml --env-file .env exec db pg_isready -U norte_gestion
```

### Common Issues

**Database Connection Error:**
```bash
# Check PostgreSQL container
docker-compose -f docker-compose.hetzner.yml --env-file .env logs db

# Reset database (WARNING: destroys data)
docker-compose -f docker-compose.hetzner.yml --env-file .env down -v
docker-compose -f docker-compose.hetzner.yml --env-file .env up -d
```

**Frontend Build Error:**
```bash
# Rebuild frontend
docker-compose -f docker-compose.hetzner.yml --env-file .env build frontend
docker-compose -f docker-compose.hetzner.yml --env-file .env up -d frontend
```

---

## 📊 Monitoring

### System Resources
```bash
# Docker stats
docker stats

# System resources
htop
df -h
```

### Application Logs
```bash
# Django logs
tail -f /var/log/django/django.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 🔄 Updates

### Update Application
```bash
cd /opt/norte-gestion

# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.hetzner.yml --env-file .env build
docker-compose -f docker-compose.hetzner.yml --env-file .env up -d

# Run migrations if needed
docker-compose -f docker-compose.hetzner.yml --env-file .env exec backend python manage.py migrate
```

---

## 🆘 Support

If you encounter issues:

1. Check the logs first
2. Verify all environment variables are set correctly
3. Ensure all services are running
4. Check firewall and network connectivity
5. Review this deployment guide

**Emergency Contact:** Contact your system administrator or Norte Gestión support.

---

*Norte Gestión - Sistema integral de gestión empresarial* 🌐