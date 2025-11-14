# Sistema Escolar - Proyecto Integrador Django

**Proyecto académico de gestión escolar** desarrollado con Django, Bootstrap 5 y bases de datos relacional.

## 📋 Descripción

Sistema web de gestión integral para instituciones educativas. Permite administrar estudiantes, profesores, cursos y matrículas con autenticación, permisos por roles y panel administrativo personalizado.

### ✨ Características

- **Gestión de Estudiantes**: CRUD completo, búsqueda avanzada, estado activo/inactivo
- **Gestión de Profesores**: Registro y edición de docentes asignados a cursos
- **Gestión de Cursos**: Creación de cursos con descripción, código único, profesor asignado
- **Sistema de Matrículas**: Asignación de estudiantes a cursos con seguimiento de notas
- **Autenticación**: Login/Logout con Django Auth, permisos granulares por rol
- **Interfaz Responsiva**: Diseño Mobile-First con Bootstrap 5, funciona en móvil y desktop
- **Panel Admin Personalizado**: Django Admin con filtros, búsqueda y edición inline
- **Búsqueda Avanzada**: Filtros por múltiples campos usando Q objects
- **Paginación**: Listados paginados para mejor rendimiento
- **Internacionalización**: Interfaz en español, zona horaria Paraguay

---

## 🏗️ Estructura del Proyecto

```
sistema_escolar/
├── core/
│   ├── models.py           # Modelos: Estudiante, Profesor, Curso, Matricula
│   ├── views.py            # Vistas CBV: CRUD, búsqueda, matriculación
│   ├── forms.py            # Formularios ModelForm con validaciones
│   ├── urls.py             # Rutas de la aplicación
│   ├── admin.py            # Admin personalizado
│   ├── templates/          # Templates con herencia
│   │   ├── base.html       # Plantilla base con sidebar
│   │   ├── home.html       # Página principal con tarjetas
│   │   ├── estudiantes/    # Templates de estudiantes
│   │   ├── cursos/         # Templates de cursos
│   │   └── profesores/     # Templates de profesores
│   └── tests.py            # Tests unitarios
├── sistema_escolar/
│   ├── settings.py         # Configuración (seguridad, BD, apps)
│   ├── urls.py             # URLs raíz
│   └── wsgi.py             # WSGI para producción
├── manage.py               # Comando Django
├── requirements.txt        # Dependencias
├── .env.example            # Variables de entorno (ejemplo)
└── db.sqlite3              # Base de datos SQLite
```

---

## 🗄️ Modelos de Datos

```
Estudiante (30 atributos base)
├── nombre
├── apellido
├── documento (único)
├── email
├── fecha_nacimiento
└── activo (boolean)
    └─→ Matricula (many-to-many vía)

Profesor (50 atributos base)
├── nombre
├── apellido
├── email
└─→ Curso (one-to-many)

Curso (50 atributos base)
├── codigo (único)
├── nombre
├── descripcion
├── profesor (FK)
└─→ Matricula (many-to-many vía)

Matricula (junction table)
├── estudiante (FK)
├── curso (FK)
├── fecha
├── nota
└── unique_together (estudiante, curso)
```

---

## 🚀 Requisitos

- Python 3.10+
- pip
- Windows/Linux/macOS

---

## 📦 Instalación y Ejecución

### 1. Clonar/descargar el repositorio
```bash
cd sistema_escolar
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
```

### 3. Activar entorno (Windows PowerShell)
```bash
.venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno
```bash
copy .env.example .env
```
*(Opcional: editar `.env` para cambiar DEBUG, SECRET_KEY, etc.)*

### 6. Aplicar migraciones y crear datos
```bash
python manage.py migrate
python manage.py create_setup
```

### 7. Ejecutar servidor
```bash
python manage.py runserver
```

La aplicación estará disponible en: **http://127.0.0.1:8000/**

---

## 🔐 Credenciales de Prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Superuser (acceso total) |
| staff | staff123 | Staff (permisos limitados) |

---

## 🌐 URLs Principales

| URL | Descripción |
|-----|-------------|
| `/` | Página principal (home) con últimos registros |
| `/admin/` | Panel administrativo Django |
| `/estudiantes/` | Listado de estudiantes |
| `/estudiantes/add/` | Crear nuevo estudiante |
| `/estudiantes/<id>/` | Detalle de estudiante |
| `/estudiantes/<id>/edit/` | Editar estudiante |
| `/estudiantes/<id>/delete/` | Eliminar estudiante |
| `/cursos/` | Listado de cursos |
| `/cursos/add/` | Crear nuevo curso |
| `/cursos/<id>/matricular/` | Asignar estudiantes a curso |
| `/profesores/` | Listado de profesores |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |

---

## 🎨 Interfaz

- **Sidebar responsivo**: Navegación vertical con iconos Bootstrap
- **Bootstrap 5.3**: Componentes modernos (cards, badges, forms)
- **Logo personalizado**: SVG educativo en favicon
- **Color scheme**: Azul (#3498db) + acentos naranja (#f39c12)
- **Mobile-first**: Adapta a pantallas <768px

---

## 🔐 Seguridad

- ✅ CSRF protection en formularios
- ✅ LoginRequiredMixin en todas las vistas
- ✅ PermissionRequiredMixin para CRUD
- ✅ DEBUG=False en producción (configurable vía .env)
- ✅ SECRET_KEY en variables de entorno
- ✅ HTTPS ready (SECURE_SSL_REDIRECT, HSTS configurables)
- ✅ Validación de formularios
- ✅ Permisos granulares (add/change/delete por modelo)

---

## 🧪 Tests

Ejecutar tests unitarios:
```bash
python manage.py test core
```

Tests incluyen:
- Creación de modelos
- Validación de constraints (unique, unique_together)
- Vistas CBV (acceso autenticado, permisos)
- Formularios y validaciones

---

## 📝 Documentación Adicional

- **Vistas**: Class-Based Views para mejor mantenibilidad
- **Formularios**: ModelForms con validación custom
- **Admin**: Personalizado con filtros, búsqueda, edición inline
- **Settings**: Configuración modularizada con .env

---

## 🚦 Estado del Proyecto

| Componente | Estado |
|-----------|--------|
| Funcionalidad | ✅ Completa |
| Autenticación | ✅ Implementada |
| Interfaz | ✅ Responsiva |
| Admin | ✅ Personalizado |
| Tests | ✅ Base |
| Documentación | ⚠️ En progreso |

---

## 📌 Notas

- Base de datos: SQLite (ideal para desarrollo, cambiar a PostgreSQL en producción)
- Zona horaria: America/Asuncion (Paraguay)
- Idioma: Español (es)

---

## 📄 Licencia

Proyecto académico - Año 2025

---

**Desarrollado con ❤️ usando Django + Bootstrap**
