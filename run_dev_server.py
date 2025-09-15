#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Set environment variables for development
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nortegestion.settings')
os.environ['DEBUG'] = 'True'
os.environ['USE_POSTGRES'] = 'False'

# Initialize Django
django.setup()

from django.core.management import execute_from_command_line

try:
    print("[INFO] Starting NorteGestión backend server...")
    print(f"[INFO] Database: {settings.DATABASES['default']['ENGINE']}")
    print(f"[INFO] Database name: {settings.DATABASES['default']['NAME']}")
    print("[INFO] Server will run on http://localhost:8000")
    print("[INFO] API endpoints available at http://localhost:8000/api/")
    print("[INFO] Authentication: JWT required for all endpoints")
    print("[INFO] Use Ctrl+C to stop the server")
    print("")

    # Run the server
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

except Exception as e:
    print(f"[ERROR] Error starting server: {e}")
    import traceback
    traceback.print_exc()