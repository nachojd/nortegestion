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
    print("[INFO] Starting data migration to motocenter user...")

    # PASO 1 - VERIFICAR DATOS ACTUALES
    print("\n=== PASO 1: VERIFICAR DATOS ACTUALES ===")

    productos_sin_usuario = Product.objects.filter(user__isnull=True).count()
    clientes_sin_usuario = Cliente.objects.filter(user__isnull=True).count()
    quotes_sin_usuario = Quote.objects.filter(user__isnull=True).count()

    print(f"Productos sin usuario: {productos_sin_usuario}")
    print(f"Clientes sin usuario: {clientes_sin_usuario}")
    print(f"Presupuestos sin usuario: {quotes_sin_usuario}")

    # Mostrar algunos ejemplos
    print("\nEjemplos de productos sin usuario:")
    for p in Product.objects.filter(user__isnull=True)[:5]:
        print(f"- {p.codigo}: {p.nombre}")

    # PASO 2 - ASIGNAR DATOS AL USUARIO MOTOCENTER
    print("\n=== PASO 2: ASIGNAR DATOS AL USUARIO MOTOCENTER ===")

    # Obtener usuario motocenter
    try:
        viejo = User.objects.get(email='motocenter@nortegestion.com')
        print(f"Usuario encontrado: {viejo.email} (ID: {viejo.id})")
        print(f"Nombre: {viejo.first_name}")
    except User.DoesNotExist:
        print("[ERROR] Usuario motocenter@nortegestion.com no encontrado!")
        sys.exit(1)

    # Migrar productos
    productos_migrados = Product.objects.filter(user__isnull=True).update(user=viejo)
    print(f"Productos migrados: {productos_migrados}")

    # Migrar clientes (si existen)
    clientes_migrados = Cliente.objects.filter(user__isnull=True).update(user=viejo)
    print(f"Clientes migrados: {clientes_migrados}")

    # Migrar presupuestos (si existen)
    quotes_migrados = Quote.objects.filter(user__isnull=True).update(user=viejo)
    print(f"Presupuestos migrados: {quotes_migrados}")

    # PASO 3 - VERIFICAR MIGRACIÓN
    print("\n=== PASO 3: VERIFICAR MIGRACIÓN ===")

    productos_viejo = Product.objects.filter(user=viejo).count()
    print(f"Productos ahora asignados al viejo: {productos_viejo}")

    # Productos sin usuario (debería ser 0)
    sin_usuario = Product.objects.filter(user__isnull=True).count()
    print(f"Productos sin usuario después de migración: {sin_usuario}")

    # Clientes del viejo
    clientes_viejo = Cliente.objects.filter(user=viejo).count()
    print(f"Clientes asignados al viejo: {clientes_viejo}")

    # Quotes del viejo
    quotes_viejo = Quote.objects.filter(user=viejo).count()
    print(f"Presupuestos asignados al viejo: {quotes_viejo}")

    print("\n[SUCCESS] MIGRACIÓN COMPLETADA!")
    print("[SUCCESS] El viejo ahora verá todos sus productos históricos cuando haga login!")

except Exception as e:
    print(f"[ERROR] Error durante la migración: {e}")
    import traceback
    traceback.print_exc()