from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import requests
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Importamos los modelos necesarios
from .models import (
    EntradaIndex,
    BlogEntrada,
    # Asegúrate de que el modelo User esté importado o disponible si se usa en ForeignKey
    # from django.contrib.auth.models import User
)

# Importar los forms necesarios
from .forms import (
    EntradaIndexForm,
    BlogEntradaForm
)

# --- VISTAS GENERALES Y DE SECCIONES ESTÁTICAS ---
# Estas vistas manejan páginas informativas o funcionalidades que no están directamente ligadas a un único modelo de contenido dinámico.

class IndexView(TemplateView):
    """
    Vista principal (Home) del sitio.
    Muestra indicadores económicos obtenidos de una API externa y las 3 entradas más recientes
    del modelo EntradaIndex para el carrusel.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Diccionario de meses en español para formato de fechas
        meses_es = {
            "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
            "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
            "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
        }

        # Obtener fecha actual para la consulta de indicadores
        fecha_actual = datetime.now()
        dia_actual = fecha_actual.strftime("%d")
        mes_actual = meses_es.get(fecha_actual.strftime("%m"), "Mes desconocido")
        año_actual = fecha_actual.strftime("%Y")

        # Intento de obtener datos de indicadores económicos de mindicador.cl
        try:
            response = requests.get("https://mindicador.cl/api")
            response.raise_for_status()  # Lanza una excepción para errores HTTP
            data = response.json()

            # Extraer mes de la fecha de UTM para mostrar en español
            fecha_utm = data["utm"]["fecha"]
            mes_utm_num = fecha_utm[5:7]
            mes_utm_esp = meses_es.get(mes_utm_num, "Mes desconocido")

            context["indicadores"] = {
                "dolar": data["dolar"]["valor"],
                "euro": data["euro"]["valor"],
                "uf": data["uf"]["valor"],
                "utm": data["utm"]["valor"],
                "utm_mes": mes_utm_esp,
                "fecha_consulta": f"{dia_actual} de {mes_actual.lower()} de {año_actual}",
            }
        except requests.exceptions.RequestException:
            # En caso de error en la petición o JSON inválido
            context["indicadores"] = {
                "dolar": None, "euro": None, "uf": None, "utm": None, "utm_mes": None,
                "fecha_consulta": f"{dia_actual} de {mes_actual.lower()} de {año_actual}",
            }

        # Obtener las 3 entradas más recientes del modelo EntradaIndex para el carrusel
        context['entradas'] = EntradaIndex.objects.order_by('-id')[:3]
        return context

class EventosView(TemplateView):
    """
    Vista para la sección de Eventos.
    Simplemente renderiza la plantilla de eventos.
    """
    template_name = 'secciones/eventos.html'

class FiestasView(TemplateView):
    """
    Vista para la sección de Fiestas.
    Simplemente renderiza la plantilla de fiestas.
    """
    template_name = 'secciones/fiestas.html'

class AboutView(TemplateView):
    """
    Vista para la sección "Sobre Nosotros".
    Simplemente renderiza la plantilla de información del sitio.
    """
    template_name = 'secciones/about.html'

class LaTertuliaView(TemplateView):
    """
    Vista para la sección "La Tertulia".
    Simplemente renderiza la plantilla específica de La Tertulia.
    """
    template_name = 'secciones/latertulia.html'

# --- VISTAS RELACIONADAS CON EL MODELO EntradaIndex ---
# Estas vistas gestionan la creación, lectura, actualización y eliminación (CRUD)
# de las entradas que aparecen en el carrusel del índice.

class AddEntradaIndexCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para la creación de nuevas entradas para el índice (carrusel).
    Requiere que el usuario esté autenticado.
    Asigna automáticamente al usuario logueado como autor.
    """
    model = EntradaIndex
    form_class = EntradaIndexForm
    template_name = 'secciones/add_entrada_index.html'
    success_url = reverse_lazy('list_entradas_index') # Redirige a la lista de entradas del índice tras el éxito

    def form_valid(self, form):
        form.instance.autor = self.request.user # Asigna el usuario logueado como autor
        messages.success(self.request, '¡Entrada agregada correctamente!') # Mensaje de éxito
        return super().form_valid(form)

class UpdateEntradaIndexView(LoginRequiredMixin, UpdateView):
    """
    Vista para la modificación de entradas del índice existentes.
    Requiere autenticación y solo permite al autor modificar sus propias entradas.
    """
    model = EntradaIndex
    form_class = EntradaIndexForm
    template_name = 'secciones/update_entrada_index.html'
    success_url = reverse_lazy('list_entradas_index') # Redirige a la lista tras la actualización

    def get_queryset(self):
        # Asegura que solo el autor de la entrada pueda modificarla
        return EntradaIndex.objects.filter(autor=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, '¡Entrada modificada correctamente!') # Mensaje de éxito
        return super().form_valid(form)

