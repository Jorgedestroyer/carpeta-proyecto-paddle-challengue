from django import forms
from django.utils.text import slugify
from .models import Comentario, Post, Categoria


class ComentarioForm(forms.ModelForm):
    """Formulario para añadir comentarios a los posts."""
    
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu comentario...',
                'required': True
            })
        }
        labels = {
            'contenido': 'Comentario'
        }


class PostForm(forms.ModelForm):
    """Formulario para crear/editar posts del blog."""

    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'imagen_destacada', 'categoria', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del post'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Contenido...'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, autor=None, commit=True):
        instance = super().save(commit=False)
        if autor and not instance.autor_id:
            instance.autor = autor
        # Generar slug único si se crea o cambia el título
        if not instance.slug:
            base = slugify(instance.titulo)[:180]
            slug = base
            counter = 1
            from .models import Post as PostModel
            while PostModel.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            instance.slug = slug
        if commit:
            instance.save()
        return instance


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            base = slugify(instance.nombre)[:90]
            slug = base
            from .models import Categoria as CategoriaModel
            counter = 1
            while CategoriaModel.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            instance.slug = slug
        if commit:
            instance.save()
        return instance