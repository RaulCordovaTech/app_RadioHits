from django import forms
from .models import (
    
    EntradaIndex,
    BlogEntrada)

#FORMULARIO PARA ENTRADA DE INFORMACIÓN EN EL ÍNDICE DE RADIO HITS
class EntradaIndexForm(forms.ModelForm):
    class Meta:
        model = EntradaIndex
        fields = ['titulo', 'imagen', 'texto']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full bg-gray-900 text-white border border-gray-700 rounded-lg px-4 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'w-full text-white bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 file:bg-red-600 file:text-white file:border-0 file:rounded-md file:px-4 file:py-2'
            }),
            'texto': forms.Textarea(attrs={
                'class': 'w-full bg-gray-900 text-white border border-gray-700 rounded-lg px-4 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'rows': 5
            }),
        }
        
#----------------------------------------------------------------------------------------------------------------------------------------------------

#FORMULARIO PARA ENTRADA DEL BLOG
class BlogEntradaForm(forms.ModelForm):
    class Meta:
        model = BlogEntrada
        fields = ['titulo', 'imagen', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full bg-gray-900 text-white border border-gray-700 rounded-lg px-4 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'w-full text-white bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 file:bg-red-600 file:text-white file:border-0 file:rounded-md file:px-4 file:py-2'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'w-full bg-gray-900 text-white border border-gray-700 rounded-lg px-4 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'rows': 10
            }),
        }
