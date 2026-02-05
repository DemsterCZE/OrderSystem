#!/bin/bash

echo "======================================================"
echo "   AUTOMATED TESTS: KAVARNA U POLE"
echo "======================================================"

if ! docker info > /dev/null 2>&1; then
    echo "❌ [ERROR] Docker neni spusten. Prosim, zapnete Docker a zkuste to znovu."
    exit 1
fi

if [ -z "$(docker ps -q -f name=web)" ]; then
    echo "[INFO] Kontejner 'web' nebezi. Startuji docasne prostredi..."
    docker-compose up -d web
    sleep 5
fi

echo "[RUN] Spoustim Django test suite..."
echo ""

docker-compose exec -T web python manage.py test --verbosity 2
RESULT=$?

echo ""
if [ $RESULT -eq 0 ]; then
    echo "------------------------------------------------------"
    echo "   ✅ [SUCCESS] Vsechny testy probehly uspesne."
    echo "------------------------------------------------------"
else
    echo "------------------------------------------------------"
    echo "   ❌ [FAILED] Nektere testy selhaly!"
    echo "------------------------------------------------------"
    exit $RESULT
fi