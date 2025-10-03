from django.contrib import admin
from .models import Partida, Feedback

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('id','jugador','nivel','puntaje','duracion_segundos','errores','combo_max','creado')
    list_filter = ('nivel','creado')
    search_fields = ('jugador__username',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','nombre','tipo','atendido','creado')
    list_filter = ('tipo','atendido','creado')
    search_fields = ('usuario__username','nombre','mensaje')
    list_editable = ('atendido',)