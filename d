# dcrm/website/views.py
from typing import Any  # Importa Any para tipos genéricos cuando Django no expone tipos específicos.
from django.contrib import messages  # Importa el sistema de mensajes flash de Django.
from django.contrib.auth import authenticate, login, logout  # Importa funciones de autenticación de Django.
from django.contrib.auth.decorators import login_required  # Importa el decorador para proteger vistas.
from django.contrib.auth.models import AnonymousUser, User  # Importa modelos de usuario para anotaciones.
from django.core.paginator import Page, Paginator  # Importa paginador y tipo de página.
from django.db.models import QuerySet  # Importa QuerySet para tipar consultas de modelos.
from django.http import HttpRequest, HttpResponse  # Importa tipos de petición y respuesta HTTP.
from django.shortcuts import get_object_or_404, redirect, render  # Importa helpers de respuesta corta.

from .forms import LoginForm, RecordForm, UserRegisterForm  # Importa formularios usados por las vistas.
from .models import Record  # Importa el modelo Record usado como cliente o registro.


def home(request: HttpRequest) -> HttpResponse:  # Define la vista principal que lista registros y maneja login.
    records_queryset: QuerySet[Record] = Record.objects.all().order_by("id")  # Obtiene todos los registros ordenados por ID.
    paginator: Paginator = Paginator(records_queryset, 5)  # Crea un paginador de cinco registros por página.
    page_number: str | None = request.GET.get("page")  # Lee el número de página desde el parámetro GET page.
    records_page: Page[Record] = paginator.get_page(page_number)  # Obtiene la página segura para el número solicitado.

    if request.method == "POST":  # Evalúa si la petición envió datos por formulario POST.
        form: LoginForm = LoginForm(request, data=request.POST)  # Crea el formulario de login con la petición y datos POST.
        if form.is_valid():  # Valida credenciales, CSRF y datos del formulario de login.
            user: User | AnonymousUser = form.get_user()  # Obtiene el usuario autenticado desde el formulario.
            login(request, user)  # Inicia sesión en Django asociando el usuario a la petición actual.
            messages.success(request, "Acceso realizado exitosamente")  # Muestra mensaje de ingreso correcto.
            return redirect("home")  # Redirige a la página principal tras iniciar sesión.
        messages.error(request, "Las credenciales no son validas")  # Muestra mensaje cuando el login falla.

    return render(request, "home.html", {"records": records_page})  # Renderiza la plantilla home con la página de registros.


def login_user(request: HttpRequest) -> HttpResponse:  # Define la vista dedicada para iniciar sesión.
    if request.method == "POST":  # Evalúa si el usuario envió el formulario de login por POST.
        form: LoginForm = LoginForm(request, data=request.POST)  # Crea el formulario de login con la petición actual.
        if form.is_valid():  # Valida credenciales y datos del formulario de login.
            user: User | AnonymousUser = form.get_user()  # Obtiene el usuario autenticado desde el formulario.
            login(request, user)  # Inicia sesión en Django para el usuario autenticado.
            messages.success(request, "Acceso realizado exitosamente")  # Muestra mensaje de ingreso correcto.
            return redirect("home")  # Redirige a la página principal tras iniciar sesión.
        messages.error(request, "Las credenciales no son validas")  # Muestra mensaje cuando el login falla.
    else:  # Para peticiones GET se muestra el formulario vacío.
        form: LoginForm = LoginForm()  # Crea un formulario de login sin datos iniciales.

    return render(request, "home.html", {"form": form})  # Renderiza home con el formulario de login para GET o errores POST.


@login_required  # Requiere autenticación antes de ejecutar la vista de cierre de sesión.
def logout_user(request: HttpRequest) -> HttpResponse:  # Define la vista para cerrar sesión del usuario.
    logout(request)  # Cierra la sesión actual eliminando el usuario de la petición.
    messages.success(request, "Cerraste la sesion correctamente")  # Muestra mensaje de cierre correcto.
    return redirect("home")  # Redirige a la página principal después de cerrar sesión.


@login_required  # Requiere autenticación antes de permitir registrar usuarios.
def register_user(request: HttpRequest) -> HttpResponse:  # Define la vista para crear usuarios nuevos.
    if request.method == "POST":  # Evalúa si se envió el formulario de registro por POST.
        form: UserRegisterForm = UserRegisterForm(request.POST)  # Crea el formulario de registro con datos POST.

        if form.is_valid():  # Valida campos obligatorios, contraseñas coincidentes y unicidad de usuario.
            form.save()  # Guarda el usuario nuevo en la base de datos.
            username: str = form.cleaned_data["username"]  # Lee el nombre de usuario validado del formulario.
            password: str = form.cleaned_data["password1"]  # Lee la contraseña validada del formulario.
            user: User | None = authenticate(request, username=username, password=password)  # Autentica al usuario recién creado.
            if user is not None:  # Verifica que la autenticación haya devuelto un usuario válido.
                login(request, user)  # Inicia sesión automáticamente después del registro exitoso.
            messages.success(request, "Registro exitoso")  # Muestra mensaje de registro correcto.
            return redirect("home")  # Redirige a la página principal tras registrar el usuario.
    else:  # Para peticiones GET se muestra un formulario vacío.
        form: UserRegisterForm = UserRegisterForm()  # Crea un formulario de registro sin datos iniciales.

    return render(request, "register.html", {"form": form})  # Renderiza la plantilla register con el formulario.


@login_required  # Requiere autenticación antes de mostrar un registro individual.
def customer_record(request: HttpRequest, pk: str) -> HttpResponse:  # Define la vista para mostrar un cliente por clave.
    customer_record: Record = get_object_or_404(Record, id=pk)  # Obtiene el registro o devuelve error 404 si no existe.
    return render(request, "record.html", {"customer_record": customer_record})  # Renderiza la plantilla record con el cliente.


@login_required  # Requiere autenticación antes de permitir eliminar registros.
def delete_record(request: HttpRequest, pk: str) -> HttpResponse:  # Define la vista para eliminar un registro.
    delete_it: Record = get_object_or_404(Record, id=pk)  # Obtiene el registro a eliminar o devuelve error 404.
    delete_it.delete()  # Elimina permanentemente el registro de la base de datos.
    messages.success(request, "Registro eliminado correctamente")  # Muestra mensaje de eliminación correcta.
    return redirect("home")  # Redirige a la página principal tras eliminar el registro.


@login_required  # Requiere autenticación antes de permitir actualizar registros.
def update_record(request: HttpRequest, pk: str) -> HttpResponse:  # Define la vista para editar un registro.
    current_record: Record = get_object_or_404(Record, id=pk)  # Obtiene el registro actual o devuelve error 404.
    form: RecordForm = RecordForm(request.POST or None, instance=current_record)  # Crea formulario ligado o vacío con la instancia.

    if form.is_valid():  # Valida los datos enviados para actualizar el registro.
        form.save()  # Guarda los cambios del formulario en la base de datos.
        messages.success(request, "Registro actualizado correctamente")  # Muestra mensaje de actualización correcta.
        return redirect("home")  # Redirige a la página principal tras guardar cambios.

    return render(request, "update_record.html", {"form": form})  # Renderiza update_record con el formulario y errores.
