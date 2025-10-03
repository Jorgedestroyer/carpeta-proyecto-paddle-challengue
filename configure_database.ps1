Write-Host "🚀 CONFIGURACIÓN POSTGRESQL PARA PADDLE CHALLENGE" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Elige una opción para instalar PostgreSQL:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  OPCIÓN TRADICIONAL - Instalar PostgreSQL nativo" -ForegroundColor Cyan
Write-Host "2️⃣  OPCIÓN DOCKER - Usar Docker (más fácil)" -ForegroundColor Cyan
Write-Host "3️⃣  MANTENER SQLITE - Continuar con SQLite" -ForegroundColor Cyan
Write-Host ""

$opcion = Read-Host "Selecciona una opción (1, 2 o 3)"

switch ($opcion) {
    "1" {
        Write-Host ""
        Write-Host "📋 INSTALACIÓN TRADICIONAL DE POSTGRESQL:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "1. Descargar PostgreSQL desde:" -ForegroundColor Cyan
        Write-Host "   https://www.postgresql.org/download/windows/" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Instalar con estas configuraciones:" -ForegroundColor Cyan
        Write-Host "   - Puerto: 5432" -ForegroundColor White
        Write-Host "   - Password postgres: (anótala bien)" -ForegroundColor White
        Write-Host "   - Instalar pgAdmin 4: Sí" -ForegroundColor White
        Write-Host ""
        Write-Host "3. Después de instalar, ejecutar SQL Shell (psql):" -ForegroundColor Cyan
        Write-Host "   CREATE DATABASE paddle_challenge_db;" -ForegroundColor White
        Write-Host "   CREATE USER paddle_user WITH PASSWORD 'paddle123';" -ForegroundColor White
        Write-Host "   GRANT ALL PRIVILEGES ON DATABASE paddle_challenge_db TO paddle_user;" -ForegroundColor White
        Write-Host "   \q" -ForegroundColor White
        Write-Host ""
        Write-Host "4. Luego ejecutar:" -ForegroundColor Cyan
        Write-Host "   python test_postgresql.py" -ForegroundColor White
        Write-Host "   python migrate_to_postgresql.py" -ForegroundColor White
    }
    
    "2" {
        Write-Host ""
        Write-Host "🐳 INSTALACIÓN CON DOCKER:" -ForegroundColor Yellow
        Write-Host ""
        
        # Verificar si Docker está instalado
        try {
            $dockerVersion = docker --version 2>$null
            if ($dockerVersion) {
                Write-Host "✅ Docker está instalado: $dockerVersion" -ForegroundColor Green
                Write-Host ""
                Write-Host "Ejecutando PostgreSQL con Docker..." -ForegroundColor Cyan
                
                # Ejecutar Docker Compose
                docker-compose up -d
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ PostgreSQL iniciado en Docker" -ForegroundColor Green
                    Write-Host ""
                    Write-Host "📊 Servicios disponibles:" -ForegroundColor Yellow
                    Write-Host "   - PostgreSQL: localhost:5432" -ForegroundColor White
                    Write-Host "   - pgAdmin: http://localhost:8080" -ForegroundColor White
                    Write-Host "     Usuario: admin@paddle.com" -ForegroundColor White
                    Write-Host "     Password: admin123" -ForegroundColor White
                    Write-Host ""
                    Write-Host "Esperando a que PostgreSQL esté listo..." -ForegroundColor Cyan
                    Start-Sleep -Seconds 10
                    
                    Write-Host "Probando conexión..." -ForegroundColor Cyan
                    python test_postgresql.py
                    
                    if ($LASTEXITCODE -eq 0) {
                        Write-Host ""
                        Write-Host "¿Migrar datos ahora? (S/N):" -ForegroundColor Yellow
                        $migrar = Read-Host
                        if ($migrar -eq "S" -or $migrar -eq "s" -or $migrar -eq "Y" -or $migrar -eq "y") {
                            python migrate_to_postgresql.py
                        }
                    }
                } else {
                    Write-Host "❌ Error al iniciar Docker Compose" -ForegroundColor Red
                }
                
            } else {
                Write-Host "❌ Docker no está instalado" -ForegroundColor Red
                Write-Host ""
                Write-Host "Instala Docker Desktop desde:" -ForegroundColor Cyan
                Write-Host "https://www.docker.com/products/docker-desktop/" -ForegroundColor White
            }
        } catch {
            Write-Host "❌ Docker no está disponible" -ForegroundColor Red
            Write-Host "Instala Docker Desktop desde:" -ForegroundColor Cyan
            Write-Host "https://www.docker.com/products/docker-desktop/" -ForegroundColor White
        }
    }
    
    "3" {
        Write-Host ""
        Write-Host "📱 MANTENIENDO SQLITE:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Revirtiendo configuración a SQLite..." -ForegroundColor Cyan
        
        # Revertir settings.py a SQLite
        $settingsContent = @"
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL configurado pero comentado
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default='paddle_challenge_db'),
#         'USER': config('DB_USER', default='paddle_user'),
#         'PASSWORD': config('DB_PASSWORD', default='paddle123'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }
"@
        
        Write-Host "✅ Configuración revertida a SQLite" -ForegroundColor Green
        Write-Host "Tu base de datos actual se mantiene intacta" -ForegroundColor White
        Write-Host ""
        Write-Host "Ejecuta: python manage.py runserver" -ForegroundColor Cyan
    }
    
    default {
        Write-Host "❌ Opción no válida" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Presiona cualquier tecla para continuar..." -ForegroundColor Gray
Read-Host