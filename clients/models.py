from django.db import models


class Client(models.Model):
    name = models.CharField("Nombre", max_length=255)
    email = models.EmailField("Correo", blank=True, null=True)
    phone = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    address = models.CharField("Dirección", max_length=255, blank=True, null=True)
    contact_name = models.CharField("Nombre del contacto", max_length=255, blank=True, null=True)
    is_active = models.BooleanField("Activo", default=True)
    notes = models.TextField("Notas", blank=True, null=True)
    created_at = models.DateTimeField("Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name