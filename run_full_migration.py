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

    print("[INFO] Starting complete migration process...")
    print("[INFO] This will migrate data from db_old.sqlite3 to the current system")
    print("[INFO] All data will be assigned to motocenter@nortegestion.com user")
    print()

    # Step 1: Export from old database
    print("=== STEP 1: EXPORT FROM OLD DATABASE ===")
    call_command('export_old_data')
    print()

    # Step 2: Import to current database
    print("=== STEP 2: IMPORT TO CURRENT DATABASE ===")
    call_command('import_old_data', '--user-email=motocenter@nortegestion.com')
    print()

    # Step 3: Verify migration
    print("=== STEP 3: VERIFY MIGRATION ===")
    from core.models import Product, Rubro, Marca
    from django.contrib.auth.models import User

    motocenter_user = User.objects.get(email='motocenter@nortegestion.com')

    productos_count = Product.objects.filter(user=motocenter_user).count()
    rubros_count = Rubro.objects.filter(user=motocenter_user).count()
    marcas_count = Marca.objects.filter(user=motocenter_user).count()

    print(f"[VERIFY] Products for motocenter user: {productos_count}")
    print(f"[VERIFY] Rubros for motocenter user: {rubros_count}")
    print(f"[VERIFY] Marcas for motocenter user: {marcas_count}")

    # Show some examples
    print(f"\n[EXAMPLES] Sample products:")
    for product in Product.objects.filter(user=motocenter_user)[:10]:
        print(f"  - {product.codigo}: {product.nombre} (${product.precio_venta})")

    print("\n[SUCCESS] MIGRATION COMPLETED SUCCESSFULLY!")
    print("[SUCCESS] motocenter@nortegestion.com can now see all historical data!")

except Exception as e:
    print(f"[ERROR] Error during migration: {e}")
    import traceback
    traceback.print_exc()