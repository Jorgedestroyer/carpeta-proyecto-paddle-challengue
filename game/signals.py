from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users.models import UserProfile, Logro, LogroUsuario
from .models import Partida

User = get_user_model()

LOGROS_PARTIDAS = [
    (1, "Primer Paso", "Jugaste tu primera partida", "fas fa-step-forward"),
    (5, "Novato Dedicado", "Jugaste 5 partidas", "fas fa-star"),
    (10, "Jugador Activo", "Jugaste 10 partidas", "fas fa-fire"),
    (25, "Veterano", "Jugaste 25 partidas", "fas fa-medal"),
    (50, "Leyenda", "Jugaste 50 partidas", "fas fa-crown"),
]

def _obtener_o_crear_logro(nombre, descripcion, icono):
    logro, _ = Logro.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion, 'icono': icono})
    return logro

@receiver(post_save, sender=Partida)
def actualizar_perfil_y_logros(sender, instance: Partida, created, **kwargs):
    if not created:
        return
    user = instance.jugador
    # Actualizar perfil
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.partidas_jugadas += 1
    profile.puntuacion_total += instance.puntaje
    # Sencilla lógica de nivel: cada 1000 puntos sube nivel
    profile.nivel_juego = max(profile.nivel_juego, 1 + profile.puntuacion_total // 1000)
    profile.save()

    # Asignar logros por conteo de partidas
    total = profile.partidas_jugadas
    for umbral, nombre, desc, icono in LOGROS_PARTIDAS:
        if total >= umbral:
            logro = _obtener_o_crear_logro(nombre, desc, icono)
            LogroUsuario.objects.get_or_create(usuario=user, logro=logro)