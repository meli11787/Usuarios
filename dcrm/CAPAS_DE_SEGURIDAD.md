# CAPAS DE SEGURIDAD PARA EL PROYECTO DCRM

## Análisis de Seguridad del Proyecto

Este documento detalla las capas de seguridad identificadas en el proyecto Django DCRM, explicando cuáles se pueden aplicar, el por qué y la definición de cada capa.

---

## 1. CAPA DE AUTENTICACIÓN Y AUTORIZACIÓN

### Estado Actual
- El proyecto utiliza el sistema de autenticación de Django (`django.contrib.auth`)
- Las vistas `customer_record`, `delete_record` y `update_record` verifican `request.user.is_authenticated`
- **Problema identificado**: No hay control de permisos específicos (cualquier usuario autenticado puede ver, editar o eliminar cualquier registro)

### Recomendación
**Aplicar: Sí**

### Definición
La autenticación verifica la identidad del usuario, mientras que la autorización controla qué acciones puede realizar cada usuario. Django proporciona un sistema robusto de permisos basado en modelos.

### Implementación Recomendada
```python
# Usar decoradores @login_required y @permission_required
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('website.view_record', raise_exception=True)
def customer_record(request, pk):
    # ...

@login_required
@permission_required('website.delete_record', raise_exception=True)
def delete_record(request, pk):
    # ...
```

---

## 2. CAPA CSRF (CROSS-SITE REQUEST FORGERY)

### Estado Actual
- **Aplicado**: Los templates `register.html` y `update_record.html` incluyen `{% csrf_token %}`
- **Problema identificado**: El template `home.html` no muestra el formulario de login con CSRF visible, pero el código POST lo procesa

### Recomendación
**Aplicar: Sí (parcialmente implementado)**

### Definición
El CSRF protege contra ataques donde un sitio malicioso hace que el usuario realice acciones no deseadas en un sitio donde está autenticado. Django incluye protección CSRF mediante tokens únicos por sesión.

### Verificación
- El middleware `CsrfViewMiddleware` está habilitado en `settings.py` (línea 48)
- Se debe asegurar que TODOS los formularios POST incluyan `{% csrf_token %}`

---

## 3. CAPA DE PROTECCIÓN CONTRA CLICKJACKING

### Estado Actual
- **Aplicado**: El middleware `XFrameOptionsMiddleware` está habilitado (línea 51 en settings.py)

### Recomendación
**Aplicar: Sí (ya implementado)**

### Definición
Protege contra ataques de clickjacking donde un sitio malicioso inserta la aplicación en un iframe transparente para engañar al usuario. Django protege automáticamente con la cabecera `X-Frame-Options: DENY`.

---

## 4. CAPA DE VALIDACIÓN DE CONTRASEÑAS

### Estado Actual
- **Aplicado**: Los validadores de contraseña están configurados en `settings.py` (líneas 93-106)
- Incluye: UserAttributeSimilarityValidator, MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator

### Recomendación
**Aplicar: Sí (ya implementado)**

### Definición
Garantiza que las contraseñas cumplan con requisitos de complejidad (longitud mínima, no sean comunes, no sean completamente numéricas, etc.)

---

## 5. CAPA DE SEGURIDAD DE LA CLAVE SECRETA

### Estado Actual
- **Problema crítico**: La `SECRET_KEY` está hardcodeada en el archivo `settings.py` (línea 24)
- **Problema**: `DEBUG = True` en producción (línea 27)

### Recomendación
**Aplicar: Sí (requiere cambios urgentes)**

### Definición
La clave secreta se usa para firmar tokens de sesión, CSRF, contraseñas reset, etc. Si se expone, un atacante podría:
- Forgear tokens de sesión
- Crear contraseñas de restablecimiento falsos
- Comprometer toda la seguridad del sitio

