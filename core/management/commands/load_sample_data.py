from django.core.management.base import BaseCommand
from core.models import Rubro, Marca, Product, Service, Cliente

class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **options):
        # Crear rubros
        rubros = [
            'Cadenas', 'Embragues', 'Juntas', 'Coronas', 'Frenos', 
            'Filtros', 'Aceites', 'Servicios de Mantenimiento'
        ]
        
        for nombre in rubros:
            rubro, created = Rubro.objects.get_or_create(nombre=nombre)
            if created:
                self.stdout.write(f'Rubro creado: {nombre}')

        # Crear marcas
        marcas = [
            'Osaka', 'Daelim', 'Smash', 'Raybar', 'Honda', 
            'Yamaha', 'Suzuki', 'Kawasaki'
        ]
        
        for nombre in marcas:
            marca, created = Marca.objects.get_or_create(nombre=nombre)
            if created:
                self.stdout.write(f'Marca creada: {nombre}')

        # Crear productos de ejemplo
        productos = [
            {
                'codigo': '2294',
                'nombre': 'CADENA OSAKA 520H X 118',
                'rubro': 'Cadenas',
                'marca': 'Osaka',
                'precio_venta': 9735.81,
                'stock_actual': 5
            },
            {
                'codigo': '2313', 
                'nombre': 'JAULA EMBRAGUE DAELIM 14X20X16',
                'rubro': 'Embragues',
                'marca': 'Daelim',
                'precio_venta': 1724.96,
                'stock_actual': 3
            },
            {
                'codigo': '2326',
                'nombre': 'JUNTAS TAPA IZQ.CIL.SMASH CHICA',
                'rubro': 'Juntas', 
                'marca': 'Smash',
                'precio_venta': 58.47,
                'stock_actual': 10
            },
            {
                'codigo': '2343',
                'nombre': 'CORONA KIT RAYBAR C/CAD.SMASH Z16-34',
                'rubro': 'Coronas',
                'marca': 'Raybar', 
                'precio_venta': 5247.98,
                'stock_actual': 2
            }
        ]
        
        for prod_data in productos:
            rubro = Rubro.objects.get(nombre=prod_data['rubro'])
            marca = Marca.objects.get(nombre=prod_data['marca'])
            
            product, created = Product.objects.get_or_create(
                codigo=prod_data['codigo'],
                defaults={
                    'nombre': prod_data['nombre'],
                    'rubro': rubro,
                    'marca': marca,
                    'precio_venta': prod_data['precio_venta'],
                    'stock_actual': prod_data['stock_actual'],
                    'precio_costo': prod_data['precio_venta'] * 0.7  # 30% margen
                }
            )
            if created:
                self.stdout.write(f'Producto creado: {prod_data["codigo"]} - {prod_data["nombre"]}')

        # Crear servicios
        servicios = [
            {
                'codigo': 'SERV001',
                'nombre': 'Cambio de Aceite',
                'descripcion': 'Cambio de aceite del motor y filtro',
                'precio': 5000.00,
                'tiempo_estimado': 30
            },
            {
                'codigo': 'SERV002', 
                'nombre': 'Revisión General',
                'descripcion': 'Revisión completa de la motocicleta',
                'precio': 8500.00,
                'tiempo_estimado': 120
            },
            {
                'codigo': 'SERV003',
                'nombre': 'Cambio de Cadena',
                'descripcion': 'Reemplazo de cadena y tensado',
                'precio': 3500.00,
                'tiempo_estimado': 45
            }
        ]
        
        for serv_data in servicios:
            service, created = Service.objects.get_or_create(
                codigo=serv_data['codigo'],
                defaults=serv_data
            )
            if created:
                self.stdout.write(f'Servicio creado: {serv_data["codigo"]} - {serv_data["nombre"]}')

        # Crear cliente de prueba
        cliente, created = Cliente.objects.get_or_create(
            nombre='Juan Pérez',
            defaults={
                'email': 'juan@example.com',
                'telefono': '+5491123456789',
                'direccion': 'Av. Libertador 1234, CABA'
            }
        )
        if created:
            self.stdout.write('Cliente de prueba creado: Juan Pérez')

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados exitosamente!'))