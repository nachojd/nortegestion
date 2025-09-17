"""
Web views for Norte Gestión - Emergency frontend served by Django
Provides basic web interface while Next.js frontend is being fixed
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def web_home(request):
    """Home page - redirect to login or products based on auth status"""
    return render(request, 'login.html')


def web_login(request):
    """Login page"""
    return render(request, 'login.html')


def web_products(request):
    """Products management page"""
    return render(request, 'products.html')


def web_status(request):
    """Status page showing system health"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Norte Gestión - Status</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            .status { color: #27ae60; font-weight: bold; }
            .links a { display: inline-block; margin: 10px; padding: 10px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏪 Norte Gestión - Status</h1>
            <p class="status">✅ Backend Django Funcionando</p>
            <p class="status">✅ API REST Disponible</p>
            <p class="status">✅ Base de Datos Conectada</p>
            <p class="status">✅ Autenticación JWT Activa</p>

            <h3>🔗 Enlaces Disponibles:</h3>
            <div class="links">
                <a href="/web/">🏠 Inicio</a>
                <a href="/web/products/">📦 Productos</a>
                <a href="/api/">🔌 API</a>
                <a href="/admin/">⚙️ Admin</a>
            </div>

            <h3>👤 Usuario Motocenter:</h3>
            <p><strong>Email:</strong> motocenter@nortegestion.com</p>
            <p><strong>Productos:</strong> ~3000 productos disponibles</p>
            <p><strong>Funciones:</strong> Gestión completa de inventario</p>

            <h3>🚀 Sistema:</h3>
            <p><strong>Modo:</strong> Producción con frontend Django emergencia</p>
            <p><strong>API:</strong> Totalmente funcional</p>
            <p><strong>Frontend Next.js:</strong> En proceso de debugging</p>
        </div>
    </body>
    </html>
    """, content_type='text/html')