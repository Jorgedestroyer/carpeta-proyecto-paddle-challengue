from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Partida
from .forms import FeedbackForm
from django.db.models import Avg, Max, Sum

@login_required
def registrar_partida(request):
    if request.method == 'POST':
        # Datos simulados (en futuro vendrán del juego real)
        nivel = int(request.POST.get('nivel', 1))
        puntaje = int(request.POST.get('puntaje', 0))
        duracion = int(request.POST.get('duracion', 0))
        errores = int(request.POST.get('errores', 0))
        combo = int(request.POST.get('combo_max', 0))
        Partida.objects.create(
            jugador=request.user,
            nivel=nivel,
            puntaje=puntaje,
            duracion_segundos=duracion,
            errores=errores,
            combo_max=combo
        )
        messages.success(request, 'Partida registrada.')
        return redirect('game:mis_partidas')
    return render(request, 'game/registrar_partida.html')

@login_required
def mis_partidas(request):
    partidas = Partida.objects.filter(jugador=request.user)
    stats = None
    if partidas.exists():
        stats = partidas.aggregate(
            total=Sum('puntaje'),
            promedio=Avg('puntaje'),
            nivel_max=Max('nivel'),
            combo_max=Max('combo_max'),
        )
        stats['partidas_count'] = partidas.count()
    paginator = Paginator(partidas, 10)
    page = request.GET.get('page')
    partidas_page = paginator.get_page(page)
    return render(request, 'game/mis_partidas.html', {'partidas': partidas_page, 'stats': stats})

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            if request.user.is_authenticated:
                fb.usuario = request.user
            fb.save()
            messages.success(request, 'Gracias por tu feedback!')
            return redirect('game:feedback')
    else:
        form = FeedbackForm()
    return render(request, 'game/feedback.html', {'form': form})
