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

    print("[INFO] Starting complete migration setup...")
    print("[INFO] This will:")
    print("  1. Apply migrations to add user fields to Rubro and Marca")
    print("  2. Export data from db_old.sqlite3")
    print("  3. Import data to motocenter@nortegestion.com user")
    print()

    # Step 1: Apply migrations
    print("=== STEP 1: APPLY MIGRATIONS ===")
    try:
        call_command('migrate', verbosity=1)
        print("[SUCCESS] Migrations applied")
    except Exception as e:
        print(f"[INFO] Migration result: {e}")
    print()

    # Step 2: Export from old database
    print("=== STEP 2: EXPORT FROM OLD DATABASE ===")
    call_command('export_old_data')
    print()

    # Step 3: Import to current database
    print("=== STEP 3: IMPORT TO CURRENT DATABASE ===")
    call_command('import_old_data', '--user-email=motocenter@nortegestion.com')
    print()

    # Step 4: Verify migration
    print("=== STEP 4: VERIFY MIGRATION ===")
    motocenter_user = User.objects.get(email='motocenter@nortegestion.com')

    productos_count = Product.objects.filter(user=motocenter_user).count()
    rubros_count = Rubro.objects.filter(user=motocenter_user).count()
    marcas_count = Marca.objects.filter(user=motocenter_user).count()

    print(f"[VERIFY] Products for motocenter user: {productos_count}")
    print(f"[VERIFY] Rubros for motocenter user: {rubros_count}")
    print(f"[VERIFY] Marcas for motocenter user: {marcas_count}")

    # Show some examples
    print(f"\n[EXAMPLES] Sample products:")
    for product in Product.objects.filter(user=motocenter_user)[:5]:
        rubro_name = product.rubro.nombre if product.rubro else "Sin rubro"
        marca_name = product.marca.nombre if product.marca else "Sin marca"
        print(f"  - {product.codigo}: {product.nombre}")
        print(f"    Rubro: {rubro_name}, Marca: {marca_name}")
        print(f"    Precio: ${product.precio_venta}")
        print()

    print("[SUCCESS] COMPLETE MIGRATION SETUP FINISHED!")
    print("[SUCCESS] motocenter@nortegestion.com can now see all historical data!")
    print(f"[SUCCESS] Total migrated: {productos_count} products, {rubros_count} rubros, {marcas_count} marcas")

except Exception as e:
    print(f"[ERROR] Error during migration setup: {e}")
    import traceback
    traceback.print_exc()