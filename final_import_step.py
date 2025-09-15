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
    from django.core.management import call_command
    from django.contrib.auth.models import User
    from core.models import Product, Rubro, Marca

    print("[INFO] Running final import step...")
    print("[INFO] This will import 3,448 products to motocenter@nortegestion.com")
    print()

    # Import to current database
    print("=== IMPORTING PRODUCTS ===")
    call_command('import_old_data', '--user-email=motocenter@nortegestion.com')
    print()

    # Verify final results
    print("=== FINAL VERIFICATION ===")
    motocenter_user = User.objects.get(email='motocenter@nortegestion.com')

    productos_count = Product.objects.filter(user=motocenter_user).count()
    rubros_count = Rubro.objects.filter(user=motocenter_user).count()
    marcas_count = Marca.objects.filter(user=motocenter_user).count()

    print(f"[FINAL] Products for motocenter user: {productos_count}")
    print(f"[FINAL] Rubros for motocenter user: {rubros_count}")
    print(f"[FINAL] Marcas for motocenter user: {marcas_count}")

    # Show some examples
    print(f"\n[EXAMPLES] Sample products:")
    for product in Product.objects.filter(user=motocenter_user)[:5]:
        rubro_name = product.rubro.nombre if product.rubro else "Sin rubro"
        marca_name = product.marca.nombre if product.marca else "Sin marca"
        print(f"  - {product.codigo}: {product.nombre}")
        print(f"    Rubro: {rubro_name}, Marca: {marca_name}")
        print(f"    Precio: ${product.precio_venta}")
        print()

    print("[SUCCESS] FINAL IMPORT COMPLETED!")
    print(f"[SUCCESS] motocenter@nortegestion.com now has {productos_count} products available!")

except Exception as e:
    print(f"[ERROR] Error during final import: {e}")
    import traceback
    traceback.print_exc()