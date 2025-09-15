#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Set environment variables for using SQLite instead of PostgreSQL
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nortegestion.settings')
os.environ['DEBUG'] = 'True'
os.environ['USE_POSTGRES'] = 'False'

# Initialize Django
django.setup()

try:
    from core.models import Product, Cliente, Quote, Rubro, Marca
    from django.contrib.auth.models import User

    print("[INFO] Django initialized successfully!")
    print("[INFO] Checking all data in the system...")

    # Check total data
    print("\n=== TOTALES EN EL SISTEMA ===")
    total_productos = Product.objects.count()
    total_clientes = Cliente.objects.count()
    total_quotes = Quote.objects.count()
    total_users = User.objects.count()

    print(f"Total de productos: {total_productos}")
    print(f"Total de clientes: {total_clientes}")
    print(f"Total de presupuestos: {total_quotes}")
    print(f"Total de usuarios: {total_users}")

    # Check users
    print("\n=== USUARIOS EN EL SISTEMA ===")
    for user in User.objects.all():
        productos_user = Product.objects.filter(user=user).count()
        clientes_user = Cliente.objects.filter(user=user).count()
        quotes_user = Quote.objects.filter(user=user).count()

        print(f"Usuario: {user.username} ({user.email})")
        print(f"  - Nombre: {user.first_name}")
        print(f"  - Productos: {productos_user}")
        print(f"  - Clientes: {clientes_user}")
        print(f"  - Presupuestos: {quotes_user}")
        print()

    # Show some product examples
    print("=== EJEMPLOS DE PRODUCTOS ===")
    for p in Product.objects.all()[:10]:
        user_name = p.user.username if p.user else "SIN USUARIO"
        print(f"- {p.codigo}: {p.nombre} (Usuario: {user_name})")

    print("\n[SUCCESS] REPORTE COMPLETADO!")

except Exception as e:
    print(f"[ERROR] Error durante el reporte: {e}")
    import traceback
    traceback.print_exc()