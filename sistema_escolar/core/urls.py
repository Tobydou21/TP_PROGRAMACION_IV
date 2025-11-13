from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Estudiantes
    path('estudiantes/', views.EstudianteListView.as_view(), name='estudiante_list'),
    path('estudiantes/add/', views.EstudianteCreateView.as_view(), name='estudiante_add'),
    path('estudiantes/<int:pk>/', views.EstudianteDetailView.as_view(), name='estudiante_detail'),
    path('estudiantes/<int:pk>/edit/', views.EstudianteUpdateView.as_view(), name='estudiante_edit'),
    path('estudiantes/<int:pk>/delete/', views.EstudianteDeleteView.as_view(), name='estudiante_delete'),

    # Cursos
    path('cursos/', views.CursoListView.as_view(), name='curso_list'),
    path('cursos/add/', views.CursoCreateView.as_view(), name='curso_add'),
    path('cursos/<int:pk>/', views.CursoDetailView.as_view(), name='curso_detail'),
    path('cursos/<int:pk>/edit/', views.CursoUpdateView.as_view(), name='curso_edit'),
    path('cursos/<int:pk>/delete/', views.CursoDeleteView.as_view(), name='curso_delete'),

    # Profesores
 path('profesores/', views.ProfesorListView.as_view(), name='profesor_list'),
 path('profesores/<int:pk>/', views.ProfesorDetailView.as_view(), name='profesor_detail'),
 path('profesores/nuevo/', views.ProfesorCreateView.as_view(), name='profesor_add'),
 path('profesores/<int:pk>/editar/', views.ProfesorUpdateView.as_view(), name='profesor_edit'),
 path('profesores/<int:pk>/borrar/', views.ProfesorDeleteView.as_view(), name='profesor_delete'),
]
   