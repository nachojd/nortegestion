-- PostgreSQL Initialization Script
-- Creates required user and database for Norte Gestión

-- Create user if not exists
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'norte_gestion') THEN
        CREATE USER norte_gestion WITH PASSWORD 'placeholder_password';
    END IF;
END
$$;

-- Create database if not exists
SELECT 'CREATE DATABASE norte_gestion_prod OWNER norte_gestion'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'norte_gestion_prod')\gexec

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE norte_gestion_prod TO norte_gestion;

-- Connect to the new database and set up permissions
\c norte_gestion_prod

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO norte_gestion;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO norte_gestion;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO norte_gestion;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO norte_gestion;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO norte_gestion;