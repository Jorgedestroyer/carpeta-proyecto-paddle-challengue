from django.core.management.base import BaseCommand
from django.db import connection
import logging

class Command(BaseCommand):
    help = "Analiza y corrige problemas específicos de encoding UTF-8"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        # 1. Verificar configuración PostgreSQL completa
        self.stdout.write("=== CONFIGURACIÓN POSTGRESQL ===")
        
        config_queries = {
            'server_encoding': "SELECT current_setting('server_encoding')",
            'client_encoding': "SELECT current_setting('client_encoding')", 
            'lc_collate': "SELECT current_setting('lc_collate')",
            'lc_ctype': "SELECT current_setting('lc_ctype')",
            'timezone': "SELECT current_setting('timezone')",
        }
        
        for name, query in config_queries.items():
            try:
                cursor.execute(query)
                value = cursor.fetchone()[0]
                self.stdout.write(f"{name}: {value}")
            except Exception as e:
                self.stdout.write(f"{name}: ERROR - {e}")
        
        # 2. Buscar datos problemáticos específicamente
        self.stdout.write("\n=== BUSCAR DATOS PROBLEMÁTICOS ===")
        
        # Buscar el byte sequence específico mencionado: 0xf3 0x6e 0x20 0x70
        search_queries = [
            # Buscar en blog_post
            ("blog_post", "contenido", "WHERE contenido LIKE '%ó%' OR contenido LIKE '%ñ%'"),
            ("blog_post", "titulo", "WHERE titulo LIKE '%ó%' OR titulo LIKE '%ñ%'"),
            # Buscar en auth_user
            ("auth_user", "first_name", "WHERE first_name LIKE '%ó%' OR first_name LIKE '%ñ%'"),
            ("auth_user", "last_name", "WHERE last_name LIKE '%ó%' OR last_name LIKE '%ñ%'"),
            # Buscar en users_userprofile
            ("users_userprofile", "sobre_mi", "WHERE sobre_mi LIKE '%ó%' OR sobre_mi LIKE '%ñ%'"),
            ("users_userprofile", "pais", "WHERE pais LIKE '%ó%' OR pais LIKE '%ñ%'"),
        ]
        
        problematic_data = []
        
        for table, column, where_clause in search_queries:
            try:
                query = f"SELECT id, {column} FROM {table} {where_clause} LIMIT 5"
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if rows:
                    self.stdout.write(f"\n{table}.{column}:")
                    for row_id, content in rows:
                        if content:
                            # Verificar si hay bytes problemáticos
                            content_bytes = content.encode('utf-8', errors='replace')
                            if b'\xf3' in content_bytes:
                                problematic_data.append((table, column, row_id, content))
                                self.stdout.write(f"  ❌ ID {row_id}: CONTIENE BYTES PROBLEMÁTICOS")
                                self.stdout.write(f"     Contenido: {content[:50]}...")
                            else:
                                self.stdout.write(f"  ✅ ID {row_id}: OK - {content[:30]}...")
            except Exception as e:
                self.stdout.write(f"Error en {table}.{column}: {e}")
        
        # 3. Recrear conexión con configuración específica
        self.stdout.write("\n=== RECONFIGURAR CONEXIÓN ===")
        try:
            # Forzar configuración de sesión
            session_config = [
                "SET client_encoding TO 'UTF8'",
                "SET standard_conforming_strings TO on",
                "SET escape_string_warning TO off",
                "SET row_security TO off",
            ]
            
            for cmd in session_config:
                cursor.execute(cmd)
                self.stdout.write(f"✅ {cmd}")
                
        except Exception as e:
            self.stdout.write(f"❌ Error configurando sesión: {e}")
        
        # 4. Test de inserción con caracteres especiales
        self.stdout.write("\n=== TEST DE INSERCIÓN ===")
        try:
            test_table = "CREATE TEMP TABLE test_utf8 (id SERIAL, texto TEXT)"
            cursor.execute(test_table)
            
            test_strings = [
                "Normal text",
                "Texto con ñ y acentos: ácido",
                "Español: niño, corazón, mañana",
                "Símbolos: © ® ™ € £ ¥",
            ]
            
            for test_str in test_strings:
                try:
                    cursor.execute("INSERT INTO test_utf8 (texto) VALUES (%s)", [test_str])
                    self.stdout.write(f"✅ Insertado: {test_str}")
                except Exception as e:
                    self.stdout.write(f"❌ Error insertando '{test_str}': {e}")
                    
            cursor.execute("DROP TABLE test_utf8")
            
        except Exception as e:
            self.stdout.write(f"❌ Error en test de inserción: {e}")
        
        # 5. Resumen
        if problematic_data:
            self.stdout.write(f"\n=== DATOS PROBLEMÁTICOS ENCONTRADOS: {len(problematic_data)} ===")
            for table, column, row_id, content in problematic_data:
                self.stdout.write(f"{table}.{column} ID {row_id}")
        else:
            self.stdout.write("\n✅ No se encontraron datos con bytes problemáticos específicos")