#----------------------------------------------------------------------------------------------------
#AQUI DEBE IR LA VISTA PARA ELIMINAR ENTRADAS DEL ÍNDICE
def delete_entrada_index(request, pk):
    """
    Vista basada en función para eliminar una entrada del índice.
    Requiere autenticación y solo permite al autor eliminar sus propias entradas.
    Utiliza SweetAlert2 para la confirmación (se maneja en el front-end).
    """
    # Obtener la entrada o devolver 404 si no existe o no pertenece al usuario
    entrada = get_object_or_404(EntradaIndex, id=pk, autor=request.user)
    
    # Solo permitir eliminación si el usuario está autenticado (redundante por LoginRequiredMixin en URL, pero buena práctica)
    if not request.user.is_authenticated:
        messages.error(request, 'Debes estar autenticado para realizar esta acción.')
        return redirect('list_entradas_index')
    
    titulo_entrada = entrada.titulo # Guarda el título antes de eliminar para el mensaje
    entrada.delete() # Elimina la entrada
    messages.success(request, f'La entrada "{titulo_entrada}" ha sido eliminada correctamente.') # Mensaje de confirmación
    return redirect('list_entradas_index') # Redirige a la lista de entradas del índice
#----------------------------------------------------------------------------------------------------

class CarruselIndexView(TemplateView):
    """
    Vista para mostrar las entradas destinadas al carrusel del índice.
    Actualmente, muestra las 3 entradas más recientes.
    """
    template_name = 'secciones/carrusel_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene las 3 entradas más recientes ordenadas por ID descendente
        context['entradas'] = EntradaIndex.objects.order_by('-id')[:3]
        return context

class EntradaIndexDetailView(TemplateView):
    """
    Vista para mostrar los detalles de una entrada específica del índice.
    """
    def get(self, request, entrada_id):
        try:
            entrada = EntradaIndex.objects.get(id=entrada_id)
            return render(request, 'secciones/detail_entrada_index.html', {'entrada': entrada})
        except EntradaIndex.DoesNotExist:
            return HttpResponse("Entrada no encontrada", status=404)

