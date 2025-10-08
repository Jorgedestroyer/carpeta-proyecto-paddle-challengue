# 🐍 Guía completa para desplegar en PythonAnywhere

## 📋 Pasos para desplegar tu aplicación Django en PythonAnywhere

### **1. Crear cuenta en PythonAnywhere**
- Ve a [pythonanywhere.com](https://www.pythonanywhere.com)
- Crea una cuenta gratuita (Beginner account)
- Inicia sesión en tu dashboard

### **2. Subir tu código**

**Opción A: Desde GitHub (Recomendado)**
```bash
# En la consola de PythonAnywhere
cd ~
git clone https://github.com/Jorgedestroyer/carpeta-proyecto-paddle-challengue.git mysite
cd mysite
```

**Opción B: Subir archivos manualmente**
- Usa el "Files" tab en PythonAnywhere
- Sube todos los archivos del proyecto a `/home/yourusername/mysite/`

### **3. Configurar base de datos MySQL**
- En tu dashboard, ve a "Databases"
- Crea una nueva base de datos MySQL: `yourusername$paddle_db`
- Anota la contraseña que te genere

### **4. Configurar variables de entorno**
Crea un archivo `.env` en `/home/yourusername/mysite/` con:
```
# PythonAnywhere Configuration
PYTHONANYWHERE_DOMAIN=1
DEBUG=False
SECRET_KEY=django-insecure-v38o%7wh0mzv4lv(ba=eh7oyc7ht)qc32=jv&vu0y9bqo)u%#6

# Database MySQL
PA_DB_NAME=yourusername$paddle_db
PA_DB_USER=yourusername
PA_DB_PASSWORD=tu_contraseña_mysql
PA_DB_HOST=yourusername.mysql.pythonanywhere-services.com
```

### **5. Instalar dependencias**
```bash
# En la consola de PythonAnywhere
cd ~/mysite
pip3.10 install --user -r requirements.txt
```

### **6. Configurar Django**
```bash
# Migrar base de datos
python3.10 manage.py migrate

# Recopilar archivos estáticos
python3.10 manage.py collectstatic --noinput

# Crear superusuario
python3.10 manage.py createsuperuser
```

### **7. Configurar aplicación web**

1. **Ve a la pestaña "Web"** en tu dashboard
2. **Crear nueva app**: Click "Add a new web app"
3. **Selecciona**: "Manual configuration" (not Django!)
4. **Python version**: Python 3.10
5. **Click "Next"**

### **8. Configurar archivos**

**A. WSGI Configuration**
- Click en el enlace del archivo WSGI
- Reemplaza todo el contenido con:
```python
import os
import sys

# Agregar el directorio del proyecto
path = '/home/yourusername/mysite'  # ¡Cambiar 'yourusername' por tu usuario!
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'paddle_web.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**B. Static Files**
En la sección "Static files" de la pestaña Web:
- **URL**: `/static/` **Directory**: `/home/yourusername/mysite/staticfiles`
- **URL**: `/media/` **Directory**: `/home/yourusername/mysite/media`

**C. Source Code**
- **Source code**: `/home/yourusername/mysite`
- **Working directory**: `/home/yourusername/mysite`

### **9. Reload y probar**
- Click "Reload yourusername.pythonanywhere.com"
- Ve a tu URL: `https://yourusername.pythonanywhere.com`

### **🎉 ¡Tu aplicación estará funcionando!**

**URLs importantes:**
- **Sitio principal**: `https://yourusername.pythonanywhere.com`
- **Admin**: `https://yourusername.pythonanywhere.com/admin`
- **API**: `https://yourusername.pythonanywhere.com/api`

### **🔧 Solución de problemas comunes**

**Error 502**: Revisa el log de errores en la pestaña Web
**Base de datos**: Verifica las credenciales MySQL
**Archivos estáticos**: Ejecuta `collectstatic` de nuevo
**Permisos**: Asegúrate de que todos los archivos estén en el lugar correcto

### **📝 Notas importantes**
- La cuenta gratuita tiene limitaciones de CPU y storage
- Se suspende después de 3 meses de inactividad
- Para dominios personalizados necesitas cuenta pagada
- Soporte para HTTPS incluido automáticamente