from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
from game.models import Partida

User = get_user_model()

class Command(BaseCommand):
    help = "Genera partidas simuladas para cada usuario (parámetro --n por usuario)."

    def add_arguments(self, parser):
        parser.add_argument('--n', type=int, default=5, help='Número de partidas por usuario')
        parser.add_argument('--max-nivel', type=int, default=10, help='Nivel máximo simulado')

    def handle(self, *args, **options):
        n = options['n']
        max_nivel = options['max_nivel']
        users = User.objects.all()
        total_creadas = 0
        for u in users:
            for _ in range(n):
                nivel = random.randint(1, max_nivel)
                puntaje_base = nivel * 200
                variacion = random.randint(-80, 250)
                puntaje = max(0, puntaje_base + variacion)
                duracion = random.randint(40, 240)
                errores = random.randint(0, 15)
                combo = random.randint(0, 30)
                Partida.objects.create(
                    jugador=u,
                    nivel=nivel,
                    puntaje=puntaje,
                    duracion_segundos=duracion,
                    errores=errores,
                    combo_max=combo,
                    creado=timezone.now()
                )
                total_creadas += 1
        self.stdout.write(self.style.SUCCESS(f"Partidas simuladas creadas: {total_creadas}"))
