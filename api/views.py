from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from users.models import UserProfile

from users.models import LogroUsuario
from game.models import Partida as GamePartida
from .serializers import LogroUsuarioSerializer, GamePartidaSerializer
from django.db.models import Avg, Max, Count, Sum


class UserInfoView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		user = request.user
		try:
			profile = UserProfile.objects.get(user=user)
			profile_data = {
				'avatar': profile.avatar.url if profile.avatar else '',
				'nivel_juego': profile.nivel_juego,
				'puntuacion_total': profile.puntuacion_total,
				'partidas_jugadas': profile.partidas_jugadas,
				'pais': profile.pais,
				'sobre_mi': profile.sobre_mi,
			}
		except UserProfile.DoesNotExist:
			profile_data = {}
		return Response({
			'username': user.username,
			'email': user.email,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'profile': profile_data,
		})


class UserLogrosView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		logros = LogroUsuario.objects.filter(usuario=request.user)
		serializer = LogroUsuarioSerializer(logros, many=True)
		return Response(serializer.data)


class UserGamePartidasView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		partidas = GamePartida.objects.filter(jugador=request.user).order_by('-creado')[:50]
		serializer = GamePartidaSerializer(partidas, many=True)
		return Response(serializer.data)

	def post(self, request):
		# Creación de partida enviada por el cliente del juego
		data = request.data
		partida = GamePartida.objects.create(
			jugador=request.user,
			nivel=data.get('nivel', 1) or 1,
			puntaje=data.get('puntaje', 0) or 0,
			duracion_segundos=data.get('duracion_segundos', 0) or 0,
			errores=data.get('errores', 0) or 0,
			combo_max=data.get('combo_max', 0) or 0,
		)
		return Response(GamePartidaSerializer(partida).data, status=201)


class UserGameStatsView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		qs = GamePartida.objects.filter(jugador=request.user)
		total = qs.count()
		if total == 0:
			return Response({'total_partidas': 0})
		agg = qs.aggregate(
			puntaje_total=Sum('puntaje'),
			puntaje_promedio=Avg('puntaje'),
			nivel_max=Max('nivel'),
			combo_max=Max('combo_max'),
			errores_promedio=Avg('errores'),
			duracion_total=Sum('duracion_segundos'),
		)
		return Response({
			'total_partidas': total,
			**agg,
		})
