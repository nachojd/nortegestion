#!/bin/bash
# Norte Gestión Database Backup Script

set -e

# Configuration
CONTAINER_NAME="motocenter-db-1"
BACKUP_DIR="/app/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
DB_NAME="${POSTGRES_DB:-norte_gestion_prod}"
DB_USER="${POSTGRES_USER:-norte_gestion}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create backup
echo "🗄️  Creating database backup..."
docker exec "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_DIR/backup_${DATE}.sql.gz"

# Verify backup
if [ -f "$BACKUP_DIR/backup_${DATE}.sql.gz" ]; then
    echo "✅ Backup created successfully: backup_${DATE}.sql.gz"
    
    # Show backup size
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/backup_${DATE}.sql.gz" | cut -f1)
    echo "📊 Backup size: $BACKUP_SIZE"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Clean old backups (keep last 7 days)
echo "🧹 Cleaning old backups..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +7 -delete

echo "✅ Backup process completed!"