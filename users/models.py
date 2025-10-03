from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    """Perfil extendido del usuario para información adicional del juego."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    nivel_juego = models.IntegerField(default=1)
    puntuacion_total = models.IntegerField(default=0)
    partidas_jugadas = models.IntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    pais = models.CharField(max_length=50, blank=True)
    sobre_mi = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.user.username})


class Logro(models.Model):
    """Logros obtenidos por los usuarios."""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300, blank=True)
    icono = models.CharField(max_length=100, blank=True)  # nombre de icono FontAwesome o url
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class LogroUsuario(models.Model):
    """Relación entre usuario y logros obtenidos."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logros')
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE)
    fecha_obtenido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.logro.nombre}"


class Partida(models.Model):
    """Partidas jugadas por los usuarios."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partidas')
    fecha = models.DateTimeField(auto_now_add=True)
    puntos = models.IntegerField(default=0)
    resultado = models.CharField(max_length=20, choices=[('victoria', 'Victoria'), ('derrota', 'Derrota'), ('empate', 'Empate')], default='empate')
    duracion = models.IntegerField(default=0)  # segundos

    def __str__(self):
        return f"{self.usuario.username} - {self.resultado} ({self.puntos} pts)"
