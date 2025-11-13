from django.test import TestCase
from .models import Estudiante

class EstudianteModelTest(TestCase):
    def test_crear_estudiante(self):
        e = Estudiante.objects.create(nombre='Juan', apellido='Perez', documento='123')
        self.assertEqual(str(e), 'Perez, Juan')
