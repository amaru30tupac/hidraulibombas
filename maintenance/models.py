from django.conf import settings
from django.db import models
from clients.models import Client


class MaintenanceRecord(models.Model):
    TYPE_CHOICES = [
        ("preventivo", "Preventivo"),
        ("correctivo", "Correctivo"),
        ("asistencia_tecnica", "Asistencia técnica"),
        ("emergencia", "Emergencia"),
    ]

    STATUS_CHOICES = [
        ("A", "Ajustadas"),
        ("C", "Cambio"),
        ("F", "Falla"),
        ("P", "Pendiente"),
        ("D", "Diagnóstico"),
        ("V", "Verificado / OK / Operando"),
        ("NA", "No aplica"),
    ]

    title = models.CharField("Título", max_length=255)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="maintenance_records")
    email = models.EmailField("Correo", blank=True, null=True)
    tower = models.CharField("Torre", max_length=100, blank=True, null=True)
    number = models.CharField("Número", max_length=100, blank=True, null=True)
    maintenance_type = models.CharField("Tipo de mantenimiento", max_length=30, choices=TYPE_CHOICES)
    equipment = models.CharField("Equipo", max_length=150)
    date = models.DateField("Fecha")
    entry_time = models.TimeField("Hora de entrada", blank=True, null=True)
    exit_time = models.TimeField("Hora de salida", blank=True, null=True)
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="maintenance_records",
        blank=True,
        null=True,
    )
    site = models.CharField("Sede", max_length=150, blank=True, null=True)
    parts_for_change = models.TextField("Partes para cambio", blank=True, null=True)
    observations = models.TextField("Observaciones", blank=True, null=True)
    general_status = models.CharField("Estado general", max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="maintenance_created",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField("Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = "Bitácora de mantenimiento"
        verbose_name_plural = "Bitácoras de mantenimiento"
        ordering = ["-date", "-created_at"]

    def __str__(self) -> str:
        return self.title


class MaintenancePhoto(models.Model):
    maintenance = models.ForeignKey(
        MaintenanceRecord,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    image = models.ImageField("Imagen", upload_to="maintenance/photos/")
    caption = models.CharField("Descripción", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foto de mantenimiento"
        verbose_name_plural = "Fotos de mantenimiento"

    def __str__(self) -> str:
        return f"Foto #{self.pk} - {self.maintenance.title}"


class InspectionValue(models.Model):
    SECTION_CHOICES = [
        ("tablero_control", "Tablero de control"),
        ("hidrosistema", "Hidrosistema"),
        ("sistema_eyector", "Sistema eyector"),
        ("motor", "Motor"),
        ("bombas", "Bombas"),
    ]

    maintenance = models.ForeignKey(
        MaintenanceRecord,
        on_delete=models.CASCADE,
        related_name="inspection_values"
    )
    section = models.CharField("Sección", max_length=30, choices=SECTION_CHOICES)
    parameter = models.CharField("Parámetro", max_length=100)
    position = models.CharField("Posición", max_length=10)
    value = models.CharField("Valor", max_length=20, blank=True, null=True)
    numeric_value = models.DecimalField(
        "Valor numérico",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Valor de inspección"
        verbose_name_plural = "Valores de inspección"
        ordering = ["section", "parameter", "position"]
        unique_together = ("maintenance", "section", "parameter", "position")

    def __str__(self) -> str:
        return f"{self.maintenance_id} - {self.section} - {self.parameter} - {self.position}"