from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('partidas/registrar/', views.registrar_partida, name='registrar_partida'),
    path('partidas/mias/', views.mis_partidas, name='mis_partidas'),
    path('feedback/', views.feedback, name='feedback'),
]