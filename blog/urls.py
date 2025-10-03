from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    # CRUD Posts - URLs específicas primero
    path('post/nuevo/', views.CrearPostView.as_view(), name='crear_post'),
    path('post/<slug:slug>/editar/', views.EditarPostView.as_view(), name='editar_post'),
    path('post/<slug:slug>/eliminar/', views.EliminarPostView.as_view(), name='eliminar_post'),
    # URL genérica después
    path('post/<slug:slug>/', views.detalle_post, name='detalle_post'),
    path('categoria/<slug:slug>/', views.posts_por_categoria, name='categoria'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    # CRUD Categorías (staff)
    path('categorias/nueva/', views.CrearCategoriaView.as_view(), name='crear_categoria'),
    path('categoria/<slug:slug>/editar/', views.EditarCategoriaView.as_view(), name='editar_categoria'),
    path('categoria/<slug:slug>/eliminar/', views.EliminarCategoriaView.as_view(), name='eliminar_categoria'),
]