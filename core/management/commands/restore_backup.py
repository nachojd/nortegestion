from django.core.management.base import BaseCommand
import json
from datetime import datetime
from productos.models import Rubro, Marca, Product
from clientes.models import Cliente
from cotizaciones.models import Quote, QuoteItem

class Command(BaseCommand):
    help = 'Restore data from backup JSON file'

    def add_arguments(self, parser):
        parser.add_argument('backup_file', type=str, help='Path to backup JSON file')

    def handle(self, *args, **options):
        backup_file = options['backup_file']
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File {backup_file} not found'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Invalid JSON in {backup_file}'))
            return

        self.stdout.write(f'Loading data from {backup_file}...')

        # Crear mapeos para preservar las relaciones
        rubro_map = {}
        marca_map = {}
        cliente_map = {}
        product_map = {}
        
        # Ordenar datos por tipo de modelo
        rubros_data = []
        marcas_data = []
        products_data = []
        clientes_data = []
        quotes_data = []
        quote_items_data = []
        
        for item in data:
            model = item['model']
            if model == 'core.rubro':
                rubros_data.append(item)
            elif model == 'core.marca':
                marcas_data.append(item)
            elif model == 'core.product':
                products_data.append(item)
            elif model == 'core.cliente':
                clientes_data.append(item)
            elif model == 'core.quote':
                quotes_data.append(item)
            elif model == 'core.quoteitem':
                quote_items_data.append(item)

        # 1. Cargar Rubros
        self.stdout.write('Loading Rubros...')
        for item in rubros_data:
            fields = item['fields']
            rubro, created = Rubro.objects.get_or_create(
                id=item['pk'],
                defaults={
                    'nombre': fields['nombre'],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
            )
            rubro_map[item['pk']] = rubro
            if created:
                self.stdout.write(f'  Created Rubro: {fields["nombre"]}')

        # 2. Cargar Marcas
        self.stdout.write('Loading Marcas...')
        for item in marcas_data:
            fields = item['fields']
            marca, created = Marca.objects.get_or_create(
                id=item['pk'],
                defaults={
                    'nombre': fields['nombre'],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
            )
            marca_map[item['pk']] = marca
            if created:
                self.stdout.write(f'  Created Marca: {fields["nombre"]}')

        # 3. Cargar Productos
        self.stdout.write('Loading Products...')
        products_created = 0
        for item in products_data:
            fields = item['fields']
            
            # Verificar que existan las relaciones
            if fields['rubro'] not in rubro_map:
                self.stdout.write(f'  Skipping product {fields["codigo"]}: rubro {fields["rubro"]} not found')
                continue
            if fields['marca'] not in marca_map:
                self.stdout.write(f'  Skipping product {fields["codigo"]}: marca {fields["marca"]} not found')
                continue
                
            product, created = Product.objects.get_or_create(
                id=item['pk'],
                defaults={
                    'codigo': fields['codigo'],
                    'nombre': fields['nombre'],
                    'rubro': rubro_map[fields['rubro']],
                    'marca': marca_map[fields['marca']],
                    'precio_costo': fields.get('precio_costo', 0),
                    'precio_venta': fields['precio_venta'],
                    'precio_lista2': fields.get('precio_lista2', 0),
                    'precio_lista3': fields.get('precio_lista3', 0),
                    'stock_actual': fields.get('stock_actual', 0),
                    'stock_minimo': fields.get('stock_minimo', 0),
                    'observaciones': fields.get('observaciones', ''),
                    'activo': fields.get('activo', True),
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
            )
            product_map[item['pk']] = product
            if created:
                products_created += 1

        self.stdout.write(f'  Created {products_created} products')

        # 4. Cargar Clientes
        self.stdout.write('Loading Clientes...')
        clientes_created = 0
        for item in clientes_data:
            fields = item['fields']
            cliente, created = Cliente.objects.get_or_create(
                id=item['pk'],
                defaults={
                    'nombre': fields['nombre'],
                    'email': fields.get('email', ''),
                    'telefono': fields.get('telefono', ''),
                    'direccion': fields.get('direccion', ''),
                    'cuit': fields.get('cuit', ''),
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
            )
            cliente_map[item['pk']] = cliente
            if created:
                clientes_created += 1

        self.stdout.write(f'  Created {clientes_created} clientes')

        self.stdout.write(self.style.SUCCESS(f'Data restoration completed!'))
        self.stdout.write(f'Summary:')
        self.stdout.write(f'  Rubros: {len(rubro_map)}')
        self.stdout.write(f'  Marcas: {len(marca_map)}') 
        self.stdout.write(f'  Products: {products_created}')
        self.stdout.write(f'  Clientes: {clientes_created}')