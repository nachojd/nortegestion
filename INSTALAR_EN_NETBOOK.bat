@echo off
echo ============================================
echo    INSTALACION MOTOCENTER PARA NETBOOK
echo ============================================
echo.

echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [2/4] Instalando dependencias Python...
pip install -r requirements.txt

echo [3/4] Configurando base de datos...
python manage.py migrate

echo [4/4] Creando acceso directo de inicio...
echo @echo off > INICIAR_MOTOCENTER.bat
echo echo ============================================ >> INICIAR_MOTOCENTER.bat
echo echo          MOTOCENTER - INICIANDO... >> INICIAR_MOTOCENTER.bat
echo echo ============================================ >> INICIAR_MOTOCENTER.bat
echo echo. >> INICIAR_MOTOCENTER.bat
echo echo [1/2] Iniciando servidor backend... >> INICIAR_MOTOCENTER.bat
echo start "Backend Django" cmd /k "cd /d %~dp0 && python manage.py runserver 127.0.0.1:8000" >> INICIAR_MOTOCENTER.bat
echo timeout /t 3 /nobreak >nul >> INICIAR_MOTOCENTER.bat
echo echo [2/2] Iniciando frontend... >> INICIAR_MOTOCENTER.bat
echo cd frontend >> INICIAR_MOTOCENTER.bat
echo start "Frontend Next.js" cmd /k "npm run dev" >> INICIAR_MOTOCENTER.bat
echo timeout /t 5 /nobreak >nul >> INICIAR_MOTOCENTER.bat
echo echo. >> INICIAR_MOTOCENTER.bat
echo echo ============================================ >> INICIAR_MOTOCENTER.bat
echo echo   MOTOCENTER INICIADO CORRECTAMENTE! >> INICIAR_MOTOCENTER.bat
echo echo   Abrir navegador en: http://localhost:3000 >> INICIAR_MOTOCENTER.bat
echo echo ============================================ >> INICIAR_MOTOCENTER.bat
echo start http://localhost:3000 >> INICIAR_MOTOCENTER.bat

echo.
echo ============================================
echo        INSTALACION COMPLETADA!
echo ============================================
echo.
echo Para usar MotoCenter:
echo 1. Hacer doble clic en: INICIAR_MOTOCENTER.bat
echo 2. Esperar que abra el navegador
echo 3. Listo para usar!
echo.
pause