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
    Lunes,  # Importa los modelos de los días de la semana
    Martes,
    Miercoles,
    Jueves,
    Viernes,
    Sabado,
    Domingo
)

# Importar los forms necesarios
from .forms import (
    EntradaIndexForm,
    BlogEntradaForm,
    LunesForm,  # Importa los formularios de los días de la semana
    MartesForm,
    MiercolesForm,
    JuevesForm,
    ViernesForm,
    SabadoForm,
    DomingoForm
)

# --- VISTAS GENERALES Y DE SECCIONES ESTÁTICAS ---
# En views.py, modificar la clase IndexView para incluir los programas semanales

class IndexView(TemplateView):
    """
    Vista principal (Home) del sitio.
    Muestra indicadores económicos, las 3 entradas más recientes
    del modelo EntradaIndex, los formularios de programación semanal
    y la programación semanal completa.
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

        # Añadir los formularios de programación semanal al contexto
        context['form_lunes'] = LunesForm()
        context['form_martes'] = MartesForm()
        context['form_miercoles'] = MiercolesForm()
        context['form_jueves'] = JuevesForm()
        context['form_viernes'] = ViernesForm()
        context['form_sabado'] = SabadoForm()
        context['form_domingo'] = DomingoForm()

        # *** NUEVA SECCIÓN: Añadir programación semanal ***
        # Obtener todos los programas de cada día ordenados por hora de inicio
        context['programas_lunes'] = Lunes.objects.all().order_by('hora_inicio')
        context['programas_martes'] = Martes.objects.all().order_by('hora_inicio')
        context['programas_miercoles'] = Miercoles.objects.all().order_by('hora_inicio')
        context['programas_jueves'] = Jueves.objects.all().order_by('hora_inicio')
        context['programas_viernes'] = Viernes.objects.all().order_by('hora_inicio')
        context['programas_sabado'] = Sabado.objects.all().order_by('hora_inicio')
        context['programas_domingo'] = Domingo.objects.all().order_by('hora_inicio')

        return context
#------------------------------------------------------------------------------------------------------------------------

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
# AQUI DEBE IR LA VISTA PARA ELIMINAR ENTRADAS DEL ÍNDICE
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

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# VISTAS PARA LA PROGRAMACIÓN SEMANAL (CreateView para cada día)

class AddProgramaLunes(LoginRequiredMixin, CreateView):
    """
    Vista para agregar un programa para el Lunes.
    Requiere que el usuario esté autenticado.
    """
    model = Lunes
    form_class = LunesForm
    template_name = 'programacion_semanal/add_programa_lunes.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Captura el 'return_day' del parámetro GET, si no existe, por defecto es 'lunes'
        context['return_day'] = self.request.GET.get('return_day', 'lunes') 
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Lunes agregado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        # Usar el return_day que se pasó en la URL al ir a la página de agregar
        return_day = self.request.GET.get('return_day', 'lunes') 
        return reverse_lazy('list_programacion') + f'?day={return_day}'


class AddProgramaMartes(LoginRequiredMixin, CreateView):
    """
    Vista para agregar un programa para el Martes.
    Requiere que el usuario esté autenticado.
    """
    model = Martes
    form_class = MartesForm
    template_name = 'programacion_semanal/add_programa_martes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'martes') 
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Martes agregado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'martes')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

class AddProgramaMiercoles(LoginRequiredMixin, CreateView):
    """
    Vista para agregar un programa para el Miércoles.
    Requiere que el usuario esté autenticado.
    """
    model = Miercoles
    form_class = MiercolesForm
    template_name = 'programacion_semanal/add_programa_miercoles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'miercoles')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Miércoles agregado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'miercoles')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

class AddProgramaJueves(LoginRequiredMixin, CreateView):
    """
    Vista para agregar un programa para el Jueves.
    Requiere que el usuario esté autenticado.
    """
    model = Jueves
    form_class = JuevesForm
    template_name = 'programacion_semanal/add_programa_jueves.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'jueves')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Jueves agregado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'jueves')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

class AddProgramaViernes(LoginRequiredMixin, CreateView):
    """
    Vista para agregar un programa para el Viernes.
    Requiere que el usuario esté autenticado.
    """
    model = Viernes
    form_class = ViernesForm
    template_name = 'programacion_semanal/add_programa_viernes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'viernes')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Viernes agregado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'viernes')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

class AddProgramaSabado(LoginRequiredMixin, CreateView):
    """
    Vista para agregar un programa para el Sábado.
    Requiere que el usuario esté autenticado.
    """
    model = Sabado
    form_class = SabadoForm
    template_name = 'programacion_semanal/add_programa_sabado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'sabado')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Sábado agregado correctamente!')
        return super().form_valid(form)

    def get_success_url(self,):
        return_day = self.request.GET.get('return_day', 'sabado')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

class AddProgramaDomingo(LoginRequiredMixin, CreateView):
    """
    Vista para agregar un programa para el Domingo.
    Requiere que el usuario esté autenticado.
    """
    model = Domingo
    form_class = DomingoForm
    template_name = 'programacion_semanal/add_programa_domingo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'domingo')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Domingo agregado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'domingo')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

# ----------------------------------------------------------------------------------------------------------------------------------------------------


# VISTA PARA LISTAR LA PROGRAMACIÓN SEMANAL

class ListProgramacionSemanal(LoginRequiredMixin, TemplateView):
    """
    Vista para listar la programación semanal completa, con opción de filtrar por día.
    Requiere que el usuario esté autenticado.
    """
    template_name = 'administracion/list_programacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Diccionario para almacenar los programas de cada día
        programas_por_dia = {
            'lunes': Lunes.objects.all().order_by('hora_inicio'),
            'martes': Martes.objects.all().order_by('hora_inicio'),
            'miercoles': Miercoles.objects.all().order_by('hora_inicio'),
            'jueves': Jueves.objects.all().order_by('hora_inicio'),
            'viernes': Viernes.objects.all().order_by('hora_inicio'),
            'sabado': Sabado.objects.all().order_by('hora_inicio'),
            'domingo': Domingo.objects.all().order_by('hora_inicio'),
        }
        context['programas_por_dia'] = programas_por_dia

        # Lista de días de la semana para el filtro
        dias_semana = [
            {'value': 'lunes', 'display': 'Lunes'},
            {'value': 'martes', 'display': 'Martes'},
            {'value': 'miercoles', 'display': 'Miércoles'},
            {'value': 'jueves', 'display': 'Jueves'},
            {'value': 'viernes', 'display': 'Viernes'},
            {'value': 'sabado', 'display': 'Sábado'},
            {'value': 'domingo', 'display': 'Domingo'},
            {'value': 'todos', 'display': 'Todos los días'} # Opción para ver todos
        ]
        context['dias_semana'] = dias_semana

        # Obtener el día seleccionado del parámetro GET
        # Si no hay 'day' en GET, intenta obtener 'return_day' (si se vino de un 'add_programa'),
        # de lo contrario, por defecto es 'lunes'.
        selected_day = self.request.GET.get('day', self.request.GET.get('return_day', 'lunes'))
        context['selected_day'] = selected_day

        # Preparar los programas a mostrar según el día seleccionado
        if selected_day == 'todos':
            context['programas_activos'] = programas_por_dia # Pasa el diccionario completo
        else:
            context['programas_activos'] = {selected_day: programas_por_dia.get(selected_day, [])}


        return context
    


#--------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------
# VISTAS UPDATE PARA LA PROGRAMACIÓN SEMANAL (UpdateView para cada día)

class UpdateProgramaLunes(LoginRequiredMixin, UpdateView):
    """
    Vista para modificar un programa de Lunes existente.
    Requiere autenticación.
    """
    model = Lunes
    form_class = LunesForm
    template_name = 'programacion_semanal/update_programa_lunes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Captura el 'return_day' del parámetro GET, si no existe, por defecto es 'lunes'
        context['return_day'] = self.request.GET.get('return_day', 'lunes')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Lunes modificado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        # Usar el return_day que se pasó en la URL al ir a la página de modificar
        return_day = self.request.GET.get('return_day', 'lunes')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class UpdateProgramaMartes(LoginRequiredMixin, UpdateView):
    """
    Vista para modificar un programa de Martes existente.
    Requiere autenticación.
    """
    model = Martes
    form_class = MartesForm
    template_name = 'programacion_semanal/update_programa_martes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'martes')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Martes modificado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'martes')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class UpdateProgramaMiercoles(LoginRequiredMixin, UpdateView):
    """
    Vista para modificar un programa de Miércoles existente.
    Requiere autenticación.
    """
    model = Miercoles
    form_class = MiercolesForm
    template_name = 'programacion_semanal/update_programa_miercoles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'miercoles')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Miércoles modificado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'miercoles')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class UpdateProgramaJueves(LoginRequiredMixin, UpdateView):
    """
    Vista para modificar un programa de Jueves existente.
    Requiere autenticación.
    """
    model = Jueves
    form_class = JuevesForm
    template_name = 'programacion_semanal/update_programa_jueves.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'jueves')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Jueves modificado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'jueves')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class UpdateProgramaViernes(LoginRequiredMixin, UpdateView):
    """
    Vista para modificar un programa de Viernes existente.
    Requiere autenticación.
    """
    model = Viernes
    form_class = ViernesForm
    template_name = 'programacion_semanal/update_programa_viernes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'viernes')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Viernes modificado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'viernes')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class UpdateProgramaSabado(LoginRequiredMixin, UpdateView):
    """
    Vista para modificar un programa de Sábado existente.
    Requiere autenticación.
    """
    model = Sabado
    form_class = SabadoForm
    template_name = 'programacion_semanal/update_programa_sabado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'sabado')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Sábado modificado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'sabado')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class UpdateProgramaDomingo(LoginRequiredMixin, UpdateView):
    """
    Vista para modificar un programa de Domingo existente.
    Requiere autenticación.
    """
    model = Domingo
    form_class = DomingoForm
    template_name = 'programacion_semanal/update_programa_domingo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_day'] = self.request.GET.get('return_day', 'domingo')
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Programa de Domingo modificado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return_day = self.request.GET.get('return_day', 'domingo')
        return reverse_lazy('list_programacion') + f'?day={return_day}'

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# VISTAS DELETE PARA LA PROGRAMACIÓN SEMANAL (Funciones de eliminación para cada día)

def delete_programa_lunes(request, pk):
    """
    Vista para eliminar un programa del día Lunes.
    Redirige al mismo día si aún hay programas, o a la vista de todos los días si no quedan.
    """
    programa = get_object_or_404(Lunes, pk=pk)
    dia_actual = 'lunes'
    programa.delete()
    messages.success(request, f'El programa del día {dia_actual} ha sido eliminado correctamente.')
    if Lunes.objects.count() > 0:
        # Redirigir al mismo día si hay registros restantes
        return redirect(f"{reverse_lazy('list_programacion')}?day={dia_actual}")
    else:
        # Redirigir a "todos los días" si no quedan registros
        return redirect('list_programacion')

def delete_programa_martes(request, pk):
    """
    Vista para eliminar un programa del día Martes.
    Redirige al mismo día si aún hay programas, o a la vista de todos los días si no quedan.
    """
    programa = get_object_or_404(Martes, pk=pk)
    dia_actual = 'martes'
    programa.delete()
    messages.success(request, f'El programa del día {dia_actual} ha sido eliminado correctamente.')
    if Martes.objects.count() > 0:
        # Redirigir al mismo día si hay registros restantes
        return redirect(f"{reverse_lazy('list_programacion')}?day={dia_actual}")
    else:
        # Redirigir a "todos los días" si no quedan registros
        return redirect('list_programacion')

def delete_programa_miercoles(request, pk):
    """
    Vista para eliminar un programa del día Miercoles.
    Redirige al mismo día si aún hay programas, o a la vista de todos los días si no quedan.
    """
    programa = get_object_or_404(Miercoles, pk=pk)
    dia_actual = 'miercoles'
    programa.delete()
    messages.success(request, f'El programa del día {dia_actual} ha sido eliminado correctamente.')
    if Miercoles.objects.count() > 0:
        # Redirigir al mismo día si hay registros restantes
        return redirect(f"{reverse_lazy('list_programacion')}?day={dia_actual}")
    else:
        # Redirigir a "todos los días" si no quedan registros
        return redirect('list_programacion')

def delete_programa_jueves(request, pk):
    """
    Vista para eliminar un programa del día Jueves.
    Redirige al mismo día si aún hay programas, o a la vista de todos los días si no quedan.
    """
    programa = get_object_or_404(Jueves, pk=pk)
    dia_actual = 'jueves'
    programa.delete()
    messages.success(request, f'El programa del día {dia_actual} ha sido eliminado correctamente.')
    if Jueves.objects.count() > 0:
        # Redirigir al mismo día si hay registros restantes
        return redirect(f"{reverse_lazy('list_programacion')}?day={dia_actual}")
    else:
        # Redirigir a "todos los días" si no quedan registros
        return redirect('list_programacion')

def delete_programa_viernes(request, pk):
    """
    Vista para eliminar un programa del día Viernes.
    Redirige al mismo día si aún hay programas, o a la vista de todos los días si no quedan.
    """
    programa = get_object_or_404(Viernes, pk=pk)
    dia_actual = 'viernes'
    programa.delete()
    messages.success(request, f'El programa del día {dia_actual} ha sido eliminado correctamente.')
    if Viernes.objects.count() > 0:
        # Redirigir al mismo día si hay registros restantes
        return redirect(f"{reverse_lazy('list_programacion')}?day={dia_actual}")
    else:
        # Redirigir a "todos los días" si no quedan registros
        return redirect('list_programacion')

def delete_programa_sabado(request, pk):
    """
    Vista para eliminar un programa del día Sábado.
    Redirige al mismo día si aún hay programas, o a la vista de todos los días si no quedan.
    """
    programa = get_object_or_404(Sabado, pk=pk)
    dia_actual = 'sabado'
    programa.delete()
    messages.success(request, f'El programa del día {dia_actual} ha sido eliminado correctamente.')
    if Sabado.objects.count() > 0:
        # Redirigir al mismo día si hay registros restantes
        return redirect(f"{reverse_lazy('list_programacion')}?day={dia_actual}")
    else:
        # Redirigir a "todos los días" si no quedan registros
        return redirect('list_programacion')

def delete_programa_domingo(request, pk):
    """
    Vista para eliminar un programa del día Domingo.
    Redirige al mismo día si aún hay programas, o a la vista de todos los días si no quedan.
    """
    programa = get_object_or_404(Domingo, pk=pk)
    dia_actual = 'domingo'
    programa.delete()
    messages.success(request, f'El programa del día {dia_actual} ha sido eliminado correctamente.')
    if Domingo.objects.count() > 0:
        # Redirigir al mismo día si hay registros restantes
        return redirect(f"{reverse_lazy('list_programacion')}?day={dia_actual}")
    else:
        # Redirigir a "todos los días" si no quedan registros
        return redirect('list_programacion')
