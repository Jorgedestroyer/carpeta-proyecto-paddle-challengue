from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Partida(models.Model):
    # Usamos related_name distinto para no chocar con users.Partida (que ya usa 'partidas')
    jugador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partidas_game')
    nivel = models.PositiveIntegerField(default=1)
    puntaje = models.PositiveIntegerField(default=0)
    duracion_segundos = models.PositiveIntegerField(default=0)
    errores = models.PositiveIntegerField(default=0)
    combo_max = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f"Partida #{self.id} - {self.jugador.username} (Nivel {self.nivel})"

class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    nombre = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    tipo = models.CharField(max_length=30, choices=[('bug','Bug'),('idea','Idea'),('balance','Balance'),('otro','Otro')], default='idea')
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        base = self.usuario.username if self.usuario else (self.nombre or 'Anónimo')
        return f"{base} - {self.tipo}"