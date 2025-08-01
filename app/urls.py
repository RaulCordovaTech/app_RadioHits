from django.urls import path
from app import views
from django.urls import path
from django.contrib.auth.mixins import LoginRequiredMixin 
from .views import (
    IndexView,
    AddEntradaIndexCreateView, UpdateEntradaIndexView, delete_entrada_index,
    CarruselIndexView, EntradaIndexDetailView, ListEntradasIndexView,
    AddEntradaView, UpdateEntradaBlogView, delete_entrada_blog,
    BlogGeneralView, BlogView, BlogDetailView, ListEntradasBlogView,
    EventosView, FiestasView, AboutView, LaTertuliaView,
    # Importa vistas de programación semanal
    AddProgramaLunes, AddProgramaMartes, AddProgramaMiercoles,
    AddProgramaJueves, AddProgramaViernes, AddProgramaSabado, AddProgramaDomingo,
    ListProgramacionSemanal,

     # Nuevas para UPDATE views
    UpdateProgramaLunes, UpdateProgramaMartes, UpdateProgramaMiercoles,
    UpdateProgramaJueves, UpdateProgramaViernes, UpdateProgramaSabado, UpdateProgramaDomingo,
    # importaciones para DELETE views (funciones)
    delete_programa_lunes, delete_programa_martes, delete_programa_miercoles,
    delete_programa_jueves, delete_programa_viernes, delete_programa_sabado, delete_programa_domingo
)

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

    #------------------------------------------------------------------------------------------------------------------------------
    
    # Rutas para la programación semanal
    path('add_programa_lunes/', AddProgramaLunes.as_view(), name='add_programa_lunes'),
    path('add_programa_martes/', AddProgramaMartes.as_view(), name='add_programa_martes'),
    path('add_programa_miercoles/', AddProgramaMiercoles.as_view(), name='add_programa_miercoles'),
    path('add_programa_jueves/', AddProgramaJueves.as_view(), name='add_programa_jueves'),
    path('add_programa_viernes/', AddProgramaViernes.as_view(), name='add_programa_viernes'),
    path('add_programa_sabado/', AddProgramaSabado.as_view(), name='add_programa_sabado'),
    path('add_programa_domingo/', AddProgramaDomingo.as_view(), name='add_programa_domingo'),
    path('list_programacion/', ListProgramacionSemanal.as_view(), name='list_programacion'),

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# URLs PARA PROGRAMACIÓN SEMANAL - Agregar al final de urlpatterns en urls.py

    # Rutas UPDATE para la programación semanal
    path('update_programa_lunes/<int:pk>/', UpdateProgramaLunes.as_view(), name='update_programa_lunes'),
    path('update_programa_martes/<int:pk>/', UpdateProgramaMartes.as_view(), name='update_programa_martes'),
    path('update_programa_miercoles/<int:pk>/', UpdateProgramaMiercoles.as_view(), name='update_programa_miercoles'),
    path('update_programa_jueves/<int:pk>/', UpdateProgramaJueves.as_view(), name='update_programa_jueves'),
    path('update_programa_viernes/<int:pk>/', UpdateProgramaViernes.as_view(), name='update_programa_viernes'),
    path('update_programa_sabado/<int:pk>/', UpdateProgramaSabado.as_view(), name='update_programa_sabado'),
    path('update_programa_domingo/<int:pk>/', UpdateProgramaDomingo.as_view(), name='update_programa_domingo'),

# ----------------------------------------------------------------------------------------------------------------------------------------------------
    # Rutas DELETE para la programación semanal
    path('delete_programa_lunes/<int:pk>/', delete_programa_lunes, name='delete_programa_lunes'),
    path('delete_programa_martes/<int:pk>/', delete_programa_martes, name='delete_programa_martes'),
    path('delete_programa_miercoles/<int:pk>/', delete_programa_miercoles, name='delete_programa_miercoles'),
    path('delete_programa_jueves/<int:pk>/', delete_programa_jueves, name='delete_programa_jueves'),
    path('delete_programa_viernes/<int:pk>/', delete_programa_viernes, name='delete_programa_viernes'),
    path('delete_programa_sabado/<int:pk>/', delete_programa_sabado, name='delete_programa_sabado'),
    path('delete_programa_domingo/<int:pk>/', delete_programa_domingo, name='delete_programa_domingo'),

# ----------------------------------------------------------------------------------------------------------------------------------------------------
]