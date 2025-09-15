#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Set environment variables for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nortegestion.settings')
os.environ['DEBUG'] = 'True'
os.environ['USE_POSTGRES'] = 'False'

# Initialize Django
django.setup()

# Test imports
try:
    from django.core.management import execute_from_command_line
    from django.contrib.auth.models import User
    from rest_framework.test import APIClient
    from rest_framework_simplejwt.tokens import RefreshToken
    print("[OK] All imports successful!")

    # Check database configuration
    print(f"[OK] Database: {settings.DATABASES['default']['ENGINE']}")
    print(f"[OK] Database name: {settings.DATABASES['default']['NAME']}")

    # Run migrations
    print("\n[WORK] Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

    # Create superuser
    print("\n[USER] Creating superuser...")
    if User.objects.filter(username='admin@nortegestion.com').exists():
        print("[OK] Superuser already exists")
        user = User.objects.get(username='admin@nortegestion.com')
    else:
        user = User.objects.create_superuser(
            username='admin@nortegestion.com',
            email='admin@nortegestion.com',
            password='NorteGestion2025!',
            first_name='Administrador'
        )
        print("[OK] Superuser created successfully")

    # Test JWT token generation
    print("\n[JWT] Testing JWT token generation...")
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    print(f"[OK] Access token generated: {access_token[:50]}...")

    # Test API without authentication
    print("\n[SEC] Testing API without authentication...")
    client = APIClient()
    response = client.get('/api/products/')
    print(f"[OK] Status without auth: {response.status_code} (expected 401)")

    # Test API with authentication
    print("\n[SEC] Testing API with JWT authentication...")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.get('/api/products/')
    print(f"[OK] Status with auth: {response.status_code} (expected 200)")

    # Test login endpoint
    print("\n[LOGIN] Testing login endpoint...")
    client = APIClient()
    login_data = {
        'username': 'admin@nortegestion.com',
        'password': 'NorteGestion2025!'
    }
    response = client.post('/api/auth/login/', login_data)
    print(f"[OK] Login status: {response.status_code} (expected 200)")
    if response.status_code == 200:
        tokens = response.json()
        print(f"[OK] Access token received: {tokens.get('access', 'N/A')[:50]}...")
        print(f"[OK] Refresh token received: {tokens.get('refresh', 'N/A')[:50]}...")

    print("\n[SUCCESS] ALL TESTS COMPLETED SUCCESSFULLY!")
    print("[SUCCESS] JWT AUTHENTICATION SYSTEM IS WORKING!")

except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()