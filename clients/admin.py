from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "contact_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "email", "phone", "contact_name")