from django.core.management.base import BaseCommand
from django.db import connection
import re

class Command(BaseCommand):
    help = "Detecta y limpia caracteres no válidos UTF-8 en la base de datos"

    def add_arguments(self, parser):
        parser.add_argument('--fix', action='store_true', help='Aplicar correcciones automáticamente')
        parser.add_argument('--table', type=str, help='Tabla específica a revisar')

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        # Tablas con contenido de texto a revisar
        text_tables = [
            ('auth_user', ['username', 'first_name', 'last_name', 'email']),
            ('blog_post', ['titulo', 'contenido', 'slug']),
            ('blog_categoria', ['nombre', 'descripcion']),
            ('blog_comentario', ['contenido']),
            ('users_userprofile', ['pais', 'sobre_mi']),
            ('game_feedback', ['nombre', 'email', 'mensaje']),
        ]
        
        if options['table']:
            # Filtrar solo la tabla especificada
            text_tables = [(t, cols) for t, cols in text_tables if t == options['table']]
        
        problematic_rows = []
        
        for table, columns in text_tables:
            self.stdout.write(f"\n=== Revisando tabla: {table} ===")
            
            try:
                # Verificar que la tabla existe
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                total_rows = cursor.fetchone()[0]
                self.stdout.write(f"Total filas: {total_rows}")
                
                if total_rows == 0:
                    continue
                
                # Revisar cada columna de texto
                for column in columns:
                    try:
                        # Buscar caracteres problemáticos
                        # Buscar caracteres no ASCII de forma más segura
                        cursor.execute(f"""
                            SELECT id, {column} 
                            FROM {table} 
                            WHERE {column} IS NOT NULL 
                            AND LENGTH({column}) != OCTET_LENGTH({column})
                            LIMIT 20
                        """)
                        
                        rows = cursor.fetchall()
                        if rows:
                            self.stdout.write(f"  Columna {column}: {len(rows)} filas con caracteres especiales")
                            for row_id, content in rows:
                                if content:
                                    # Detectar bytes problemáticos
                                    try:
                                        content.encode('utf-8')
                                    except UnicodeEncodeError as e:
                                        problematic_rows.append((table, column, row_id, str(e)))
                                        self.stdout.write(f"    ID {row_id}: ERROR - {str(e)}")
                                    
                                    # Mostrar caracteres no ASCII para revisión manual
                                    non_ascii = ''.join([c for c in content if ord(c) > 127])
                                    if non_ascii:
                                        self.stdout.write(f"    ID {row_id}: chars especiales '{non_ascii[:20]}...'")
                        
                    except Exception as e:
                        self.stdout.write(f"  Error en columna {column}: {str(e)}")
                        
            except Exception as e:
                self.stdout.write(f"Error en tabla {table}: {str(e)}")
        
        # Aplicar correcciones si se solicita
        if options['fix'] and problematic_rows:
            self.stdout.write(f"\n=== Aplicando correcciones a {len(problematic_rows)} problemas ===")
            
            for table, column, row_id, error in problematic_rows:
                try:
                    # Obtener contenido actual
                    cursor.execute(f"SELECT {column} FROM {table} WHERE id = %s", [row_id])
                    current_content = cursor.fetchone()[0]
                    
                    if current_content:
                        # Limpiar caracteres problemáticos
                        clean_content = current_content.encode('utf-8', errors='ignore').decode('utf-8')
                        clean_content = re.sub(r'[^\x00-\x7F]+', '', clean_content)  # Remover no-ASCII
                        
                        # Actualizar
                        cursor.execute(f"UPDATE {table} SET {column} = %s WHERE id = %s", 
                                     [clean_content, row_id])
                        self.stdout.write(f"  Corregido {table}.{column} ID {row_id}")
                        
                except Exception as e:
                    self.stdout.write(f"  Error corrigiendo {table}.{column} ID {row_id}: {str(e)}")
        
        if problematic_rows:
            self.stdout.write(f"\n=== Resumen ===")
            self.stdout.write(f"Problemas encontrados: {len(problematic_rows)}")
            if not options['fix']:
                self.stdout.write("Usa --fix para aplicar correcciones automáticas")
        else:
            self.stdout.write(f"\n✅ No se encontraron problemas de codificación UTF-8")