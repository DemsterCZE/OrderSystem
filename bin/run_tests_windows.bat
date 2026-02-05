@echo off
setlocal
title Kavarna U Pole - Unit Testing

echo ======================================================
echo    AUTOMATED TESTS: KAVARNA U POLE
echo ======================================================
echo.

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker neni spusten nebo neni v PATH.
    echo Prosim, spustte Docker Desktop a zkuste to znovu.
    echo.
    pause
    exit /b
)

docker-compose ps | findstr "Up" >nul
if %errorlevel% neq 0 (
    echo [INFO] Kontejnery nebezi. Startuji docasne prostredi pro testy...
    docker-compose up -d web
)

echo [RUN] Spoustim Django test suit...
echo.

docker-compose exec -T web python manage.py test --verbosity 2

if %errorlevel% equ 0 (
    echo.
    echo ------------------------------------------------------
    echo    [SUCCESS] Vsechny testy probehly uspesne.
    echo ------------------------------------------------------
) else (
    echo.
    echo ------------------------------------------------------
    echo    [FAILED] Nektere testy selhaly! Proverte logy vyse.
    echo ------------------------------------------------------
)

echo.
pause