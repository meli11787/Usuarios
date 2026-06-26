# Proyecto DCRM

Proyecto Django para gestionar registros de clientes.

## Correcciones realizadas

### 1. Error en `views.py`

El archivo `dcrm/website/views.py` tenia codigo duplicado pegado dentro de la funcion `home()`.

Eso provocaba un error de sintaxis parecido a:

```text
SyntaxError: invalid syntax
```

Se corrigio dejando las funciones separadas correctamente:

- `home`
- `login_user`
- `logout_user`
- `register_user`
- `customer_record`
- `delete_record`
- `update_record`

### 2. Error de paginacion

La paginacion no funcionaba porque el template enviaba el parametro:

```text
?page=2
```

pero la vista estaba buscando:

```python
request.GET.get("page_number")
```

Se corrigio en `dcrm/website/views.py` usando el mismo nombre del parametro:

```python
page_number = request.GET.get("page")
```

Tambien se ordenaron los registros antes de paginar:

```python
records = Record.objects.all().order_by("id")
```

Esto ayuda a que la paginacion sea estable.

### 3. Error con rutas `delete_record` y `update_record`

El template `record.html` usa estas rutas:

```django
{% url 'delete_record' customer_record.id %}
{% url 'update_record' customer_record.id %}
```

Para que funcionen, deben existir en `dcrm/website/urls.py`:

```python
path('delete_record/<str:pk>/', views.delete_record, name='delete_record'),
path('update_record/<str:pk>/', views.update_record, name='update_record'),
```

Estas rutas ya estan configuradas.

### 4. Correccion de `update_record.html`

El template `dcrm/website/templates/update_record.html` tenia etiquetas HTML sin cerrar correctamente.

Se corrigio cerrando el formulario y el contenedor:

```html
</form>
</div>
```

## Archivos modificados

- `dcrm/website/views.py`
- `dcrm/website/templates/update_record.html`
- `README.md`

## Verificacion

Se ejecuto:

```bash
entorno\Scripts\python.exe dcrm\manage.py check
```

Resultado:

```text
System check identified no issues (0 silenced).
```

## Como probar la paginacion

1. Iniciar el servidor:

```bash
entorno\Scripts\python.exe dcrm\manage.py runserver
```

2. Abrir el navegador en:

```text
http://127.0.0.1:8000/
```

3. Iniciar sesion.

4. Probar los botones de paginacion:

```text
?page=1
?page=2
?page=3
```

La vista debe mostrar 5 registros por pagina.

## Tutorial de paginacion

La paginacion del proyecto se divide en tres partes: la consulta ordenada, el paginador de Django y los enlaces del template.

### 1. Preparar los registros en la vista

En [`home()`](dcrm/website/views.py:16), la vista obtiene todos los registros del modelo `Record` y los ordena por `id` antes de paginar:

```python
records_queryset: QuerySet[Any] = Record.objects.all().order_by("id")
```

Ordenar antes de paginar es importante porque evita que los registros aparezcan en un orden impredecible cuando la base de datos devuelve los datos.

Luego se crea el paginador:

```python
paginator: Paginator = Paginator(records_queryset, 5)
```

El segundo argumento, `5`, define la cantidad de registros por pagina. Con este valor, si existen 12 registros, Django calcula automaticamente 3 paginas.

Despues se lee el parametro `page` desde la URL:

```python
page_number: str | None = request.GET.get("page")
```

Esto permite que la URL controle que pagina se muestra, por ejemplo:

```text
?page=1
?page=2
?page=3
```

Finalmente, la vista obtiene la pagina segura:

```python
records_page: Page = paginator.get_page(page_number)
```

`get_page()` es util porque no falla si el parametro no existe, si viene vacio o si contiene un valor invalido. En esos casos devuelve una pagina valida en lugar de lanzar un error.

### 2. Enviar la pagina al template

Al final de [`home()`](dcrm/website/views.py:16), la vista renderiza el template `home.html` y pasa la pagina calculada con el nombre `records`:

```python
return render(request, "home.html", {"records": records_page})
```

