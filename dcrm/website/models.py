# dcrm/website/models.py # Comentario que indica la ruta del archivo dentro del proyecto. Sirve como referencia visual, no se ejecuta.
from django.db import models  # Importa el módulo models de Django, que contiene las clases (Model, CharField, EmailField, etc.) necesarias para definir la estructura de las tablas de la base de datos.


class Record(models.Model):  # Define la clase Record heredando de models.Model, lo que la convierte en un modelo de Django. Django la mapeará a una tabla en la base de datos (por defecto 'website_record').
    created_at = models.DateTimeField(auto_now_add=True)  # Campo de fecha y hora. auto_now_add=True hace que se guarde automáticamente la fecha/hora actual al crear el registro (no se actualiza en ediciones posteriores). cam
    first_name = models.CharField(max_length=50)  # Campo de texto corto (varchar) de máximo 50 caracteres para almacenar el nombre del cliente/registro.
    last_name = models.CharField(max_length=50)  # Campo de texto corto de máximo 50 caracteres para almacenar el apellido del cliente/registro.
    email = models.EmailField(max_length=100)  # Campo específico para correos electrónicos (max 100). Django valida internamente que el valor tenga formato de email válido.
    phone = models.CharField(max_length=15)  # Campo de texto (CharField) de máximo 15 caracteres para el teléfono. Se usa CharField y no IntegerField para permitir formatos como '+57', guiones o espacios.
    address = models.CharField(max_length=100)  # Campo de texto corto de máximo 100 caracteres para almacenar la dirección del cliente.
    city = models.CharField(max_length=50)  # Campo de texto corto de máximo 50 caracteres para almacenar la ciudad del cliente.
    state = models.CharField(max_length=50)  # Campo de texto corto de máximo 50 caracteres para almacenar el departamento/estado del cliente.
    zip_code = models.CharField(max_length=10)  # Campo de texto corto de máximo 10 caracteres para el código postal. Se usa CharField para permitir ceros a la izquierda (un IntegerField los eliminaría).

    def __str__(self):  # Método especial __str__ que define cómo se muestra el objeto cuando se imprime o en el panel admin de Django. Retorna un f-string con nombre, apellido y email concatenados.
        return (f"{self.first_name} {self.last_name} {self.email}")
