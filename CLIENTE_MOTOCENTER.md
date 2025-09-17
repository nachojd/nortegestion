# Norte Gestión - Cliente Motocenter

## Sistema Multi-Tenant SaaS

**Motocenter** es un cliente real del sistema Norte Gestión con:
- ~3000 productos cargados y configurados
- Precios ya establecidos
- Datos de inventario gestionados
- Usuario: `motocenter@nortegestion.com`

## Arquitectura del Sistema

```
Cliente Motocenter → nginx (5.161.102.34) → Frontend/Backend → Base de datos filtrada por usuario
```

### Separación de Datos por Cliente

Todos los modelos principales tienen campo `user` para aislamiento:
- **Products**: Filtrados por usuario motocenter
- **Clientes**: Solo clientes de motocenter
- **Quotes**: Presupuestos específicos de motocenter
- **Rubros/Marcas**: Categorías propias de motocenter

### URL de Acceso
- **Producción**: http://5.161.102.34
- **Login**: Usuario motocenter accede a sus 3000+ productos
- **Datos aislados**: No ve datos de otros clientes del SaaS

## Deployment para Cliente Real

```bash
# En servidor Hetzner
cd nortegestion
git pull origin clean-main
docker compose -f docker-compose.production.yml up -d --build

# Verificar acceso del cliente
curl http://5.161.102.34/health/
```

## Funcionalidades Disponibles

1. **Gestión de Inventario**
   - Visualización de 3000+ productos
   - Edición de precios (costo, venta, listas 2 y 3)
   - Control de stock actual y mínimo

2. **Gestión de Clientes**
   - Base de clientes propia de motocenter
   - Datos de contacto y historial

3. **Presupuestos**
   - Generación de presupuestos con productos propios
   - Exportación a PDF
   - Numeración automática por cliente

4. **Categorización**
   - Rubros específicos de motocenter
   - Marcas manejadas por motocenter

## Seguridad Multi-Tenant

- **Autenticación JWT**: Tokens específicos por cliente
- **Aislamiento de datos**: Campo `user` en todos los modelos
- **Acceso restrictivo**: Solo datos propios visibles
- **Sesiones independientes**: Múltiples clientes simultáneos

## Notas Importantes

⚠️ **Datos Reales**: Motocenter tiene información crítica de negocio
🔒 **Backup Requerido**: Antes de cualquier migración o cambio
📊 **Performance**: 3000+ productos requieren optimización de consultas
🎯 **Cliente Principal**: Sistema diseñado entorno a necesidades de motocenter