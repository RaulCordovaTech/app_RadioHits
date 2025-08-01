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


#MODELOS PARA LA PROGRAMAVIÓN SEMANAL DE RADIO HITS

#--------------------------------------------------------------------------------------------------------------------------------------
#MODELO LUNES
class Lunes(models.Model):
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    nombre_programa = models.CharField(max_length=200, verbose_name='Nombre del programa')

    def __str__(self):
        return self.nombre_programa

#--------------------------------------------------------------------------------------------------------------------------------------   
#MODELO MARTES
class Martes(models.Model):
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    nombre_programa = models.CharField(max_length=200, verbose_name='Nombre del programa')

    def __str__(self):
        return self.nombre_programa

#--------------------------------------------------------------------------------------------------------------------------------------   
#MODELO MIERCOLES
class Miercoles(models.Model):
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    nombre_programa = models.CharField(max_length=200, verbose_name='Nombre del programa')

    def __str__(self):
        return self.nombre_programa
    
#--------------------------------------------------------------------------------------------------------------------------------------
#MODELO JUEVES
class Jueves(models.Model):
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    nombre_programa = models.CharField(max_length=200, verbose_name='Nombre del programa')

    def __str__(self):
        return self.nombre_programa
#--------------------------------------------------------------------------------------------------------------------------------------
#MODELO VIERNES
class Viernes(models.Model):
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    nombre_programa = models.CharField(max_length=200, verbose_name='Nombre del programa')

    def __str__(self):
        return self.nombre_programa
#--------------------------------------------------------------------------------------------------------------------------------------
#MODELO SÁBADO
class Sabado(models.Model):
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    nombre_programa = models.CharField(max_length=200, verbose_name='Nombre del programa')

    def __str__(self):
        return self.nombre_programa
#--------------------------------------------------------------------------------------------------------------------------------------
#MODELO DOMINGO
class Domingo(models.Model):
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    nombre_programa = models.CharField(max_length=200, verbose_name='Nombre del programa')

    def __str__(self):
        return self.nombre_programa
#--------------------------------------------------------------------------------------------------------------------------------------

