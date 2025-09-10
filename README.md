# 🏍️ MotoCenter - Sistema de Gestión

Sistema completo de gestión para talleres de motocicletas con Django REST Framework y frontend integrado.

## ✨ Características

- 📦 **Gestión de Productos**: Inventario completo con códigos, precios, stock, marcas y rubros
- 🔧 **Servicios**: Catálogo de servicios con precios y duración estimada
- 👥 **Clientes**: Base de datos de clientes con información de contacto
- 📋 **Presupuestos**: Sistema completo de cotizaciones con PDF y WhatsApp
- 🎨 **Frontend Moderno**: Interfaz web responsiva con Tailwind CSS
- 📱 **API REST**: API completa para integraciones externas
- 🐳 **Docker Ready**: Containerizado y listo para producción

## 🚀 Deployment Rápido

### Railway (Recomendado)
1. Fork este repositorio
2. Conecta tu cuenta de Railway a GitHub
3. Despliega desde el dashboard de Railway
4. Configura las variables de entorno

### Render
1. Fork este repositorio
2. Conecta tu cuenta de Render a GitHub
3. El archivo `render.yaml` configurará todo automáticamente

### DigitalOcean App Platform
1. Fork este repositorio
2. Conecta tu cuenta de DigitalOcean
3. Usa el Dockerfile para el deployment

## 🛠️ Desarrollo Local

### Opción 1: Docker (Recomendado)
```bash
# Desarrollo con SQLite
docker-compose -f docker-compose.dev.yml up --build

# Producción completa con PostgreSQL
docker-compose up --build
```

### Opción 2: Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar desarrollo
cp .env.development .env

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## 📱 URLs de Acceso

- **Frontend**: `http://localhost:8000`
- **Admin Django**: `http://localhost:8000/admin/`
- **API REST**: `http://localhost:8000/api/`
- **Documentación API**: `http://localhost:8000/api/` (DRF Browsable API)

## 🗄️ Estructura de la API

### Endpoints Principales
- `GET/POST /api/products/` - Productos
- `GET/POST /api/services/` - Servicios  
- `GET/POST /api/clientes/` - Clientes
- `GET/POST /api/quotes/` - Presupuestos
- `GET /api/quotes/{id}/pdf/` - Descargar PDF del presupuesto

### Funcionalidades Especiales
- **Búsqueda**: Todos los endpoints soportan búsqueda con `?search=`
- **Filtros**: Productos se pueden filtrar por rubro, marca, etc.
- **Paginación**: 20 items por página por defecto
- **PDF**: Generación automática de PDFs para presupuestos

## ⚙️ Variables de Entorno

### Producción
```env
DEBUG=False
SECRET_KEY=tu-clave-super-secreta-aqui
DB_NAME=motocenter
DB_USER=tu-usuario-db
DB_PASSWORD=tu-password-db
DB_HOST=tu-host-db
DB_PORT=5432
USE_POSTGRES=True
```

### Desarrollo
```env
DEBUG=True
SECRET_KEY=cualquier-clave-para-desarrollo
USE_POSTGRES=False
```

## 🐳 Docker Configurations

### Desarrollo
```bash
docker-compose -f docker-compose.dev.yml up
```

### Producción
```bash
docker-compose up --build
```

### Solo la app (sin nginx)
```bash
docker build -t motocenter .
docker run -p 8000:8000 motocenter
```

## 📊 Stack Tecnológico

- **Backend**: Django 4.2 + Django REST Framework
- **Base de Datos**: PostgreSQL (prod) / SQLite (dev)
- **Frontend**: HTML + Tailwind CSS + Vanilla JS
- **PDF**: ReportLab
- **Deployment**: Docker + Gunicorn + WhiteNoise
- **Proxy**: Nginx (opcional)

## 🔒 Seguridad

- Headers de seguridad configurados para producción
- CORS configurado apropiadamente
- WhiteNoise para archivos estáticos seguros
- Usuario no-root en Docker
- Health checks incluidos

## 📈 Escalabilidad

- Multi-stage Docker build para imágenes optimizadas
- Gunicorn con múltiples workers
- Configuración lista para load balancer
- Static files servidos eficientemente
- Base de datos PostgreSQL para alta concurrencia

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas:
1. Revisa la documentación de la API en `/api/`
2. Verifica los logs con `docker-compose logs`
3. Abre un issue en GitHub con detalles del problema

---

**MotoCenter** - Sistema profesional para talleres de motocicletas 🏍️
