from django.contrib import admin
from .models import BlogEntrada, EntradaIndex  # Importa los modelos que deseas registrar

#Registrar el modelo BlogEntrada en el panel de administración de Django
#-----------------------------------------------------------------------------------------------------------------------------------------------

# Registrar el modelo EntradaIndex en el panel de administración de Django
class EntradaIndexAdmin(admin.ModelAdmin):
    list_display = ('autor', 'fecha_creacion', 'titulo', 'imagen', 'texto')
    search_fields = ('titulo',)
    
admin.site.register(EntradaIndex, EntradaIndexAdmin)

#-----------------------------------------------------------------------------------------------------------------------------------------------
class BlogEntradaAdmin(admin.ModelAdmin):
    list_display = ('autor', 'fecha_publicacion', 'titulo', 'imagen')
    search_fields = ('titulo',)
    
admin.site.register(BlogEntrada, BlogEntradaAdmin)


# Register your models here.
