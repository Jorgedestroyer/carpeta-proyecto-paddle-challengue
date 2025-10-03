from django.core.management.base import BaseCommand
from django.db import connection
import psycopg2

class Command(BaseCommand):
    help = "Fuerza configuración UTF-8 en PostgreSQL y valida conexión"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        try:
            # Configuración robusta de encoding
            commands = [
                "SET client_encoding TO 'UTF8'",
                "SET standard_conforming_strings TO on",
                "SET check_function_bodies TO false",
                "SET default_text_search_config = 'pg_catalog.spanish'",
            ]
            
            for cmd in commands:
                try:
                    cursor.execute(cmd)
                    self.stdout.write(f"✅ {cmd}")
                except Exception as e:
                    self.stdout.write(f"⚠️  {cmd} - Error: {str(e)}")
            
            # Verificar configuración actual
            cursor.execute("SHOW client_encoding")
            client_enc = cursor.fetchone()[0]
            
            cursor.execute("SHOW server_encoding") 
            server_enc = cursor.fetchone()[0]
            
            cursor.execute("SHOW lc_ctype")
            lc_ctype = cursor.fetchone()[0]
            
            self.stdout.write(f"\n=== Estado de Codificación ===")
            self.stdout.write(f"Server encoding: {server_enc}")
            self.stdout.write(f"Client encoding: {client_enc}")
            self.stdout.write(f"LC_CTYPE: {lc_ctype}")
            
            # Test con caracteres especiales
            test_data = "Prueba con ñ, á, é, í, ó, ú, ü"
            cursor.execute("SELECT %s::text", [test_data])
            result = cursor.fetchone()[0]
            
            if result == test_data:
                self.stdout.write(f"✅ Test UTF-8: {result}")
            else:
                self.stdout.write(f"❌ Test UTF-8 falló: esperado '{test_data}', obtenido '{result}'")
                
            # Mostrar version PostgreSQL
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            self.stdout.write(f"\nPostgreSQL: {version[:80]}...")
            
        except psycopg2.Error as e:
            self.stdout.write(f"❌ Error PostgreSQL: {str(e)}")
        except Exception as e:
            self.stdout.write(f"❌ Error general: {str(e)}")