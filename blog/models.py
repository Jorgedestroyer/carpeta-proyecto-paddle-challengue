from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Categoria(models.Model):
    """Categorías para organizar los posts del blog."""
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=300, blank=True)
    
    class Meta:
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('blog:categoria', kwargs={'slug': self.slug})


class Post(models.Model):
    """Modelo para los posts del blog."""
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    ]
    
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    contenido = models.TextField()
    imagen_destacada = models.ImageField(upload_to='blog/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='posts')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    visualizaciones = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name_plural = "Posts"
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('blog:detalle_post', kwargs={'slug': self.slug})


class Comentario(models.Model):
    """Modelo para los comentarios de los posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField(max_length=1000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['fecha_creacion']
        verbose_name_plural = "Comentarios"
    
    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.post.titulo}'
