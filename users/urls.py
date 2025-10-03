from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='mi_perfil'),
    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('jugadores/', views.lista_jugadores, name='lista_jugadores'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]