# Sistema Escolar - Gestión Educativa 🎓

Un sistema web completo de gestión escolar desarrollado con Django 5.2, Bootstrap 5.3 y SQLite. Permite gestionar estudiantes, cursos, profesores y matrículas con interfaz responsive y autenticación integrada.

## Características Principales ✨

- 🎯 **CRUD Completo**: Gestión de estudiantes, cursos, profesores y matrículas
- 🔐 **Autenticación Multi-nivel**: Login/logout con permisos por rol (admin/staff)
- 🔍 **Búsqueda Avanzada**: Filtrado por múltiples campos con paginación
- 📱 **Interfaz Responsive**: Diseño mobile-first con Bootstrap 5.3
- 📊 **Dashboard Personalizado**: Visualización de últimos registros en home
- 📥 **Exportación de Datos**: Descarga en CSV y PDF de todos los listados
- 🎨 **Diseño Profesional**: Logo personalizado, tema consistente, UX optimizada
- 🌐 **Internacionalización**: Interfaz completa en español
- ✅ **Tests Unitarios**: Cobertura de modelos y vistas
- 🚀 **Deployment Ready**: Configuración segura con variables de entorno

## Estructura del Proyecto

```
sistema_escolar/
├── core/                          # App principal
│   ├── models.py                  # 4 modelos: Estudiante, Profesor, Curso, Matricula
│   ├── views.py                   # 14+ vistas basadas en clases (CBV)
│   ├── forms.py                   # Formularios con validación personalizada
│   ├── admin.py                   # Admin panel customizado
│   ├── urls.py                    # Rutas de la aplicación
│   ├── tests.py                   # Tests unitarios
│   ├── templates/
│   │   ├── base.html              # Template base con sidebar
│   │   ├── home.html              # Dashboard con tarjetas de estadísticas
│   │   ├── estudiantes/           # Templates para CRUD de estudiantes
│   │   ├── cursos/                # Templates para CRUD de cursos
│   │   └── profesores/            # Templates para CRUD de profesores
│   ├── management/
│   │   └── commands/
│   │       └── create_setup.py    # Comando para generar datos de prueba
│   └── migrations/                # Migraciones de base de datos
├── sistema_escolar/               # Configuración Django
│   ├── settings.py                # Configuración con soporte .env
│   ├── urls.py                    # URLs globales
│   ├── wsgi.py                    # WSGI para deployment
├── static/
│   └── logo.svg                   # Logo personalizado
├── .env.example                   # Plantilla de variables de entorno
├── requirements.txt               # Dependencias Python
├── manage.py                      # CLI de Django
└── db.sqlite3                     # Base de datos (no incluir en Git)
```

## Diagrama de Modelos

```
┌─────────────────┐
│   Estudiante    │
├─────────────────┤
│ id (PK)         │
│ nombre          │
│ apellido        │
│ documento (UK)  │
│ email           │
│ fecha_nac       │
│ activo (bool)   │
└────────┬────────┘
         │
         │ 1:N
         ├──────────────┐
         │              │
    ┌────▼────────────┐ │
    │   Matricula     │ │
    ├─────────────────┤ │
    │ id (PK)         │ │
    │ estudiante (FK) ◄─┘
    │ curso (FK)      ├──┐
    │ fecha           │  │
    │ nota            │  │
    └─────────────────┘  │
         ▲               │
         │ 1:N           │
         │               │
         ├───────────────┘
         │
    ┌────┴────────────┐
    │     Curso       │
    ├─────────────────┤
    │ id (PK)         │
    │ codigo (UK)     │
    │ nombre          │
    │ descripcion     │
    │ profesor (FK)   ├──┐
    └─────────────────┘  │
         ▲               │
         │ N:1           │
         │               │
    ┌────┴────────────┐
    │    Profesor     │
    ├─────────────────┤
    │ id (PK)         │
    │ nombre          │
    │ apellido        │
    │ email           │
    └─────────────────┘
```

## Funcionalidades Detalladas

### 1. Gestión de Estudiantes
- Crear, listar, editar y eliminar estudiantes
- Campos: nombre, apellido, documento (único), email, fecha de nacimiento, estado activo
- Búsqueda por nombre, apellido o documento
- Ver todas las matrículas de cada estudiante
- Exportar lista en CSV y PDF

### 2. Gestión de Cursos
- Crear, listar, editar y eliminar cursos
- Asignar profesor responsable
- Ver estudiantes matriculados en cada curso
- Búsqueda por código, nombre o profesor
- Exportar lista en CSV y PDF

### 3. Gestión de Profesores
- Crear, listar, editar y eliminar profesores
- Ver todos los cursos que imparte
- Exportar lista en CSV y PDF

### 4. Matrículas
- Matricular estudiantes en cursos
- Filtro automático: solo muestra estudiantes no matriculados
- Registro de fecha de matrícula
- Posibilidad de agregar notas (para futuros cálculos de promedios)

### 5. Autenticación y Permisos
- **Admin**: Acceso total a todas las funciones
- **Staff**: Acceso limitado a gestión (según permisos específicos)
- **Anónimo**: Acceso solo a login

## Tecnologías Utilizadas

- **Backend**: Django 5.2 (Python Web Framework)
- **Frontend**: Bootstrap 5.3, HTML5, CSS3
- **Base de Datos**: SQLite (configurable a PostgreSQL)
- **Servidor**: Django development server (manage.py runserver)
- **Autenticación**: Django Auth built-in
- **Exportación**: CSV (stdlib), PDF (ReportLab 4.0+)
- **Configuración**: python-dotenv para variables de entorno
- **Testing**: Django TestCase

