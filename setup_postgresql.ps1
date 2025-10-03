# Script para configurar PostgreSQL para Paddle Challenge
# Ejecutar este script paso a paso

Write-Host "🚀 CONFIGURACIÓN DE POSTGRESQL PARA PADDLE CHALLENGE" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

Write-Host ""
Write-Host "📋 PASOS PARA INSTALAR POSTGRESQL:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Descargar PostgreSQL desde: https://www.postgresql.org/download/windows/" -ForegroundColor Cyan
Write-Host "   - Versión recomendada: PostgreSQL 15 o 16" -ForegroundColor White
Write-Host "   - Incluye pgAdmin 4 (interfaz gráfica)" -ForegroundColor White
Write-Host ""

Write-Host "2. Durante la instalación:" -ForegroundColor Cyan
Write-Host "   - Puerto: 5432 (por defecto)" -ForegroundColor White  
Write-Host "   - Password del superusuario (postgres): Anota bien esta contraseña" -ForegroundColor White
Write-Host ""

Write-Host "3. Después de instalar PostgreSQL, crear la base de datos:" -ForegroundColor Cyan
Write-Host "   - Abrir 'SQL Shell (psql)' desde el menú inicio" -ForegroundColor White
Write-Host "   - Presionar Enter para todos los valores por defecto" -ForegroundColor White
Write-Host "   - Introducir la contraseña del superusuario" -ForegroundColor White
Write-Host ""

Write-Host "4. Ejecutar estos comandos en psql:" -ForegroundColor Cyan
Write-Host "   CREATE DATABASE paddle_challenge_db;" -ForegroundColor White
Write-Host "   CREATE USER paddle_user WITH PASSWORD 'paddle123';" -ForegroundColor White
Write-Host "   GRANT ALL PRIVILEGES ON DATABASE paddle_challenge_db TO paddle_user;" -ForegroundColor White
Write-Host "   \q" -ForegroundColor White
Write-Host ""

Write-Host "5. Alternativa con pgAdmin:" -ForegroundColor Cyan
Write-Host "   - Abrir pgAdmin 4" -ForegroundColor White
Write-Host "   - Click derecho en 'Databases' -> Create -> Database" -ForegroundColor White
Write-Host "   - Nombre: paddle_challenge_db" -ForegroundColor White
Write-Host "   - Owner: postgres" -ForegroundColor White
Write-Host ""

Write-Host "6. Después de crear la BD, ejecutar:" -ForegroundColor Cyan
Write-Host "   python manage.py makemigrations" -ForegroundColor White
Write-Host "   python manage.py migrate" -ForegroundColor White
Write-Host "   python generate_basic_data.py" -ForegroundColor White
Write-Host ""

Write-Host "🔧 CONFIGURACIÓN ACTUAL EN .env:" -ForegroundColor Yellow
Write-Host "DB_NAME=paddle_challenge_db" -ForegroundColor White
Write-Host "DB_USER=paddle_user" -ForegroundColor White
Write-Host "DB_PASSWORD=paddle123" -ForegroundColor White
Write-Host "DB_HOST=localhost" -ForegroundColor White
Write-Host "DB_PORT=5432" -ForegroundColor White
Write-Host ""

Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Red
Write-Host "- Asegúrate de que PostgreSQL esté corriendo" -ForegroundColor White
Write-Host "- El servicio se llama 'postgresql-x64-15' o similar" -ForegroundColor White
Write-Host "- Puedes verificarlo en Services (services.msc)" -ForegroundColor White
Write-Host ""

Write-Host "✅ Una vez configurado PostgreSQL, presiona cualquier tecla para continuar..." -ForegroundColor Green
Read-Host