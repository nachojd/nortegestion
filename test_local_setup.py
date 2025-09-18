#!/usr/bin/env python
"""
Script para testing local del sistema Norte Gestión
Simula el entorno de producción para verificar que todo funciona
"""

import os
import sys
import subprocess
import time
import signal
import django
from pathlib import Path

# Add the current directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configure Django settings for development
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motocenter.settings.development')

def run_command(cmd, description):
    """Execute a command and show its output"""
    print(f"\n[RUNNING] {description}")
    print(f"Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"[OK] Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def setup_database():
    """Setup SQLite database with migrations and test data"""
    print("\n[SETUP] SETTING UP LOCAL DATABASE")

    # Clean start
    db_path = BASE_DIR / 'db_local_test.sqlite3'
    if db_path.exists():
        db_path.unlink()
        print("[CLEAN] Removed existing test database")

    # Run migrations
    if not run_command("python manage.py migrate", "Creating database schema"):
        return False

    # Create test user (motocenter)
    print("\n[USER] Creating test user (motocenter)")
    django.setup()
    from django.contrib.auth.models import User

    try:
        user = User.objects.create_user(
            username='motocenter@nortegestion.com',
            email='motocenter@nortegestion.com',
            password='test123',
            first_name='Motocenter'
        )
        print(f"[OK] Created user: {user.username}")

        # Create some test products
        from core.models import Product, Rubro, Marca

        # Create test categories
        rubro = Rubro.objects.create(nombre="Repuestos", user=user)
        marca = Marca.objects.create(nombre="Test Marca", user=user)

        # Create test products
        for i in range(5):
            Product.objects.create(
                codigo=f"TEST{i:03d}",
                nombre=f"Producto de Prueba {i+1}",
                precio_costo=100.0 + i*10,
                precio_venta=150.0 + i*15,
                stock_actual=10 + i,
                stock_minimo=5,
                rubro=rubro,
                marca=marca,
                user=user
            )

        print(f"[OK] Created 5 test products for user {user.username}")
        return True

    except Exception as e:
        print(f"[ERROR] Error creating test data: {e}")
        return False

def test_backend():
    """Test backend functionality"""
    print("\n[TEST] TESTING BACKEND")

    if not run_command("python manage.py check", "Django system check"):
        return False

    # Start server in background
    print("[SERVER] Starting Django development server...")
    import threading
    import urllib.request
    import json

    # Start server in a separate thread
    def start_server():
        os.system("python manage.py runserver 127.0.0.1:8000 --noreload --verbosity=0")

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait for server to start
    time.sleep(3)

    try:
        # Test API endpoint
        print("[API] Testing API endpoints...")

        # Test auth endpoint
        auth_data = {
            'username': 'motocenter@nortegestion.com',
            'password': 'test123'
        }

        auth_request = urllib.request.Request(
            'http://127.0.0.1:8000/api/auth/login/',
            data=json.dumps(auth_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        with urllib.request.urlopen(auth_request) as response:
            auth_result = json.loads(response.read().decode('utf-8'))
            token = auth_result['access']
            print("[OK] JWT Authentication successful")

        # Test products endpoint with auth
        products_request = urllib.request.Request(
            'http://127.0.0.1:8000/api/products/',
            headers={'Authorization': f'Bearer {token}'}
        )

        with urllib.request.urlopen(products_request) as response:
            products_data = json.loads(response.read().decode('utf-8'))
            print(f"[OK] Products API successful - {products_data['count']} products found")

        return True

    except Exception as e:
        print(f"[ERROR] Backend test failed: {e}")
        return False

def test_frontend():
    """Test frontend build and basic functionality"""
    print("\n[TEST] TESTING FRONTEND")

    # Clean frontend cache
    frontend_dir = BASE_DIR / 'frontend'

    print("[CLEAN] Cleaning frontend cache...")
    for cache_dir in ['.next', 'node_modules/.cache']:
        cache_path = frontend_dir / cache_dir
        if cache_path.exists():
            run_command(f'rmdir /s /q "{cache_path}"', f"Removing {cache_dir}")

    # Change to frontend directory and test
    os.chdir(frontend_dir)

    if not run_command("npm run build", "Building frontend"):
        return False

    print("[OK] Frontend build successful")
    return True

def main():
    """Main testing function"""
    print("NORTE GESTION - LOCAL TESTING SUITE")
    print("=" * 50)

    # Setup database
    if not setup_database():
        print("[ERROR] Database setup failed")
        return False

    # Test backend
    if not test_backend():
        print("[ERROR] Backend test failed")
        return False

    # Test frontend
    if not test_frontend():
        print("[ERROR] Frontend test failed")
        return False

    print("\n" + "=" * 50)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("[OK] Sistema listo para produccion")
    print("[OK] Backend funciona con autenticacion JWT")
    print("[OK] Frontend compila correctamente")
    print("[OK] Datos de Motocenter accesibles")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[WARNING] Test interrupted by user")
        sys.exit(1)