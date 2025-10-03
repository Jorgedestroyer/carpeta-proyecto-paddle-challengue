#!/usr/bin/env python
"""Script para verificar problemas de encoding en la base de datos"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paddle_web.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile, Logro, LogroUsuario
from blog.models import Post

def check_encoding():
    print("=== VERIFICANDO CODIFICACIÓN DE DATOS ===\n")
    
    # Verificar usuarios
    print("1. Usuarios:")
    try:
        for user in User.objects.all():
            print(f"   - Usuario: {user.username}")
            print(f"     Nombre: {user.first_name}")
            print(f"     Apellido: {user.last_name}")
            print(f"     Email: {user.email}")
            print()
    except Exception as e:
        print(f"   Error al leer usuarios: {e}")
    
    # Verificar perfiles
    print("2. Perfiles de usuario:")
    try:
        for profile in UserProfile.objects.all():
            print(f"   - {profile.user.username}: {profile.bio}")
    except Exception as e:
        print(f"   Error al leer perfiles: {e}")
    
    # Verificar logros
    print("3. Logros:")
    try:
        for logro in Logro.objects.all():
            print(f"   - {logro.nombre}: {logro.descripcion}")
    except Exception as e:
        print(f"   Error al leer logros: {e}")
    
    # Verificar posts
    print("4. Posts del blog:")
    try:
        for post in Post.objects.all():
            print(f"   - {post.titulo}")
            print(f"     Contenido: {post.contenido[:100]}...")
    except Exception as e:
        print(f"   Error al leer posts: {e}")

if __name__ == "__main__":
    check_encoding()