### Implementación Recomendada
```python
# Usar variables de entorno
import os
from dotenv import load_dotenv

SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-por-defecto-solo-para-desarrollo')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

---

## 6. CAPA DE CABECERAS DE SEGURIDAD HTTP

### Estado Actual
- **No implementado**: Faltan cabeceras de seguridad adicionales

### Recomendación
**Aplicar: Sí**

### Definición
Las cabeceras HTTP de seguridad añaden protecciones adicionales contra varios tipos de ataques:

| Cabecera | Protección |
|----------|------------|
| `X-Content-Type-Options: nosniff` | Previene MIME type sniffing |
| `X-XSS-Protection` | Protección contra XSS (legacy browsers) |
| `Content-Security-Policy` | Previene XSS y carga de recursos externos no confiables |
| `Strict-Transport-Security` | Fuerza HTTPS |
| `Referrer-Policy` | Controla información de referencia |

### Implementación Recomendada
```python
# En settings.py
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True  # Solo en producción
```

---

## 7. CAPA DE CONTROL DE ACCESO A RECURSOS (PERMISOS POR OBJETO)

### Estado Actual
- **Problema**: Cualquier usuario autenticado puede ver/editar/eliminar cualquier registro
- No hay verificación de propiedad del registro

### Recomendación
**Aplicar: Sí**

### Definición
Control de acceso basado en el principio de "necesidad de conocimiento" - un usuario solo debe poder acceder a los recursos que le pertenecen o que está autorizado a ver.

### Implementación Recomendada
```python
def customer_record(request, pk):
    if request.user.is_authenticated:
        # Verificar que el usuario tiene permiso para ver este registro específico
        customer_record = get_object_or_404(Record, id=pk)
        # O agregar un campo 'owner' al modelo y verificar:
        # customer_record = get_object_or_404(Record, id=pk, owner=request.user)
```

---

## 8. CAPA DE RATE LIMITING (LIMITACIÓN DE PETICIONES)

### Estado Actual
- **No implementado**: No hay protección contra ataques de fuerza bruta

### Recomendación
**Aplicar: Sí**

### Definición
Limita la cantidad de peticiones que un usuario puede hacer en un período de tiempo, protegiendo contra:
- Ataques de fuerza bruta en login
- DoS (Denegación de Servicio)
- Spam en formularios

### Implementación Recomendada
```bash
pip install django-axes
```
O usar `django-ratelimit`:
```python
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True)
@ratelimit(key='ip', rate='5/m', block=True)
def login_user(request):
    # ...
```

---

## 9. CAPA DE VALIDACIÓN DE ENTRADA (INPUT VALIDATION)

### Estado Actual
- **Aplicado parcialmente**: Los formularios usan Django Forms con validación básica
- **Problema**: No hay validación de datos de entrada en el view `home` (acceso directo a `request.POST["username"]`)

### Recomendación
**Aplicar: Sí**

### Definición
Valida y sanitiza todos los datos de entrada para prevenir:
- Inyección SQL (Django ORM ya protege)
- XSS (Django templates ya escapan)
- Datos maliciosos o incompletos

### Problema identificado en `views.py` línea 17-18:
```python
# Código actual (vulnerable):
username = request.POST["username"]
password = request.POST["password"]

# Debería usar un formulario de login:
from django.contrib.auth.forms import AuthenticationForm
```

---

## 10. CAPA DE LOGGING Y MONITOREO

### Estado Actual
- **No implementado**: No hay registro de actividades sospechosas

### Recomendación
**Aplicar: Sí**

### Definición
Registra eventos de seguridad para detección de intrusiones y auditoría:
- Intentos de login fallidos
- Eliminaciones de registros
- Accesos no autorizados

### Implementación Recomendada
```python
# En settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

---

## 11. CAPA DE HTTPS Y SEGURO COOKIE SETTINGS

### Estado Actual
- **No implementado**: Configuración insegura para producción

### Recomendación
**Aplicar: Sí (para producción)**

### Definición
Garantiza que las comunicaciones sean encriptadas y que las cookies se transmitan de forma segura.

