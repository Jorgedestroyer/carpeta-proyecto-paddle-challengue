#!/usr/bin/env python
"""
Script para verificar PostgreSQL 18 después de la instalación
"""
import os
import sys
from decouple import config

def check_postgresql18():
    """Verifica la instalación de PostgreSQL 18"""
    print("🔍 VERIFICANDO POSTGRESQL 18...")
    print("=" * 50)
    
    try:
        import psycopg2
        print("✅ psycopg2 instalado correctamente")
        
        # Configuración de conexión
        db_config = {
            'database': config('DB_NAME', default='paddle_challenge_db'),
            'user': config('DB_USER', default='paddle_user'),
            'password': config('DB_PASSWORD', default='paddle123'),
            'host': config('DB_HOST', default='localhost'),
            'port': config('DB_PORT', default='5432')
        }
        
        print(f"🗄️  Base de datos: {db_config['database']}")
        print(f"👤 Usuario: {db_config['user']}")
        print(f"🌐 Host: {db_config['host']}:{db_config['port']}")
        print()
        
        # Intentar conexión
        print("🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Verificar versión
        cursor.execute("SELECT version();")
        version_info = cursor.fetchone()[0]
        print(f"✅ Conexión exitosa!")
        print(f"📊 Versión: {version_info}")
        
        # Verificar características de PostgreSQL 18
        if "PostgreSQL 18" in version_info:
            print("🎉 PostgreSQL 18 detectado - ¡Versión más reciente!")
        elif "PostgreSQL 1" in version_info:
            print("✅ PostgreSQL moderno detectado")
        
        # Probar funcionalidades
        cursor.execute("SELECT current_database(), current_user;")
        db_info = cursor.fetchone()
        print(f"🗄️  Base de datos actual: {db_info[0]}")
        print(f"👤 Usuario actual: {db_info[1]}")
        
        # Verificar permisos
        cursor.execute("SELECT has_database_privilege(%s, 'CREATE');", (db_config['database'],))
        can_create = cursor.fetchone()[0]
        if can_create:
            print("✅ Permisos de creación: OK")
        else:
            print("⚠️  Permisos limitados")
        
        cursor.close()
        conn.close()
        
        print("\n🎊 ¡PostgreSQL 18 listo para Django!")
        print("🚀 Siguiente paso: python migrate_to_postgresql.py")
        
        return True
        
    except ImportError:
        print("❌ psycopg2 no instalado")
        print("🔧 Ejecuta: pip install psycopg2-binary")
        return False
        
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 POSIBLES SOLUCIONES:")
        
        if "connection refused" in error_msg.lower():
            print("1. ¿PostgreSQL está corriendo?")
            print("   - Verificar en Services (services.msc)")
            print("   - Buscar 'postgresql-x64-18' o similar")
            print("2. ¿Puerto 5432 está libre?")
            
        elif "authentication failed" in error_msg.lower():
            print("1. Verificar credenciales en .env")
            print("2. ¿Creaste el usuario paddle_user?")
            print("3. Ejecutar comandos en psql:")
            print("   CREATE USER paddle_user WITH PASSWORD 'paddle123';")
            
        elif "database" in error_msg.lower() and "not exist" in error_msg.lower():
            print("1. ¿Creaste la base de datos?")
            print("2. Ejecutar en psql:")
            print("   CREATE DATABASE paddle_challenge_db;")
            
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = check_postgresql18()
    if success:
        print("\n¿Proceder con la migración? (S/N):")
        response = input().strip().lower()
        if response in ['s', 'si', 'y', 'yes']:
            os.system('python migrate_to_postgresql.py')