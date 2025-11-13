from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from core.models import Estudiante, Curso, Profesor, Matricula
from datetime import date
import random

class Command(BaseCommand):
    help = "Crea grupos, usuarios y datos de ejemplo (profesores, cursos, estudiantes, matrículas)."

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name='admin')
        staff_group, _ = Group.objects.get_or_create(name='staff')

        ct_models = [Estudiante, Curso]
        for ct in ct_models:
            content_type = ContentType.objects.get_for_model(ct)
            for perm in Permission.objects.filter(content_type=content_type):
                if perm.codename.startswith(('view_', 'add_', 'change_')):
                    staff_group.permissions.add(perm)
                else:
                    admin_group.permissions.add(perm)
        admin_group.permissions.set(Permission.objects.all())

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        if not User.objects.filter(username='staff').exists():
            u = User.objects.create_user('staff', 'staff@example.com', 'staff123')
            u.groups.add(staff_group)

        # Datos de ejemplo
        profesores = [Profesor.objects.create(nombre=f"Profesor {i}", email=f"prof{i}@mail.com") for i in range(1,4)]
        cursos = [
            Curso.objects.create(codigo=f"C{i:02}", nombre=f"Curso {i}", profesor=random.choice(profesores))
            for i in range(1,6)
        ]
        estudiantes = [
            Estudiante.objects.create(
                nombre=f"Nombre{i}",
                apellido=f"Apellido{i}",
                documento=f"{1000+i}",
                email=f"alumno{i}@mail.com",
                fecha_nacimiento=date(2000+i%5, random.randint(1,12), random.randint(1,28)),
                activo=True
            )
            for i in range(1,11)
        ]
        for e in estudiantes:
            for c in random.sample(cursos, 2):
                Matricula.objects.get_or_create(estudiante=e, curso=c)

        self.stdout.write(self.style.SUCCESS("Grupos, usuarios y datos de ejemplo creados con éxito."))
