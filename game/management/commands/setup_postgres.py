from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Instala extensiones necesarias para pgAdmin y limpia logs problemáticos"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        # 1. Instalar extensiones útiles para pgAdmin
        extensions = [
            'pg_stat_statements',  # Para estadísticas de consultas
            'pgstattuple',         # Para estadísticas de tuplas
        ]
        
        self.stdout.write("=== INSTALANDO EXTENSIONES ===")
        for ext in extensions:
            try:
                cursor.execute(f'CREATE EXTENSION IF NOT EXISTS {ext}')
                self.stdout.write(f"✅ Extensión {ext} instalada/verificada")
            except Exception as e:
                self.stdout.write(f"⚠️  Extensión {ext}: {str(e)}")
        
        # 2. Verificar extensiones instaladas
        self.stdout.write("\n=== EXTENSIONES DISPONIBLES ===")
        try:
            cursor.execute("SELECT extname, extversion FROM pg_extension ORDER BY extname")
            extensions_installed = cursor.fetchall()
            for name, version in extensions_installed:
                self.stdout.write(f"  {name} (v{version})")
        except Exception as e:
            self.stdout.write(f"Error listando extensiones: {e}")
        
        # 3. Limpiar logs de PostgreSQL que puedan tener errores de encoding
        self.stdout.write("\n=== LIMPIEZA DE LOGS ===")
        try:
            # Rotar log actual si es posible
            cursor.execute("SELECT pg_rotate_logfile()")
            self.stdout.write("✅ Log rotado exitosamente")
        except Exception as e:
            self.stdout.write(f"⚠️  No se pudo rotar log: {e}")
        
        # 4. Configurar logging para evitar problemas futuros
        self.stdout.write("\n=== CONFIGURACIÓN DE LOGGING ===")
        logging_settings = [
            "SET log_statement TO 'none'",           # Reduce logging verboso
            "SET log_min_duration_statement TO 1000", # Solo queries lentas
            "SET log_line_prefix TO '%t [%p]: '",     # Formato simple
        ]
        
        for setting in logging_settings:
            try:
                cursor.execute(setting)
                self.stdout.write(f"✅ {setting}")
            except Exception as e:
                self.stdout.write(f"⚠️  {setting}: {e}")
        
        # 5. Test final
        self.stdout.write("\n=== TEST FINAL ===")
        try:
            # Test con datos que podrían causar el error original
            test_data = "Configuración del juego"
            cursor.execute("SELECT %s::text", [test_data])
            result = cursor.fetchone()[0]
            
            if result == test_data:
                self.stdout.write(f"✅ Test UTF-8 exitoso: {result}")
            else:
                self.stdout.write(f"❌ Test falló: esperado '{test_data}', obtenido '{result}'")
                
        except Exception as e:
            self.stdout.write(f"❌ Error en test: {e}")
        
        self.stdout.write("\n=== INSTRUCCIONES ADICIONALES ===")
        self.stdout.write("1. Reinicia pgAdmin completamente")
        self.stdout.write("2. Si persiste el error, ejecuta en pgAdmin:")
        self.stdout.write("   CREATE EXTENSION IF NOT EXISTS pg_stat_statements;")
        self.stdout.write("3. Para monitorear logs: tail -f /var/log/postgresql/postgresql-18-main.log")
        self.stdout.write("4. El error de encoding puede venir de scripts externos, no de Django")