"""
URL configuration for paddle_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import models
from blog.models import Post
from users.models import UserProfile


def home(request):
    """Vista para la página principal."""
    from users.models import LogroUsuario
    
    # Estadísticas para la página principal
    total_usuarios = User.objects.count()
    total_posts = Post.objects.filter(estado='publicado').count()
    total_partidas = UserProfile.objects.aggregate(
        total=models.Sum('partidas_jugadas')
    )['total'] or 0
    total_logros = LogroUsuario.objects.count()
    
    # Top 5 jugadores
    top_players = UserProfile.objects.select_related('user').order_by('-puntuacion_total')[:5]
    
    # Posts recientes
    recent_posts = Post.objects.filter(estado='publicado').select_related('autor').order_by('-fecha_publicacion')[:5]
    
    # Logros recientes
    featured_achievements = LogroUsuario.objects.select_related('usuario', 'logro').order_by('-fecha_obtenido')[:6]
    
    context = {
        'total_usuarios': total_usuarios,
        'total_posts': total_posts,
        'total_partidas': total_partidas,
        'total_logros': total_logros,
        'top_players': top_players,
        'recent_posts': recent_posts,
        'featured_achievements': featured_achievements,
    }
    return render(request, 'home.html', context)


def game_config_view(request):
    """Página estática que muestra la configuración del juego."""
    return render(request, 'game_config.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('configuracion-juego/', game_config_view, name='game_config'),
    path('users/', include('users.urls')),
    path('blog/', include('blog.urls')),
    path('game/', include('game.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
