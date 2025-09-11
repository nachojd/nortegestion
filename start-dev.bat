@echo off
echo Levantando stack DESARROLLO...
echo Frontend: http://localhost:3001 (tambien desde red: http://192.168.1.18:3001)
echo Backend: http://localhost:8001 (tambien desde red: http://192.168.1.18:8001)
echo Base de datos: Puerto 5432

docker compose -p motocenter-dev -f docker-compose.dev.yml up -d

echo.
echo Stack desarrollo levantado!
echo Hot-reload activado para desarrollo
pause