class ListEntradasIndexView(LoginRequiredMixin, ListView):
    """
    Vista para listar y paginar las entradas del índice.
    Permite filtrar por año y mes. Requiere autenticación.
    """
    model = EntradaIndex
    template_name = 'administracion/list_entradas_index.html'
    context_object_name = 'entradas'
    paginate_by = 6 # Número de entradas por página

    def get_queryset(self):
        queryset = EntradaIndex.objects.all()

        # Obtener parámetros de filtro de la URL (GET request)
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')

        # Aplicar filtros por año y mes usando .extra() para control directo SQL
        # Esto es para evitar problemas de zona horaria con funciones de Django si el motor DB es MySQL/MariaDB
        if year:
            try:
                year_int = int(year)
                # Filtra por el año de la fecha_creacion
                queryset = queryset.extra(
                    where=["YEAR(fecha_creacion) = %s"],
                    params=[year_int]
                )
            except (ValueError, TypeError):
                pass # Ignora valores inválidos

        if month:
            try:
                month_int = int(month)
                # Filtra por el mes de la fecha_creacion
                queryset = queryset.extra(
                    where=["MONTH(fecha_creacion) = %s"],
                    params=[month_int]
                )
            except (ValueError, TypeError):
                pass # Ignora valores inválidos

        # Ordenar las entradas por fecha de creación de forma descendente (más reciente primero)
        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el año actual
        año_actual = datetime.now().year
        
        # Obtener los años únicos de las entradas existentes para el filtro
        años_con_entradas = set()
        if EntradaIndex.objects.exists():
            # Obtiene las fechas únicas de creación (solo el año)
            años_query = EntradaIndex.objects.dates('fecha_creacion', 'year', order='DESC')
            for fecha in años_query:
                if fecha and fecha.year:
                    años_con_entradas.add(fecha.year)
        
        # Asegurarse de que el año actual siempre esté en la lista de años disponibles
        años_con_entradas.add(año_actual)
        años_lista = sorted(list(años_con_entradas), reverse=True) # Ordenar de más nuevo a más viejo

        # Preparar la lista de años para el contexto de la plantilla, indicando el año actual
        context['años'] = []
        for año in años_lista:
            context['años'].append({
                'year': año,
                'display': f'{año} (Año actual)' if año == año_actual else str(año),
                'is_current': año == año_actual
            })

        # Lista de meses para el filtro
        context['meses'] = [
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
            (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
            (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]

        # Mantener los valores de filtro seleccionados en el contexto
        context['selected_year'] = self.request.GET.get('year')
        context['selected_month'] = self.request.GET.get('month')
        
        # Convertir a entero si son dígitos válidos
        context['selected_year_int'] = int(context['selected_year']) if context['selected_year'] and context['selected_year'].isdigit() else None
        context['selected_month_int'] = int(context['selected_month']) if context['selected_month'] and context['selected_month'].isdigit() else None

        # Pasar los parámetros de filtro a la plantilla para mantenerlos en la paginación
        filter_params = {}
        if context['selected_year']:
            filter_params['year'] = context['selected_year']
        if context['selected_month']:
            filter_params['month'] = context['selected_month']
        context['filter_params'] = filter_params
        
        # Información adicional de paginación
        paginator = context.get('paginator')
        if paginator:
            context['total_entries'] = paginator.count
            context['entries_per_page'] = self.paginate_by
            
        return context






# --- VISTAS RELACIONADAS CON EL MODELO BlogEntrada ---
# Estas vistas gestionan la creación, lectura, actualización y eliminación (CRUD)
# de las entradas del blog.

class AddEntradaView(LoginRequiredMixin, CreateView):
    """
    Vista para la creación de nuevas entradas de blog.
    Requiere que el usuario esté autenticado.
    Asigna automáticamente al usuario logueado como autor.
    """
    model = BlogEntrada
    form_class = BlogEntradaForm
    template_name = 'secciones/add_entrada.html'
    success_url = reverse_lazy('list_entradas_blog') # Redirige a la lista de entradas del blog

    def form_valid(self, form):
        form.instance.autor = self.request.user # Asigna el usuario logueado como autor
        messages.success(self.request, '¡Entrada creada exitosamente!') # Mensaje de éxito
        return super().form_valid(form)

class UpdateEntradaBlogView(LoginRequiredMixin, UpdateView):
    """
    Vista para la modificación de entradas de blog existentes.
    Requiere autenticación y solo permite al autor modificar sus propias entradas.
    """
    model = BlogEntrada
    form_class = BlogEntradaForm
    template_name = 'secciones/update_entrada_blog.html'
    success_url = reverse_lazy('list_entradas_blog') # Redirige a la lista tras la actualización

    def get_queryset(self):
        # Asegura que solo el autor de la entrada pueda modificarla
        return BlogEntrada.objects.filter(autor=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, '¡Entrada modificada exitosamente!') # Mensaje de éxito
        return super().form_valid(form)

def delete_entrada_blog(request, pk):
    """
    Vista basada en función para eliminar una entrada de blog.
    Requiere autenticación y solo permite al autor eliminar sus propias entradas.
    Utiliza SweetAlert2 para la confirmación (se maneja en el front-end).
    """
    # Obtener la entrada o devolver 404 si no existe o no pertenece al usuario
    entrada = get_object_or_404(BlogEntrada, id=pk, autor=request.user)
    
    # Solo permitir eliminación si el usuario está autenticado (redundante por LoginRequiredMixin en URL, pero buena práctica)
    if not request.user.is_authenticated:
        messages.error(request, 'Debes estar autenticado para realizar esta acción.')
        return redirect('list_entradas_blog')
    
    titulo_entrada = entrada.titulo # Guarda el título antes de eliminar para el mensaje
    entrada.delete() # Elimina la entrada
    messages.success(request, f'La entrada "{titulo_entrada}" ha sido eliminada exitosamente.') # Mensaje de confirmación
    return redirect('list_entradas_blog') # Redirige al blog

class BlogGeneralView(ListView):
    """
    Vista general del blog, que muestra todas las entradas paginadas.
    Las entradas se ordenan por fecha de publicación descendente.
    """
    model = BlogEntrada
    template_name = 'secciones/blog.html'
    context_object_name = 'blog_entradas' # Nombre de la variable en el contexto para las entradas
    paginate_by = 6 # Número de entradas por página

    def get_queryset(self):
        # Ordenar las entradas por fecha de publicación de forma descendente
        return BlogEntrada.objects.all().order_by('-fecha_publicacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Información adicional de paginación (total de entradas, entradas por página)
        paginator = context.get('paginator')
        if paginator:
            context['total_entries'] = paginator.count
            context['entries_per_page'] = self.paginate_by
            
        return context

class BlogView(TemplateView):
    """
    Vista para mostrar una entrada específica del blog.
    Esta vista es funcional y usa un método 'get' para manejar la solicitud.
    """
    def get(self, request, entrada_id):
        try:
            entrada = BlogEntrada.objects.get(id=entrada_id) # Intenta obtener la entrada por ID
            return render(request, 'secciones/entrada_blog.html', {'entrada': entrada}) # Renderiza la plantilla con la entrada
        except BlogEntrada.DoesNotExist:
            return HttpResponse("Entrada no encontrada", status=404) # Devuelve un 404 si no encuentra la entrada

class BlogDetailView(TemplateView):
    """
    Vista para mostrar los detalles de una entrada específica del blog.
    Similar a BlogView, pero con una plantilla diferente ('detail_blog.html').
    """
    def get(self, request, entrada_id):
        try:
            entrada = BlogEntrada.objects.get(id=entrada_id) # Intenta obtener la entrada por ID
            return render(request, 'secciones/detail_blog.html', {'entrada': entrada}) # Renderiza la plantilla con la entrada
        except BlogEntrada.DoesNotExist:
            return HttpResponse("Entrada no encontrada", status=404) # Devuelve un 404 si no encuentra la entrada

class ListEntradasBlogView(LoginRequiredMixin, ListView):
    """
    Vista para listar y paginar las entradas del blog.
    Permite filtrar por año y mes. Requiere autenticación.
    """
    model = BlogEntrada
    template_name = 'administracion/list_entradas_blog.html'
    context_object_name = 'entradas'
    paginate_by = 6 # Número de entradas por página

    def get_queryset(self):
        queryset = BlogEntrada.objects.all()
        
        # Obtener parámetros de filtro de la URL (GET request)
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        
        # Aplicar filtros por año y mes usando .extra() para control directo SQL
        # Esto es para evitar problemas de zona horaria con funciones de Django si el motor DB es MySQL/MariaDB
        if year:
            try:
                year_int = int(year)
                # Filtra por el año de la fecha_publicacion
                queryset = queryset.extra(
                    where=["YEAR(fecha_publicacion) = %s"],
                    params=[year_int]
                )
            except (ValueError, TypeError):
                pass # Ignora valores inválidos
        
        if month:
            try:
                month_int = int(month)
                # Filtra por el mes de la fecha_publicacion
                queryset = queryset.extra(
                    where=["MONTH(fecha_publicacion) = %s"],
                    params=[month_int]
                )
            except (ValueError, TypeError):
                pass # Ignora valores inválidos
        
        # Ordenar las entradas por fecha de publicación de forma descendente (más reciente primero)
        return queryset.order_by('-fecha_publicacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el año actual
        año_actual = datetime.now().year
        
        # Obtener los años únicos de las entradas existentes para el filtro
        años_con_entradas = set()
        if BlogEntrada.objects.exists():
            # Obtiene las fechas únicas de publicación (solo el año)
            años_query = BlogEntrada.objects.dates('fecha_publicacion', 'year', order='DESC')
            for fecha in años_query:
                if fecha and fecha.year:
                    años_con_entradas.add(fecha.year)
        
        # Asegurarse de que el año actual siempre esté en la lista de años disponibles
        años_con_entradas.add(año_actual)
        años_lista = sorted(list(años_con_entradas), reverse=True) # Ordenar de más nuevo a más viejo
        
        # Preparar la lista de años para el contexto de la plantilla, indicando el año actual
        context['años'] = []
        for año in años_lista:
            context['años'].append({
                'year': año,
                'display': f'{año} (Año actual)' if año == año_actual else str(año),
                'is_current': año == año_actual
            })

        # Lista de meses para el filtro
        context['meses'] = [
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
            (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
            (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]

        # Mantener los valores de filtro seleccionados en el contexto
        context['selected_year'] = self.request.GET.get('year')
        context['selected_month'] = self.request.GET.get('month')
        
        # Convertir a entero si son dígitos válidos
        context['selected_year_int'] = int(context['selected_year']) if context['selected_year'] and context['selected_year'].isdigit() else None
        context['selected_month_int'] = int(context['selected_month']) if context['selected_month'] and context['selected_month'].isdigit() else None

        # Pasar los parámetros de filtro a la plantilla para mantenerlos en la paginación
        filter_params = {}
        if context['selected_year']:
            filter_params['year'] = context['selected_year']
        if context['selected_month']:
            filter_params['month'] = context['selected_month']
        context['filter_params'] = filter_params
        
        # Información adicional de paginación
        paginator = context.get('paginator')
        if paginator:
            context['total_entries'] = paginator.count
            context['entries_per_page'] = self.paginate_by
            
        return context