### Implementación Recomendada
```python
# En settings.py (producción)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## 12. CAPA DE PROTECCIÓN CONTRA BOTs (CAPTCHA)

### Estado Actual
- **No implementado**: Formulario de registro sin protección

### Recomendación
**Aplicar: Sí**

### Definición
Previene registros automatizados por bots, reduciendo spam y carga en el sistema.

### Implementación Recomendada
```bash
pip install django-recaptcha
```

---

## RESUMEN DE CAPAS APLICADAS vs RECOMENDADAS

| # | Capa de Seguridad | Estado | Prioridad |
|---|-------------------|--------|-----------|
| 1 | Autenticación/Autorización | ✅ **Implementado** | Alta |
| 2 | CSRF | Parcial | Alta |
| 3 | Clickjacking | Implementado | Media |
| 4 | Validación de contraseñas | Implementado | Media |
| 5 | Clave secreta | ❌ No | Crítica |
| 6 | Cabeceras HTTP | ❌ No | Alta |
| 7 | Control de acceso por objeto | Parcial | Alta |
| 8 | Rate Limiting | ❌ No | Alta |
| 9 | Validación de entrada | ✅ **Implementado** | Alta |
| 10 | Logging/Monitoreo | ❌ No | Media |
| 11 | HTTPS/Cookies seguras | ❌ No | Alta (producción) |
| 12 | CAPTCHA | ❌ No | Media |

---

## CAMBIOS IMPLEMENTADOS

### 1. Autenticación/Autorización (✅ Implementado)
Se agregaron los decoradores `@login_required` a las siguientes vistas:
- `customer_record` - Vista protegida para ver registros
- `delete_record` - Vista protegida para eliminar registros
- `update_record` - Vista protegida para actualizar registros
- `logout_user` - Vista protegida para cerrar sesión
- `register_user` - Vista protegida para registro de usuarios

**Por qué**: El decorador `@login_required` es la forma estándar de Django para asegurar que solo usuarios autenticados puedan acceder a ciertas vistas. Es más seguro y limpio que verificar manualmente `request.user.is_authenticated` en cada vista.

### 2. Validación de entrada (✅ Implementado)
Se modificó la vista `home` para usar `LoginForm` (AuthenticationForm) en lugar de acceder directamente a `request.POST`:
- Se agregó el formulario `LoginForm` en `forms.py`
- Se usa `form.is_valid()` para validar las credenciales
- Se usa `form.get_user()` para obtener el usuario autenticado

**Por qué**: Usar formularios de Django para el login proporciona:
- Validación automática de datos
- Protección CSRF integrada
- Manejo seguro de errores
- Prevención de inyección de código malicioso

### 3. Manejo seguro de objetos (✅ Implementado)
Se reemplazó `Record.objects.get(id=pk)` por `get_object_or_404(Record, id=pk)` en:
- `customer_record`
- `delete_record`
- `update_record`

**Por qué**: `get_object_or_404` maneja de forma segura los errores cuando un objeto no existe, retornando un error 404 en lugar de una excepción 500 que podría revelar información sensible del sistema.

---

## LISTA DE CHEQUEO - ARCHIVOS MODIFICADOS

| # | Archivo | Cambio Realizado | Capa de Seguridad |
|---|---------|-----------------|-------------------|
| 1 | `dcrm/website/views.py` | Agregado `@login_required` a vistas protegidas | 1, 7 |
| 2 | `dcrm/website/views.py` | Reemplazado `Record.objects.get()` por `get_object_or_404()` | 7 |
| 3 | `dcrm/website/views.py` | Modificado login para usar `LoginForm` con validación | 9 |
| 4 | `dcrm/website/forms.py` | Agregado `LoginForm` (AuthenticationForm) | 9 |

---

## RECOMENDACIONES INMEDIATAS

1. **URGENTE**: Cambiar `SECRET_KEY` a variable de entorno
2. **URGENTE**: Desactivar `DEBUG` en producción
3. **ALTA**: Configurar cabeceras de seguridad HTTP
4. **ALTA**: Implementar rate limiting en login
5. **MEDIA**: Agregar sistema de permisos por objeto
6. **MEDIA**: Implementar logging de seguridad

---

*Documento generado el: 2026-06-12*
*Proyecto: DCRM - Sistema de Gestión de Clientes*