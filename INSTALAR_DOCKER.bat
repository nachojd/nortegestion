@echo off
echo ============================================
echo   MOTOCENTER - INSTALACION CON DOCKER
echo ============================================
echo.

echo [1/3] Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Docker no está instalado
    echo.
    echo 📥 DESCARGAR DOCKER:
    echo https://www.docker.com/products/docker-desktop/
    echo.
    echo ⚠️  IMPORTANTE: Después de instalar Docker:
    echo    1. Reiniciar la computadora
    echo    2. Ejecutar este archivo de nuevo
    echo.
    pause
    exit /b 1
)

echo ✅ Docker encontrado

echo [2/3] Construyendo aplicación...
docker-compose build

echo [3/3] Iniciando MotoCenter...
docker-compose up -d

echo.
echo ============================================
echo        ✅ MOTOCENTER INICIADO!
echo ============================================
echo.
echo 🌐 Abrir en navegador: http://localhost:3000
echo.
echo 📋 COMANDOS ÚTILES:
echo   • Parar:      docker-compose down
echo   • Reiniciar:  docker-compose restart
echo   • Actualizar: ACTUALIZAR_DOCKER.bat
echo.

timeout /t 5 /nobreak >nul
start http://localhost:3000

pause