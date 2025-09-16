@echo off
echo Parando todos los stacks...

echo Parando stack estable...
docker compose -p nortegestion-stable -f docker-compose.stable.yml down

echo Parando stack desarrollo...
docker compose -p nortegestion-dev -f docker-compose.dev.yml down

echo.
echo Todos los stacks parados!
pause