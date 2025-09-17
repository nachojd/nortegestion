#!/usr/bin/env python
"""
Script para configurar la contraseña del usuario Motocenter
"""

import os
import sys
import django

# Add the current directory to Python path
sys.path.insert(0, '/opt/nortegestion/nortegestion')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motocenter.settings.production')

try:
    django.setup()
    from django.contrib.auth.models import User

    print("[SETUP] Configurando contraseña para usuario Motocenter...")

    try:
        user = User.objects.get(email='motocenter@nortegestion.com')
        print(f"[FOUND] Usuario encontrado: {user.email}")
        print(f"[INFO] Nombre: {user.first_name}")
        print(f"[INFO] Username: {user.username}")

        # Set the password
        user.set_password('JorgeD12345')
        user.save()

        print("[SUCCESS] ✅ Contraseña actualizada correctamente!")
        print("[INFO] Credenciales de Motocenter:")
        print(f"[INFO]   Usuario: {user.email}")
        print("[INFO]   Contraseña: JorgeD12345")
        print("[INFO]")
        print("[ACCESS] URLs de acceso:")
        print("[ACCESS]   Web App: http://5.161.102.34/")
        print("[ACCESS]   API: http://5.161.102.34/api/")
        print("[ACCESS]   Admin: http://5.161.102.34/admin/")

    except User.DoesNotExist:
        print("[ERROR] ❌ Usuario motocenter@nortegestion.com no encontrado!")
        print("[INFO] Creando usuario...")

        user = User.objects.create_user(
            username='motocenter@nortegestion.com',
            email='motocenter@nortegestion.com',
            password='JorgeD12345',
            first_name='Motocenter',
            is_active=True
        )

        print("[SUCCESS] ✅ Usuario creado correctamente!")
        print("[INFO] Credenciales de Motocenter:")
        print(f"[INFO]   Usuario: {user.email}")
        print("[INFO]   Contraseña: JorgeD12345")

except Exception as e:
    print(f"[ERROR] ❌ Error configurando usuario: {e}")
    sys.exit(1)

print("\n[READY] 🚀 Motocenter puede acceder al sistema ahora!")