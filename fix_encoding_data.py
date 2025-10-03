#!/usr/bin/env python
"""Script para limpiar y recrear datos básicos con codificación UTF-8 correcta"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paddle_web.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile, Logro, LogroUsuario
from blog.models import Post, Categoria
from django.db import transaction

def clean_and_recreate_data():
    print("=== LIMPIANDO Y RECREANDO DATOS ===\n")
    
    with transaction.atomic():
        # Limpiar datos existentes
        print("1. Limpiando datos existentes...")
        LogroUsuario.objects.all().delete()
        Post.objects.all().delete()
        Categoria.objects.all().delete()
        Logro.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        print("   ✓ Datos limpiados")
        
        # Crear usuarios de prueba
        print("\n2. Creando usuarios de prueba...")
        usuarios_data = [
            {
                'username': 'carlos_pro',
                'first_name': 'Carlos',
                'last_name': 'Martinez',
                'email': 'carlos@paddle.com',
                'password': 'paddle123'
            },
            {
                'username': 'ana_gamer',
                'first_name': 'Ana',
                'last_name': 'Rodriguez', 
                'email': 'ana@paddle.com',
                'password': 'paddle123'
            },
            {
                'username': 'miguel_rookie',
                'first_name': 'Miguel',
                'last_name': 'Lopez',
                'email': 'miguel@paddle.com',
                'password': 'paddle123'
            }
        ]
        
        usuarios = []
        for data in usuarios_data:
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password']
            )
            usuarios.append(user)
            print(f"   ✓ Usuario creado: {user.username}")
        
        # Crear perfiles de usuario
        print("\n3. Creando perfiles de usuario...")
        perfiles_data = [
            {'partidas_jugadas': 25, 'puntuacion_total': 750, 'nivel_juego': 5},
            {'partidas_jugadas': 18, 'puntuacion_total': 620, 'nivel_juego': 4},
            {'partidas_jugadas': 8, 'puntuacion_total': 280, 'nivel_juego': 2}
        ]
        
        for i, user in enumerate(usuarios):
            UserProfile.objects.create(
                user=user,
                partidas_jugadas=perfiles_data[i]['partidas_jugadas'],
                puntuacion_total=perfiles_data[i]['puntuacion_total'],
                nivel_juego=perfiles_data[i]['nivel_juego']
            )
            print(f"   ✓ Perfil creado para: {user.username}")
        
        # Crear logros
        print("\n4. Creando logros...")
        logros_data = [
            {
                'nombre': 'Primer Paso',
                'descripcion': 'Jugaste tu primera partida',
                'icono': '🎾'
            },
            {
                'nombre': 'Novato Dedicado',
                'descripcion': 'Jugaste 5 partidas',
                'icono': '🏅'
            },
            {
                'nombre': 'Jugador Activo',
                'descripcion': 'Jugaste 10 partidas',
                'icono': '⭐'
            },
            {
                'nombre': 'Puntuacion Alta',
                'descripcion': 'Conseguiste mas de 500 puntos',
                'icono': '🏆'
            },
            {
                'nombre': 'Elite',
                'descripcion': 'Conseguiste mas de 1000 puntos',
                'icono': '👑'
            }
        ]
        
        logros = []
        for data in logros_data:
            logro = Logro.objects.create(**data)
            logros.append(logro)
            print(f"   ✓ Logro creado: {logro.nombre}")
        
        # Asignar algunos logros a usuarios
        print("\n5. Asignando logros a usuarios...")
        logros_usuarios = [
            (usuarios[0], [logros[0], logros[1], logros[2], logros[3]]),  # carlos_pro
            (usuarios[1], [logros[0], logros[1], logros[2]]),             # ana_gamer  
            (usuarios[2], [logros[0], logros[1]])                         # miguel_rookie
        ]
        
        for usuario, logros_asignados in logros_usuarios:
            for logro in logros_asignados:
                LogroUsuario.objects.create(usuario=usuario, logro=logro)
                print(f"   ✓ Logro '{logro.nombre}' asignado a {usuario.username}")
        
        # Crear categorías de blog
        print("\n6. Creando categorías de blog...")
        categorias_data = [
            {
                'nombre': 'Noticias', 
                'slug': 'noticias',
                'descripcion': 'Ultimas noticias del mundo del paddle'
            },
            {
                'nombre': 'Tutoriales', 
                'slug': 'tutoriales',
                'descripcion': 'Consejos y tutoriales para mejorar tu juego'
            },
            {
                'nombre': 'Torneos', 
                'slug': 'torneos',
                'descripcion': 'Informacion sobre torneos y competiciones'
            }
        ]
        
        categorias = []
        for data in categorias_data:
            categoria = Categoria.objects.create(**data)
            categorias.append(categoria)
            print(f"   ✓ Categoria creada: {categoria.nombre}")
        
        # Crear posts de blog
        print("\n7. Creando posts de blog...")
        posts_data = [
            {
                'titulo': 'Bienvenido al Paddle Challenge',
                'slug': 'bienvenido-paddle-challenge',
                'contenido': 'Descubre el emocionante mundo del paddle con nuestra plataforma. Aqui podras seguir tus estadisticas, conseguir logros y conectar con otros jugadores.',
                'categoria': categorias[0],
                'autor': usuarios[0],
                'estado': 'publicado'
            },
            {
                'titulo': 'Como mejorar tu saque en paddle',
                'slug': 'como-mejorar-saque-paddle',
                'contenido': 'El saque es fundamental en el paddle. En este tutorial te enseñamos las tecnicas basicas para un saque efectivo que te ayude a ganar mas puntos.',
                'categoria': categorias[1],
                'autor': usuarios[1],
                'estado': 'publicado'
            }
        ]
        
        for data in posts_data:
            post = Post.objects.create(**data)
            print(f"   ✓ Post creado: {post.titulo}")
    
    print("\n✅ DATOS RECREADOS EXITOSAMENTE")
    print("\nEstadísticas finales:")
    print(f"   - Usuarios: {User.objects.count()}")
    print(f"   - Perfiles: {UserProfile.objects.count()}")
    print(f"   - Logros: {Logro.objects.count()}")
    print(f"   - Logros asignados: {LogroUsuario.objects.count()}")
    print(f"   - Categorías: {Categoria.objects.count()}")
    print(f"   - Posts: {Post.objects.count()}")

if __name__ == "__main__":
    clean_and_recreate_data()