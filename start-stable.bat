@echo off
echo Levantando stack ESTABLE (para netbook)...
echo Puerto: http://localhost:8081 (nginx)
echo Backend: http://localhost:8080
echo Frontend: http://localhost:3080
echo Base de datos: Puerto 5433

docker compose -p motocenter-stable -f docker-compose.stable.yml up -d

echo.
echo Stack estable levantado!
echo La netbook puede acceder en: http://TU_IP:8081
pause