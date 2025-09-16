import sqlite3
import json
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export data from old SQLite database (db_old.sqlite3) to JSON file'

    def handle(self, *args, **options):
        old_db_path = 'db_old.sqlite3'

        # Check if old database exists
        if not os.path.exists(old_db_path):
            self.stdout.write(
                self.style.ERROR(f'ERROR: {old_db_path} not found in project root!')
            )
            self.stdout.write(
                self.style.WARNING('Please place the old SQLite database as db_old.sqlite3 in the project root.')
            )
            return

        try:
            # Conectar directamente a la base SQLite vieja
            self.stdout.write('Connecting to old database: db_old.sqlite3')
            conn = sqlite3.connect(old_db_path)
            conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
            cursor = conn.cursor()

            # Verificar tablas existentes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.stdout.write(f'Found tables: {", ".join(tables)}')

            # Exportar rubros (try different table names)
            self.stdout.write('Exporting rubros...')
            rubros = []
            for table_name in ['core_rubro', 'productos_rubro']:
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rubros = [dict(row) for row in cursor.fetchall()]
                    self.stdout.write(f'Found {len(rubros)} rubros in table {table_name}')
                    break
                except sqlite3.OperationalError:
                    continue
            if not rubros:
                self.stdout.write(self.style.WARNING('No rubro table found, using empty list'))

            # Exportar marcas (try different table names)
            self.stdout.write('Exporting marcas...')
            marcas = []
            for table_name in ['core_marca', 'productos_marca']:
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    marcas = [dict(row) for row in cursor.fetchall()]
                    self.stdout.write(f'Found {len(marcas)} marcas in table {table_name}')
                    break
                except sqlite3.OperationalError:
                    continue
            if not marcas:
                self.stdout.write(self.style.WARNING('No marca table found, using empty list'))

            # Exportar productos (try different table names and approaches)
            self.stdout.write('Exporting productos...')
            productos = []

            # Try with JOIN first
            for product_table, rubro_table, marca_table in [
                ('core_product', 'core_rubro', 'core_marca'),
                ('productos_product', 'productos_rubro', 'productos_marca')
            ]:
                try:
                    cursor.execute(f"""
                        SELECT p.*, r.nombre as rubro_nombre, m.nombre as marca_nombre
                        FROM {product_table} p
                        LEFT JOIN {rubro_table} r ON p.rubro_id = r.id
                        LEFT JOIN {marca_table} m ON p.marca_id = m.id
                        WHERE p.activo = 1
                    """)
                    productos = [dict(row) for row in cursor.fetchall()]
                    self.stdout.write(f'Found {len(productos)} active productos in {product_table} (with JOIN)')
                    break
                except sqlite3.OperationalError:
                    continue

            # If JOIN failed, try simple query
            if not productos:
                for table_name in ['core_product', 'productos_product']:
                    try:
                        cursor.execute(f"SELECT * FROM {table_name} WHERE activo = 1")
                        productos = [dict(row) for row in cursor.fetchall()]
                        self.stdout.write(f'Found {len(productos)} productos in {table_name} (without JOIN)')
                        break
                    except sqlite3.OperationalError:
                        continue

            if not productos:
                self.stdout.write(self.style.WARNING('No product table found, using empty list'))

            conn.close()

            # Guardar JSON
            export_data = {
                'rubros': rubros,
                'marcas': marcas,
                'productos': productos,
                'total_productos': len(productos),
                'total_rubros': len(rubros),
                'total_marcas': len(marcas),
                'export_info': {
                    'source_database': old_db_path,
                    'tables_found': tables
                }
            }

            output_file = 'nortegestion_migration_data.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)

            self.stdout.write(
                self.style.SUCCESS(
                    f'[SUCCESS] Export completed successfully!'
                )
            )
            self.stdout.write(f'[DATA] Exported data:')
            self.stdout.write(f'   - Rubros: {len(rubros)}')
            self.stdout.write(f'   - Marcas: {len(marcas)}')
            self.stdout.write(f'   - Productos: {len(productos)}')
            self.stdout.write(f'[FILE] Data saved to: {output_file}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'[ERROR] Error during export: {str(e)}')
            )
            import traceback
            traceback.print_exc()