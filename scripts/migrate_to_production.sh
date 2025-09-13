#!/bin/bash
# Norte Gestión Migration Script - SQLite to PostgreSQL

set -e

echo "🚀 Norte Gestión - Migrating to Production Database"
echo "=================================================="

# Check if SQLite database exists
if [ ! -f "db.sqlite3" ]; then
    echo "❌ SQLite database not found!"
    exit 1
fi

# Export data from SQLite
echo "📦 Exporting data from SQLite..."
python migrate_sqlite_to_postgres.py export

# Check if export was successful
if [ ! -f "norte_gestion_data.json" ]; then
    echo "❌ Data export failed!"
    exit 1
fi

echo "✅ Data exported successfully"

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
docker-compose -f docker-compose.hetzner.yml --env-file .env.hetzner exec db pg_isready -U "${POSTGRES_USER}"

# Run migrations
echo "🔧 Running Django migrations..."
docker-compose -f docker-compose.hetzner.yml --env-file .env.hetzner exec backend python manage.py migrate

# Import data to PostgreSQL
echo "📥 Importing data to PostgreSQL..."
docker-compose -f docker-compose.hetzner.yml --env-file .env.hetzner exec backend python migrate_sqlite_to_postgres.py import

# Create superuser (interactive)
echo "👤 Create Django superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    docker-compose -f docker-compose.hetzner.yml --env-file .env.hetzner exec backend python manage.py createsuperuser
fi

# Collect static files
echo "🎨 Collecting static files..."
docker-compose -f docker-compose.hetzner.yml --env-file .env.hetzner exec backend python manage.py collectstatic --noinput

# Create initial backup
echo "🗄️  Creating initial backup..."
./scripts/backup_db.sh

echo ""
echo "✅ Migration to production completed successfully!"
echo "🌐 Your Norte Gestión system is ready at:"
echo "   Frontend: http://5.161.102.34"
echo "   Backend:  http://5.161.102.34:8000"
echo "   Admin:    http://5.161.102.34:8000/admin/"
echo ""
echo "📝 Next steps:"
echo "   1. Configure your domain (optional)"
echo "   2. Setup SSL certificate (recommended)"
echo "   3. Configure firewall rules"
echo "   4. Setup monitoring"