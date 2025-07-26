from django.urls import path
from app import views
from .views import IndexView, EventosView, FiestasView, AboutView,\
    AddEntradaView, BlogGeneralView, BlogView, UpdateEntradaBlogView, LaTertuliaView, delete_entrada_blog,\
    AddEntradaIndexCreateView, delete_entrada_index, CarruselIndexView, ListEntradasIndexView, ListEntradasBlogView, BlogDetailView, \
     UpdateEntradaIndexView
from django.contrib.auth.mixins import LoginRequiredMixin # No es necesario importar aquí si no se usa directamente en urls.py

urlpatterns = [
    path('', IndexView.as_view(), name='index'),    # Ruta para la vista del índice
    path('fiestas/', FiestasView.as_view(), name='fiestas'),    # Ruta para la vista de fiestas
    path('eventos/', EventosView.as_view(), name='eventos'),    # Ruta para la vista de eventos
    path('about/', AboutView.as_view(), name='about'),    # Ruta para la vista de about
    
    # Rutas para el Blog General (modelo BlogEntrada)
    path('add_entrada_blog/', AddEntradaView.as_view(), name='add_entrada_blog'), # Renombrado para claridad
    path('update_entrada_blog/<int:pk>/', UpdateEntradaBlogView.as_view(), name='update_entrada_blog'),
    path('delete_entrada_blog/<int:pk>/', delete_entrada_blog, name='delete_entrada_blog'),
    path('blog/', BlogGeneralView.as_view(), name='blog'),
    path('blog/<int:entrada_id>/', BlogView.as_view(), name='entrada_blog'),
    path('list_entradas_blog/', ListEntradasBlogView.as_view(), name='list_entradas_blog'),
    path('blog/detail/<int:entrada_id>/', BlogDetailView.as_view(), name='blog_detail'),
    path('latertulia/', LaTertuliaView.as_view(), name='latertulia'),
    
    #------------------------------------------------------------------------------------------------------------------------------
    
    # Rutas para las Entradas del Índice (modelo EntradaIndex)
    path('add_entrada_index/', AddEntradaIndexCreateView.as_view(), name='add_entrada_index'),
    path('update_entrada_index/<int:pk>/', UpdateEntradaIndexView.as_view(), name='update_entrada_index'),
    path('delete_entrada_index/<int:pk>/', delete_entrada_index, name='delete_entrada_index'),
    path('carrusel_index/', CarruselIndexView.as_view(), name='carrusel_index'),
    path('list_entradas_index/', ListEntradasIndexView.as_view(), name='list_entradas_index'),
]