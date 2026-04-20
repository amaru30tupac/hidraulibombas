from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": ("role", "phone", "is_active_technician", "photo"),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Información adicional", {
            "fields": ("role", "phone", "is_active_technician", "photo"),
        }),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active_technician",
        "is_staff",
    )
    list_filter = ("role", "is_active_technician", "is_staff", "is_superuser", "is_active")