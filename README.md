<<<<<<< HEAD
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
=======
# 🏍️ NorteGestion - Sistema de Gestión

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
>>>>>>> main

# Crear superusuario
python manage.py createsuperuser

<<<<<<< HEAD
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
=======
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
DB_NAME=nortegestion
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
docker build -t nortegestion .
docker run -p 8000:8000 nortegestion
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
>>>>>>> main

## 🤝 Contribuir

1. Fork el proyecto
<<<<<<< HEAD
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---
**Norte Gestión** - Sistema de gestión empresarial integral para todos los sectores 🌐
=======
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

**NorteGestion** - Sistema profesional para talleres de motocicletas 🏍️
>>>>>>> main
