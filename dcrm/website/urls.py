from django.urls import path
from . import views  # Importa el archivo views.py de la misma carpeta

urlpatterns = [  # type: ignore
    path('', views.home, name='home'), # Aquí SÍ va el path # type: ignore
    path('login/', views.login_user, name='login'), # type: ignore
    path('logout/', views.logout_user, name='logout'), # type: ignore
    path('registrar/',views.register_user, name='register'),
    path('record/<str:pk>/', views.customer_record, name='customer_record'), # type: ignore# Aquí SÍ va el path para mostrar el registro de un cliente específico, utilizando su clave 
    path('delete_record/<str:pk>/', views.delete_record, name='delete_record'),# type: ignore# Aquí SÍ va el path para eliminar un registro de cliente específico, utilizando su clave primaria (pk) como parte de la URL
    path('update_record/<str:pk>/', views.update_record, name='update_record'), # Aquí SÍ va el path para actualizar un registro de cliente específico, utilizando su clave primaria (pk) como parte de la URL

]