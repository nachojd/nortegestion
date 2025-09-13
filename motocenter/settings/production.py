"""
Production settings for Norte Gestión project.
"""

import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required for production")

# Production hosts
ALLOWED_HOSTS = [
    '5.161.102.34',  # Hetzner server IP
    'localhost',
    '127.0.0.1',
]

# Add custom domain when ready
if os.getenv('DOMAIN'):
    ALLOWED_HOSTS.extend([
        os.getenv('DOMAIN'),
        f"www.{os.getenv('DOMAIN')}"
    ])

# Database - PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'norte_gestion_prod'),
        'USER': os.getenv('POSTGRES_USER', 'norte_gestion'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 60,
        },
        'CONN_MAX_AGE': 60,
    }
}

if not DATABASES['default']['PASSWORD']:
    raise ValueError("POSTGRES_PASSWORD environment variable is required for production")

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    f"http://5.161.102.34",
    f"https://5.161.102.34",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add custom domain when ready
if os.getenv('DOMAIN'):
    CORS_ALLOWED_ORIGINS.extend([
        f"https://{os.getenv('DOMAIN')}",
        f"https://www.{os.getenv('DOMAIN')}",
    ])

CORS_ALLOW_CREDENTIALS = True

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL settings (uncomment when domain/SSL is ready)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Add WhiteNoise for static files
INSTALLED_APPS.insert(2, 'whitenoise.runserver_nostatic')