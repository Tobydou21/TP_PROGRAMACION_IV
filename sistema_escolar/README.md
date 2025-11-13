# Sistema Escolar - Proyecto Django (entrega exprés)

## Requisitos
- Python 3.10+ (vos tenés 3.14 — perfecto)
- pip

## Instalación y ejecución en Windows (PowerShell o CMD)
1. Abrir terminal en la carpeta descomprimida `sistema_escolar`
2. Crear entorno virtual:
   ```bash
   python -m venv .venv
   ```
3. Activar entorno:
   ```bash
   .venv\Scripts\activate
   ```
4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Copiar .env.example a .env:
   ```bash
   copy .env.example .env
   ```
6. Migrar base de datos y crear datos de ejemplo:
   ```bash
   python manage.py migrate
   python manage.py create_setup
   ```
7. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```

## Accesos de prueba
- admin / admin123 (superuser)
- staff / staff123 (usuario de grupo 'staff')

## URLs
- http://127.0.0.1:8000/  (app)
- http://127.0.0.1:8000/admin/  (panel admin)
