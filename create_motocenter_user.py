#!/usr/bin/env python
"""
Script para crear usuario motocenter en el sistema multi-tenant
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motocenter.settings.development')
django.setup()

from django.contrib.auth.models import User

def create_motocenter_user():
    """Create motocenter user for testing"""
    username = 'motocenter'
    email = 'motocenter@nortegestion.com'
    password = 'motocenter123'

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"✅ Usuario '{username}' ya existe")
        user = User.objects.get(username=username)
    else:
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Moto',
            last_name='Center'
        )
        print(f"✅ Usuario '{username}' creado exitosamente")

    print(f"📧 Email: {user.email}")
    print(f"🔑 Password: {password}")
    print(f"🆔 User ID: {user.id}")

    return user

if __name__ == '__main__':
    try:
        user = create_motocenter_user()
        print("\n🎯 LISTO PARA LOGIN:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Password: motocenter123")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)