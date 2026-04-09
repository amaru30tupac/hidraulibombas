from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("supervisor", "Supervisor"),
        ("tecnico", "Técnico"),
        ("consulta", "Consulta"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="tecnico")
    phone = models.CharField(max_length=30, blank=True, null=True)
    is_active_technician = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.get_full_name() or self.username} ({self.role})"