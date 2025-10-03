#!/usr/bin/env python
"""
Script para probar conexión a PostgreSQL
"""
import os
import sys
from decouple import config

def test_postgresql_connection():
    """Prueba la conexión a PostgreSQL"""
    print("🔍 PROBANDO CONEXIÓN A POSTGRESQL...")
    print("=" * 50)
    
    # Configuración desde .env
    db_config = {
        'ENGINE': 'postgresql',
        'NAME': config('DB_NAME', default='paddle_challenge_db'),
        'USER': config('DB_USER', default='paddle_user'), 
        'PASSWORD': config('DB_PASSWORD', default='paddle123'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
    
    print(f"🗄️  Base de datos: {db_config['NAME']}")
    print(f"👤 Usuario: {db_config['USER']}")
    print(f"🌐 Host: {db_config['HOST']}:{db_config['PORT']}")
    print()
    
    try:
        import psycopg2
        print("✅ psycopg2 está instalado")
        
        # Intentar conexión
        conn = psycopg2.connect(
            database=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT']
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Conexión exitosa a PostgreSQL")
        print(f"📊 Versión: {version[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡PostgreSQL está listo!")
        print("🚀 Puedes ejecutar: python migrate_to_postgresql.py")
        
    except ImportError:
        print("❌ psycopg2 no está instalado")
        print("🔧 Ejecuta: pip install psycopg2-binary")
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Posibles soluciones:")
        print("1. Verificar que PostgreSQL esté corriendo")
        print("2. Verificar credenciales en .env")
        print("3. Crear la base de datos y usuario:")
        print("   CREATE DATABASE paddle_challenge_db;")
        print("   CREATE USER paddle_user WITH PASSWORD 'paddle123';")
        print("   GRANT ALL PRIVILEGES ON DATABASE paddle_challenge_db TO paddle_user;")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_postgresql_connection()