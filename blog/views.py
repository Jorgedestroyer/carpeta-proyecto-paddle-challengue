from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Categoria, Comentario
from .forms import ComentarioForm, PostForm, CategoriaForm


def lista_posts(request):
    """Vista para listar todos los posts publicados."""
    posts = Post.objects.filter(estado='publicado').select_related('autor', 'categoria')
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(titulo__icontains=query) | 
            Q(contenido__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(posts, 6)  # 6 posts por página
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    return render(request, 'blog/lista_posts.html', {
        'posts': posts_page,
        'query': query
    })


def detalle_post(request, slug):
    """Vista para mostrar el detalle de un post."""
    post = get_object_or_404(Post, slug=slug, estado='publicado')
    
    # Incrementar visualizaciones
    post.visualizaciones += 1
    post.save()
    
    # Comentarios
    comentarios = post.comentarios.filter(activo=True)
    nuevo_comentario = None
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            comentario_form = ComentarioForm(data=request.POST)
            if comentario_form.is_valid():
                nuevo_comentario = comentario_form.save(commit=False)
                nuevo_comentario.post = post
                nuevo_comentario.autor = request.user
                nuevo_comentario.save()
                messages.success(request, 'Tu comentario ha sido añadido.')
                return redirect('blog:detalle_post', slug=post.slug)
        else:
            messages.error(request, 'Debes iniciar sesión para comentar.')
            return redirect('login')
    else:
        comentario_form = ComentarioForm()
    
    # Posts relacionados (misma categoría)
    posts_relacionados = Post.objects.filter(
        categoria=post.categoria,
        estado='publicado'
    ).exclude(id=post.id)[:3]
    
    return render(request, 'blog/detalle_post.html', {
        'post': post,
        'comentarios': comentarios,
        'nuevo_comentario': nuevo_comentario,
        'comentario_form': comentario_form,
        'posts_relacionados': posts_relacionados
    })


def posts_por_categoria(request, slug):
    """Vista para mostrar posts de una categoría específica."""
    categoria = get_object_or_404(Categoria, slug=slug)
    posts = Post.objects.filter(categoria=categoria, estado='publicado').select_related('autor')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    return render(request, 'blog/posts_categoria.html', {
        'categoria': categoria,
        'posts': posts_page
    })


def lista_categorias(request):
    """Vista para listar todas las categorías."""
    categorias = Categoria.objects.all()
    return render(request, 'blog/lista_categorias.html', {'categorias': categorias})


# ===== CRUD Posts =====

class PuedeEditarPostMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object() if hasattr(self, 'get_object') else None
        user = self.request.user
        if not user.is_authenticated:
            return False
        # Staff siempre puede
        if user.is_staff:
            return True
        # Autor puede editar/eliminar su propio post
        return obj is None or obj.autor_id == user.id

class CrearPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.save(autor=self.request.user)
        messages.success(self.request, 'Post creado correctamente.')
        return redirect(form.instance.get_absolute_url())

class EditarPostView(LoginRequiredMixin, PuedeEditarPostMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, 'Post actualizado.')
        return super().form_valid(form)

class EliminarPostView(LoginRequiredMixin, PuedeEditarPostMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blog:lista_posts')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post eliminado.')
        return super().delete(request, *args, **kwargs)


# ===== CRUD Categorías (opcional restringido a staff) =====
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class CrearCategoriaView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'blog/categoria_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada.')
        return super().form_valid(form)

class EditarCategoriaView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'blog/categoria_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada.')
        return super().form_valid(form)

class EliminarCategoriaView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'blog/categoria_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blog:lista_categorias')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Categoría eliminada.')
        return super().delete(request, *args, **kwargs)
