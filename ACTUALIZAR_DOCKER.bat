@echo off
echo ============================================
echo   ACTUALIZAR MOTOCENTER (DOCKER)
echo ============================================
echo.

echo [1/4] Parando aplicación actual...
docker-compose down

echo [2/4] Descargando últimos cambios...
git pull origin main

echo [3/4] Reconstruyendo con cambios...
docker-compose build --no-cache

echo [4/4] Iniciando versión actualizada...
docker-compose up -d

echo.
echo ============================================
echo     ✅ ACTUALIZACION COMPLETADA!
echo ============================================
echo.
echo 🌐 Abrir en navegador: http://localhost:3000
echo.

timeout /t 3 /nobreak >nul
start http://localhost:3000

pause