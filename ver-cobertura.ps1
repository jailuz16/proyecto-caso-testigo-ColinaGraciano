Write-Host "📊 GENERANDO REPORTE DE COBERTURA COMPLETO" -ForegroundColor Green
Write-Host ""

# Backend Coverage
Write-Host "🔧 BACKEND COVERAGE:" -ForegroundColor Yellow
cd backend
pytest --cov=app --cov-report=term
Write-Host ""

# Frontend Coverage  
Write-Host "⚛️  FRONTEND COVERAGE:" -ForegroundColor Yellow
cd ../frontend
npx jest --coverage --watchAll=false
Write-Host ""

Write-Host "✅ Reportes HTML generados en:" -ForegroundColor Green
Write-Host "   Backend:  backend/htmlcov/index.html" -ForegroundColor Cyan
Write-Host "   Frontend: frontend/coverage/lcov-report/index.html" -ForegroundColor Cyan