#!/bin/bash
# Script de deployment para Hetzner CX22

echo "🚀 Deploying Norte Gestión to Hetzner CX22..."

# 1. Exportar datos de SQLite
echo "📦 Exporting SQLite data..."
python migrate_sqlite_to_postgres.py export

# 2. Build and start production containers
echo "🐳 Building Docker containers..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod build

echo "🔄 Starting production stack..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# 3. Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 30

# 4. Run migrations
echo "🔧 Running migrations..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod exec backend python manage.py migrate

# 5. Import data
echo "📥 Importing data to PostgreSQL..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod exec backend python migrate_sqlite_to_postgres.py import

# 6. Create superuser (optional)
echo "👤 Create superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    docker-compose -f docker-compose.prod.yml --env-file .env.prod exec backend python manage.py createsuperuser
fi

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at your server IP"
echo "🔧 Admin panel: http://your-ip/admin/"