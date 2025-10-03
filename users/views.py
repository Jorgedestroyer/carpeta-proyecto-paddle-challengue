from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .models import UserProfile
from .forms import UserProfileForm, UserRegistrationForm
from game.models import Partida as GamePartida
from django.db.models import Sum, Avg, Max, Count


def registro(request):
    """Vista para el registro de nuevos usuarios."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                # Crear el perfil automáticamente
                UserProfile.objects.create(user=user)
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido a Paddle Challenge.')
                return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/registro.html', {'form': form})


@login_required
def perfil(request, username=None):
    """Vista para mostrar el perfil de un usuario."""
    from .models import LogroUsuario
    
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Obtener logros del usuario
    user_achievements = LogroUsuario.objects.filter(usuario=user).select_related('logro').order_by('-fecha_obtenido')
    
    return render(request, 'users/perfil.html', {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': user == request.user,
        'user_achievements': user_achievements,
    })


@login_required
def editar_perfil(request):
    """Vista para editar el perfil del usuario."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('users:perfil', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'users/editar_perfil.html', {'form': form})


def lista_jugadores(request):
    """Vista para mostrar la lista de jugadores con ranking global básico."""
    perfiles = UserProfile.objects.select_related('user').order_by('-puntuacion_total')
    # Ranking adicional derivado de partidas en game (si existen)
    partidas_aggr = GamePartida.objects.values('jugador').annotate(
        total_puntaje=Sum('puntaje'),
        partidas=Count('id'),
        promedio=Avg('puntaje'),
        nivel_max=Max('nivel'),
        combo_max=Max('combo_max'),
    )
    # Convertir a dict indexado por user id para lookup rápido
    partidas_map = {row['jugador']: row for row in partidas_aggr}
    # Enriquecer perfiles con datos runtime (sin tocar DB)
    ranking = []
    for p in perfiles:
        extra = partidas_map.get(p.user_id, {})
        ranking.append({
            'profile': p,
            'total_puntaje_game': extra.get('total_puntaje', 0),
            'partidas_game': extra.get('partidas', 0),
            'promedio_game': extra.get('promedio') or 0,
            'nivel_max_game': extra.get('nivel_max') or 0,
            'combo_max_game': extra.get('combo_max') or 0,
        })
    # Orden principal por total_puntaje_game si hay datos, fallback a puntuacion_total
    ranking.sort(key=lambda r: (r['total_puntaje_game'], r['profile'].puntuacion_total), reverse=True)
    return render(request, 'users/lista_jugadores.html', {
        'perfiles': perfiles,
        'ranking': ranking,
    })


def cerrar_sesion(request):
    """Cerrar sesión del usuario."""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('home')
