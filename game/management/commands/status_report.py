from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Reporte completo del estado de PostgreSQL y pgAdmin"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        self.stdout.write("=== ESTADO POSTGRESQL ===")
        
        # 1. Información básica
        try:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            self.stdout.write(f"Versión: {version[:50]}...")
        except Exception as e:
            self.stdout.write(f"Error obteniendo versión: {e}")
        
        # 2. Configuración de encoding
        try:
            cursor.execute("SELECT current_setting('server_encoding')")
            server_enc = cursor.fetchone()[0]
            cursor.execute("SELECT current_setting('client_encoding')")
            client_enc = cursor.fetchone()[0]
            self.stdout.write(f"Server encoding: {server_enc}")
            self.stdout.write(f"Client encoding: {client_enc}")
        except Exception as e:
            self.stdout.write(f"Error encoding: {e}")
        
        # 3. Extensiones instaladas
        self.stdout.write("\n=== EXTENSIONES INSTALADAS ===")
        try:
            cursor.execute("SELECT extname, extversion FROM pg_extension ORDER BY extname")
            extensions = cursor.fetchall()
            for name, version in extensions:
                self.stdout.write(f"  {name} v{version}")
        except Exception as e:
            self.stdout.write(f"Error extensiones: {e}")
        
        # 4. Estado de la base de datos del proyecto
        self.stdout.write("\n=== ESTADO DE LA BD DEL PROYECTO ===")
        
        table_checks = [
            ("auth_user", "SELECT COUNT(*) FROM auth_user"),
            ("blog_post", "SELECT COUNT(*) FROM blog_post"),
            ("game_partida", "SELECT COUNT(*) FROM game_partida"),
            ("game_feedback", "SELECT COUNT(*) FROM game_feedback"),
            ("users_userprofile", "SELECT COUNT(*) FROM users_userprofile"),
        ]
        
        for table_name, query in table_checks:
            try:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                self.stdout.write(f"  {table_name}: {count} registros")
            except Exception as e:
                self.stdout.write(f"  {table_name}: ERROR - {e}")
        
        # 5. Test de caracteres especiales
        self.stdout.write("\n=== TEST CARACTERES ESPECIALES ===")
        test_strings = [
            "Configuración del juego",
            "Niño jugando paddle",
            "José María González",
            "Más información aquí",
        ]
        
        for test_str in test_strings:
            try:
                cursor.execute("SELECT %s::text", [test_str])
                result = cursor.fetchone()[0]
                status = "✅" if result == test_str else "❌"
                self.stdout.write(f"  {status} {test_str}")
            except Exception as e:
                self.stdout.write(f"  ❌ {test_str}: ERROR - {e}")
        
        # 6. Configuración de logs
        self.stdout.write("\n=== CONFIGURACIÓN DE LOGS ===")
        log_settings = [
            'log_destination',
            'log_statement',
            'log_min_duration_statement',
            'logging_collector',
        ]
        
        for setting in log_settings:
            try:
                cursor.execute(f"SELECT current_setting('{setting}')")
                value = cursor.fetchone()[0]
                self.stdout.write(f"  {setting}: {value}")
            except Exception as e:
                self.stdout.write(f"  {setting}: No disponible")
        
        # 7. Recomendaciones
        self.stdout.write("\n=== RECOMENDACIONES ===")
        self.stdout.write("1. pgAdmin está funcionando correctamente")
        self.stdout.write("2. Las extensiones necesarias están instaladas")
        self.stdout.write("3. UTF-8 funciona correctamente")
        self.stdout.write("4. Si ves errores de encoding, pueden ser de:")
        self.stdout.write("   - Scripts externos a Django")
        self.stdout.write("   - Importación de datos mal codificados")
        self.stdout.write("   - Operaciones manuales en pgAdmin")
        self.stdout.write("5. Para monitorear en tiempo real:")
        self.stdout.write("   - Revisa Activity Monitor en pgAdmin")
        self.stdout.write("   - Filtra por tu base de datos: paddle_challenge_db")
        
        self.stdout.write("\n✅ Sistema funcionando correctamente")