@echo off
echo ============================================
echo        🏍️ INICIANDO MOTOCENTER 
echo ============================================
echo.

echo ⚡ Iniciando aplicación...
docker-compose up -d

echo ⏳ Esperando que arranque...
timeout /t 8 /nobreak >nul

echo.
echo ============================================
echo         ✅ MOTOCENTER LISTO!
echo ============================================
echo.
echo 🌐 Abriendo navegador...

start http://localhost:3000

echo.
echo 💡 Para cerrar MotoCenter:
echo    Ejecutar: PARAR_MOTOCENTER.bat
echo.
pause