import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Product, Rubro, Marca
from django.db import transaction


class Command(BaseCommand):
    help = 'Import data from JSON file to current multi-tenant system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            default='motocenter@nortegestion.com',
            help='Email of the user to assign imported data to (default: motocenter@nortegestion.com)'
        )
        parser.add_argument(
            '--file',
            type=str,
            default='nortegestion_migration_data.json',
            help='JSON file to import from (default: nortegestion_migration_data.json)'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        user_email = options['user_email']

        # Check if JSON file exists
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'[ERROR] {file_path} not found!')
            )
            self.stdout.write(
                self.style.WARNING('Please run "python manage.py export_old_data" first.')
            )
            return

        try:
            # Get target user
            try:
                target_user = User.objects.get(email=user_email)
                self.stdout.write(f'[USER] Target user: {target_user.email} ({target_user.first_name})')
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] User {user_email} not found!')
                )
                return

            # Load JSON data
            self.stdout.write(f'[FILE] Loading data from: {file_path}')
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.stdout.write(f'[DATA] Data summary:')
            self.stdout.write(f'   - Rubros: {len(data.get("rubros", []))}')
            self.stdout.write(f'   - Marcas: {len(data.get("marcas", []))}')
            self.stdout.write(f'   - Productos: {len(data.get("productos", []))}')

            # Import with transaction
            with transaction.atomic():
                # Import rubros
                self.stdout.write('\n[RUBROS] Importing rubros...')
                rubros_map = {}
                for rubro_data in data.get('rubros', []):
                    rubro, created = Rubro.objects.get_or_create(
                        nombre=rubro_data['nombre'],
                        defaults={'user': target_user}
                    )
                    if created:
                        self.stdout.write(f'   [+] Created: {rubro.nombre}')
                    else:
                        self.stdout.write(f'   [=] Exists: {rubro.nombre}')
                    rubros_map[rubro_data['id']] = rubro

                # Import marcas
                self.stdout.write('\n[MARCAS] Importing marcas...')
                marcas_map = {}
                for marca_data in data.get('marcas', []):
                    marca, created = Marca.objects.get_or_create(
                        nombre=marca_data['nombre'],
                        defaults={'user': target_user}
                    )
                    if created:
                        self.stdout.write(f'   [+] Created: {marca.nombre}')
                    else:
                        self.stdout.write(f'   [=] Exists: {marca.nombre}')
                    marcas_map[marca_data['id']] = marca

                # Import productos
                self.stdout.write('\n[PRODUCTOS] Importing productos...')
                productos_created = 0
                productos_skipped = 0

                for producto_data in data.get('productos', []):
                    # Check if product already exists for this user
                    existing = Product.objects.filter(
                        codigo=producto_data['codigo'],
                        user=target_user
                    ).first()

                    if existing:
                        self.stdout.write(f'   [=] Skipped (exists): {producto_data["codigo"]} - {producto_data["nombre"]}')
                        productos_skipped += 1
                        continue

                    # Get rubro and marca
                    rubro = rubros_map.get(producto_data.get('rubro_id')) if producto_data.get('rubro_id') else None
                    marca = marcas_map.get(producto_data.get('marca_id')) if producto_data.get('marca_id') else None

                    # Create product - map old field names to new ones
                    producto = Product.objects.create(
                        user=target_user,
                        codigo=producto_data['codigo'],
                        nombre=producto_data['nombre'],
                        observaciones=producto_data.get('descripcion', ''),
                        precio_costo=producto_data.get('precio_compra', 0),
                        precio_venta=producto_data.get('precio_venta', 0),
                        stock_actual=producto_data.get('stock', 0),
                        rubro=rubro,
                        marca=marca,
                        activo=True
                    )

                    self.stdout.write(f'   [+] Created: {producto.codigo} - {producto.nombre}')
                    productos_created += 1

            # Final summary
            self.stdout.write(
                self.style.SUCCESS(f'\n[SUCCESS] Import completed successfully!')
            )
            self.stdout.write(f'[SUMMARY] Import summary:')
            self.stdout.write(f'   - Rubros processed: {len(data.get("rubros", []))}')
            self.stdout.write(f'   - Marcas processed: {len(data.get("marcas", []))}')
            self.stdout.write(f'   - Productos created: {productos_created}')
            self.stdout.write(f'   - Productos skipped: {productos_skipped}')
            self.stdout.write(f'[USER] All data assigned to: {target_user.email}')

            # Verify final count
            final_count = Product.objects.filter(user=target_user).count()
            self.stdout.write(f'[TOTAL] Total products for {target_user.email}: {final_count}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'[ERROR] Error during import: {str(e)}')
            )
            import traceback
            traceback.print_exc()