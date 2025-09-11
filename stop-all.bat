@echo off
echo Parando todos los stacks...

echo Parando stack estable...
docker compose -p motocenter-stable -f docker-compose.stable.yml down

echo Parando stack desarrollo...
docker compose -p motocenter-dev -f docker-compose.dev.yml down

echo.
echo Todos los stacks parados!
pause