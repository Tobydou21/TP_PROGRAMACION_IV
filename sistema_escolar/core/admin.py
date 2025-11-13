from django.contrib import admin
from .models import Estudiante, Profesor, Curso, Matricula

# Personalización del Admin para Estudiante
@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de estudiantes
    list_display = ('apellido', 'nombre', 'documento', 'email', 'activo')
    # Campos por los que se puede filtrar la lista
    list_filter = ('activo', 'fecha_nacimiento')
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'apellido', 'documento', 'email')
    # Permite editar el campo 'activo' directamente desde la lista
    list_editable = ('activo',)
    # Mostrar la fecha de creación/actualización (opcional, si los tienes en el modelo)
    # readonly_fields = ('fecha_creacion',)


# Personalización del Admin para Curso
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'profesor', 'descripcion_corta')
    list_filter = ('profesor',)
    search_fields = ('nombre', 'codigo')

    # Función para mostrar una descripción corta en la lista
    def descripcion_corta(self, obj):
        # Trunca la descripción a 50 caracteres para la vista de lista
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'


# Personalización del Admin para Profesor
@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')
    search_fields = ('nombre', 'email')


# Registro simple para el modelo Matricula
@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'fecha', 'nota')
    list_filter = ('curso', 'fecha')
    search_fields = ('estudiante__apellido', 'curso__nombre')
