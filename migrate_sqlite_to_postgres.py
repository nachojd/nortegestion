#!/usr/bin/env python
"""
Script para migrar datos de SQLite a PostgreSQL manteniendo los 3000+ productos
"""
import os
import django
import json
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motocenter.settings')
django.setup()

from django.core import serializers
from core.models import Product, Marca, Rubro, Cliente

def export_data():
    """Exporta todos los datos a un archivo JSON"""
    print("🔄 Exportando datos de SQLite...")
    
    # Obtener todos los modelos
    data = []
    
    # Exportar marcas
    marcas = list(Marca.objects.all())
    print(f"📋 Marcas: {len(marcas)}")
    data.extend(serializers.serialize('json', marcas))
    
    # Exportar rubros
    rubros = list(Rubro.objects.all())
    print(f"📋 Rubros: {len(rubros)}")
    data.extend(serializers.serialize('json', rubros))
    
    # Exportar productos
    productos = list(Product.objects.all())
    print(f"📋 Productos: {len(productos)}")
    data.extend(serializers.serialize('json', productos))
    
    # Exportar clientes
    clientes = list(Cliente.objects.all())
    print(f"📋 Clientes: {len(clientes)}")
    data.extend(serializers.serialize('json', clientes))
    
    # Guardar en archivo
    with open('norte_gestion_data.json', 'w', encoding='utf-8') as f:
        f.write('[' + ','.join(data) + ']')
    
    print("✅ Datos exportados a norte_gestion_data.json")
    print(f"📊 Total de registros: {len(marcas) + len(rubros) + len(productos) + len(clientes)}")

def import_data():
    """Importa los datos desde el archivo JSON"""
    print("🔄 Importando datos a PostgreSQL...")
    
    try:
        with open('norte_gestion_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Importando {len(data)} registros...")
        
        # Usar Django's loaddata
        execute_from_command_line(['manage.py', 'loaddata', 'norte_gestion_data.json'])
        print("✅ Datos importados exitosamente")
        
    except FileNotFoundError:
        print("❌ Archivo norte_gestion_data.json no encontrado")
        print("💡 Ejecuta primero: python migrate_sqlite_to_postgres.py export")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'export':
            export_data()
        elif sys.argv[1] == 'import':
            import_data()
        else:
            print("Uso: python migrate_sqlite_to_postgres.py [export|import]")
    else:
        print("Uso: python migrate_sqlite_to_postgres.py [export|import]")
        print("  export - Exporta datos de SQLite")
        print("  import - Importa datos a PostgreSQL")