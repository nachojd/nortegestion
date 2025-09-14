@echo off
echo Levantando stack ESTABLE (para netbook)...
echo Frontend: http://localhost:3080 (desde red: http://192.168.1.18:3080)
echo Backend: http://localhost:8080 (desde red: http://192.168.1.18:8080)
echo Nginx: http://localhost:8081 (desde red: http://192.168.1.18:8081)
echo Base de datos: Puerto 5433

docker compose -p nortegestion-stable -f docker-compose.stable-simple.yml up -d

echo.
echo Stack estable levantado!
echo La netbook puede acceder en: http://192.168.1.18:3080
pause