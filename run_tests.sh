#!/bin/bash

echo "========================================"
echo "Ejecutando Tests de Selenium"
echo "========================================"
echo ""
echo "1. Verificando servicios..."
docker-compose ps
echo ""
echo "2. Ejecutando tests en una MISMA sesión..."
echo "   Puedes ver la sesión en:"
echo "   - VNC: http://localhost:7900 (password: secret)"
echo "   - Grid: http://localhost:4444"
echo ""
docker-compose exec -T test-runner pytest /tests/test_login.py -v -s
echo ""
echo "========================================"
echo "Tests completados"
echo "========================================"
