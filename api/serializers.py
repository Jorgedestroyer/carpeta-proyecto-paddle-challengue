from rest_framework import serializers
from users.models import Logro, LogroUsuario
from game.models import Partida as GamePartida

class LogroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logro
        fields = ['id', 'nombre', 'descripcion', 'icono']

class LogroUsuarioSerializer(serializers.ModelSerializer):
    logro = LogroSerializer()
    class Meta:
        model = LogroUsuario
        fields = ['id', 'logro', 'fecha_obtenido']

class GamePartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePartida
        fields = ['id', 'nivel', 'puntaje', 'duracion_segundos', 'errores', 'combo_max', 'creado']
