# -*- coding: utf-8 -*-
#dcrm/website/admin.py
from django.contrib import admin
from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
        "state",
        "created_at",
    )
    list_display_links = ("id", "first_name", "last_name")
    search_fields = ("first_name", "last_name", "email", "phone", "city", "state")
    list_filter = ("city", "state", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
