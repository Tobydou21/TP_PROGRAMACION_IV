from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import models
from .models import Estudiante, Curso, Profesor
from .forms import EstudianteForm, CursoForm
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
# Reemplaza tu CursoListView con este código en views.py
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
                Q(profesor__apellido__icontains=q) # Se agregó el apellido del profesor
            ).distinct() # Añade .distinct() para evitar duplicados si un profesor coincide dos veces

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

class ProfesorListView(LoginRequiredMixin, ListView):
    model = Profesor
    template_name = 'profesores/profesor_list.html'

class ProfesorDetailView(LoginRequiredMixin, DetailView):
    model = Profesor
    template_name = 'profesores/profesor_detail.html'

class ProfesorCreateView(LoginRequiredMixin, CreateView):
    model = Profesor
    fields = ['nombre', 'email']
    template_name = 'profesores/profesor_form.html'
    success_url = reverse_lazy('profesor_list')

class ProfesorUpdateView(LoginRequiredMixin, UpdateView):
    model = Profesor
    fields = ['nombre', 'email']
    template_name = 'profesores/profesor_form.html'
    success_url = reverse_lazy('profesor_list')

class ProfesorDeleteView(LoginRequiredMixin, DeleteView):
    model = Profesor
    template_name = 'profesores/profesor_confirm_delete.html'
    success_url = reverse_lazy('profesor_list')