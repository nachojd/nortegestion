# 🌐 Norte Gestión - Sistema Integral de Gestión

Sistema completo de gestión empresarial multi-sector con Django REST Framework y Next.js.

## ✨ Características

- 📦 **Gestión de Productos**: Inventario completo multi-sector con códigos, precios, stock, marcas y rubros
- 👥 **Clientes**: Base de datos centralizada de clientes con información de contacto
- 📋 **Presupuestos**: Sistema completo de cotizaciones con PDF y WhatsApp
- 🏢 **Multi-Sector**: Adaptable a talleres, ferreterías, repuestos, servicios y más
- 🎨 **Frontend Moderno**: Interfaz web responsiva con Next.js y Tailwind CSS
- 📱 **API REST**: API completa para integraciones externas
- 🔍 **Búsqueda Avanzada**: Filtros y ordenamiento en tiempo real

## 🚀 Desarrollo Local

### Requisitos
- Python 3.11+
- Node.js 18+
- npm o yarn

### Instalación Rápida

1. **Backend Django**:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 192.168.1.18:8000
```

2. **Frontend Next.js**:
```bash
cd frontend
npm install
npm run dev -- --hostname 0.0.0.0
```

3. **O usar el script automático**:
```bash
python start_dev.py
```

### URLs de Acceso
- **Aplicación**: http://192.168.1.18:3002/
- **API Backend**: http://192.168.1.18:8000/api/
- **Admin Django**: http://192.168.1.18:8000/admin/

## 📊 Estructura del Proyecto

```
norte-gestion/
├── 🐍 Backend Django
│   ├── core/           # Modelos principales y API
│   ├── motocenter/     # Configuración Django (legacy name)
│   ├── manage.py       # Django CLI
│   └── db.sqlite3      # Base de datos
├── ⚡ Frontend Next.js
│   ├── src/           # Páginas y componentes
│   ├── public/        # Archivos estáticos
│   └── package.json   # Dependencias Node.js
└── 🛠️ Configuración
    ├── requirements.txt
    ├── start_dev.py    # Script de desarrollo
    └── .env           # Variables de entorno
```

## 📱 API Endpoints

```http
GET /api/products/     # Lista de productos
GET /api/clientes/     # Lista de clientes  
GET /api/quotes/       # Lista de cotizaciones
GET /api/rubros/       # Lista de rubros
GET /api/marcas/       # Lista de marcas
```

## 🏗️ Stack Tecnológico

### Backend
- **Django 4.2** - Framework web
- **Django REST Framework** - API REST
- **SQLite** - Base de datos (desarrollo)
- **PostgreSQL** - Base de datos (producción)

### Frontend  
- **Next.js 15** - Framework React
- **Tailwind CSS** - Estilos
- **TypeScript** - Tipado estático

## 🔧 Scripts Útiles

```bash
# Desarrollo completo
python start_dev.py

# Solo backend
python manage.py runserver 192.168.1.18:8000

# Solo frontend  
cd frontend && npm run dev -- --hostname 0.0.0.0

# Crear superusuario
python manage.py createsuperuser

# Generar migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

## 📝 Base de Datos

El sistema incluye:
- **136 rubros** de productos
- **210 marcas** diferentes  
- **3,448 productos** precargados
- Estructura lista para producción

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---
**Norte Gestión** - Sistema de gestión empresarial integral para todos los sectores 🌐