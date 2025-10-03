#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paddle_web.settings')
    django.setup()

    from django.contrib.auth.models import User
    from users.models import UserProfile, Logro, LogroUsuario, Partida
    from blog.models import Post

    print("🚀 Generando datos de prueba profesionales...")

    # 1. Crear logros si no existen
    logros_data = [
        ("Primer Paso", "Jugaste tu primera partida", "fas fa-play"),
        ("Novato Dedicado", "Jugaste 5 partidas", "fas fa-star"),
        ("Jugador Activo", "Jugaste 10 partidas", "fas fa-fire"),
        ("Veterano", "Jugaste 25 partidas", "fas fa-medal"),
        ("Maestro del Paddle", "Jugaste 50 partidas", "fas fa-crown"),
        ("Puntuación Alta", "Conseguiste más de 500 puntos", "fas fa-chart-line"),
        ("Élite", "Conseguiste más de 1000 puntos", "fas fa-gem"),
        ("Leyenda", "Conseguiste más de 2000 puntos", "fas fa-trophy"),
        ("Bloguero", "Escribiste tu primer post", "fas fa-pen"),
        ("Influencer", "Escribiste 5 posts", "fas fa-microphone"),
    ]

    for nombre, descripcion, icono in logros_data:
        logro, created = Logro.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion, 'icono': icono}
        )
        if created:
            print(f"✅ Creado logro: {nombre}")

    # 2. Crear usuarios de prueba
    usuarios_demo = [
        ("carlos_pro", "Carlos", "Martinez", "carlos@paddle.com", 5, "España", "¡Hola! Soy un jugador profesional de paddle. Me encanta competir y ayudar a otros jugadores a mejorar."),
        ("ana_gamer", "Ana", "Rodriguez", "ana@paddle.com", 4, "Argentina", "Gamer apasionada y jugadora de paddle los fines de semana. ¡Siempre lista para una partida!"),
        ("miguel_rookie", "Miguel", "Lopez", "miguel@paddle.com", 3, "México", "Nuevo en el paddle pero con muchas ganas de aprender. ¡Busco compañeros para jugar!"),
        ("sofia_champ", "Sofia", "Torres", "sofia@paddle.com", 5, "Colombia", "Campeona regional de paddle. Me gusta compartir técnicas y estrategias con la comunidad."),
        ("pedro_casual", "Pedro", "Sanchez", "pedro@paddle.com", 2, "Chile", "Juego paddle por diversión y para mantenerme en forma. ¡Gran deporte!"),
    ]

    for username, first_name, last_name, email, nivel, pais, bio in usuarios_demo:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
        )
        if created:
            user.set_password('paddle123')
            user.save()
            print(f"✅ Creado usuario: {username}")

        # Crear perfil
        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'nivel_juego': nivel,
                'pais': pais,
                'sobre_mi': bio,
                'puntuacion_total': random.randint(100, 2500),
                'partidas_jugadas': random.randint(5, 60),
            }
        )

        if profile_created:
            print(f"  → Perfil creado para {username}")

    # 3. Asignar logros realistas
    usuarios = User.objects.filter(username__in=[u[0] for u in usuarios_demo])
    logros = Logro.objects.all()

    for user in usuarios:
        profile = user.userprofile
        
        # Logros basados en estadísticas reales
        if profile.partidas_jugadas >= 1:
            LogroUsuario.objects.get_or_create(
                usuario=user, 
                logro=Logro.objects.get(nombre="Primer Paso"),
                defaults={'fecha_obtenido': datetime.now() - timedelta(days=random.randint(1, 30))}
            )
        
        if profile.partidas_jugadas >= 5:
            LogroUsuario.objects.get_or_create(
                usuario=user, 
                logro=Logro.objects.get(nombre="Novato Dedicado"),
                defaults={'fecha_obtenido': datetime.now() - timedelta(days=random.randint(1, 20))}
            )
        
        if profile.partidas_jugadas >= 10:
            LogroUsuario.objects.get_or_create(
                usuario=user, 
                logro=Logro.objects.get(nombre="Jugador Activo"),
                defaults={'fecha_obtenido': datetime.now() - timedelta(days=random.randint(1, 15))}
            )

        if profile.puntuacion_total >= 500:
            LogroUsuario.objects.get_or_create(
                usuario=user, 
                logro=Logro.objects.get(nombre="Puntuación Alta"),
                defaults={'fecha_obtenido': datetime.now() - timedelta(days=random.randint(1, 10))}
            )

    # 4. Crear partidas de ejemplo
    usuarios = User.objects.all()
    for user in usuarios:
        num_partidas = random.randint(3, 15)
        for i in range(num_partidas):
            Partida.objects.get_or_create(
                usuario=user,
                puntos=random.randint(50, 300),
                defaults={
                    'resultado': random.choice(['victoria', 'derrota']),
                    'duracion': random.randint(1800, 5400),  # 30-90 minutos en segundos
                    'fecha': datetime.now() - timedelta(days=random.randint(1, 60))
                }
            )

    # 5. Crear posts del blog
    posts_demo = [
        ("5 Técnicas Esenciales para Mejorar tu Paddle", "carlos_pro", "Descubre las técnicas más importantes que todo jugador de paddle debe dominar. Desde la posición correcta hasta los golpes más efectivos."),
        ("Mi Experiencia en el Torneo Regional", "sofia_champ", "Comparto mi experiencia participando en el torneo regional de paddle. Tips, estrategias y anécdotas de la competencia."),
        ("Equipo Recomendado para Principiantes", "ana_gamer", "Una guía completa sobre qué equipo comprar cuando empiezas en el paddle. Palas, calzado, ropa y accesorios esenciales."),
        ("Ejercicios de Calentamiento para Paddle", "miguel_rookie", "La importancia del calentamiento antes de jugar paddle. Rutina de 10 minutos para evitar lesiones."),
        ("Paddle vs Tenis: Diferencias y Similitudes", "pedro_casual", "Comparativa entre paddle y tenis. ¿Cuál es más fácil de aprender? ¿Qué beneficios ofrece cada uno?"),
    ]

    for titulo, author_username, contenido in posts_demo:
        try:
            autor = User.objects.get(username=author_username)
            post, created = Post.objects.get_or_create(
                titulo=titulo,
                defaults={
                    'autor': autor,
                    'contenido': contenido + "\n\n" + "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                    'estado': 'publicado',
                    'fecha_publicacion': datetime.now() - timedelta(days=random.randint(1, 30))
                }
            )
            if created:
                print(f"✅ Creado post: {titulo}")
        except User.DoesNotExist:
            print(f"❌ Usuario {author_username} no encontrado para el post {titulo}")

    print("\n🎉 ¡Datos de prueba generados exitosamente!")
    print("📊 Resumen:")
    print(f"   👥 Usuarios: {User.objects.count()}")
    print(f"   🏆 Logros: {Logro.objects.count()}")
    print(f"   🥇 Logros desbloqueados: {LogroUsuario.objects.count()}")
    print(f"   🎮 Partidas: {Partida.objects.count()}")
    print(f"   📝 Posts del blog: {Post.objects.count()}")
    print("\n🚀 ¡Tu proyecto está listo para impresionar!")