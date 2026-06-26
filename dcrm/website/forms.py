# dcrm/website/forms.py  # Ruta del archivo de formularios de la aplicación Django
from django import forms  # Importa el módulo de formularios de Django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Importa formularios de autenticación predefinidos
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django

from .models import Record  # Importa el modelo Record desde la app local


class LoginForm(AuthenticationForm):  # Formulario de inicio de sesión basado en AuthenticationForm
    """Formulario de login con estilos y protección CSRF integrada."""  # Docstring que describe el formulario
    username = forms.CharField(  # Define el campo de nombre de usuario
        label="",  # Sin etiqueta visible en el formulario
        widget=forms.TextInput(attrs={"placeholder": "Nombre de usuario", "class": "form-control"})  # Widget de texto con placeholder y clase CSS
    )
    password = forms.CharField(  # Define el campo de contraseña
        label="",  # Sin etiqueta visible en el formulario
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña", "class": "form-control"})  # Widget de contraseña con placeholder y clase CSS
    )


class UserRegisterForm(UserCreationForm):  # Formulario de registro de usuario basado en UserCreationForm
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"placeholder": "Correo electronico"}))  # Campo de correo electrónico
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Nombre"}))  # Campo de nombre
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Apellido"}))  # Campo de apellido

    class Meta:  # Clase Meta para configuración del formulario
        model = User  # Modelo de usuario asociado al formulario
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]  # Campos incluidos en el formulario

    def __init__(self, *args, **kwargs):  # Constructor del formulario
        super(UserRegisterForm, self).__init__(*args, **kwargs)  # Llama al constructor de la clase padre

        self.fields["username"].widget.attrs["class"] = "form-control"  # Agrega clase CSS al widget de username
        self.fields["username"].widget.attrs["placeholder"] = "Nombre de usuario"  # Establece placeholder para username
        self.fields["username"].label = ""  # Elimina la etiqueta del campo username
        self.fields["username"].help_text = (  # Establece texto de ayuda para username
            '<span class="form-text text-muted">Requerido. 150 caracteres o menos. '
            "Letras, digitos y @/./+/-/_ solamente.</span>"
        )

        self.fields["password1"].widget.attrs["class"] = "form-control"  # Agrega clase CSS al widget de password1
        self.fields["password1"].widget.attrs["placeholder"] = "Contrasena"  # Establece placeholder para password1
        self.fields["password1"].label = ""  # Elimina la etiqueta del campo password1
        self.fields["password1"].help_text = (  # Establece texto de ayuda para password1
            '<ul class="form-text text-muted">'
            "<li>Tu contrasena no puede ser demasiado similar a tu otra informacion personal.</li>"
            "<li>Tu contrasena debe contener al menos 8 caracteres.</li>"
            "<li>Tu contrasena no puede ser una contrasena comun.</li>"
            "<li>Tu contrasena no puede ser completamente numerica.</li>"
            "</ul>"
        )

        self.fields["password2"].widget.attrs["class"] = "form-control"  # Agrega clase CSS al widget de password2
        self.fields["password2"].widget.attrs["placeholder"] = "Confirmar contrasena"  # Establece placeholder para password2
        self.fields["password2"].label = ""  # Elimina la etiqueta del campo password2
        self.fields["password2"].help_text = (  # Establece texto de ayuda para password2
            '<span class="form-text text-muted">Requerido. Debe coincidir con la contrasena anterior.</span>'
        )


class RecordForm(forms.ModelForm):  # Formulario para crear/editar registros basado en ModelForm
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control"}))  # Campo de nombre
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Apellido", "class": "form-control"}))  # Campo de apellido
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}))  # Campo de correo electrónico
    phone= forms.CharField(  # Campo de teléfono
        label="",  # Sin etiqueta visible
        widget=forms.TextInput(attrs={"placeholder": "Telefono", "class": "form-control"}),  # Widget de texto con placeholder y clase CSS
    )
    address = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Direccion", "class": "form-control"}))  # Campo de dirección
    city = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Ciudad", "class": "form-control"}))  # Campo de ciudad
    state = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Estado", "class": "form-control"}))  # Campo de estado/provincia
    zip_code = forms.CharField(  # Campo de código postal
        label="",  # Sin etiqueta visible
        widget=forms.TextInput(attrs={"placeholder": "Codigo Postal", "class": "form-control"}),  # Widget de texto con placeholder y clase CSS
    )

    class Meta:  # Clase Meta para configuración del formulario
        model = Record  # Modelo Record asociado al formulario
        fields = ["first_name", "last_name", "email", "phone", "address", "city", "state", "zip_code"]  # Campos incluidos en el formulario
