import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paddle_web.settings')
django.setup()

# Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@paddlegame.com', 'admin123')
    print("Superusuario 'admin' creado exitosamente!")
    print("Usuario: admin")
    print("Email: admin@paddlegame.com") 
    print("Contraseña: admin123")
else:
    print("El superusuario 'admin' ya existe.")