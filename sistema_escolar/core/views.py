from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.db import models
from .models import Estudiante, Curso, Profesor, Matricula 
from .forms import EstudianteForm, CursoForm, ProfesorForm, MatriculaForm
from django.db.models import Q
import csv
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime


def home(request):
    """
    Vista de página principal.
    
    Muestra los últimos 6 registros de estudiantes, cursos y profesores
    para dar una vista rápida del estado del sistema.
    """
    recent_students = Estudiante.objects.order_by('-id')[:6]
    recent_courses = Curso.objects.order_by('-id')[:6]
    recent_professors = Profesor.objects.order_by('-id')[:6]
    return render(request, 'home.html', {
        'recent_students': recent_students,
        'recent_courses': recent_courses,
        'recent_professors': recent_professors,
    })

# ============================================================================
# VISTAS DE ESTUDIANTES
# ============================================================================

class EstudianteListView(LoginRequiredMixin, ListView):
    """
    Vista de listado de estudiantes con búsqueda avanzada y exportación.
    
    Características:
        - Paginación: 10 registros por página
        - Búsqueda: Por nombre, apellido o documento (case-insensitive)
        - Exportación: CSV y PDF mediante ?export=csv y ?export=pdf
        - Autenticación: Requiere LoginRequiredMixin
    
    URLs:
        /estudiantes/ - Listado con paginación
        /estudiantes/?q=busca - Búsqueda filtrada
        /estudiantes/?export=csv - Descarga CSV
        /estudiantes/?export=pdf - Descarga PDF
    """
    model = Estudiante
    paginate_by = 10
    template_name = 'estudiantes/estudiante_list.html'

    def get_queryset(self):
        """
        Retorna queryset filtrado según parámetro de búsqueda 'q'.
        
        Búsqueda: Se filtra por nombre, apellido o documento con búsqueda
        case-insensitive usando Q objects de Django.
        
        Parámetro GET:
            q: Término de búsqueda
        
        Returns:
            QuerySet: Estudiantes filtrados o todos si no hay búsqueda
        """
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                models.Q(nombre__icontains=q) |
                models.Q(apellido__icontains=q) |
                models.Q(documento__icontains=q)
            )
        return queryset

    def get(self, request, *args, **kwargs):
        """Maneja solicitud GET: si export=csv, descarga CSV; si export=pdf, descarga PDF; si no, lista normal"""
        if request.GET.get('export') == 'csv':
            return self.export_csv()
        if request.GET.get('export') == 'pdf':
            return self.export_pdf()
        return super().get(request, *args, **kwargs)

    def export_csv(self):
        """Exporta todos los estudiantes a archivo CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="estudiantes.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Apellido', 'Documento', 'Email', 'Fecha de Nacimiento', 'Activo'])
        
        for estudiante in self.get_queryset():
            writer.writerow([
                estudiante.nombre,
                estudiante.apellido,
                estudiante.documento,
                estudiante.email,
                estudiante.fecha_nacimiento,
                'Sí' if estudiante.activo else 'No'
            ])
        
        return response

    def export_pdf(self):
        """Exporta todos los estudiantes a archivo PDF con tabla formateada"""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="estudiantes.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20,
            alignment=1
        )
        story.append(Paragraph('Reporte de Estudiantes', title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Datos para la tabla
        data = [['Nombre', 'Apellido', 'Documento', 'Email', 'F. Nacimiento', 'Activo']]
        for estudiante in self.get_queryset():
            data.append([
                estudiante.nombre,
                estudiante.apellido,
                estudiante.documento,
                estudiante.email,
                estudiante.fecha_nacimiento.strftime('%d/%m/%Y') if estudiante.fecha_nacimiento else '-',
                'Sí' if estudiante.activo else 'No'
            ])
        
        # Tabla con estilo
        table = Table(data, colWidths=[1.3*inch, 1.3*inch, 1.2*inch, 1.3*inch, 1.1*inch, 0.7*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        story.append(table)
        
        # Footer con fecha
        story.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
        story.append(Paragraph(f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', footer_style))
        
        doc.build(story)
        return response

class EstudianteDetailView(LoginRequiredMixin, DetailView):
    """
    Vista de detalle de estudiante con matrículas y cursos asociados.
    
    Muestra:
        - Datos completos del estudiante
        - Lista de todas sus matrículas
        - Información de cursos matriculados
        - Notas asignadas
    
    Optimización: Usa prefetch_related para evitar problema N+1 en queries.
    """
    model = Estudiante
    template_name = 'estudiantes/estudiante_detail.html'

    def get_queryset(self):
        """
        Retorna queryset optimizado con prefetch_related.
        
        Optimización: Carga matrículas y sus cursos asociados en una sola
        consulta adicional, evitando queries separadas por cada matrícula.
        
        Returns:
            QuerySet: Estudiantes con matrículas y cursos precargadas
        """
        return super().get_queryset().prefetch_related('matriculas__curso')

class EstudianteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Vista para crear un nuevo estudiante en el sistema.
    
    Requiere:
        - Estar autenticado (LoginRequiredMixin)
        - Tener permiso 'core.add_estudiante'
    
    Formulario: EstudianteForm con validación custom
    Campos: nombre, apellido, documento (único), email, fecha_nacimiento, activo
    Redirección exitosa: /estudiantes/ (lista de estudiantes)
    """
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'estudiantes/estudiante_form.html'
    permission_required = 'core.add_estudiante'
    success_url = reverse_lazy('estudiante_list')

class EstudianteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Vista para editar un estudiante existente.
    
    Requiere:
        - Estar autenticado
        - Tener permiso 'core.change_estudiante'
    
    Nota importante: El documento no puede modificarse (es único en BD)
    Redirección exitosa: /estudiantes/ (lista de estudiantes)
    """
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'estudiantes/estudiante_form.html'
    permission_required = 'core.change_estudiante'
    success_url = reverse_lazy('estudiante_list')

class EstudianteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Vista para eliminar un estudiante del sistema.
    
    Requiere:
        - Estar autenticado
        - Tener permiso 'core.delete_estudiante'
    
    Muestra página de confirmación antes de eliminar.
    Redirección exitosa: /estudiantes/ (lista de estudiantes)
    """
    model = Estudiante
    template_name = 'estudiantes/estudiante_confirm_delete.html'
    permission_required = 'core.delete_estudiante'
    success_url = reverse_lazy('estudiante_list')

# ============================================================================
# VISTAS DE CURSOS
# ============================================================================

class CursoListView(LoginRequiredMixin, ListView):
    """
    Vista de listado de cursos con búsqueda avanzada y exportación.
    
    Características:
        - Paginación: 10 registros por página
        - Búsqueda: Por código, nombre o profesor
        - Exportación: CSV y PDF mediante parámetros GET
        - Optimización: select_related('profesor') para evitar N+1
    
    URLs:
        /cursos/ - Listado completo
        /cursos/?q=busca - Búsqueda filtrada
        /cursos/?export=csv - Descarga CSV
        /cursos/?export=pdf - Descarga PDF
    """
    model = Curso
    paginate_by = 10
    template_name = 'cursos/curso_list.html'

    def get_queryset(self):
        """
        Retorna queryset filtrado y optimizado con select_related(profesor).
        
        Optimización: select_related('profesor') carga el profesor en la misma
        query que el curso, evitando una query adicional por cada curso.
        
        Búsqueda: Filtra por código, nombre o datos del profesor.
        
        Returns:
            QuerySet: Cursos filtrados con profesor precargado
        """
        queryset = super().get_queryset().select_related('profesor')
        q = self.request.GET.get('q')

        if q:
            # Búsqueda por múltiples campos: código, nombre o datos del profesor
            queryset = queryset.filter(
                Q(codigo__icontains=q) |
                Q(nombre__icontains=q) |
                Q(profesor__nombre__icontains=q) |
                Q(profesor__apellido__icontains=q) 
            ).distinct() 

        return queryset

    def get(self, request, *args, **kwargs):
        """Maneja solicitud GET: si export=csv, descarga CSV; si export=pdf, descarga PDF; si no, lista normal"""
        if request.GET.get('export') == 'csv':
            return self.export_csv()
        if request.GET.get('export') == 'pdf':
            return self.export_pdf()
        return super().get(request, *args, **kwargs)

    def export_csv(self):
        """Exporta todos los cursos a archivo CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cursos.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Código', 'Nombre', 'Profesor', 'Descripción'])
        
        for curso in self.get_queryset():
            writer.writerow([
                curso.codigo,
                curso.nombre,
                f"{curso.profesor.nombre} {curso.profesor.apellido}" if curso.profesor else "Sin profesor",
                curso.descripcion
            ])
        
        return response

    def export_pdf(self):
        """Exporta todos los cursos a archivo PDF con tabla formateada"""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cursos.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20,
            alignment=1
        )
        story.append(Paragraph('Reporte de Cursos', title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Datos para la tabla
        data = [['Código', 'Nombre', 'Profesor', 'Descripción']]
        for curso in self.get_queryset():
            profesor_nombre = f"{curso.profesor.nombre} {curso.profesor.apellido}" if curso.profesor else "Sin profesor"
            data.append([
                curso.codigo,
                curso.nombre,
                profesor_nombre,
                curso.descripcion[:50] + "..." if len(curso.descripcion) > 50 else curso.descripcion
            ])
        
        # Tabla con estilo
        table = Table(data, colWidths=[1*inch, 1.5*inch, 2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        story.append(table)
        
        # Footer con fecha
        story.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
        story.append(Paragraph(f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', footer_style))
        
        doc.build(story)
        return response
        
class CursoDetailView(LoginRequiredMixin, DetailView):
    """
    Vista de detalle de curso con estudiantes matriculados.
    
    Muestra:
        - Datos del curso (código, nombre, descripción)
        - Profesor asignado
        - Estudiantes matriculados
        - Notas de cada estudiante (si existen)
    
    Optimización: Usa select_related + prefetch_related para evitar N+1 queries
    """
    model = Curso
    template_name = 'cursos/curso_detail.html'

    def get_queryset(self):
        """
        Retorna queryset optimizado con select_related y prefetch_related.
        
        Optimizaciones:
            - select_related('profesor'): Carga profesor en primera query
            - prefetch_related('matriculas__estudiante'): Matrículas y estudiantes
        
        Returns:
            QuerySet: Cursos con profesor y matrículas precargadas
        """
        return super().get_queryset().select_related('profesor').prefetch_related('matriculas__estudiante')

class CursoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Vista para crear un nuevo curso en el sistema.
    
    Requiere:
        - Estar autenticado
        - Tener permiso 'core.add_curso'
    
    Campos: código (único), nombre, descripción, profesor (FK)
    Redirección exitosa: /cursos/ (lista de cursos)
    """
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    permission_required = 'core.add_curso'
    success_url = reverse_lazy('curso_list')

class CursoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Vista para editar un curso existente.
    
    Requiere:
        - Estar autenticado
        - Tener permiso 'core.change_curso'
    
    Nota: El código no puede modificarse (es único en BD)
    Redirección exitosa: /cursos/ (lista de cursos)
    """
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    permission_required = 'core.change_curso'
    success_url = reverse_lazy('curso_list')

class CursoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Vista para eliminar un curso del sistema.
    
    Requiere:
        - Estar autenticado
        - Tener permiso 'core.delete_curso'
    
    Muestra página de confirmación antes de eliminar.
    Redirección exitosa: /cursos/ (lista de cursos)
    """
    model = Curso
    template_name = 'cursos/curso_confirm_delete.html'
    permission_required = 'core.delete_curso'
    success_url = reverse_lazy('curso_list')


# ============================================================================
# VISTA DE MATRÍCULA
# ============================================================================

class MatriculaCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para matricular estudiantes en cursos.
    
    Características:
        - Filtra automáticamente estudiantes NO matriculados
        - Asigna el curso desde la URL
        - Valida que no exista matrícula duplicada
        - Guarda fecha de matrícula automáticamente
    
    URL: /cursos/<id>/matricular/
    Redirección exitosa: /cursos/<id>/ (detalle del curso)
    
    Lógica: El formulario recibe el curso_id de la URL y filtra
            los estudiantes que YA NO están matriculados en ese curso.
    """
    model = Matricula
    form_class = MatriculaForm
    template_name = 'cursos/matricular_form.html'
    
    def get_form_kwargs(self):
        """Obtiene el curso de la URL (kwargs['pk']) y lo pasa al formulario para filtrado"""
        kwargs = super().get_form_kwargs()
        self.curso = get_object_or_404(Curso, pk=self.kwargs['pk'])
        kwargs['curso'] = self.curso 
        return kwargs

    def get_context_data(self, **kwargs):
        """Pasa el curso al contexto para mostrar en el template"""
        context = super().get_context_data(**kwargs)
        context['curso'] = self.curso
        return context

    def form_valid(self, form):
        """Asigna automáticamente el curso seleccionado a la matrícula"""
        form.instance.curso = self.curso
        return super().form_valid(form)

    def get_success_url(self):
        """Redirige al detalle del curso tras guardar exitosamente"""
        return reverse('curso_detail', kwargs={'pk': self.curso.pk})


# ============================================================================
# VISTAS DE PROFESORES
# ============================================================================

class ProfesorListView(LoginRequiredMixin, ListView):
    """
    Vista de listado de todos los profesores del sistema.
    
    Características:
        - Listado completo sin búsqueda (tabla simple)
        - Exportación: CSV y PDF mediante ?export=csv y ?export=pdf
        - Muestra: Nombre, apellido, email
        - Acciones: Ver detalle, editar, eliminar
    
    URLs:
        /profesores/ - Listado completo
        /profesores/?export=csv - Descarga CSV
        /profesores/?export=pdf - Descarga PDF
    """
    model = Profesor
    template_name = 'profesores/profesor_list.html'

    def get(self, request, *args, **kwargs):
        """Maneja solicitud GET: si export=csv, descarga CSV; si export=pdf, descarga PDF; si no, lista normal"""
        if request.GET.get('export') == 'csv':
            return self.export_csv()
        if request.GET.get('export') == 'pdf':
            return self.export_pdf()
        return super().get(request, *args, **kwargs)

    def export_csv(self):
        """Exporta todos los profesores a archivo CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="profesores.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Apellido', 'Email'])
        
        for profesor in self.get_queryset():
            writer.writerow([
                profesor.nombre,
                profesor.apellido,
                profesor.email
            ])
        
        return response

    def export_pdf(self):
        """Exporta todos los profesores a archivo PDF con tabla formateada"""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="profesores.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20,
            alignment=1
        )
        story.append(Paragraph('Reporte de Profesores', title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Datos para la tabla
        data = [['Nombre', 'Apellido', 'Email']]
        for profesor in self.get_queryset():
            data.append([
                profesor.nombre,
                profesor.apellido,
                profesor.email
            ])
        
        # Tabla con estilo
        table = Table(data, colWidths=[2*inch, 2*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        story.append(table)
        
        # Footer con fecha
        story.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
        story.append(Paragraph(f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', footer_style))
        
        doc.build(story)
        return response

class ProfesorDetailView(LoginRequiredMixin, DetailView):
    """
    Vista de detalle de profesor con cursos que imparte.
    
    Muestra:
        - Datos del profesor (nombre, apellido, email)
        - Lista de cursos que imparte
        - Cantidad de estudiantes por curso
    
    Optimización: Usa prefetch_related para cargar cursos en una consulta
    """
    model = Profesor
    template_name = 'profesores/profesor_detail.html'

    def get_queryset(self):
        """
        Retorna queryset optimizado con prefetch_related.
        
        Optimización: Carga todos los cursos del profesor en una consulta
        adicional, en lugar de una query por cada curso.
        
        Returns:
            QuerySet: Profesores con cursos precargados
        """
        return super().get_queryset().prefetch_related('curso_set')

class ProfesorCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear un nuevo profesor en el sistema.
    
    Requiere: Estar autenticado
    
    Campos: nombre, apellido, email
    Redirección exitosa: /profesores/ (lista de profesores)
    """
    model = Profesor
    form_class = ProfesorForm
    template_name = 'profesores/profesor_form.html'
    success_url = reverse_lazy('profesor_list')

class ProfesorUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar un profesor existente.
    
    Requiere: Estar autenticado
    
    Redirección exitosa: /profesores/ (lista de profesores)
    """
    model = Profesor
    form_class = ProfesorForm
    template_name = 'profesores/profesor_form.html'
    success_url = reverse_lazy('profesor_list')

class ProfesorDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar un profesor del sistema.
    
    Requiere: Estar autenticado
    
    Muestra página de confirmación antes de eliminar.
    Redirección exitosa: /profesores/ (lista de profesores)
    """
    model = Profesor
    template_name = 'profesores/profesor_confirm_delete.html'
    success_url = reverse_lazy('profesor_list')