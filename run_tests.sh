#!/bin/bash

# Script para ejecutar todas las suites de prueba
echo "🚀 Iniciando ejecución de todas las pruebas..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para ejecutar y mostrar resultado
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -e "\n${YELLOW}▶ Ejecutando: $test_name${NC}"
    if eval $test_command; then
        echo -e "${GREEN}✅ $test_name: PASÓ${NC}"
        return 0
    else
        echo -e "${RED}❌ $test_name: FALLÓ${NC}"
        return 1
    fi
}

# Verificar que los servicios estén corriendo
echo -e "\n${YELLOW}🔍 Verificando servicios...${NC}"

# Backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend funcionando${NC}"
else
    echo -e "${RED}❌ Backend no responde. Iniciando servicios...${NC}"
    docker-compose up -d
    sleep 10
fi

# Frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✅ Frontend funcionando${NC}"
else
    echo -e "${RED}❌ Frontend no responde${NC}"
fi

# Ejecutar pruebas del backend
echo -e "\n${YELLOW}🧪 PRUEBAS BACKEND${NC}"
run_test "Pruebas unitarias Backend" "cd backend && pytest test_main.py -v --cov=app --cov-report=term-missing"
run_test "Pruebas de rendimiento Backend" "cd tests/performance && python -m pytest test_performance.py -v"

# Ejecutar pruebas del frontend
echo -e "\n${YELLOW}🧪 PRUEBAS FRONTEND${NC}"
run_test "Pruebas unitarias Frontend" "cd frontend && npm test -- --coverage --watchAll=false --silent"

# Ejecutar pruebas E2E
echo -e "\n${YELLOW}🧪 PRUEBAS END-TO-END${NC}"
run_test "Pruebas E2E" "cd tests/e2e && python -m pytest test_calculator_e2e.py -v"

# Mostrar resumen
echo -e "\n${YELLOW}📊 RESUMEN EJECUCIÓN${NC}"
echo -e "Todas las pruebas han sido ejecutadas."
echo -e "Ver los reportes individuales para detalles de cobertura."

# Limpiar servicios si se iniciaron en este script
if [ "$1" == "cleanup" ]; then
    echo -e "\n${YELLOW}🧹 Limpiando servicios...${NC}"
    docker-compose down
fi

echo -e "\n🎯 Ejecución completada!"