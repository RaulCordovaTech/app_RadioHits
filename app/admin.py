from django.contrib import admin
# Importamos todos los modelos que queremos que aparezcan en el panel de administración.
from .models import (
    BlogEntrada, 
    EntradaIndex,
    Lunes,
    Martes,
    Miercoles,
    Jueves,
    Viernes,
    Sabado,
    Domingo
)

# ---------------------------------------------------------------------------------
# REGISTRO DE MODELOS DE CONTENIDO (Blog y Entradas del Índice)
# ---------------------------------------------------------------------------------

@admin.register(EntradaIndex)
class EntradaIndexAdmin(admin.ModelAdmin):
    """
    Configuración para el modelo EntradaIndex en el panel de administración.
    Permite visualizar, buscar y filtrar las entradas del carrusel principal.
    """
    list_display = ('titulo', 'autor', 'fecha_creacion')
    search_fields = ('titulo', 'autor__username')
    list_filter = ('fecha_creacion', 'autor')
    ordering = ('-fecha_creacion',)

@admin.register(BlogEntrada)
class BlogEntradaAdmin(admin.ModelAdmin):
    """
    Configuración para el modelo BlogEntrada en el panel de administración.
    Permite visualizar, buscar y filtrar las entradas del blog.
    """
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido', 'autor__username')
    list_filter = ('fecha_publicacion', 'autor')
    ordering = ('-fecha_publicacion',)

# ---------------------------------------------------------------------------------
# REGISTRO DE MODELOS DE PROGRAMACIÓN SEMANAL
# ---------------------------------------------------------------------------------

class ProgramaSemanalAdmin(admin.ModelAdmin):
    """
    Clase de administración genérica para los modelos de programación de cada día.
    Muestra la hora de inicio, fin y el nombre del programa.
    Ordena los programas por la hora de inicio.
    """
    list_display = ('hora_inicio', 'hora_fin', 'nombre_programa')
    ordering = ('hora_inicio',)

# Registramos todos los modelos de los días de la semana usando la misma configuración.
dias_semana = [Lunes, Martes, Miercoles, Jueves, Viernes, Sabado, Domingo]
for dia_model in dias_semana:
    admin.site.register(dia_model, ProgramaSemanalAdmin)
