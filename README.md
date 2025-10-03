# Paddle Challenge Community

Una plataforma web construida con Django para la comunidad de jugadores de Paddle Challenge, diseñada para integrarse con el juego desarrollado en Godot.

## Características

### 🔐 Sistema de Usuarios
- **Registro de usuarios** con información completa (nombre, email, fecha de nacimiento)
- **Autenticación** segura con login/logout
- **Perfiles extendidos** con avatar, estadísticas de juego y información personal
- **Sistema de niveles** y puntuaciones para gamificación

### 📝 Sistema de Blog
- **Posts categorizados** con imágenes destacadas
- **Sistema de comentarios** para fomentar la interacción
- **Búsqueda avanzada** en posts y categorías
- **Paginación** para mejor experiencia de usuario
- **Panel de administración** para gestionar contenido

### 👥 Comunidad
- **Lista de jugadores** con estadísticas visibles
- **Ranking de usuarios** por puntuación y nivel
- **Perfiles públicos** para conectar con otros jugadores

### 🎮 Preparado para Godot
- **API endpoints** listos para integración con juegos
- **Sistema de estadísticas** para tracking de partidas
- **Arquitectura escalable** para futuras funcionalidades

## Diseño y Colores

El proyecto utiliza una paleta de colores elegante y sofisticada:

- **🏆 Dorado**: Colores primarios para elementos destacados
- **🌰 Canela**: Tonos cálidos para acciones secundarias
- **⚫ Grises y Negros**: Base elegante para la navegación
- **🎨 Acentos**: Combinaciones armoniosas para una experiencia premium

## Tecnologías Utilizadas

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5.1.3 + Font Awesome
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción recomendado)
- **Autenticación**: Sistema Django integrado
- **Media**: Pillow para manejo de imágenes

## Instalación y Configuración

### Requisitos
- Python 3.8+
- Entorno virtual configurado

### Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "carpeta proyecto paddle challengue"
   ```

2. **Activar entorno virtual** (ya configurado)
   ```bash
   .venv\Scripts\activate
   ```

3. **Instalar dependencias** (ya instaladas)
   ```bash
   pip install django pillow
   ```

4. **Aplicar migraciones** (ya aplicadas)
   ```bash
   python manage.py migrate
   ```

5. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

## URLs Principales

- **Página principal**: http://localhost:8000/
- **Panel de administración**: http://localhost:8000/admin/
- **Blog**: http://localhost:8000/blog/
- **Registro**: http://localhost:8000/users/registro/
- **Login**: http://localhost:8000/accounts/login/
- **Lista de jugadores**: http://localhost:8000/users/jugadores/

## Credenciales de Admin

- **Usuario**: admin
- **Email**: admin@paddlechallenge.com
- **Contraseña**: admin123

## Estructura del Proyecto

```
paddle_web/
├── manage.py
├── paddle_web/          # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/               # App de usuarios
│   ├── models.py        # UserProfile
│   ├── views.py         # Registro, perfiles
│   ├── forms.py         # Formularios personalizados
│   ├── admin.py         # Admin personalizado
│   └── urls.py
├── blog/                # App de blog
│   ├── models.py        # Post, Categoria, Comentario
│   ├── views.py         # Lista, detalle, búsqueda
│   ├── forms.py         # Formulario de comentarios
│   ├── admin.py         # Admin con funciones avanzadas
│   └── urls.py
├── templates/           # Plantillas HTML
│   ├── base.html        # Plantilla base
│   ├── home.html        # Página principal
│   ├── users/           # Templates de usuarios
│   ├── blog/            # Templates del blog
│   └── registration/    # Templates de autenticación
├── static/              # Archivos estáticos (CSS, JS, imágenes)
└── media/               # Archivos subidos por usuarios
    ├── avatars/         # Fotos de perfil
    └── blog/           # Imágenes de posts
```

## Funcionalidades para el Futuro

### Integración con Godot
- API REST para estadísticas de juego
- Endpoints para actualizar puntuaciones
- Sistema de matchmaking
- Torneo online

### Mejoras de Comunidad
- Chat en tiempo real
- Foros de discusión
- Sistema de amigos
- Notificaciones push

### Funciones de Juego
- Replay de partidas
- Estadísticas avanzadas
- Logros y trofeos
- Temporadas competitivas

## Desarrollo

Para continuar el desarrollo:

1. **Agregar más campos al perfil** según necesidades del juego
2. **Crear API endpoints** para Godot
3. **Implementar sistema de torneos**
4. **Añadir notificaciones en tiempo real**
5. **Optimizar para producción** (PostgreSQL, Redis, etc.)

## Soporte

Para más información o soporte, contacta al desarrollador del proyecto.

---
*Desarrollado para la comunidad de Paddle Challenge - 2025*