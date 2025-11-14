from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Estudiante, Profesor, Curso, Matricula


class ModelTests(TestCase):
    def test_crear_estudiante_str(self):
        e = Estudiante.objects.create(nombre='Juan', apellido='Perez', documento='123')
        self.assertEqual(str(e), 'Perez, Juan')

    def test_profesor_curso_str(self):
        p = Profesor.objects.create(nombre='Ana', apellido='Gomez')
        c = Curso.objects.create(codigo='C001', nombre='Matemáticas', profesor=p)
        self.assertEqual(str(p), 'Gomez, Ana')
        self.assertEqual(str(c), 'C001 - Matemáticas')

    def test_matricula_unique_constraint(self):
        est = Estudiante.objects.create(nombre='Luis', apellido='Lopez', documento='999')
        prof = Profesor.objects.create(nombre='Doc', apellido='Torres')
        curso = Curso.objects.create(codigo='C100', nombre='Historia', profesor=prof)
        Matricula.objects.create(estudiante=est, curso=curso)
        # Intentar crear una matrícula duplicada debe fallar por unique_together
        with self.assertRaises(IntegrityError):
            Matricula.objects.create(estudiante=est, curso=curso)


class ViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='secret')
        self.client = Client()

    def test_estudiante_list_redirects_for_anonymous(self):
        url = reverse('estudiante_list')
        resp = self.client.get(url)
        # LoginRequiredMixin should redirect anonymous users to login
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp.url)

    def test_estudiante_list_shows_items_for_logged_in(self):
        Estudiante.objects.create(nombre='Carla', apellido='Sosa', documento='200')
        self.client.login(username='admin', password='secret')
        resp = self.client.get(reverse('estudiante_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Sosa')

    def test_estudiante_create_view_creates_when_user_has_permission(self):
        self.client.login(username='admin', password='secret')
        data = {
            'nombre': 'Miguel',
            'apellido': 'Diaz',
            'documento': '444',
            'email': 'm@example.com',
            'fecha_nacimiento': '2000-01-01',
            'activo': True,
        }
        resp = self.client.post(reverse('estudiante_add'), data)
        # Redirect on success to the list view
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Estudiante.objects.filter(documento='444').exists())
