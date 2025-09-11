# Motocenter - Configuración Docker

## Setup de Dos Stacks Independientes

Este proyecto está configurado para correr dos entornos Docker completamente independientes:

### 🔹 Stack ESTABLE (Para la Netbook)
- **Puerto Principal**: http://localhost:8081 (nginx)
- **Backend**: http://localhost:8080
- **Frontend**: http://localhost:3080
- **Base de Datos**: Puerto 5433
- **Volúmenes**: postgres_data_stable, static_volume_stable

### 🔹 Stack DESARROLLO (Para desarrollo local)
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Base de Datos**: Puerto 5432
- **Volúmenes**: postgres_data_dev
- **Hot-reload activado**

## Comandos Rápidos

### Levantar Stack Estable (Netbook)
```bash
# Opción 1: Script
start-stable.bat

# Opción 2: Manual
docker compose -p motocenter-stable -f docker-compose.stable.yml up -d
```

### Levantar Stack Desarrollo
```bash
# Opción 1: Script
start-dev.bat

# Opción 2: Manual
docker compose -p motocenter-dev -f docker-compose.dev.yml up -d
```

### Parar Todos los Stacks
```bash
# Script para parar todo
stop-all.bat

# Manual
docker compose -p motocenter-stable -f docker-compose.stable.yml down
docker compose -p motocenter-dev -f docker-compose.dev.yml down
```

## Acceso desde la Netbook

Para acceder desde la netbook, usar la IP de la PC principal:
```
http://IP_DE_TU_PC:8081
```

## Bases de Datos

- **Estable**: motocenter_stable (Puerto 5433)
- **Desarrollo**: motocenter_dev (Puerto 5432)

Cada stack tiene su propia base de datos completamente independiente.

## Archivos Importantes

- `docker-compose.stable.yml` - Stack estable para netbook
- `docker-compose.dev.yml` - Stack desarrollo con hot-reload
- `.env.stable` - Variables de entorno para estable
- `nginx.stable.conf` - Configuración nginx para estable
- `start-stable.bat` - Script para levantar estable
- `start-dev.bat` - Script para levantar desarrollo
- `stop-all.bat` - Script para parar todo

## Flujo de Trabajo

1. **Desarrollo**: Trabajar en el stack dev (puerto 3000/8000)
2. **Testing**: Probar cambios en dev
3. **Cuando esté listo**: Rebuild del stack estable
4. **Netbook**: Siempre apunta al stack estable (puerto 8081)

De esta forma la netbook nunca se ve afectada por cambios en desarrollo.