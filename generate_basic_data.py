#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paddle_web.settings')
    django.setup()

    from django.contrib.auth.models import User
    from users.models import UserProfile, Logro, LogroUsuario

    print("🚀 Generando datos básicos...")

    # 1. Crear logros si no existen
    logros_data = [
        ("Primer Paso", "Jugaste tu primera partida", "fas fa-play"),
        ("Novato Dedicado", "Jugaste 5 partidas", "fas fa-star"),
        ("Jugador Activo", "Jugaste 10 partidas", "fas fa-fire"),
        ("Puntuación Alta", "Conseguiste más de 500 puntos", "fas fa-chart-line"),
        ("Élite", "Conseguiste más de 1000 puntos", "fas fa-gem"),
    ]

    for nombre, descripcion, icono in logros_data:
        logro, created = Logro.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion, 'icono': icono}
        )
        if created:
            print(f"✅ Creado logro: {nombre}")

    # 2. Crear usuarios de prueba básicos
    usuarios_demo = [
        ("carlos_pro", "Carlos", "Martinez", 5, 2350, 47),
        ("ana_gamer", "Ana", "Rodriguez", 4, 1850, 32),
        ("miguel_rookie", "Miguel", "Lopez", 3, 850, 18),
    ]

    for username, first_name, last_name, nivel, puntos, partidas in usuarios_demo:
        try:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f'{username}@paddle.com',
                }
            )
            if created:
                user.set_password('paddle123')
                user.save()
                print(f"✅ Creado usuario: {username}")

            # Actualizar perfil
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.nivel_juego = nivel
            profile.puntuacion_total = puntos
            profile.partidas_jugadas = partidas
            profile.save()
            
            # Asignar logros básicos
            if partidas >= 1:
                LogroUsuario.objects.get_or_create(usuario=user, logro=Logro.objects.get(nombre="Primer Paso"))
            if partidas >= 5:
                LogroUsuario.objects.get_or_create(usuario=user, logro=Logro.objects.get(nombre="Novato Dedicado"))
            if puntos >= 500:
                LogroUsuario.objects.get_or_create(usuario=user, logro=Logro.objects.get(nombre="Puntuación Alta"))

        except Exception as e:
            print(f"❌ Error creando {username}: {e}")

    print("\n🎉 ¡Datos básicos generados!")
    print("📊 Resumen:")
    print(f"   👥 Usuarios: {User.objects.count()}")
    print(f"   🏆 Logros: {Logro.objects.count()}")
    print(f"   🥇 Logros desbloqueados: {LogroUsuario.objects.count()}")
    print("\n🚀 ¡Tu proyecto está listo!")