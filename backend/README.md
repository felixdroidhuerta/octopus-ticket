# Octopus Helpdesk Backend (MySQL)

Este backend implementa un sistema de help desk similar a Jira con gestión de proyectos, tickets, wikis e inventario. Está desarrollado con **FastAPI** y **SQLAlchemy** usando **MySQL** como base de datos principal.

## 🚀 Requisitos

- Python 3.11+
- Servidor MySQL 8+
- Herramientas de línea de comandos (`pip`, `venv`)

## 📦 Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` para que `DATABASE_URL` apunte a tu instancia MySQL.

Crea la base de datos si aún no existe:

```sql
CREATE DATABASE helpdesk CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'helpdesk'@'%' IDENTIFIED BY 'helpdesk';
GRANT ALL PRIVILEGES ON helpdesk.* TO 'helpdesk'@'%';
FLUSH PRIVILEGES;
```

## ▶️ Ejecutar el servidor

```bash
uvicorn app.main:app --reload --port 8001
```

La API estará disponible en `http://localhost:8001` y la documentación interactiva en `http://localhost:8001/docs`.

## 👤 Usuario administrador inicial

En el arranque se crea automáticamente el usuario admin configurado en `.env` (`FIRST_SUPERUSER_EMAIL` y `FIRST_SUPERUSER_PASSWORD`). Cambia esta contraseña en producción.

## 🧩 Funcionalidades principales

- Autenticación con JWT y verificación opcional de dos factores
- Gestión de usuarios y roles (ADMIN, JEFE_PROYECTO, USUARIO, VISUALIZADOR)
- CRUD de proyectos, tickets, wikis e inventario
- Estadísticas del dashboard (totales y tickets por estado)

## 🔐 Seguridad y buenas prácticas

- Usa contraseñas robustas y cambia la `SECRET_KEY`
- Restringe el acceso a la base de datos por IP
- Habilita 2FA para administradores y jefes de proyecto
- Configura HTTPS en despliegues productivos

## 🧪 Pruebas

Puedes generar datos de prueba ejecutando solicitudes contra la API con herramientas como `curl`, `httpie` o Postman. Asegúrate de crear proyectos antes de crear tickets o wikis.
