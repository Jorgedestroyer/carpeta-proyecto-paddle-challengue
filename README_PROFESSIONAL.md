# 🏓 Paddle Challenge Community

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)
![API](https://img.shields.io/badge/API-REST-orange.svg)

## 📖 Descripción

**Paddle Challenge Community** es una plataforma web completa diseñada para jugadores de paddle, que combina funcionalidades de comunidad, gestión de perfiles, blog y una API REST para integración con juegos desarrollados en Godot.

## ✨ Funcionalidades Principales

### 🎮 **Para Jugadores**
- **Sistema de Registro y Autenticación** completo
- **Perfiles Personalizables** con estadísticas detalladas
- **Sistema de Logros** con badges visuales
- **Leaderboard Global** con rankings
- **Blog Comunitario** para compartir experiencias
- **Panel de Estadísticas** en tiempo real

### 🔧 **Para Desarrolladores**
- **API REST completa** con autenticación JWT
- **Integración con Godot** mediante HTTPRequest
- **Endpoints** para usuarios, logros y partidas
- **Documentación de API** incluida

### 🎨 **Diseño y UX**
- **Interfaz Moderna** con animaciones CSS profesionales
- **Paleta de Colores Personalizada** (dorado, canela, grises)
- **Responsive Design** optimizado para móviles
- **Efectos Hover** y transiciones suaves

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.13+
- pip (incluido con Python)

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd "carpeta proyecto paddle challengue"
```

### 2. Crear Entorno Virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias
```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### 4. Configurar Base de Datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 6. Generar Datos de Prueba (Opcional)
```bash
python generate_demo_data.py
```

### 7. Ejecutar Servidor
```bash
python manage.py runserver
```

## 📱 Uso de la Aplicación

### Acceso Web
- **URL Principal:** http://127.0.0.1:8000/
- **Panel Admin:** http://127.0.0.1:8000/admin/
- **API Base:** http://127.0.0.1:8000/api/

### Usuarios Demo
Si ejecutaste `generate_demo_data.py`, tienes estos usuarios disponibles:
- **carlos_pro** / paddle123 (Nivel 5)
- **ana_gamer** / paddle123 (Nivel 4)
- **miguel_rookie** / paddle123 (Nivel 3)
- **sofia_champ** / paddle123 (Nivel 5)
- **pedro_casual** / paddle123 (Nivel 2)

## 🔌 API REST - Integración con Godot

### Autenticación JWT
```http
POST /api/token/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_password"
}
```

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/user/` | Información del usuario autenticado |
| `GET` | `/api/user/logros/` | Logros del usuario |
| `POST` | `/api/user/logros/` | Asignar nuevo logro |
| `GET` | `/api/user/partidas/` | Partidas del usuario |
| `POST` | `/api/user/partidas/` | Registrar nueva partida |

### Ejemplo de Integración en Godot

```gdscript
extends Node

var api_url = "http://127.0.0.1:8000/api/"
var jwt_token = ""

func login(username: String, password: String):
    var http_request = HTTPRequest.new()
    add_child(http_request)
    
    var body = JSON.stringify({"username": username, "password": password})
    var headers = ["Content-Type: application/json"]
    
    http_request.request(api_url + "token/", headers, HTTPClient.METHOD_POST, body)
    
func get_user_stats():
    var http_request = HTTPRequest.new()
    add_child(http_request)
    
    var headers = [
        "Content-Type: application/json",
        "Authorization: Bearer " + jwt_token
    ]
    
    http_request.request(api_url + "user/", headers, HTTPClient.METHOD_GET)
```

## 🏗️ Estructura del Proyecto

```
paddle_challenge/
├── 📁 api/                    # API REST
│   ├── views.py              # Endpoints de la API
│   ├── serializers.py        # Serializers para modelos
│   └── urls.py               # Rutas de la API
├── 📁 blog/                  # Sistema de blog
│   ├── models.py             # Modelo Post
│   └── views.py              # Vistas del blog
├── 📁 users/                 # Sistema de usuarios
│   ├── models.py             # UserProfile, Logros, Partidas
│   ├── views.py              # Vistas de usuarios
│   └── templates/            # Templates de usuario
├── 📁 templates/             # Templates globales
│   ├── base.html             # Template base
│   └── home.html             # Página principal
├── 📁 static/                # Archivos estáticos
│   └── css/
│       └── paddle-challenge.css  # Estilos personalizados
├── manage.py                 # Script de Django
├── generate_demo_data.py     # Generador de datos de prueba
└── requirements.txt          # Dependencias
```

## 🎯 Características Técnicas

### Backend
- **Framework:** Django 5.2.6
- **Base de Datos:** SQLite3 (desarrollo)
- **API:** Django REST Framework
- **Autenticación:** JWT (Simple JWT)

### Frontend
- **CSS Framework:** Bootstrap 5.1.3
- **Iconos:** Font Awesome 6.0
- **Animaciones:** CSS3 personalizadas
- **Responsive:** Mobile-first design

### Funcionalidades Avanzadas
- **Sistema de Logros** con fecha y tracking
- **Leaderboard** dinámico por puntuación
- **Dashboard** con estadísticas en tiempo real
- **Blog** con sistema de posts y autores
- **API REST** completa para integración externa

## 📊 Estadísticas del Proyecto

- **Modelos de Datos:** 6 (User, UserProfile, Post, Logro, LogroUsuario, Partida)
- **Endpoints API:** 5 principales + autenticación
- **Templates:** 10+ páginas responsivas
- **Líneas de Código:** 2000+ líneas
- **Funcionalidades:** 15+ características principales

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Jorge Torres**
- Proyecto: Paddle Challenge Community
- Curso: Desarrollo Web con Django

## 🙏 Agradecimientos

- [Django](https://www.djangoproject.com/) - Framework web
- [Bootstrap](https://getbootstrap.com/) - CSS Framework
- [Font Awesome](https://fontawesome.com/) - Iconos
- [Godot Engine](https://godotengine.org/) - Motor de juegos

---

⭐ **¡Proyecto listo para entrega!** ⭐