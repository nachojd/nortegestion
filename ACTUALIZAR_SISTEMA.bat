@echo off
echo ============================================
echo     ACTUALIZAR MOTOCENTER DESDE GIT
echo ============================================
echo.

echo [1/3] Descargando últimos cambios...
git pull origin main

echo [2/3] Actualizando dependencias...
pip install -r requirements.txt
cd frontend
call npm install
cd ..

echo [3/3] Aplicando cambios de base de datos...
python manage.py migrate

echo.
echo ============================================
echo        ACTUALIZACION COMPLETADA!
echo ============================================
echo Para usar la versión actualizada:
echo 1. Hacer doble clic en: INICIAR_MOTOCENTER.bat
echo.
pause