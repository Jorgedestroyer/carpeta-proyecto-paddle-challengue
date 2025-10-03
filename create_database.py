#!/usr/bin/env python
"""
Script para crear la base de datos PostgreSQL usando el superusuario
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    print("🚀 CREANDO BASE DE DATOS POSTGRESQL...")
    print("=" * 50)
    
    # Pedir la contraseña del superusuario postgres
    postgres_password = input("Introduce la contraseña del usuario 'postgres': ")
    
    try:
        # Conectar como superusuario postgres
        print("🔌 Conectando como superusuario...")
        conn = psycopg2.connect(
            database='postgres',  # BD por defecto
            user='postgres',      # Superusuario
            password=postgres_password,
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa como postgres")
        
        # Crear la base de datos
        print("📋 Creando base de datos 'paddle_challenge_db'...")
        try:
            cursor.execute("CREATE DATABASE paddle_challenge_db;")
            print("✅ Base de datos creada")
        except psycopg2.errors.DuplicateDatabase:
            print("⚠️  Base de datos ya existe")
        
        # Crear el usuario
        print("👤 Creando usuario 'paddle_user'...")
        try:
            cursor.execute("CREATE USER paddle_user WITH PASSWORD 'paddle123';")
            print("✅ Usuario creado")
        except psycopg2.errors.DuplicateObject:
            print("⚠️  Usuario ya existe")
        
        # Dar permisos
        print("🔐 Asignando permisos...")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE paddle_challenge_db TO paddle_user;")
        cursor.execute("ALTER USER paddle_user CREATEDB;")
        print("✅ Permisos asignados")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡BASE DE DATOS CONFIGURADA!")
        print("=" * 50)
        print("✅ Base de datos: paddle_challenge_db")
        print("✅ Usuario: paddle_user")
        print("✅ Contraseña: paddle123")
        print("\n🚀 Siguiente: python migrate_to_postgresql.py")
        
        return True
        
    except psycopg2.OperationalError as e:
        if "authentication failed" in str(e):
            print("❌ Contraseña incorrecta para el usuario 'postgres'")
            print("💡 Intenta de nuevo o resetea la contraseña")
        else:
            print(f"❌ Error de conexión: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_database()