from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import models
from .models import Estudiante, Curso, Profesor, Matricula 
from .forms import EstudianteForm, CursoForm, ProfesorForm, MatriculaForm # ⬅️ CORRECCIÓN 1: Se añadió ProfesorForm
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

# Estudiantes
class EstudianteListView(LoginRequiredMixin, ListView):
    model = Estudiante
    paginate_by = 10
    template_name = 'estudiantes/estudiante_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                models.Q(nombre__icontains=q) |
                models.Q(apellido__icontains=q) |
                models.Q(documento__icontains=q)
            )
        return queryset

class EstudianteDetailView(LoginRequiredMixin, DetailView):
    model = Estudiante
    template_name = 'estudiantes/estudiante_detail.html'

class EstudianteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'estudiantes/estudiante_form.html'
    permission_required = 'core.add_estudiante'
    success_url = reverse_lazy('estudiante_list')

class EstudianteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'estudiantes/estudiante_form.html'
    permission_required = 'core.change_estudiante'
    success_url = reverse_lazy('estudiante_list')

class EstudianteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Estudiante
    template_name = 'estudiantes/estudiante_confirm_delete.html'
    permission_required = 'core.delete_estudiante'
    success_url = reverse_lazy('estudiante_list')

# Cursos
class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    paginate_by = 10
    template_name = 'cursos/curso_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')

        if q:
            # Usamos Q para filtrar por Código, Nombre, o Nombre/Apellido del Profesor
            queryset = queryset.filter(
                Q(codigo__icontains=q) |
                Q(nombre__icontains=q) |
                Q(profesor__nombre__icontains=q) |
                Q(profesor__apellido__icontains=q) 
            ).distinct() 

        return queryset
        
class CursoDetailView(LoginRequiredMixin, DetailView):
    model = Curso
    template_name = 'cursos/curso_detail.html'

class CursoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    permission_required = 'core.add_curso'
    success_url = reverse_lazy('curso_list')

class CursoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    permission_required = 'core.change_curso'
    success_url = reverse_lazy('curso_list')

class CursoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Curso
    template_name = 'cursos/curso_confirm_delete.html'
    permission_required = 'core.delete_curso'
    success_url = reverse_lazy('curso_list')


# VISTA DE MATRÍCULA (NUEVA)
class MatriculaCreateView(LoginRequiredMixin, CreateView):
    model = Matricula
    form_class = MatriculaForm # Asume que esta clase existe en forms.py
    template_name = 'cursos/matricular_form.html'
    
    # 1. Obtener el curso usando el PK de la URL (kwargs['pk'])
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.curso = get_object_or_404(Curso, pk=self.kwargs['pk'])
        # Pasamos el curso al formulario para que filtre los estudiantes
        kwargs['curso'] = self.curso 
        return kwargs

    # 2. Pasar el curso al contexto para el template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = self.curso
        return context

    # 3. Asignar el curso al objeto antes de guardar
    def form_valid(self, form):
        form.instance.curso = self.curso
        return super().form_valid(form)

    # 4. Redirigir al detalle del curso
    def get_success_url(self):
        return reverse('curso_detail', kwargs={'pk': self.curso.pk})


# Profesores
class ProfesorListView(LoginRequiredMixin, ListView):
    model = Profesor
    template_name = 'profesores/profesor_list.html'

class ProfesorDetailView(LoginRequiredMixin, DetailView):
    model = Profesor
    template_name = 'profesores/profesor_detail.html'

class ProfesorCreateView(LoginRequiredMixin, CreateView):
    model = Profesor
    # ⬅️ CORRECCIÓN 2: Reemplazado 'fields' por 'form_class'
    form_class = ProfesorForm
    template_name = 'profesores/profesor_form.html'
    success_url = reverse_lazy('profesor_list')

class ProfesorUpdateView(LoginRequiredMixin, UpdateView):
    model = Profesor
    # ⬅️ CORRECCIÓN 3: Reemplazado 'fields' por 'form_class'
    form_class = ProfesorForm
    template_name = 'profesores/profesor_form.html'
    success_url = reverse_lazy('profesor_list')

class ProfesorDeleteView(LoginRequiredMixin, DeleteView):
    model = Profesor
    template_name = 'profesores/profesor_confirm_delete.html'
    success_url = reverse_lazy('profesor_list')