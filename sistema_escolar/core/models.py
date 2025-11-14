from django.db import models

class Profesor(models.Model):
    """
    Modelo Profesor - Representa un docente en el sistema.
    
    Atributos:
        nombre (str): Nombre del profesor (máx 200 caracteres)
        apellido (str): Apellido del profesor con valor por defecto
        email (str): Email del profesor (opcional)
    """
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200, default='(sin apellido)') 
    email = models.EmailField(blank=True)

    def __str__(self):
        """Retorna la representación en string: 'Apellido, Nombre'"""
        return f"{self.apellido}, {self.nombre}"

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ['apellido', 'nombre']


class Curso(models.Model):
    """
    Modelo Curso - Representa un curso académico.
    
    Atributos:
        codigo (str): Código único del curso (máx 20 caracteres, ej: MAT001)
        nombre (str): Nombre del curso (máx 200 caracteres)
        descripcion (str): Descripción opcional del contenido del curso
        profesor (FK): Profesor asignado al curso (puede ser nulo)
    """
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """Retorna la representación en string: 'CODIGO - Nombre'"""
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['codigo']


class Estudiante(models.Model):
    """
    Modelo Estudiante - Representa un alumno del sistema.
    
    Atributos:
        nombre (str): Nombre del estudiante (máx 200 caracteres)
        apellido (str): Apellido del estudiante (máx 200 caracteres)
        documento (str): Documento de identidad único (ej: cédula, DNI)
        email (str): Email del estudiante (opcional)
        fecha_nacimiento (date): Fecha de nacimiento (opcional)
        activo (bool): Indica si el estudiante está activo en el sistema
    """
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    documento = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        """Retorna la representación en string: 'Apellido, Nombre'"""
        return f"{self.apellido}, {self.nombre}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['apellido', 'nombre']


class Matricula(models.Model):
    """
    Modelo Matricula - Relación many-to-many entre Estudiante y Curso.
    
    Atributos:
        estudiante (FK): Estudiante matriculado (CASCADE al eliminar)
        curso (FK): Curso en el que está matriculado (CASCADE al eliminar)
        fecha (date): Fecha de matrícula (auto_now_add: se establece al crear)
        nota (decimal): Nota del estudiante en el curso (0-10, opcional)
    
    Constraints:
        unique_together: Un estudiante no puede estar dos veces en el mismo curso
    """
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='matriculas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas')
    fecha = models.DateField(auto_now_add=True)
    nota = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('estudiante', 'curso')
        verbose_name = "Matricula"
        verbose_name_plural = "Matriculas"
        ordering = ['curso', 'estudiante']

    def __str__(self):
        """Retorna la representación en string: 'Estudiante -> Curso'"""
        return f"{self.estudiante} -> {self.curso}"
