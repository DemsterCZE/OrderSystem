@echo off
setlocal
title Kavarna U Pole - Deployment

echo ======================================================
echo   KAVARNA U POLE - AUTOMATED DEPLOYMENT
echo ======================================================
echo.

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker neni spusten. Prosim, zapnete Docker Desktop.
    pause
    exit /b
)

echo [1/3] Sestavuji a spoustim kontejnery...
docker-compose up -d --build

echo [2/3] Provadim automatickou migraci databaze...
docker-compose exec web python manage.py migrate --noinput

echo [3/3] Kontrola dostupnosti aplikace...
timeout /t 5 /nobreak >nul

echo.
echo ------------------------------------------------------
echo  Aplikace uspesne nastartovana!
echo  URL: http://localhost:8000
echo  Admin: http://localhost:8000/admin
echo ------------------------------------------------------
echo.

start http://localhost:8000

pause