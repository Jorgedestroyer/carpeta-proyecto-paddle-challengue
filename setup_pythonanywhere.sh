#!/bin/bash
# Script de configuración para PythonAnywhere

echo "=== Configurando Paddle Challenge en PythonAnywhere ==="

# 1. Instalar dependencias
echo "Instalando dependencias..."
pip3.10 install --user -r requirements.txt

# 2. Configurar variables de entorno
echo "Configurando variables de entorno..."
export PYTHONANYWHERE_DOMAIN=1
export DEBUG=False

# 3. Crear directorio para archivos estáticos
echo "Creando directorios..."
mkdir -p /home/$USER/mysite/static
mkdir -p /home/$USER/mysite/media

# 4. Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python3.10 manage.py collectstatic --noinput

# 5. Ejecutar migraciones
echo "Ejecutando migraciones..."
python3.10 manage.py migrate

# 6. Crear superusuario (opcional)
echo "Para crear un superusuario, ejecuta:"
echo "python3.10 manage.py createsuperuser"

echo "=== Configuración completada ==="
echo ""
echo "Próximos pasos:"
echo "1. Ve a la pestaña 'Web' en tu dashboard de PythonAnywhere"
echo "2. Crea una nueva aplicación web"
echo "3. Selecciona 'Manual configuration' con Python 3.10"
echo "4. En 'Code' section, configura:"
echo "   - Source code: /home/$USER/mysite"
echo "   - Working directory: /home/$USER/mysite"
echo "5. En 'WSGI configuration file', reemplaza el contenido con el archivo pythonanywhere_wsgi.py"
echo "6. En 'Static files', agrega:"
echo "   - URL: /static/"
echo "   - Directory: /home/$USER/mysite/staticfiles"
echo "   - URL: /media/"  
echo "   - Directory: /home/$USER/mysite/media"