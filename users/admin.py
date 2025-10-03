from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nivel_juego', 'puntuacion_total', 'partidas_jugadas', 'fecha_registro')
    list_filter = ('nivel_juego', 'pais', 'fecha_registro')
    search_fields = ('user__username', 'user__email', 'pais')
    readonly_fields = ('fecha_registro',)
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': ('avatar', 'fecha_nacimiento', 'pais', 'sobre_mi')
        }),
        ('Estadísticas del Juego', {
            'fields': ('nivel_juego', 'puntuacion_total', 'partidas_jugadas')
        }),
        ('Fechas', {
            'fields': ('fecha_registro',)
        }),
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
