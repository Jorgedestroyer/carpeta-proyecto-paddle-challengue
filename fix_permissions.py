#!/usr/bin/env python
"""
Script para arreglar permisos de PostgreSQL
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def fix_permissions():
    print("🔧 ARREGLANDO PERMISOS DE POSTGRESQL...")
    print("=" * 50)
    
    # Pedir la contraseña del superusuario postgres
    postgres_password = input("Introduce la contraseña del usuario 'postgres': ")
    
    try:
        # Conectar como superusuario postgres
        print("🔌 Conectando como superusuario...")
        conn = psycopg2.connect(
            database='paddle_challenge_db',  # Conectar directamente a nuestra BD
            user='postgres',      # Superusuario
            password=postgres_password,
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa")
        
        # Dar permisos completos al usuario paddle_user
        print("🔐 Asignando permisos completos...")
        
        # Hacer owner de la base de datos
        cursor.execute("ALTER DATABASE paddle_challenge_db OWNER TO paddle_user;")
        print("✅ paddle_user es owner de la base de datos")
        
        # Permisos en el esquema public
        cursor.execute("GRANT ALL ON SCHEMA public TO paddle_user;")
        cursor.execute("GRANT CREATE ON SCHEMA public TO paddle_user;")
        cursor.execute("ALTER SCHEMA public OWNER TO paddle_user;")
        print("✅ Permisos en esquema public asignados")
        
        # Hacer superusuario (temporalmente)
        cursor.execute("ALTER USER paddle_user WITH SUPERUSER;")
        print("✅ paddle_user es superusuario temporalmente")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡PERMISOS ARREGLADOS!")
        print("=" * 50)
        print("✅ paddle_user tiene permisos completos")
        print("🚀 Siguiente: python manage.py migrate")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_permissions()