En el template, `records` no es una lista normal. Es un objeto `Page` de Django, por eso permite usar propiedades como:

- `records.has_previous`: indica si existe una pagina anterior.
- `records.previous_page_number`: numero de la pagina anterior.
- `records.has_next`: indica si existe una pagina siguiente.
- `records.next_page_number`: numero de la pagina siguiente.
- `records.number`: pagina actual.
- `records.paginator.num_pages`: total de paginas.
- `records.paginator.page_range`: rango de paginas disponibles.

### 3. Mostrar solo los registros de la pagina actual

En [`home.html`](dcrm/website/templates/home.html:388), el template valida que existan registros y recorre unicamente los registros de la pagina actual:

```django
{% if records %}
    {% for record in records %}
        ...
    {% endfor %}
{% else %}
    <tr>
        <td colspan="10" class="records-empty text-center">No hay registros disponibles.</td>
    </tr>
{% endif %}
```

Esto significa que la tabla nunca muestra todos los registros a la vez. Solo muestra los 5 registros que pertenecen a la pagina solicitada.

### 4. Entender los botones de paginacion

La seccion de paginacion esta en [`home.html`](dcrm/website/templates/home.html:411). Los botones funcionan con enlaces que cambian el parametro `page` de la URL.

Boton para ir a la primera pagina:

```django
<a href="?page=1">&laquo;</a>
```

Boton para ir a la pagina anterior:

```django
<a href="?page={{ records.previous_page_number }}">&lsaquo;</a>
```

Botones numerados cercanos a la pagina actual:

```django
{% for num in records.paginator.page_range %}
    {% if num >= records.number|add:'-2' and num <= records.number|add:'2' %}
        <a href="?page={{ num }}">{{ num }}</a>
    {% endif %}
{% endfor %}
```

La condicion `records.number|add:'-2'` y `records.number|add:'2'` muestra solo las dos paginas antes y despues de la pagina actual. Por ejemplo, si el usuario esta en la pagina 5, se muestran las paginas 3, 4, 5, 6 y 7.

Boton para ir a la pagina siguiente:

```django
<a href="?page={{ records.next_page_number }}">&rsaquo;</a>
```

Boton para ir a la ultima pagina:

```django
<a href="?page={{ records.paginator.num_pages }}">&raquo;</a>
```

### 5. Deshabilitar botones cuando no hay pagina

Cuando no hay pagina anterior, el template muestra los botones deshabilitados:

```django
<li class="page-item disabled">
    <span class="page-link">&laquo;</span>
</li>
```

Lo mismo ocurre cuando no hay pagina siguiente. Esto evita que el usuario intente navegar a una pagina que no existe.

### 6. Mostrar pagina actual y total

Al final del bloque de paginacion, el template muestra un texto informativo:

```django
<p>Página {{ records.number }} de {{ records.paginator.num_pages }}</p>
```

Ejemplo:

```text
Página 2 de 4
```

Esto confirma al usuario en que pagina esta y cuantas paginas existen en total.

### 7. Flujo completo

El flujo de la paginacion funciona asi:

1. El usuario abre `http://127.0.0.1:8000/`.
2. [`home()`](dcrm/website/views.py:16) consulta los registros ordenados por `id`.
3. Django divide los registros en grupos de 5.
4. La vista lee `?page=2` si existe en la URL.
5. Django devuelve la pagina correspondiente.
6. `home.html` muestra solo los registros de esa pagina.
7. Los botones cambian el parametro `page` para navegar entre paginas.

### 8. Cambiar la cantidad de registros por pagina

Para mostrar mas o menos registros por pagina, se debe modificar el segundo argumento del paginador en [`home()`](dcrm/website/views.py:16):

```python
Paginator(records_queryset, 5)
```

Ejemplos:

```python
Paginator(records_queryset, 10)
```

Muestra 10 registros por pagina.

```python
Paginator(records_queryset, 20)
```

Muestra 20 registros por pagina.

No es necesario cambiar el template cuando se modifica este valor, porque Django recalcula automaticamente el total de paginas y los botones de navegacion.
