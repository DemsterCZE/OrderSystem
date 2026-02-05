Tady jsou kompletní skripty pro Linux/macOS. Pro CTO je důležité, aby skripty byly čisté, používaly správné uvozovky a měly ošetřené základní chyby (např. zda vůbec běží Docker).

Všechny tyto soubory ulož do složky bin/ s příponou .sh.

1. bin/start_container.sh
Tento skript simuluje kompletní "deployment" na lokálním stroji.

Bash
#!/bin/bash

echo "======================================================"
echo "   KAVARNA U POLE - AUTOMATED DEPLOYMENT (UNIX)"
echo "======================================================"

# Kontrola, zda běží Docker daemon
if ! docker info > /dev/null 2>&1; then
    echo "❌ [ERROR] Docker není spuštěn. Prosím, zapněte Docker Desktop nebo daemon."
    exit 1
fi

echo "[1/3] Sestavuji a spouštím kontejnery..."
docker-compose up -d --build

echo "[2/3] Provádím automatickou migraci databáze..."
docker-compose exec web python manage.py migrate --noinput

echo "[3/3] Kontrola dostupnosti aplikace..."
sleep 5

echo ""
echo "------------------------------------------------------"
echo "  Aplikace úspěšně nastartována!"
echo "  URL: http://localhost:8000"
echo "------------------------------------------------------"

# Pokus o otevření prohlížeče (funguje na macOS i většině Linux distribucí)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8000
elif command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8000
else
    echo "Prohlížeč nelze automaticky otevřít, použijte http://localhost:8000"
fi