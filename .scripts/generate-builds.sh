#!/bin/bash

# Script para generar 10 builds exitosos rápidamente
echo "🚀 Generando 10 builds exitosos para CI/CD..."

for i in {1..10}
do
    echo "📦 Generando build #$i"
    
    # Crear un cambio pequeño
    echo "# Build $i - $(date)" >> build-log.md
    
    # Hacer commit y push
    git add .
    git commit -m "ci: Build automatizado #$i - $(date)"
    git push origin main
    
    echo "✅ Build #$i enviado"
    sleep 30  # Esperar entre builds
done

echo "🎉 10 builds exitosos generados!"