## Instalación y Setup

### Requisitos
- Python 3.8+
- pip o conda
- Windows, macOS o Linux

### Pasos de Instalación (Windows PowerShell)

1. **Clonar el repositorio**
```powershell
git clone https://github.com/Tobydou21/TP_PROGRAMACION_IV.git
cd TP_PROGRAMACION_IV
```

2. **Entrar en la carpeta del proyecto**
```powershell
cd sistema_escolar
```
**⚠️ IMPORTANTE**: Todos los pasos siguientes deben ejecutarse DESDE dentro de la carpeta `sistema_escolar`

3. **Crear virtual environment**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. **Instalar dependencias**
```powershell
pip install -r requirements.txt
```

5. **Configurar variables de entorno**
```powershell
cp .env.example .env
# Editar .env si es necesario (opciones por defecto funcionan)
```

6. **Aplicar migraciones**
```powershell
python manage.py migrate
```

7. **Crear datos de prueba y usuarios**
```powershell
python manage.py create_setup
```

8. **Ejecutar servidor**
```powershell
python manage.py runserver
```

El sistema estará disponible en `http://127.0.0.1:8000`

## Credenciales de Prueba

| Usuario | Contraseña | Rol | Acceso |
|---------|-----------|-----|--------|
| admin | admin123 | Superuser | Total |
| staff | staff123 | Staff | Gestión limitada |

## URLs Principales

| Ruta | Descripción |
|------|-------------|
| `/` | Home / Dashboard |
| `/accounts/login/` | Login |
| `/estudiantes/` | Listado de estudiantes |
| `/estudiantes/add/` | Crear estudiante |
| `/estudiantes/<id>/` | Ver detalle estudiante |
| `/estudiantes/<id>/edit/` | Editar estudiante |
| `/estudiantes/<id>/delete/` | Eliminar estudiante |
| `/cursos/` | Listado de cursos |
| `/cursos/add/` | Crear curso |
| `/cursos/<id>/` | Ver detalle curso |
| `/cursos/<id>/matricular/` | Matricular estudiantes |
| `/profesores/` | Listado de profesores |
| `/profesores/add/` | Crear profesor |

### Exportación de Datos

Agregar `?export=csv` o `?export=pdf` a cualquier URL de listado:

```
/estudiantes/?export=csv      # Descargar estudiantes en CSV
/estudiantes/?export=pdf      # Descargar estudiantes en PDF
/cursos/?export=csv           # Descargar cursos en CSV
/profesores/?export=pdf       # Descargar profesores en PDF
```

## Tests

Ejecutar pruebas unitarias:

```powershell
python manage.py test core
```

Tests incluyen:
- ✓ Creación de modelos
- ✓ Validaciones de constraints
- ✓ Autenticación y permisos
- ✓ Funcionalidad de vistas

## Seguridad

- **CSRF Protection**: Token CSRF en todos los formularios
- **SQL Injection**: Protegido por ORM de Django
- **Session Management**: Cookies seguras (HTTPS ready)
- **SECRET_KEY**: Almacenado en .env (no en Git)
- **DEBUG Mode**: False por defecto en producción
- **Validación de Formularios**: Validación backend y frontend

## Variables de Entorno (.env)

```env
# Seguridad
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# HTTPS (producción)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
```

Ver `.env.example` para todas las opciones disponibles.

## Próximas Mejoras

- [ ] Notificaciones por email
- [ ] Dashboard con gráficos de estadísticas
- [ ] API REST con Django REST Framework
- [ ] Integración con más bases de datos
- [ ] Docker + Docker Compose
- [ ] Deployment en servidor cloud (Heroku, AWS)
- [ ] Autenticación OAuth2 (Google, GitHub)

## Problemas Comunes

### Error: "Module not found"
```powershell
pip install -r requirements.txt
```

Si al ejecutar `python manage.py migrate` recibes un error parecido a:

```
ModuleNotFoundError: No module named 'widget_tweaks'
```
significa que falta la dependencia `django-widget-tweaks` en el entorno virtual.

Solución rápida:

```powershell
# Asegúrate de activar el entorno virtual
.\.venv\Scripts\Activate.ps1
# Instala la librería faltante
pip install django-widget-tweaks
# O reinstala todas las dependencias listadas
pip install -r requirements.txt
```

Verifica que la librería quedó instalada:

```powershell
pip show django-widget-tweaks
```

Si aparece información del paquete, vuelve a ejecutar las migraciones:

```powershell
python manage.py migrate
```

### Error: "port 8000 already in use"
```powershell
python manage.py runserver 8001
```

### Error: "No such table"
```powershell
python manage.py migrate
```

## Estructura de Carpetas Explicada

- **core/**: Lógica principal de la aplicación
- **templates/**: Archivos HTML (respeta estructura de Django)
- **static/**: Archivos CSS, JS, imágenes
- **migrations/**: Cambios en la base de datos versionados
- **.env**: Variables sensibles (no incluir en Git)
- **requirements.txt**: Dependencias del proyecto

## Contribuciones

Proyecto de TP (Trabajo Práctico) para materia de Programación IV.

**Autor**: Tobydou21  
**Fecha**: Noviembre 2025  
**Licencia**: MIT

---

**Estado del Proyecto**: ✅ Funcional y documentado  
**Última actualización**: 14/11/2025  
**Versión**: 1.3
