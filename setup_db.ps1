Write-Host "CONFIGURACION POSTGRESQL PARA PADDLE CHALLENGE" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Opciones disponibles:" -ForegroundColor Yellow
Write-Host "1. Instalar PostgreSQL tradicional" -ForegroundColor Cyan
Write-Host "2. Usar Docker (recomendado)" -ForegroundColor Cyan  
Write-Host "3. Mantener SQLite" -ForegroundColor Cyan
Write-Host ""

$opcion = Read-Host "Selecciona una opcion (1, 2 o 3)"

if ($opcion -eq "1") {
    Write-Host ""
    Write-Host "INSTALACION TRADICIONAL:" -ForegroundColor Yellow
    Write-Host "1. Descargar de: https://www.postgresql.org/download/windows/" -ForegroundColor White
    Write-Host "2. Instalar con puerto 5432" -ForegroundColor White
    Write-Host "3. Crear base de datos con psql" -ForegroundColor White
    Write-Host "4. Ejecutar: python test_postgresql.py" -ForegroundColor White
    Write-Host "5. Ejecutar: python migrate_to_postgresql.py" -ForegroundColor White
}

if ($opcion -eq "2") {
    Write-Host ""
    Write-Host "INSTALACION CON DOCKER:" -ForegroundColor Yellow
    
    $dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
    if ($dockerInstalled) {
        Write-Host "Docker detectado. Iniciando PostgreSQL..." -ForegroundColor Green
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "PostgreSQL iniciado correctamente" -ForegroundColor Green
            Write-Host "PostgreSQL: localhost:5432" -ForegroundColor White
            Write-Host "pgAdmin: http://localhost:8080" -ForegroundColor White
            Write-Host "  Usuario: admin@paddle.com" -ForegroundColor White
            Write-Host "  Password: admin123" -ForegroundColor White
            
            Write-Host "Esperando 10 segundos..." -ForegroundColor Cyan
            Start-Sleep 10
            
            Write-Host "Probando conexion..." -ForegroundColor Cyan
            python test_postgresql.py
        }
    } else {
        Write-Host "Docker no esta instalado" -ForegroundColor Red
        Write-Host "Descargar de: https://www.docker.com/products/docker-desktop/" -ForegroundColor White
    }
}

if ($opcion -eq "3") {
    Write-Host ""
    Write-Host "MANTENIENDO SQLITE" -ForegroundColor Yellow
    Write-Host "Tu base de datos actual se mantiene" -ForegroundColor White
    Write-Host "Ejecuta: python manage.py runserver" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Presiona Enter para continuar..."
Read-Host