from django import forms
from .models import Estudiante, Curso

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre','apellido','documento','email','fecha_nacimiento','activo']

    def clean_documento(self):
        doc = self.cleaned_data.get('documento')
        if not doc:
            raise forms.ValidationError("Documento obligatorio")
        return doc

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo','nombre','descripcion','profesor']
