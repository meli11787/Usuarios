from django.apps import AppConfig
# -*- coding: utf-8 -*-


class WebsiteConfig(AppConfig):# Configuración de la aplicación del sitio web
    default_auto_field = 'django.db.models.BigAutoField'# Tipo de campo de clave primaria predeterminado para los modelos de esta aplicación
    name = 'website'# Nombre de la aplicación
