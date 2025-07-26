from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario

# Create your models here.

#MODELOS PARA LA APLICACIÓN DE RADIO HITS
#--------------------------------------------------------------------------------------------------------------------------------------
#MODELO PARA LA CREACIÓN DE IMAGENES Y TEXTO EN EL INDICE DE RADIO HITS
class EntradaIndex(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')  # Relación con el modelo User
    titulo = models.CharField(max_length=200, verbose_name='Título')
    imagen = models.ImageField(upload_to='entrada_imagenes/', blank=True, null=True, verbose_name='Imagen')  # Campo para la imagen
    texto = models.TextField(verbose_name='Texto')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')  # Fecha de creación automática al crear la entrada      
    def __str__(self):
        return self.titulo

#--------------------------------------------------------------------------------------------------------------------------------------   
#--------------------------------------------------------------------------------------------------------------------------------------

#MODELO PARA LA CREACIÓN DE UNA ENTRADA DE BLOG

class BlogEntrada(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')  # Relación con el modelo User
    titulo = models.CharField(max_length=200, verbose_name='Título')
    imagen = models.ImageField(upload_to='blog_imagenes/', blank=True, null=True, verbose_name='Imagen')  # Campo para la imagen de la entrada
    contenido = models.TextField(verbose_name='Contenido')
    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de la publicación') # Fecha de publicación automática al crear la entrada

    def __str__(self):
        return self.titulo

