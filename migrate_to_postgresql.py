#!/usr/bin/env python
"""
Script para migrar datos de SQLite a PostgreSQL
Ejecutar después de configurar PostgreSQL
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paddle_web.settings')
django.setup()

def migrate_to_postgresql():
    """Migra los datos a PostgreSQL"""
    print("🔄 MIGRANDO A POSTGRESQL...")
    print("=" * 50)
    
    try:
        # 1. Crear migraciones
        print("\n📋 1. Creando migraciones...")
        os.system('python manage.py makemigrations')
        
        # 2. Aplicar migraciones
        print("\n📋 2. Aplicando migraciones...")
        os.system('python manage.py migrate')
        
        # 3. Crear superusuario si no existe
        print("\n📋 3. Verificando superusuario...")
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            print("Creando superusuario admin...")
            User.objects.create_superuser('admin', 'admin@paddlegame.com', 'admin123')
            print("✅ Superusuario creado: admin / admin123")
        else:
            print("✅ Superusuario admin ya existe")
        
        # 4. Generar datos demo
        print("\n📋 4. Generando datos demo...")
        os.system('python generate_basic_data.py')
        
        print("\n🎉 ¡MIGRACIÓN COMPLETADA!")
        print("=" * 50)
        print("✅ Base de datos PostgreSQL configurada")
        print("✅ Datos demo generados")
        print("✅ Superusuario: admin / admin123")
        print("\n🚀 Puedes ejecutar: python manage.py runserver")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        print("\n🔧 Posibles soluciones:")
        print("- Verificar que PostgreSQL esté corriendo")
        print("- Verificar credenciales en .env")
        print("- Verificar que la base de datos 'paddle_challenge_db' exista")

if __name__ == "__main__":
    migrate_to_postgresql()