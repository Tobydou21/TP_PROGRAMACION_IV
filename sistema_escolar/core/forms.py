from django import forms
# AÑADIDO: Importar Profesor y Matricula
from .models import Estudiante, Curso, Profesor, Matricula

# 1. EstudianteForm (Con Datepicker "cheto")
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre','apellido','documento','email','fecha_nacimiento','activo']
        
        # AÑADIDO: Widgets para el Datepicker (type='date') y clases de Bootstrap
        widgets = {
            # Esto usa el selector de fecha nativo del navegador (el "datepicker cheto")
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    # MANTENIDA: Tu validación existente
    def clean_documento(self):
        doc = self.cleaned_data.get('documento')
        if not doc:
            raise forms.ValidationError("Documento obligatorio")
        return doc

# 2. ProfesorForm (Nuevo: para manejar 'apellido')
class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellido', 'email'] # Ya incluye 'apellido'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# 3. CursoForm (Actualizado con widgets por consistencia, mantiene fields)
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo','nombre','descripcion','profesor']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profesor': forms.Select(attrs={'class': 'form-select'}),
        }

# 4. MatriculaForm (Nuevo: para agregar alumnos a cursos)
class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['estudiante', 'nota'] 
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'placeholder': 'Nota inicial (opcional)'}),
        }
    
    # Filtra estudiantes que NO están matriculados en el curso actual
    def __init__(self, *args, **kwargs):
        self.curso = kwargs.pop('curso', None) 
        super().__init__(*args, **kwargs)
        
        if self.curso:
            # Obtiene los IDs de los estudiantes ya matriculados
            matriculados_ids = self.curso.matriculas.values_list('estudiante_id', flat=True)
            # Filtra el queryset de estudiantes excluyendo a los que ya tienen matrícula
            self.fields['estudiante'].queryset = Estudiante.objects.exclude(id__in=matriculados_ids).order_by('apellido')
            self.fields['estudiante'].label = "Seleccionar Alumno"
            self.fields['nota'].required = False