from django.contrib import admin
from .models import Categoria, Post, Comentario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    readonly_fields = ('autor', 'fecha_creacion')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'estado', 'fecha_publicacion', 'visualizaciones')
    list_filter = ('estado', 'categoria', 'fecha_creacion', 'fecha_publicacion', 'autor')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    ordering = ('estado', '-fecha_creacion')
    inlines = [ComentarioInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'slug', 'autor', 'categoria', 'estado')
        }),
        ('Contenido', {
            'fields': ('contenido', 'imagen_destacada')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion',)
        }),
        ('Estadísticas', {
            'fields': ('visualizaciones',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo post
            obj.autor = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'post', 'fecha_creacion', 'activo')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('autor__username', 'contenido')
    actions = ['aprobar_comentarios', 'desaprobar_comentarios']
    
    def aprobar_comentarios(self, request, queryset):
        queryset.update(activo=True)
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"
    
    def desaprobar_comentarios(self, request, queryset):
        queryset.update(activo=False)
    desaprobar_comentarios.short_description = "Desaprobar comentarios seleccionados"
